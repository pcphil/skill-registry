# P2-L1: Traits & Generics

## Concept

A **trait** is a shared set of behavior — like an interface. A type *implements* a trait to promise it provides those methods:

```rust
use std::fmt;
impl fmt::Display for Task {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "#{} {} [{}]", self.id, self.title, self.status_label())
    }
}
```

Once `Task` implements `Display`, you print it with `{}` (not `{:?}`) — `println!("{task}")`. The standard library defines many traits you'll implement or derive: `Display`, `Debug`, `Clone`, `PartialEq`, `Default`.

**Generics** let one function or type work over many types, constrained by traits. `fn print_all<T: Display>(items: &[T])` accepts a slice of *anything* that implements `Display`. The `T: Display` is a **trait bound** — it says "T must be printable," and the compiler checks it at the call site.

## Analogy

A trait is a job certification. "Implements `Display`" is like "certified to give a presentation" — any type holding that cert can be asked to present itself, and callers don't care what the type is, only that it's certified. Generics are hiring by certification instead of by name: "send me anyone who's `Display`-certified," not "send me specifically a `Task`."

## Workshop

**Setup:** The `tasker` project. Editing `src/main.rs`.

**Task:**
1. Implement `Display` for `Task` so it renders `"#<id> <title> [<label>]"`. Switch your `list` command to print with `{}` instead of `{:?}`.
2. Write a generic function `fn print_numbered<T: Display>(items: &[T])` that prints each item on its own line prefixed with its 1-based position (`"1. ..."`). Use it to render the task list.
3. Confirm `cargo run -- list` still works and now uses your `Display` impl through the generic function.

## Acceptance Criteria / Edge Cases

- `Task` implements `Display`; the `list` output comes from `{}`, not `{:?}`.
- `print_numbered` is generic with a `T: Display` bound and borrows a slice (`&[T]`), not an owned `Vec`.
- Passing a `&[Task]` to `print_numbered` compiles and produces numbered output.

## Common Mistakes

- Implementing `fmt` but calling `.to_string()` inside it (infinite recursion — `to_string` uses `Display`). Use `write!(f, ...)`.
- Taking `Vec<T>` by value in the generic fn, moving the caller's tasks. Borrow with `&[T]`.
- Forgetting the trait bound and getting `T doesn't implement Display` — the bound is what unlocks `{}` inside the generic body.

## Ship vs Portfolio Note

**Ship a real tool:** a clean `Display` is your tool's user-facing voice — it's what shows up in every list, error, and log line. Design it to read well.

**Learning/portfolio:** traits + generics are how Rust achieves polymorphism without inheritance. This is the mental shift from OOP — behavior is composed via traits, not inherited from a base class.

## Bridge

`Task` presents itself well. Now the list is a plain `Vec` you scan by hand. Next: iterators and closures — filter, sort, and transform tasks with expressive pipelines instead of manual loops.
