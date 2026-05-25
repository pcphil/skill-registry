# P1-L3: Strings and f-strings

**Concept:** Strings are sequences of characters. f-strings (`f"..."`) embed expressions directly inside them — cleaner and more readable than concatenation. Most real Python output uses f-strings.

**Task:** Update `hello.py`. Replace any string concatenation with f-strings. Add a line that prints the name in uppercase and counts its characters.

Expected output (for name "Alice"):
```
Hello Alice! In 10 years you'll be 40.
Your name has 5 characters: ALICE
```

**Acceptance criteria:**
- No `+` string concatenation anywhere
- Uses `f"..."` syntax
- Uses `.upper()` and `len()`

**Common mistakes:**
- Mixing `f"..."` with `.format()` — pick one (prefer f-strings)
- Forgetting `len()` counts characters, not words
- Writing `f"Hello {name()}"` — no parentheses on a variable, only on function calls

**Bridge:** Strings handled. Next: store multiple values in a single variable.
