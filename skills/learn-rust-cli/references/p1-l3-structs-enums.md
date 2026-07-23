# P1-L3: Structs, Enums & Pattern Matching

## Concept

A **struct** groups related fields under one type:

```rust
struct Task {
    id: u32,
    title: String,
    status: Status,
}
```

An **enum** models a value that is exactly one of several variants — perfect for state:

```rust
enum Status {
    Todo,
    InProgress,
    Done,
}
```

Rust enums are richer than most languages': variants can carry data (`Blocked(String)` holding a reason). You inspect an enum with **`match`**, which must be **exhaustive** — cover every variant or the code won't compile. That exhaustiveness is a feature: add a new `Status` variant later and the compiler shows you every `match` that needs updating.

Methods live in an `impl` block: `impl Task { fn is_done(&self) -> bool { matches!(self.status, Status::Done) } }`. `&self` borrows the instance; `self` would consume it.

## Analogy

A struct is a form with labeled fields — name, id, status boxes all filled in on one sheet. An enum is a multiple-choice question where exactly one bubble is filled: a task is Todo *or* InProgress *or* Done, never two at once, never none. `match` is the grader that must have an answer key for every possible bubble.

## Workshop

**Setup:** Standalone `.rs` file (e.g., `model.rs`). This is the last standalone lesson — next lesson these types graduate into the real project.

**Task:**
1. Define a `Status` enum with `Todo`, `InProgress`, `Done`.
2. Define a `Task` struct with `id: u32`, `title: String`, `status: Status`.
3. `impl Task` with a method `fn status_label(&self) -> &str` that uses `match` to return `"todo"`, `"in progress"`, or `"done"`.
4. In `main`, create two tasks with different statuses and print `"#<id> <title> [<label>]"` for each.

## Acceptance Criteria / Edge Cases

- The `match` in `status_label` is exhaustive (no `_` wildcard — list all three variants so future additions are caught).
- `status_label` takes `&self` (borrows, doesn't consume the task).
- `Task` owns its `title: String`.

## Common Mistakes

- Using a `_ => ...` catch-all in the `match` — it silences the exhaustiveness check you actually want. List every variant explicitly here.
- Deriving nothing and then trying to print a `Task` with `{}` — that needs `Display` (Phase 2) or `#[derive(Debug)]` + `{:?}`.
- Taking `self` instead of `&self` in a method, then being unable to call it twice.

## Ship vs Portfolio Note

**Ship a real tool:** model illegal states out of existence. If a task can't be both done and blocked, an enum guarantees it — no defensive checks needed downstream.

**Learning/portfolio:** enums + exhaustive `match` are Rust's superpower for correctness. Get comfortable letting the compiler enforce "did you handle every case?"

## Bridge

You have a `Task` type with real state. But creating one from user input can fail — an empty title, a bad id. Next: `Option`, `Result`, and `?` — how Rust handles absence and failure without exceptions.
