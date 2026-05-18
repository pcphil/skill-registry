# P1-L4: Lists, Dicts, Sets, Tuples

**Concept:** Lists store ordered sequences (mutable). Dicts store key-value pairs (fast lookup by key). Sets store unique unordered values. Tuples are immutable lists. Choosing the right one for the job is a core Python skill.

**Task:** Create `data_types.py`. Define:
- A list of 5 student names
- A dict mapping each name to a grade (0–100)
- A set of names for students who passed (grade ≥ 60)

Print all three clearly labeled.

**Acceptance criteria:**
- All three data structures present and correctly typed
- Set contains only students with grade ≥ 60
- Output labels each structure (e.g., "Students:", "Grades:", "Passing:")

**Common mistakes:**
- Using a list when a dict makes lookup cleaner
- Expecting a set to print in insertion order — sets are unordered
- Using `[]` (list) when `{}` (set or dict) was intended — `{}` alone creates an empty dict, not a set

**Bridge:** You can store structured data. Next: make decisions and repeat actions.
