# P1-L2: Variables, Types, print, input

**Concept:** Variables are named containers. Python infers types automatically — no declarations needed. `print()` sends output to the terminal; `input()` reads a line from the user. These four tools underpin every Python program.

**Task:** Create `hello.py`. Write a script that asks for the user's name and age, then prints a greeting with arithmetic.

Expected behavior:
```
What is your name? Alice
How old are you? 30
Hello Alice! In 10 years you'll be 40.
```

**Acceptance criteria:**
- Script runs without error
- Output uses both entered values
- Age arithmetic is correct (requires `int()` conversion)

**Common mistakes:**
- Forgetting `int()` before doing math on `input()` — returns a string by default
- Using `+` to join string and number without converting: `"Age: " + age` fails
- Printing the literal word "Alice" instead of the variable

**Bridge:** You can collect and display data. Next: format strings more powerfully with f-strings.
