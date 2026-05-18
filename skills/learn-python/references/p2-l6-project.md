# P2-L6: Intermediate Mini-Project

Full project spec: `references/projects.md` → "Intermediate Mini-Project: expenses.py"

**What this combines:**
OOP, error handling, modules, list comprehensions, context managers, file I/O — all Phase 2 concepts applied together.

**What to build:** A CLI expense tracker using only Python stdlib:

```bash
python expenses.py add "Coffee" 4.50
python expenses.py list
python expenses.py total
python expenses.py list --category food
```

**Required files:**
- `expense.py` — `Expense` class with `id`, `description`, `amount`, `category`, `date`
- `storage.py` — `load_expenses(filepath)` and `save_expenses(expenses, filepath)` using `with open`
- `expenses.py` — entry point, parses `sys.argv`, calls storage and prints results

**Acceptance criteria:**
- `add` writes to `expenses.json` (creates on first run)
- `list` prints a formatted table with ID, description, amount, category, date
- `total` prints sum of all amounts
- List comprehension used for filtering (e.g., by category)
- Bad amount input prints an error and exits with code 1
- No third-party packages — stdlib only (`json`, `sys`, `datetime`)

**Review approach:** Read each file with the Read tool. Verify `Expense` class exists, storage uses `with open`, and the entry point handles all three commands.
