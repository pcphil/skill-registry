# P1-L5: Project Scaffold — `cargo new tasker`

## Concept

`cargo` is Rust's build tool and package manager. `cargo new tasker` creates a project:

```
tasker/
├── Cargo.toml     # manifest: name, version, dependencies
└── src/
    └── main.rs    # entry point — fn main()
```

`cargo run` compiles and runs; `cargo build` compiles; `cargo check` type-checks fast without producing a binary. Dependencies go under `[dependencies]` in `Cargo.toml` and are pulled from crates.io.

A binary reads command-line arguments via `std::env::args()`, which yields an iterator of `String`s (the first is the program name). Collect them: `let args: Vec<String> = std::env::args().collect();`.

This lesson **starts the continuous project.** The `Task` and `Status` types from earlier lessons now live in `src/main.rs` (a dedicated module comes in Phase 2). From here, every lesson adds to *this* codebase.

## Analogy

`cargo new` is unpacking a flat-pack furniture kit: you get the frame (`main.rs`), the parts list (`Cargo.toml`), and standard fittings, so you start assembling instead of milling your own screws. `cargo run` is the one button that both builds and switches it on.

## Workshop

**Setup:** `cargo new tasker`, then `cd tasker`. From now on this is the project — do not delete it.

**Task:** Build a minimal in-memory task list:
1. Bring the `Task` struct and `Status` enum into `src/main.rs`. Add `#[derive(Debug)]` to both so you can print them with `{:?}`.
2. In `main`, create a `Vec<Task>` and seed it with two or three tasks.
3. Read `std::env::args()`. If the first argument is `"list"`, print each task as `"#<id> <title> [<status>]"`. If it's `"add"`, take the next argument as a title, push a new task (auto-increment the id), and print confirmation. Otherwise print a short usage line.
4. Run `cargo run -- list` and `cargo run -- add "Write tests"` to test both paths.

## Acceptance Criteria / Edge Cases

- `cargo run -- list` prints the seeded tasks; `cargo run -- add "X"` reports the new task.
- No arguments (or an unknown command) prints a usage message instead of panicking or indexing out of bounds.
- Argument indexing is bounds-safe — use `.get(1)` / `match` on the args, not `args[1]` blind.

## Common Mistakes

- Indexing `args[1]` when no argument was passed → panic. Use `args.get(1)` and handle `None`.
- Forgetting the `--` in `cargo run -- add "X"` — without it, cargo tries to interpret the args itself.
- Reconstructing the whole `Vec` on `add` instead of `push`ing — you have a `mut` binding; mutate it.

## Ship vs Portfolio Note

**Ship a real tool:** a clear usage message and bounds-safe argument handling are the first thing a real user hits. Get the "no args" and "bad command" paths right from day one.

**Learning/portfolio:** you now have a running program you can grow. Commit it to git — each future lesson is a natural commit and a visible portfolio history.

## Bridge

`tasker` runs and holds tasks in memory. It prints with the crude `{:?}` debug format. Next: traits — teach `Task` how to present itself properly with `Display`, and meet generics.
