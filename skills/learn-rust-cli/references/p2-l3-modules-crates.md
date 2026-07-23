# P2-L3: Modules & Crates

## Concept

**Modules** organize code within a crate and control visibility. Items are private by default; `pub` exposes them. You can declare a module inline (`mod task { ... }`) or in a separate file: `mod task;` in `main.rs` tells the compiler to load `src/task.rs`. Reference items by path: `task::Task`, or bring them into scope with `use task::Task;`.

A typical small binary splits into:
```
src/
├── main.rs     # entry point, arg wiring
├── task.rs     # Task, Status, their impls
└── store.rs    # the task collection + add/list/find logic
```

A **crate** is a package. External crates are declared in `Cargo.toml` under `[dependencies]` and downloaded from crates.io. **`clap`** is the standard CLI-argument crate — it parses subcommands, flags, and `--help` for you, replacing your hand-rolled `args` matching. Add it with `cargo add clap --features derive`, then define your CLI as a struct with `#[derive(Parser)]`.

## Analogy

Modules are the rooms of a house with doors you choose to lock (`pub` = unlocked). Everything's private until you deliberately open a door. Adding a crate is hiring a specialist contractor — `clap` is the one who's built a thousand front-desk intake systems, so you stop reinventing argument parsing and just describe what commands you want.

## Workshop

**Setup:** The `tasker` project.

**Task:**
1. Move `Task`/`Status` and their `impl`s into `src/task.rs`; declare `mod task;` in `main.rs` and `use` what you need. Make the types and methods `pub` as required.
2. Move the collection + operations (add, list, find, count) into `src/store.rs` as a `TaskStore` struct with methods.
3. `cargo add clap --features derive`. Define a `#[derive(Parser)]` CLI with subcommands `Add { title: String }`, `List`, `Done { id: u32 }`. Replace the manual `std::env::args` matching with `Cli::parse()` and a `match` on the subcommand.
4. Verify `cargo run -- --help`, `cargo run -- add "X"`, and `cargo run -- list` all work.

## Acceptance Criteria / Edge Cases

- Code compiles split across `main.rs`, `task.rs`, `store.rs` with correct `pub` visibility.
- `clap` generates `--help` and rejects unknown subcommands with a real error message (no manual usage string needed).
- `main` is now thin: parse args → call into `TaskStore`.

## Common Mistakes

- Forgetting `pub` on a type or method used across modules → `private` visibility errors. Expose only what's needed.
- Declaring `mod task;` but naming the file wrong (`Task.rs` vs `task.rs`) — the module name must match the filename.
- Over-deriving on the clap struct or mismatching subcommand field names — start minimal, add flags once the skeleton parses.

## Ship vs Portfolio Note

**Ship a real tool:** `clap` gives you `--help`, `--version`, and clear parse errors for free — table stakes for a tool anyone else runs. A clean module split keeps the codebase maintainable as commands grow.

**Learning/portfolio:** this is the moment `tasker` looks like a real Rust project. Understanding `mod`/`pub`/`use` and pulling a crate from crates.io are everyday skills.

## Bridge

`tasker` has real commands but forgets everything on exit. Next: persistence with `serde` — serialize the task store to JSON on disk and reload it on startup, so state survives between runs.
