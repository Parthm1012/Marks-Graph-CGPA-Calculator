import io
import base64
import matplotlib
matplotlib.use("Agg")            # draw charts without opening a window
import matplotlib.pyplot as plt
from flask import Flask, render_template, request

app = Flask(__name__)

NUM_SUBJECTS = 5


def get_grade(marks):
    """Return (grade letter, grade point) on a 10-point scale."""
    if marks >= 90:
        return "O", 10
    elif marks >= 80:
        return "A+", 9
    elif marks >= 70:
        return "A", 8
    elif marks >= 60:
        return "B+", 7
    elif marks >= 50:
        return "B", 6
    elif marks >= 40:
        return "C", 5
    else:
        return "F", 0


def calculate_cgpa(subjects):
    """CGPA = sum(grade point x credits) / sum(credits)."""
    total_credits = sum(s["credits"] for s in subjects)
    total_points = sum(s["gp"] * s["credits"] for s in subjects)
    return round(total_points / total_credits, 2)


def to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=110)
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode("utf-8")


def marks_bar_graph(subjects):
    names = [s["name"] for s in subjects]
    marks = [s["marks"] for s in subjects]
    colors = ["#16a34a" if m >= 40 else "#dc2626" for m in marks]

    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(names, marks, color=colors)
    ax.bar_label(bars, fontsize=9)
    ax.axhline(40, color="gray", linestyle="--", label="Pass mark (40)")
    ax.set_ylim(0, 110)
    ax.set_title("Subject-wise Marks")
    ax.set_xlabel("Subjects")
    ax.set_ylabel("Marks (out of 100)")
    ax.legend()
    return to_base64(fig)


def grade_point_graph(subjects):
    names = [s["name"] for s in subjects]
    gps = [s["gp"] for s in subjects]

    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(names, gps, color="#4f46e5")
    ax.bar_label(bars, fontsize=9)
    ax.set_ylim(0, 11)
    ax.set_title("Subject-wise Grade Points")
    ax.set_xlabel("Subjects")
    ax.set_ylabel("Grade Point (out of 10)")
    return to_base64(fig)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        subjects = []
        for i in range(1, NUM_SUBJECTS + 1):
            name = request.form.get(f"name{i}", "").strip() or f"Subject {i}"
            marks = float(request.form.get(f"marks{i}", 0))
            credits = float(request.form.get(f"credits{i}", 1))
            grade, gp = get_grade(marks)
            subjects.append({"name": name, "marks": marks, "credits": credits,
                             "grade": grade, "gp": gp})

        total = sum(s["marks"] for s in subjects)
        percentage = round(total / len(subjects), 2)
        cgpa = calculate_cgpa(subjects)
        result = "FAIL" if any(s["grade"] == "F" for s in subjects) else "PASS"

        return render_template("result.html", subjects=subjects, total=total,
                               percentage=percentage, cgpa=cgpa, result=result,
                               bar=marks_bar_graph(subjects),
                               gp_bar=grade_point_graph(subjects))

    return render_template("index.html", count=NUM_SUBJECTS)


if __name__ == "__main__":
    # Open http://127.0.0.1:5000 in your browser after running
    app.run(debug=True, port=5000)
