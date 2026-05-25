# P1-L6: Functions

**Concept:** Functions are named, reusable blocks of logic. They take inputs (parameters) and return outputs. A good function does one thing. Splitting code into functions is the difference between a script and a program.

**Task:** Refactor `data_types.py`. Extract:
- `get_label(grade)` → returns "Distinction", "Pass", or "Fail"
- `print_report(students)` → takes the dict, prints the labeled list

Call both functions at the bottom of the file. No logic should live outside a function.

**Acceptance criteria:**
- Two functions defined
- `get_label` uses `return`, not `print`
- Output identical to Lesson 5
- `if __name__ == "__main__":` guard wraps the function calls

**Common mistakes:**
- Putting `print()` inside `get_label` — it should `return` the string
- Forgetting `return` entirely (function silently returns `None`)
- Defining function after calling it — Python reads top to bottom

**Bridge:** Logic is reusable. Next: read and write data to files.
