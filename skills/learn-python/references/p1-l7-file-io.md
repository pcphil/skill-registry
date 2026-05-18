# P1-L7: File I/O

**Concept:** `open()` reads or writes files. The `with` statement ensures the file closes automatically even if an error occurs. Real programs persist data — this is the primary mechanism in Python.

**Task:** Create `students.csv` with 5 student records. Write `file_io.py` that reads it using only stdlib (no pandas), builds a students dict, and writes `pass_list.txt` containing only passing student names.

`students.csv` format:
```
name,grade
Alice,85
Bob,45
Carol,92
Dave,60
Eve,38
```

**Acceptance criteria:**
- Script uses `with open(...)` for both read and write
- No hardcoded student data — all read from the CSV
- `pass_list.txt` contains only names of students with grade ≥ 60
- Each name on its own line in the output file

**Common mistakes:**
- Not stripping `\n` from lines: `line.split(",")` leaves a newline on the grade
- Opening file without `with` — file may not flush/close properly
- Using `int(grade)` without handling the header row (first row is "name,grade")

**Bridge:** You can now read, process, and write data. Time to combine everything — mini-project.
