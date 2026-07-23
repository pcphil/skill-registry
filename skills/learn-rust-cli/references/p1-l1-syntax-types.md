# P1-L1: Syntax & Types

## Concept

Rust is statically typed with inference — `let count = 5` infers `i32`, but the type is fixed after that. Bindings are **immutable by default**: `let x = 5` cannot be reassigned; you must opt into mutation with `let mut x = 5`. This is the opposite default from most languages and it's deliberate — immutability is the safe path, mutation is the exception you declare.

Core scalar types: `i32`/`i64`/`u32`/`usize` (integers), `f64` (float), `bool`, `char`. Compound types: tuples `(i32, &str)` and arrays `[i32; 3]`. Text has two forms you'll juggle constantly — `&str` (a borrowed string slice, often a literal) and `String` (an owned, growable string). Functions declare parameter and return types explicitly: `fn add(a: i32, b: i32) -> i32 { a + b }`. Note the last expression with no semicolon *is* the return value.

Control flow: `if` is an expression (`let x = if cond { 1 } else { 2 };`), `loop`/`while`/`for`, and `match` (covered fully in L3).

## Analogy

Think of `let` bindings like ink versus pencil. `let x = 5` is ink — written once, permanent. `let mut x = 5` is pencil — you chose an eraser on purpose. Most languages hand you a pencil and hope you don't scribble; Rust hands you ink and makes you ask for the pencil.

## Workshop

**Setup:** No project yet. Write plain Rust in a `.rs` file (e.g., `basics.rs`), compile and run with `rustc basics.rs && ./basics` — or if you prefer, `cargo new scratch` and edit `src/main.rs`, run with `cargo run`.

**Task:** Write a `main` function that:
- Binds an immutable `title: &str` and a mutable `priority: i32`.
- Increments `priority` at least once (proving it's `mut`).
- Defines a separate function `fn format_task(title: &str, priority: i32) -> String` that returns `"[P<priority>] <title>"` using `format!`.
- Calls it and prints the result with `println!`.

Use an explicit `fn` with typed parameters and a typed return — no closures yet.

## Acceptance Criteria / Edge Cases

- Compiles with no warnings. Reassigning the immutable binding must fail to compile (try it once to see the error, then remove it).
- `format_task` returns an owned `String` (via `format!`), not a `&str`.
- `println!("{}", ...)` prints the formatted string; the `{}` placeholder count matches the args.

## Common Mistakes

- Forgetting `mut` and getting `cannot assign twice to immutable variable`.
- Trying to return a `&str` built from `format!` — that borrows a temporary and won't compile. Return `String`.
- Adding a semicolon after the final expression in a function, turning the return value into `()` (unit).

## Ship vs Portfolio Note

**Ship a real tool:** immutable-by-default is a correctness feature — it makes accidental mutation a compile error, not a runtime bug. Lean into it; reach for `mut` only when you truly rebind.

**Learning/portfolio:** focus on the mental model — every value has one owner and a known type at all times. Getting comfortable reading compiler errors now pays off for the entire course.

## Bridge

You can name and format a single task's fields. Next: ownership and borrowing — the rule that governs who is allowed to touch a value and when. This is the concept that makes Rust *Rust*.
