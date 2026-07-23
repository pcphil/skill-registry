# P2-L4: Persistence with `serde`

## Concept

**`serde`** is Rust's serialization framework; **`serde_json`** is the JSON backend. You derive two traits on your types and serde generates the conversion code:

```rust
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize)]
struct Task { /* ... */ }
```

`enum Status` needs the same derives. Then:
- **Save**: `let json = serde_json::to_string_pretty(&tasks)?;` then `std::fs::write("tasks.json", json)?;`
- **Load**: `let json = std::fs::read_to_string("tasks.json")?;` then `let tasks: Vec<Task> = serde_json::from_str(&json)?;`

Both file I/O and parsing return `Result`, so the `?` operator threads errors up cleanly — the load/save functions return `Result`. On first run the file won't exist; handle that (start empty) rather than erroring.

Add the crates: `cargo add serde --features derive` and `cargo add serde_json`.

## Analogy

Serde is a translator between two languages your program and your disk each speak. In memory a `Task` is a live Rust struct; on disk it's flat JSON text. `Serialize` is translating your thoughts to a letter you can mail; `Deserialize` is reading a received letter back into thoughts. You derive the translator once and never hand-write the phrasebook.

## Workshop

**Setup:** The `tasker` project.

**Task:**
1. `cargo add serde --features derive` and `cargo add serde_json`. Add `#[derive(Serialize, Deserialize)]` to `Task` and `Status`.
2. In `TaskStore`, add `fn load(path: &str) -> Result<TaskStore, ...>` that reads and deserializes `tasks.json` — returning an **empty** store if the file doesn't exist yet.
3. Add `fn save(&self, path: &str) -> Result<(), ...>` that serializes to pretty JSON and writes the file.
4. Wire `main` to `load` at startup and `save` after any mutating command (`add`, `done`). Confirm state survives: `add` a task, exit, run `list` again and see it.

## Acceptance Criteria / Edge Cases

- Tasks persist across separate `cargo run` invocations via `tasks.json`.
- First run (no file) starts with an empty store instead of erroring — check for `NotFound` specifically, don't swallow all errors.
- Save writes valid, human-readable JSON (`to_string_pretty`).
- Mutating commands save; read-only commands (`list`) don't need to.

## Common Mistakes

- Deriving `Serialize`/`Deserialize` on `Task` but forgetting `Status` — serde needs it on every nested type.
- Treating "file not found" as a fatal error on first run. Distinguish `ErrorKind::NotFound` (→ empty store) from real I/O errors (→ propagate).
- Forgetting to `save` after `add`, so changes vanish on exit — the classic "it worked in memory" bug.

## Ship vs Portfolio Note

**Ship a real tool:** decide where the file lives — a fixed `tasks.json` in the cwd is fragile; a real tool uses a config/data dir. Note this as a known limitation now, fix it in the capstone.

**Learning/portfolio:** serde's derive-based approach is a highlight of Rust's ecosystem — zero boilerplate, fully type-checked. This pattern (derive + `to_string`/`from_str`) recurs across the whole ecosystem.

## Bridge

`tasker` now persists, but the load/save code is littered with `?` returning stringly-typed or mismatched errors. Next: design a proper error type with `thiserror` so every failure has one clean, typed channel.
