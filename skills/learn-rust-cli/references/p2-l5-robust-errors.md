# P2-L5: Robust Error Handling

## Concept

So far errors have been `String`s or mismatched types papered over with `?`. Real Rust uses **one typed error enum** per crate, where each variant represents a failure mode:

```rust
#[derive(thiserror::Error, Debug)]
enum TaskError {
    #[error("task {0} not found")]
    NotFound(u32),
    #[error("invalid input: {0}")]
    Parse(String),
    #[error(transparent)]
    Io(#[from] std::io::Error),
    #[error(transparent)]
    Json(#[from] serde_json::Error),
}
```

**`thiserror`** derives the `Display` and `Error` impls from those attributes. The `#[from]` attribute auto-converts a `std::io::Error` or `serde_json::Error` into your type — so `?` "just works" across I/O, JSON, and your own logic, all funneling into `Result<T, TaskError>`.

Rule of thumb: **`thiserror`** for libraries / defined error types (you want callers to match on variants); **`anyhow`** for application `main` where you just want "any error, with context, printed nicely." A CLI often uses both: `thiserror` in the store, `anyhow::Result` in `main`.

## Analogy

Stringly-typed errors are sticky notes in a dozen handwritings — you can't sort or act on them programmatically. A typed error enum is a form with checkboxes: NotFound, BadInput, DiskProblem. Now any handler can glance at the box that's ticked and respond precisely, and `#[from]` is the mailroom that automatically reclassifies incoming errors from other departments into your form.

## Workshop

**Setup:** The `tasker` project.

**Task:**
1. `cargo add thiserror`. Define a `TaskError` enum with variants for: task-not-found (carrying the id), bad input, and `#[from]` conversions for `std::io::Error` and `serde_json::Error`.
2. Change `TaskStore` methods (`load`, `save`, `find`, `done`) to return `Result<_, TaskError>`. Delete the ad-hoc `String` errors — the `?` on I/O and JSON now converts automatically via `#[from]`.
3. Make `done <id>` return `TaskError::NotFound(id)` when the id doesn't exist.
4. In `main`, handle the top-level `Result`: print the error's `Display` message to stderr and exit non-zero on failure. (Optionally `cargo add anyhow` and make `main() -> anyhow::Result<()>`.)

## Acceptance Criteria / Edge Cases

- One `TaskError` enum funnels all failures; no more `String` errors in the store.
- `?` compiles across I/O, JSON, and domain errors thanks to `#[from]`.
- `done` on a missing id prints `"task N not found"` and exits non-zero — not a panic.
- Error messages go to **stderr**; the process exit code reflects failure.

## Common Mistakes

- Adding a variant but forgetting its `#[error("...")]` message — `thiserror` needs it to generate `Display`.
- Two `#[from]` impls for the same source type — each source can convert into exactly one variant.
- Printing errors to stdout, polluting the tool's real output. Errors → stderr; results → stdout.

## Ship vs Portfolio Note

**Ship a real tool:** typed errors + correct exit codes make `tasker` scriptable — other programs can rely on its exit status. This is the difference between a toy and a Unix citizen.

**Learning/portfolio:** the `thiserror`-in-lib / `anyhow`-in-main split is the idiomatic pattern you'll reuse in every Rust project. Knowing when to use which is a sign of maturity.

## Bridge

Phase 2 done — `tasker` is a real, persistent, well-behaved CLI. Phase 3 goes deeper into Rust's systems side. First: lifetimes and smart pointers — the tools for borrows and ownership shapes the simple cases didn't need.
