# P2-L2: Error Handling

**Concept:** Programs fail — files go missing, inputs are malformed, APIs go down. `try/except` catches errors and handles them gracefully instead of crashing. Specific exception types (`ValueError`, `FileNotFoundError`) make handling precise rather than catching everything.

**Task:** Update `file_io.py`. Add:
1. `try/except FileNotFoundError` around the CSV read — print a clear error message and exit cleanly if missing
2. `try/except ValueError` around the grade parse — skip rows with non-numeric grades and warn

**Acceptance criteria:**
- Running with missing CSV prints an error message (not a traceback) and exits with code 1
- A row with grade "INVALID" is skipped with a warning printed to stderr
- No bare `except:` or `except Exception:` clauses

**Common mistakes:**
- Using `except Exception:` — catches everything including bugs you want to see
- Catching `FileNotFoundError` but re-raising accidentally via wrong indentation
- Swallowing errors silently with an empty `except` block — always print something

**Bridge:** Code handles failure. Next: use the Python ecosystem — install and organize third-party packages.
