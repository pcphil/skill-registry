# Real-World Project Specs

Each project is the target artifact that lessons build toward. Every exercise in a phase adds a piece to it — students don't do throwaway exercises.

---

## Foundation Mini-Project: report.py

**Goal:** A standalone script that reads student data from a CSV file, applies pass/fail logic, prints a formatted report, and writes a filtered output file.

**Files:**
```
python-learning/
├── students.csv      # Input data
├── report.py         # Main script
└── pass_list.txt     # Generated output
```

**students.csv format:**
```
name,grade
Alice,85
Bob,45
Carol,92
Dave,60
Eve,38
```

**Expected console output:**
```
=== Student Report ===
Alice       85   Pass
Bob         45   Fail
Carol       92   Distinction
Dave        60   Pass
Eve         38   Fail

Passing students: 3/5
Average grade: 64.0
```

**pass_list.txt content:**
```
Alice
Carol
Dave
```

**Requirements:**
- All data read from `students.csv` — no hardcoding
- Grade thresholds: Distinction ≥ 90, Pass ≥ 60, Fail < 60
- Functions: `read_students(filepath)`, `get_label(grade)`, `print_report(students)`, `write_pass_list(students, filepath)`
- Entry point guarded with `if __name__ == "__main__":`
- Handles `FileNotFoundError` on missing CSV

---

## Intermediate Mini-Project: expenses.py

**Goal:** A CLI expense tracker using only Python stdlib. Persists data to a JSON file. Supports adding, listing, and totalling expenses.

**Files:**
```
python-learning/
├── expenses.py        # Entry point
├── expense.py         # Expense class
├── storage.py         # JSON read/write
└── expenses.json      # Auto-created on first add
```

**Usage:**
```bash
python expenses.py add "Coffee" 4.50
python expenses.py add "Lunch" 12.00
python expenses.py list
python expenses.py total
python expenses.py list --category food
```

**Expected list output:**
```
ID  Description    Amount   Category   Date
1   Coffee         $4.50    general    2024-01-15
2   Lunch          $12.00   general    2024-01-15
```

**Requirements:**
- `Expense` class: `id`, `description`, `amount`, `category`, `date`
- `storage.py`: `load_expenses(filepath)` and `save_expenses(expenses, filepath)` using context manager
- Error handling: bad amount (non-number), missing file on first run
- List comprehension used somewhere meaningful (e.g., filtering by category)
- `if __name__ == "__main__":` guard in entry point

---

## Web/APIs Project: weather_app

**Goal:** A FastAPI web service that wraps the wttr.in weather API and exposes clean endpoints.

**Files:**
```
weather_app/
├── main.py            # FastAPI app
├── weather.py         # requests wrapper
├── models.py          # Pydantic response models
└── requirements.txt
```

**Endpoints:**
```
GET  /weather/{city}           → current weather for city
GET  /weather/{city}/forecast  → 3-day forecast
POST /favorites                → save a favorite city
GET  /favorites                → list favorite cities
DELETE /favorites/{city}       → remove favorite
```

**Sample response for GET /weather/London:**
```json
{
  "city": "London",
  "temp_c": 14,
  "description": "Partly cloudy",
  "humidity": 72,
  "wind_kph": 18
}
```

**Requirements:**
- Uses `requests` to call `wttr.in/?format=j1`
- Pydantic models for response validation
- `HTTPException` for city not found
- Favorites stored in-memory (dict) — no database
- Run: `uvicorn main:app --reload`

---

## Data/Automation Project: pipeline.py

**Goal:** A data processing pipeline that ingests messy CSV data, cleans it, and produces a structured summary report.

**Files:**
```
python-learning/
├── raw_data/
│   └── sales_2024.csv    # Messy input (provided below)
├── pipeline.py            # Main pipeline
├── cleaner.py             # Cleaning functions
├── reporter.py            # Summary/output logic
└── output/
    ├── clean_sales.csv    # Cleaned data
    └── summary.txt        # Stats report
```

**raw_data/sales_2024.csv (sample — messy):**
```
product,region,sales,date
Widget A,North,1200,2024-01-05
Widget B,,850,2024-01-06
Widget A,South,BAD_VALUE,2024-01-07
widget a,North,950,01/08/2024
Widget B,East,1100,2024-01-09
,North,200,2024-01-10
```

**Cleaning steps:**
1. Normalize product names (strip, title case)
2. Fill missing region with "Unknown"
3. Drop rows with non-numeric sales values
4. Standardize date format to YYYY-MM-DD
5. Drop rows missing product name

**Summary output:**
```
=== Sales Summary 2024 ===
Total records (clean): 5
Total sales: $5,300

By Product:
  Widget A: $2,150
  Widget B: $1,950

By Region:
  North: $2,150
  East:  $1,100
  Unknown: $850 (1 row with missing region)
```

**Requirements:**
- pandas for all data manipulation
- `cleaner.py` contains pure functions (no side effects)
- `reporter.py` uses `groupby()` and `agg()`
- Automation: `schedule` library to run pipeline every 60 seconds (demo mode)

---

## CLI Tools Project: devtool

**Goal:** A production-quality CLI app using typer and rich for a developer utility toolbelt.

**Files:**
```
devtool/
├── main.py            # Entry point, app definition
├── commands/
│   ├── env.py         # env subcommands
│   ├── files.py       # file utilities
│   └── config.py      # config management
├── config.py          # Config load/save
└── pyproject.toml     # Optional: make it installable
```

**Commands:**
```bash
devtool env list                    # List env vars as rich table
devtool env get VAR_NAME            # Get single env var
devtool files count ./src           # Count files by extension
devtool files size ./src            # Show directory size breakdown
devtool config set theme dark       # Write to ~/.devtool/config.json
devtool config get theme            # Read config value
devtool config list                 # Show all config as table
```

**Requirements:**
- typer `@app.command()` structure with subgroups
- rich `Table` for tabular output, `Console` for colored output
- Config persisted to `~/.devtool/config.json`
- `--help` works on all commands (typer gives this free)
- Error messages use `typer.echo(err=True)` with non-zero exit code

---

## AI/ML Basics Project: agent.py

**Goal:** A simple agentic loop using the OpenAI API that can answer questions and read/write local files as tools.

**Files:**
```
python-learning/
├── agent.py           # Main agent loop
├── tools.py           # Tool definitions and handlers
└── memory.json        # Conversation history (auto-created)
```

**What it does:**
```
You: summarize the file students.csv
Agent: [calls read_file tool] Here's a summary: 5 students, average grade 64, ...

You: write a haiku about Python and save it to haiku.txt
Agent: [calls write_file tool] Saved haiku.txt.

You: quit
Agent: Goodbye! Conversation saved to memory.json
```

**Tools the agent can use:**
- `read_file(path)` — reads a local file, returns content
- `write_file(path, content)` — writes content to a file
- `list_files(directory)` — returns list of files in directory

**Requirements:**
- Uses OpenAI `chat.completions.create` with `tools` parameter
- Tool handlers in `tools.py` as plain functions
- Agent loop: input → API call → check for tool call → handle → continue or respond
- Conversation history persisted to `memory.json`
- Handles `openai.APIError` gracefully
- `OPENAI_API_KEY` read from environment variable (not hardcoded)
