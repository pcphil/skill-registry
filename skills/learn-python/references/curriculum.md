# Python Curriculum — Detailed Lesson Specs

Each lesson follows this structure:
- **Concept** — the why in 2-3 sentences
- **Task** — exact file name + what to write
- **Acceptance criteria** — what correct output looks like
- **Common mistakes** — what to watch for when reviewing
- **Bridge** — one sentence connecting to the next lesson

---

## Phase 1: Foundations

### Lesson 1: Environment Setup

**Concept:** Python needs an isolated environment per project so dependencies don't collide across projects. `venv` is the built-in solution; `pip` installs packages into that environment. Getting this right once means every future project starts clean.

**Task:** Create a project folder called `python-learning/`. Inside it, create and activate a virtual environment, then verify Python works by running `python --version`.

```bash
mkdir python-learning && cd python-learning
python -m venv .venv
# Windows: .venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate
python --version
```

**Acceptance criteria:** `python --version` prints a version ≥ 3.10. Prompt shows `(.venv)` prefix.

**Common mistakes:** Running `python3` on systems where `python` points to 2.x. Forgetting to activate before installing packages.

**Bridge:** Environment is ready. Now write the first actual Python code.

---

### Lesson 2: Variables, Types, print, input

**Concept:** Variables are named containers. Python infers types automatically — you don't declare them. `print()` shows output; `input()` reads from the user. These four things underpin every Python program ever written.

**Task:** Create `hello.py`. Write a script that asks for the user's name and age, then prints a greeting using both values.

```python
# Expected behavior:
# What is your name? Alice
# How old are you? 30
# Hello Alice! In 10 years you'll be 40.
```

**Acceptance criteria:** Script runs without error. Output uses the entered values. Age arithmetic is correct (uses `int()`).

**Common mistakes:** Forgetting `int()` conversion on `input()` before doing math. Concatenating with `+` instead of converting types.

**Bridge:** You can collect and display data. Next: format strings more powerfully.

---

### Lesson 3: Strings and f-strings

**Concept:** Strings are sequences of characters. f-strings (prefix `f"..."`) let you embed expressions directly inside them — cleaner than concatenation. Most real Python output uses f-strings.

**Task:** Update `hello.py`. Replace any string concatenation with f-strings. Add a line that prints the name in uppercase and counts its characters.

```python
# Example output:
# Hello Alice! In 10 years you'll be 40.
# Your name has 5 characters: ALICE
```

**Acceptance criteria:** No `+` string concatenation. Uses `f"..."`, `.upper()`, and `len()`.

**Common mistakes:** Mixing `f"..."` and `.format()` — pick one (f-strings). Forgetting that `len()` counts characters, not words.

**Bridge:** Strings handled. Next: store multiple values in a single variable.

---

### Lesson 4: Lists, Dicts, Sets, Tuples

**Concept:** Lists store ordered sequences (mutable). Dicts store key-value pairs (fast lookup). Sets store unique unordered values. Tuples are like lists but immutable. Knowing when to use which is a core Python skill.

**Task:** Create `data_types.py`. Define a list of 5 student names, a dict mapping each name to a grade (0-100), and a set of passing names (grade ≥ 60). Print each.

**Acceptance criteria:** All three data structures present. Set contains only students who passed. Output shows all three clearly labeled.

