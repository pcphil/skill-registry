# P2-L4: List Comprehensions and Generators

**Concept:** List comprehensions replace verbose `for` + `append` loops with a single expressive line. Generators are lazy — they produce values one at a time without building the full list in memory. Use a list when you need all values at once; use a generator for large or infinite sequences.

**Task:** Refactor `io_utils.py`:
1. Replace any `for` loop that builds a list with a list comprehension
2. Add a generator function `passing_students(students)` that `yield`s only students with grade ≥ 60

**Acceptance criteria:**
- At least one list comprehension present (not just a loop-in-brackets)
- `passing_students` uses `yield`, not `return`
- Behavior of `main.py` unchanged

**Common mistakes:**
- Comprehension that's too complex to read in one pass — split into two lines if needed
- Trying to index into a generator like a list — generators are consumed once
- Using `return [x for x in ...]` inside a generator function — defeats lazy evaluation

**Bridge:** Writing idiomatic Python. Next: manage resources safely with context managers.
