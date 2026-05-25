# P1-L8: Foundation Mini-Project

Full project spec: `references/projects.md` → "Foundation Mini-Project: report.py"

**What this combines:**
File I/O, dicts, loops, functions, f-strings, control flow — all Phase 1 concepts applied together.

**What to build:** A standalone script `report.py` that:
1. Reads `students.csv`
2. Applies Distinction/Pass/Fail logic
3. Prints a formatted report to the console
4. Writes `pass_list.txt` with passing student names only

**Required functions:**
- `read_students(filepath)` → returns dict
- `get_label(grade)` → returns label string
- `print_report(students)` → prints formatted table + summary
- `write_pass_list(students, filepath)` → writes file

**Acceptance criteria:**
- Script runs with no arguments: `python report.py`
- All logic in named functions — no bare code outside `if __name__ == "__main__":`
- Console output shows each student with grade and label, plus total count and average
- `pass_list.txt` created with correct names
- Handles `FileNotFoundError` if CSV is missing

**Review approach:** Read `report.py` with the Read tool. Check that all four functions exist, that no data is hardcoded, and that the output matches the expected format in `projects.md`.