**Common mistakes:** Using a list when a dict would make lookup cleaner. Forgetting that sets are unordered (don't expect a specific print order).

**Bridge:** You can store structured data. Next: make decisions and repeat actions.

---

### Lesson 5: Control Flow

**Concept:** `if/elif/else` branches based on conditions. `for` iterates over a sequence. `while` runs until a condition is false. These are the tools that make a program *do different things* depending on input.

**Task:** Update `data_types.py`. Loop through the students dict, print each student's name and grade, and add a label: "Pass", "Fail", or "Distinction" (≥ 90).

**Acceptance criteria:** All students listed. Each has the correct label. No manual if-chains — use a loop.

**Common mistakes:** Using `=` instead of `==` in conditions. Off-by-one in grade thresholds.

**Bridge:** Program can branch and loop. Next: extract reusable logic into functions.

---

### Lesson 6: Functions

**Concept:** Functions are named, reusable blocks of logic. They take inputs (parameters) and return outputs. Good functions do one thing. Splitting logic into functions is the difference between a script and a program.

**Task:** Refactor `data_types.py`. Extract a function `get_label(grade)` that returns "Distinction", "Pass", or "Fail". Extract a function `print_report(students)` that takes the dict and prints the labeled list. Call both from the bottom of the file.

**Acceptance criteria:** Two functions defined. No logic duplicated inside the loop. Output identical to Lesson 5.

**Common mistakes:** Putting `print()` inside `get_label` — it should `return`. Forgetting `return` entirely (returns `None`).

**Bridge:** Logic is reusable. Next: read and write data to files.

---

### Lesson 7: File I/O

**Concept:** `open()` reads or writes files. The `with` statement ensures the file is closed automatically, even if an error occurs. Real programs persist data — this is how Python does it.

**Task:** Create `students.csv` with 5 students and grades. Write `file_io.py` that reads the CSV using only stdlib (no pandas yet), builds the students dict, and writes a `pass_list.txt` containing only the names of passing students.

```
# students.csv format:
name,grade
Alice,85
Bob,45
...
```

**Acceptance criteria:** `pass_list.txt` created with correct names only. Script uses `with open(...)`. No hardcoded student data — all read from file.

**Common mistakes:** Not stripping newlines (`\n`) when reading lines. Opening file without `with`. Hardcoding the data instead of reading it.

**Bridge:** You can now read, process, and write data. Mini-project time.

---

### Lesson 8: Phase 1 Mini-Project — report.py

Full spec: `references/projects.md` → Foundation Mini-Project.

**What it combines:** File I/O, dicts, loops, functions, f-strings, control flow.

**Acceptance criteria:** Script runs with no arguments. Reads `students.csv`. Prints a formatted report to console. Writes `pass_list.txt`. All logic in named functions.

---

## Phase 2: Intermediate

### Lesson 1: OOP — Classes

**Concept:** Classes group related data and behavior into one unit. `__init__` is the constructor. `self` refers to the instance. Use a class when you have multiple things of the same type, each with their own state.

**Task:** Create `student.py`. Define a `Student` class with `name`, `grade`, and a `label()` method that returns "Distinction"/"Pass"/"Fail". Instantiate 3 students, call `label()` on each, and print results.

**Acceptance criteria:** Class defined with `__init__` and `label()`. All three instances work correctly. No global logic outside functions/methods.

**Common mistakes:** Forgetting `self` as first parameter. Calling `student.label` without `()`. Putting print inside `label()` instead of returning.

**Bridge:** Now you can model real-world things. Next: handle when things go wrong.

---

### Lesson 2: Error Handling

**Concept:** Programs fail. `try/except` catches errors gracefully instead of crashing. `finally` always runs — use it for cleanup. Specific exception types (`ValueError`, `FileNotFoundError`) make handling precise.

**Task:** Update `file_io.py`. Wrap the file reading in `try/except FileNotFoundError`. If the file is missing, print a helpful error message and exit cleanly. Add a `try/except ValueError` around grade parsing in case a non-number appears.

**Acceptance criteria:** Script handles missing file gracefully. Script handles bad grade data gracefully. No bare `except:` clauses.

**Common mistakes:** Catching `Exception` broadly instead of specific types. Swallowing errors silently without printing anything.

**Bridge:** Code is robust. Next: use the Python ecosystem — third-party packages.

---

### Lesson 3: Modules and Packages

**Concept:** `import` brings in code from other files or installed packages. `pip install` adds third-party packages to your virtual environment. Organizing your own code into modules keeps things maintainable.

**Task:** Split `file_io.py` into two modules: `io_utils.py` (file reading/writing functions) and `main.py` (entry point). Import from `io_utils` in `main`. Run `python main.py` — same behavior.

**Acceptance criteria:** Two files. `main.py` uses `from io_utils import ...`. Running `main.py` produces identical output to before.

**Common mistakes:** Circular imports. Running the module file directly and wondering why `main()` runs twice (missing `if __name__ == "__main__"` guard).

**Bridge:** Code is organized. Next: write Python the idiomatic way.

---

### Lesson 4: List Comprehensions and Generators

**Concept:** List comprehensions replace verbose `for` + `append` loops with a single expressive line. Generators are lazy — they produce values one at a time, saving memory for large datasets.

**Task:** Refactor `io_utils.py`. Replace any `for` loop that builds a list with a list comprehension. Add a generator function `passing_students(students)` that yields only students with grade ≥ 60.

**Acceptance criteria:** At least one list comprehension present. Generator function uses `yield`. Behavior unchanged.

**Common mistakes:** Forcing a generator where a list is needed (or vice versa). Overly complex comprehensions that hurt readability — split into two if needed.

**Bridge:** Writing idiomatic Python. Next: handle resources safely.

---

### Lesson 5: Context Managers

**Concept:** Context managers handle setup and teardown automatically via `with`. You already used `with open()` — now understand why. You can write your own with `__enter__`/`__exit__` or `contextlib.contextmanager`.

**Task:** Create `timer.py`. Write a context manager `Timer` using `contextlib.contextmanager` that prints how long a block of code took. Use it to time the file-reading logic in `main.py`.

```python
with Timer("Reading students"):
    students = read_students("students.csv")
# Output: Reading students took 0.003s
```

**Acceptance criteria:** `Timer` is a context manager. Timing is accurate. Used in `main.py`.

**Common mistakes:** Using `__enter__`/`__exit__` when `contextlib.contextmanager` is simpler. Forgetting `yield` inside the generator-style context manager.

**Bridge:** Python fundamentals solid. Mini-project time.

---

### Lesson 6: Phase 2 Mini-Project — expenses.py

Full spec: `references/projects.md` → Intermediate Mini-Project.

**What it combines:** OOP, error handling, modules, list comprehensions, context managers, file I/O.

---

## Phase 3: Domain Tracks

### Web/APIs Track

**L1 — HTTP with requests:** Fetch data from a public API (wttr.in weather). Parse JSON response. Print formatted output.

**L2 — REST concepts:** What are resources, endpoints, methods (GET/POST/PUT/DELETE), status codes. No framework yet.

**L3 — FastAPI basics:** Install FastAPI + uvicorn. Create `weather_app/main.py` with a single `GET /weather/{city}` endpoint. Run with uvicorn.

**L4 — CRUD app:** Add POST, PUT, DELETE endpoints. Use an in-memory dict as storage. Test with curl or httpx.

Full project spec: `references/projects.md` → Web/APIs Project.

---

### Data/Automation Track

**L1 — pandas basics:** Read CSV into DataFrame. Select columns, filter rows, sort. `df.head()`, `df.describe()`.

**L2 — Cleaning messy data:** Handle missing values, wrong types, duplicate rows. `dropna()`, `fillna()`, `astype()`.

**L3 — Aggregation and output:** `groupby()`, `agg()`. Write clean CSV and a stats summary.

**L4 — Automation script:** Schedule script to run daily using `schedule` library. Process files from an input folder, archive processed files.

Full project spec: `references/projects.md` → Data/Automation Project.

---

### CLI Tools Track

**L1 — typer basics:** Install typer + rich. Create `devtool/main.py` with one command. `typer.run()`.

**L2 — Multiple commands:** `@app.command()` for multiple subcommands. Arguments vs options.

**L3 — Rich output:** Tables, progress bars, colored output with rich. Replace plain print calls.

**L4 — Config and persistence:** Read/write a `~/.devtool/config.json`. Add a `config set` command.

Full project spec: `references/projects.md` → CLI Tools Project.

---

### AI/ML Basics Track

**L1 — OpenAI API client:** Install openai. Send a chat completion. Print the response. Handle errors.

**L2 — Prompt engineering:** System prompts, temperature, token limits. Build a simple Q&A assistant.

**L3 — Tool use / function calling:** Define a tool, let the model call it, handle the result.

**L4 — Simple agent loop:** Loop that reads user input → calls model → optionally calls tools → prints response. Saves conversation history.

Full project spec: `references/projects.md` → AI/ML Project.
