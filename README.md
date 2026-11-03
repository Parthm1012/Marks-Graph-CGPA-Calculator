# Marks Graph & CGPA Calculator (Flask)

## Quick Start in VS Code

1. **Open this folder in VS Code**
2. Open the integrated terminal (`Ctrl+`` ` or View → Terminal)
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the app:
   ```
   python app.py
   ```
5. Open your browser at **http://127.0.0.1:5000**

## Grading Scale
| Marks | Grade | Grade Point |
|-------|-------|-------------|
| ≥ 90  | O     | 10          |
| 80–89 | A+    | 9           |
| 70–79 | A     | 8           |
| 60–69 | B+    | 7           |
| 50–59 | B     | 6           |
| 40–49 | C     | 5           |
| < 40  | F     | 0           |

## Files
- `app.py` — Flask routes + chart generation
- `templates/index.html` — Input form
- `templates/result.html` — Results page
- `static/style.css` — Styles
