# P1-L2: Ownership & Borrowing

## Concept

This is the core of Rust. Every value has exactly **one owner**. When the owner goes out of scope, the value is freed — no garbage collector, no manual `free`. Three rules:

1. **Move**: assigning or passing a heap value (like `String`) transfers ownership. The old binding becomes invalid. `let a = String::from("hi"); let b = a;` — now `a` is moved out and using it is a compile error. (Copy types like `i32` are duplicated instead of moved.)
2. **Borrow**: instead of moving, you can lend a reference with `&`. `fn len(s: &String) -> usize` borrows `s` without taking ownership — the caller keeps it.
3. **Mutable borrow**: `&mut` lets a borrower modify. The rule: you may have **either** any number of shared `&` borrows **or** exactly one `&mut` borrow at a time — never both. This is what prevents data races at compile time.

A **slice** (`&str`, `&[T]`) is a borrowed view into part of a collection — no ownership, no copy.

## Analogy

Ownership is a library book. Only one person can be the borrower on record (the owner). You can *show* the book to friends to read over your shoulder (`&`, shared borrows — many at once, read-only). You can hand it to exactly one friend to write notes in (`&mut` — one at a time, no readers looking on). You can't have someone scribbling in it while others are trying to read — that's the rule the compiler enforces.

## Workshop

**Setup:** Standalone `.rs` file (e.g., `ownership.rs`).

**Task:**
1. Write `fn describe(task: &String) -> String` that **borrows** a task name and returns `"Task: <name>"`. Call it twice on the same `String` to prove borrowing didn't consume it.
2. Write `fn append_tag(task: &mut String, tag: &str)` that pushes `" #<tag>"` onto the string via a mutable borrow. Call it, then print the mutated string.
3. Deliberately trigger a move error: assign a `String` to a second binding, then try to use the first. Read the compiler error, then fix it by borrowing (or `.clone()`) and note in a comment which you chose and why.

## Acceptance Criteria / Edge Cases

- `describe` takes `&String` (or `&str`) and the original is still usable after — no move.
- `append_tag` takes `&mut String`; the caller's string reflects the change afterward.
- You can articulate the difference between the compile error before the fix and why borrowing resolves it.
- No `&` and `&mut` to the same value alive at once.

## Common Mistakes

- Using a value after it was moved (`borrow of moved value`) — the #1 beginner error.
- Reaching for `.clone()` everywhere to dodge the borrow checker. Clone is a real copy with a cost; borrow first, clone only when you genuinely need a second owner.
- Trying to take a `&mut` while a `&` is still in scope — restructure so the shared borrow ends first.

## Ship vs Portfolio Note

**Ship a real tool:** borrowing over cloning keeps a CLI fast and memory-light. Every needless `.clone()` in a hot path is wasted work — build the habit of borrowing now.

**Learning/portfolio:** don't fight the borrow checker — *listen* to it. Each error is teaching you an aliasing rule. When stuck, ask "who owns this, and who's borrowing it right now?"

## Bridge

You understand who owns and who borrows a value. Next: bundle related fields into a `Task` struct and model its state with an `enum` — the shapes your whole CLI will revolve around.
