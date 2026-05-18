# P1-L5: Control Flow

**Concept:** `if/elif/else` branches based on conditions. `for` iterates over a sequence. `while` runs until a condition turns false. These make a program respond differently to different data.

**Task:** Update `data_types.py`. Loop through the students dict and print each name, grade, and a label:
- "Distinction" if grade ≥ 90
- "Pass" if grade ≥ 60
- "Fail" otherwise

**Acceptance criteria:**
- All students printed with correct label
- Uses a `for` loop over the dict (not manual if-chains per student)
- Threshold checks are in the right order (≥ 90 before ≥ 60)

**Common mistakes:**
- Using `=` (assignment) instead of `==` (comparison) in conditions
- Checking `grade >= 60` before `grade >= 90` — Distinction never triggers
- Iterating `.keys()` when `.items()` gives both name and grade at once

**Bridge:** Program can branch and loop. Next: extract reusable logic into functions.
