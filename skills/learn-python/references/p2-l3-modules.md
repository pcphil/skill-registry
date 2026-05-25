# P2-L3: Modules and Packages

**Concept:** `import` pulls code from other files or installed packages. Splitting code into modules keeps each file focused. `pip install` adds third-party packages to the active virtual environment. The `if __name__ == "__main__":` guard prevents code from running when a file is imported.

**Task:** Split `file_io.py` into two modules:
- `io_utils.py` — file reading and writing functions only
- `main.py` — entry point that imports from `io_utils` and runs the program

Run `python main.py` — output must be identical to before.

**Acceptance criteria:**
- `io_utils.py` contains only functions — no top-level executable code
- `main.py` uses `from io_utils import read_students, write_pass_list`
- `main.py` has `if __name__ == "__main__":` guard
- Running `python main.py` produces same output as before

**Common mistakes:**
- Circular imports: `main.py` imports `io_utils`, `io_utils` imports `main` — avoid
- Running `io_utils.py` directly and expecting output — it has no entry point
- Missing `__main__` guard: importing `main.py` from another file triggers the whole program

**Bridge:** Code is organized. Next: write Python the idiomatic way — list comprehensions and generators.
