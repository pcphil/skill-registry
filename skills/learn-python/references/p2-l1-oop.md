# P2-L1: OOP — Classes

**Concept:** Classes group related data and behavior into one unit. `__init__` is the constructor — it runs when you create an instance. `self` refers to the specific instance being worked on. Use a class when you have multiple things of the same kind, each with their own state.

**Task:** Create `student.py`. Define a `Student` class with `name` and `grade` attributes and a `label()` method that returns "Distinction", "Pass", or "Fail". Instantiate 3 students and print each one's name, grade, and label.

```python
# Expected output:
# Alice: 85 → Pass
# Carol: 92 → Distinction
# Bob: 45 → Fail
```

**Acceptance criteria:**
- `Student` class defined with `__init__` and `label()`
- All three instances created and printed
- `label()` returns a string — does not print directly

**Common mistakes:**
- Forgetting `self` as first parameter in every method
- Calling `student.label` without `()` — returns the method object, not the result
- Putting `print()` inside `label()` instead of `return`

**Bridge:** You can model real-world objects. Next: handle when things go wrong gracefully.
