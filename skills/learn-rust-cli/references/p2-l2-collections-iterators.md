# P2-L2: Collections & Iterators

## Concept

Rust's workhorse collections: **`Vec<T>`** (growable array), **`HashMap<K, V>`** (key→value), and **`HashSet<T>`**. You already use `Vec`. A `HashMap<u32, Task>` lets you look tasks up by id in O(1).

**Iterators** are lazy, composable pipelines. `.iter()` borrows each element; `.into_iter()` consumes; `.iter_mut()` gives mutable references. Chain **adapters** and finish with a **consumer**:

```rust
let open: Vec<&Task> = tasks.iter()
    .filter(|t| !t.is_done())
    .collect();
```

Key adapters: `.map(...)`, `.filter(...)`, `.enumerate()`, `.take(n)`. Consumers: `.collect()`, `.count()`, `.sum()`, `.find(...)`, `.any(...)`. Sorting: `.sort_by(|a, b| ...)` or `.sort_by_key(|t| ...)` on a `Vec`.

**Closures** are inline anonymous functions: `|t| t.id`. They capture their environment (borrow or move surrounding variables) — that's what lets `.filter(|t| t.status == target)` see `target`.

## Analogy

An iterator pipeline is a factory conveyor belt. Raw items enter one end; each adapter (`filter`, `map`) is a station that inspects or reshapes them as they pass; nothing actually moves until a consumer (`collect`) switches the belt on and pulls items through. Closures are the instruction card taped to each station telling the worker exactly what to do.

## Workshop

**Setup:** The `tasker` project. Editing `src/main.rs`.

**Task:**
1. Add a `list --open` variant (or a `pending` command) that uses `.iter().filter(...)` to print only non-`Done` tasks.
2. Add sorting: before printing, sort tasks by status then id (`sort_by_key` or `sort_by`).
3. Add a `count` command that reports totals using iterator consumers — e.g. `"3 total, 1 done, 2 open"` computed with `.filter(...).count()`.
4. (If you're storing in a `Vec`) add a `find <id>` command using `.iter().find(|t| t.id == id)` returning an `Option<&Task>`, and print the task or "not found".

## Acceptance Criteria / Edge Cases

- Filtering and counting use iterator adapters/consumers, not hand-rolled `for` loops with a mutable counter.
- `find` returns `Option<&Task>` and both `Some`/`None` cases are handled.
- Sorting is stable and correct; an empty task list prints sensibly (no panic, no "1 done" nonsense).

## Common Mistakes

- Forgetting `.collect()` (or another consumer) and wondering why nothing happens — iterators are lazy.
- Calling `.into_iter()` when you meant `.iter()`, consuming the `Vec` you still need.
- Annotating `.collect()` with the wrong target type — the compiler needs to know `Vec<_>` vs `HashMap<_,_>`; give it a type hint on the binding.

## Ship vs Portfolio Note

**Ship a real tool:** iterator pipelines are both faster and clearer than manual loops — the compiler optimizes them heavily. Prefer them for any filtering/aggregation a user command needs.

**Learning/portfolio:** this is where Rust starts feeling expressive. Fluency with `map`/`filter`/`collect` is a marker of idiomatic Rust — practice reading a pipeline as one sentence.

## Bridge

`main.rs` is getting crowded — types, commands, and logic all in one file. Next: split the project into modules and pull in your first real dependency (`clap`) to parse commands properly.
