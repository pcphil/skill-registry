# P3-L1: Lifetimes & Smart Pointers

## Concept

**Lifetimes** are the compiler's way of guaranteeing a reference never outlives the data it points to. Most of the time they're inferred (elided). You write them explicitly when a function returns a reference and the compiler can't tell which input it borrows from:

```rust
fn longest_title<'a>(a: &'a Task, b: &'a Task) -> &'a str {
    if a.title.len() >= b.title.len() { &a.title } else { &b.title }
}
```

`'a` is a name for a scope; it says "the returned reference lives as long as both inputs." Lifetimes don't change runtime behavior — they're purely a compile-time proof of validity.

**Smart pointers** own heap data with extra behavior:
- **`Box<T>`** — a single owned value on the heap. Needed for recursive types (`enum Tree { Node(Box<Tree>) }`) or trait objects (`Box<dyn Error>`).
- **`Rc<T>`** — reference-counted shared ownership (single-threaded); many owners, freed when the last drops.
- **`RefCell<T>`** — interior mutability: mutate through a shared reference, with borrow rules checked at *runtime* instead of compile time. Often paired as `Rc<RefCell<T>>`.

## Analogy

A lifetime is a "best before" date the compiler stamps on every borrowed reference, then refuses to let you use one past the date its data is valid — no dangling pointers, checked before the program ever runs. `Box` is renting one storage unit for a big item. `Rc` is a shared storage unit with a signed clipboard of key-holders — the unit's emptied only when the last name is crossed off. `RefCell` is a unit with a single "in use" sign you flip yourself, and you get caught (a panic) if two people flip it at once.

## Workshop

**Setup:** The `tasker` project.

**Task:**
1. Add a function to `store.rs` that returns a **reference** derived from two borrowed inputs, requiring an explicit lifetime — e.g. `fn newer_of<'a>(a: &'a Task, b: &'a Task) -> &'a Task` (compare by id), or `longest_title` above. Wire it into a small command or a test call.
2. In a comment, explain *why* the lifetime annotation is required here (the compiler can't infer which input the output borrows from).
3. Demonstrate one smart pointer meaningfully: e.g. change your top-level error handling to `Box<dyn std::error::Error>`, **or** prototype a small `Rc<RefCell<...>>` shared counter and note in a comment where single-ownership would have been simpler.

## Acceptance Criteria / Edge Cases

- The lifetime-annotated function compiles and is actually called somewhere.
- You can articulate why elision doesn't cover this case.
- The smart-pointer demo compiles and you've noted what it buys you over a plain owned value.

## Common Mistakes

- Sprinkling `'a` everywhere hoping to satisfy the compiler. Add lifetimes only where inference genuinely fails, and let the error message guide the exact placement.
- Reaching for `Rc<RefCell<T>>` to dodge the borrow checker when a plain `&mut` or restructuring would work — it trades compile-time safety for runtime panics. Use it only when shared mutable ownership is truly needed.
- Returning a reference to a local (`&String` created inside the fn) — no lifetime can save that; return an owned `String`.

## Ship vs Portfolio Note

**Ship a real tool:** most CLI code needs neither explicit lifetimes nor `Rc`/`RefCell` — prefer owned data and simple borrows. Know these tools so you recognize when you actually need them, not so you use them everywhere.

**Learning/portfolio:** lifetimes are the last big conceptual wall in Rust. Understanding that they're proofs, not runtime machinery, dissolves most of the confusion.

## Bridge

You've rounded out Rust's ownership model. Now put it to work concurrently: next, spawn threads and pass data between them with channels — safely, because the ownership rules you've learned are exactly what make it safe.
