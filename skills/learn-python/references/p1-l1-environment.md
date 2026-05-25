# P1-L1: Environment Setup

**Concept:** Python needs an isolated environment per project so dependencies don't collide. `venv` is the built-in solution; `pip` installs packages into it. Getting this right once means every future project starts clean.

**Task:** Create a folder called `python-learning/`. Inside it, create and activate a virtual environment, then verify Python works.

```bash
mkdir python-learning && cd python-learning
python -m venv .venv

# Windows:
.venv\Scripts\activate

# Mac/Linux:
source .venv/bin/activate

python --version
```

**Acceptance criteria:** `python --version` prints ≥ 3.10. Terminal prompt shows `(.venv)` prefix.

**Common mistakes:**
- Running `python3` on systems where `python` maps to 2.x — use `python3 -m venv` if needed
- Forgetting to activate before installing packages
- Creating venv inside the wrong directory

**Bridge:** Environment ready. Next: write first Python code — variables, types, and printing output.
