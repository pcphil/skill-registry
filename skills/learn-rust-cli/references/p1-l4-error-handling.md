# P1-L4: Error Handling — Option, Result, `?`

## Concept

Rust has no exceptions. Absence and failure are values you handle explicitly:

- **`Option<T>`** — a value that may be missing: `Some(x)` or `None`. Use it for "this might not exist" (a lookup that finds nothing).
- **`Result<T, E>`** — an operation that may fail: `Ok(x)` or `Err(e)`. Use it for "this could go wrong" (parsing, I/O).

You get the inner value by handling both cases — usually with `match`, or the ergonomic combinators (`.unwrap_or(...)`, `.map(...)`, `.ok_or(...)`). The **`?` operator** is the workhorse: in a function returning `Result`, `let n = s.parse::<u32>()?;` unwraps `Ok` or **returns the `Err` early** to the caller. It turns a pyramid of matches into a straight line.

`panic!` (and `.unwrap()`/`.expect()`) aborts the program — reserve it for truly unrecoverable bugs, not ordinary bad input. Bad input is a `Result`.

## Analogy

`Result` is a sealed delivery box that's either the item you ordered (`Ok`) or a "damaged in transit" slip (`Err`). You can't use the contents without opening the box and checking which it is. The `?` operator is a return-to-sender reflex: if it's the damage slip, don't struggle with it — hand it straight back up the chain to whoever can deal with it.

## Workshop

**Setup:** Standalone `.rs` file (e.g., `parse.rs`). Reuse the `Task`/`Status` types from L3 (copy them in).

**Task:** Write `fn parse_task(input: &str) -> Result<Task, String>` that parses a line like `"3|Buy milk"`:
1. Split on `'|'` into id and title parts.
2. If either part is missing, return `Err("expected '<id>|<title>'".to_string())`.
3. Parse the id with `.parse::<u32>()` — on failure return an `Err` describing it (use `?` or `.map_err(...)`).
4. Reject an empty title with an `Err`.
5. On success return `Ok(Task { id, title, status: Status::Todo })`.

In `main`, call it on one valid and two invalid inputs, and print the outcome of each with a `match`.

## Acceptance Criteria / Edge Cases

- Valid input → `Ok(Task)`; each bad input → a distinct, descriptive `Err`.
- Handles: missing `|`, non-numeric id, empty title, empty input.
- No `.unwrap()` / `.expect()` on the parse path — failures are returned, not panicked.

## Common Mistakes

- Reaching for `.unwrap()` to get past a `Result` — it panics on bad input, crashing the tool on data you should handle.
- Forgetting the function's return type must be `Result<_, _>` for `?` to work.
- Confusing `Option` (maybe absent) with `Result` (maybe failed) — use `.ok_or(...)` to convert `Option` → `Result` when you need an error message.

## Ship vs Portfolio Note

**Ship a real tool:** every `.unwrap()` is a potential crash in front of a user. Returning `Result` and reporting a clear message is the difference between a tool people trust and one that panics on a typo.

**Learning/portfolio:** internalize "errors are values." `?` will become second nature — it's the idiom that keeps error-handling code readable instead of nested.

## Bridge

You can model tasks and parse them safely. Time to stop writing throwaway files: next you scaffold the real `tasker` project with `cargo`, and everything from here builds on one growing codebase.
