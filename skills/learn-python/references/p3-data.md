# P3: Data / Automation Track

Full project spec: `references/projects.md` → "Data/Automation Project: pipeline.py"

## L1: pandas Basics

**Concept:** pandas represents tabular data as a `DataFrame` — rows and columns like a spreadsheet, but in memory. `read_csv()` loads a CSV in one line. `df.head()`, `df.describe()`, `df["column"]`, and `df[condition]` cover 80% of day-to-day data work.

**Task:** Install pandas. Write `explore.py` that reads `raw_data/sales_2024.csv`, prints the first 5 rows, prints column data types, and prints how many rows have a missing region.

```bash
pip install pandas
python explore.py
```

**Acceptance criteria:** Output shows head, dtypes, and missing count. Script runs without error even on the messy CSV (NaN values are fine at this stage).

**Common mistakes:** Using `df["region"] == None` — use `df["region"].isna()` instead. Forgetting that `read_csv` reads all columns as strings by default unless you specify dtypes.

---

## L2: Cleaning Messy Data

**Concept:** Real data is dirty: missing values, wrong types, inconsistent formatting, duplicates. pandas has targeted tools for each: `fillna()`, `dropna()`, `astype()`, `str.strip()`, `str.title()`, `drop_duplicates()`.

**Task:** Create `cleaner.py` with pure functions (no side effects). Implement:
- `normalize_products(df)` — strip and title-case the product column
- `fill_missing_region(df)` — fill NaN regions with "Unknown"
- `drop_bad_sales(df)` — drop rows where sales can't be converted to a number
- `normalize_dates(df)` — standardize date column to YYYY-MM-DD

**Acceptance criteria:** Each function takes a DataFrame and returns a new one (no mutation). Running them in sequence on `sales_2024.csv` yields a clean DataFrame with no NaN values and consistent types.

**Common mistakes:** Mutating the input DataFrame — always return a copy (`df.copy()`). Using `df["col"].apply(lambda x: ...)` when a vectorized method exists (e.g., `str.strip()`).

---

## L3: Aggregation and Output

**Concept:** `groupby()` splits a DataFrame into groups. `agg()` applies functions to each group. Together they answer "what's the total sales per region?" and similar questions efficiently.

**Task:** Create `reporter.py`. Write functions that:
- Print total sales by product using `groupby` + `sum`
- Print total sales by region
- Write `output/clean_sales.csv` (cleaned data)
- Write `output/summary.txt` (stats report matching the expected format in `projects.md`)

**Acceptance criteria:** Both output files created. Summary matches expected format. All logic in named functions.

**Common mistakes:** Forgetting `as_index=False` in groupby when you want the group key as a column. Using `print(df)` for the output file instead of `to_csv()`.

---

## L4: Automation Script

**Concept:** The `schedule` library lets Python scripts run on a timer. Combine it with file-watching logic to build a pipeline that processes new files automatically.

**Task:** Add a `--watch` flag to `pipeline.py`. When passed, use `schedule` to run the full pipeline every 60 seconds. Print "Pipeline ran — N rows processed" each time.

```bash
pip install schedule
python pipeline.py --watch
```

**Acceptance criteria:** Script runs in a loop, re-processes on schedule. `Ctrl+C` exits cleanly. `python pipeline.py` (no flag) runs once and exits.

**Common mistakes:** Calling `schedule.run_pending()` without a `time.sleep()` — CPU spins at 100%. Not handling `KeyboardInterrupt` — user sees a traceback on Ctrl+C.
