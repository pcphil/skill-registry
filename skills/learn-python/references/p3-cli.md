# P3: CLI Tools Track

Full project spec: `references/projects.md` → "CLI Tools Project: devtool"

## L1: typer Basics

**Concept:** typer turns Python functions into CLI commands using type hints. Add `@app.command()` to a function, and typer gives it argument parsing, `--help`, and error messages for free. No argparse boilerplate needed.

**Task:** Install typer and rich. Create `devtool/main.py` with one command: `devtool hello <name>` that prints a greeting.

```bash
pip install typer rich
python main.py hello Alice
# Hello, Alice!
python main.py --help
# Shows usage automatically
```

**Acceptance criteria:** Command runs. `--help` output is clean. Name argument is required (typer errors if missing).

**Common mistakes:** Not calling `typer.run()` or `app()` at the bottom — the script does nothing. Mixing `print()` with rich `Console` — pick one.

---

## L2: Multiple Commands

**Concept:** `typer.Typer()` creates an app with multiple subcommands. Each `@app.command()` function becomes a subcommand. Arguments (positional) vs options (`--flag`) work via type annotations: `name: str` is an argument, `name: str = typer.Option(...)` is an option.

**Task:** Expand `main.py`. Add these commands under an `app`:
- `devtool env list` — prints all environment variables
- `devtool env get VAR_NAME` — prints a single var's value
- `devtool files count PATH` — counts files by extension in a directory

Use sub-apps (typer groups) for `env` and `files`.

**Acceptance criteria:** All three commands work. `devtool --help` shows both subgroups. Missing required argument shows a helpful error.

**Common mistakes:** Using `@app.command("env")` for multiple env subcommands — use a nested `typer.Typer()` added with `app.add_typer()`. Option vs argument confusion: `path: str` vs `path: str = typer.Argument(...)`.

---

## L3: Rich Output

**Concept:** rich renders tables, progress bars, colored text, and markdown in the terminal. `Console` is the main entry point. `Table` builds formatted tables. Colors and styles use markup like `[bold green]text[/]`.

**Task:** Update all commands to use rich output:
- `env list` → rich `Table` with columns: Name, Value
- `files count` → rich `Table` with columns: Extension, Count, % of total
- Errors → `console.print("[bold red]Error:[/] ...")` to stderr

**Acceptance criteria:** Tables render with borders. Error messages are red. `--no-color` flag (typer/rich) disables styling.

**Common mistakes:** Creating a new `Console()` in every function — create once at module level. Forgetting `console.print(table)` — just `Table()` doesn't print itself.

---

## L4: Config and Persistence

**Concept:** CLI tools often need user settings that persist between runs. Storing config in `~/.devtool/config.json` is the conventional approach on all platforms. `pathlib.Path.home()` gets the home directory portably.

**Task:** Create `config.py`. Implement:
- `load_config()` → reads `~/.devtool/config.json`, returns dict (empty if missing)
- `save_config(config)` → writes updated config
- Add `devtool config set KEY VALUE` and `devtool config get KEY` commands
- Add `devtool config list` → rich table of all settings

**Acceptance criteria:** Settings persist between runs. `config get` on missing key prints "Not set". Config directory created automatically if absent.

**Common mistakes:** Using `open("~/.devtool/config.json")` — `~` not expanded; use `Path.home() / ".devtool" / "config.json"`. Not creating the parent directory before writing: `path.parent.mkdir(parents=True, exist_ok=True)`.
