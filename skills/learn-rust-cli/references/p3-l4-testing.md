# P3-L4: Testing

## Concept

Rust has a first-class, built-in test runner — no external framework needed. `cargo test` compiles and runs everything marked `#[test]`.

**Unit tests** live in the same file as the code they test, inside a module gated by `#[cfg(test)]` (so they're excluded from release builds):

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parses_valid_line() {
        let t = parse_task("3|Buy milk").unwrap();
        assert_eq!(t.id, 3);
        assert_eq!(t.title, "Buy milk");
    }

    #[test]
    fn rejects_empty_title() {
        assert!(parse_task("3|").is_err());
    }
}
```

Assertions: `assert!(cond)`, `assert_eq!(a, b)`, `assert_ne!`. A test that returns `Result<(), E>` can use `?` and passes on `Ok`. Test a panic with `#[should_panic]`.

**Integration tests** live in a top-level `tests/` directory — each file is a separate crate that uses your library's *public* API, testing it as a real consumer would. (This works best if your logic lives in a `lib.rs` the binary calls, but you can also test the binary's behavior.)

## Analogy

Tests are the safety net under a trapeze act. The compiler already checks you're holding the bar correctly (types, ownership). Tests check you actually land the trick — that `parse_task` really produces the right task, that `done` really flips the status. Unit tests inspect each move up close; integration tests watch the whole routine from the audience seats, using only what the public can see.

## Workshop

**Setup:** The `tasker` project.

**Task:**
1. Add a `#[cfg(test)] mod tests` to `task.rs` (or wherever your parser lives). Write tests covering: a valid line parses correctly, a missing `|` errors, a non-numeric id errors, an empty title errors.
2. Add tests in `store.rs` for core operations: adding a task increments the count; `done(id)` flips status to `Done`; `done` on a missing id returns `TaskError::NotFound`; `find` returns `Some`/`None` correctly.
3. Run `cargo test` and get everything green. Deliberately break one assertion to see a failure report, then fix it.
4. (Optional, if you have a `lib.rs`) add one integration test under `tests/` exercising add-then-list through the public API.

## Acceptance Criteria / Edge Cases

- `cargo test` passes; tests cover both success and failure paths (errors are asserted, not just happy paths).
- Test module is gated with `#[cfg(test)]` so it's excluded from the release binary.
- At least one test asserts a specific `Err` variant, not merely `is_err()`.

## Common Mistakes

- Only testing the happy path. The failure branches (bad input, missing id) are where bugs hide — assert them.
- Forgetting `use super::*;` inside the test module, so it can't see the items under test.
- Tests that depend on a real `tasks.json` on disk, making them order-dependent and flaky. Test in-memory logic; keep file I/O out of unit tests (or use a temp path).

## Ship vs Portfolio Note

**Ship a real tool:** tests are your regression net — they let you refactor and add features without fear. Run `cargo test` in CI before every release.

**Learning/portfolio:** a project with a green test suite signals engineering maturity to anyone reviewing it. Testing the error variants specifically shows you understand your own failure model.

## Bridge

`tasker` is correct, concurrent, persistent, and tested. Final step: the capstone — polish it into something you'd actually ship (or showcase). Clippy, a release build, and an error-handling audit.
