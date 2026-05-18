# P2-L5: Context Managers

**Concept:** Context managers handle setup and teardown automatically via `with`. You already used `with open()` — now understand why. `contextlib.contextmanager` lets you write your own with a generator function. The `yield` is where the `with` block body runs.

**Task:** Create `timer.py`. Write a `Timer` context manager using `contextlib.contextmanager` that prints how long a block of code took. Use it in `main.py` to time the student-reading step.

```python
with Timer("Reading students"):
    students = read_students("students.csv")
# Output: Reading students took 0.003s
```

**Acceptance criteria:**
- `Timer` defined using `contextlib.contextmanager` decorator
- Timing uses `time.perf_counter()` (not `time.time()`)
- Used in `main.py` around the file read call
- Output shows label and elapsed time in seconds

**Common mistakes:**
- Using `__enter__`/`__exit__` when `contextlib.contextmanager` is simpler for this case
- Forgetting `yield` inside the generator-style context manager — nothing runs
- Putting the timer print before `yield` — it prints before the block runs, not after

**Bridge:** Resource management mastered. Time to apply everything — Phase 2 mini-project.
