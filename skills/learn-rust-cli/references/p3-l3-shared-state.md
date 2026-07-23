# P3-L3: Shared State — `Arc<Mutex<T>>`

## Concept

When multiple threads must read and write the **same** value, channels aren't enough — you need shared ownership plus synchronized access:

- **`Arc<T>`** — *Atomically Reference-Counted* pointer. Like `Rc`, but the count is thread-safe, so multiple threads can co-own the data. `Arc::clone(&x)` is cheap — it bumps a counter, it does not deep-copy the data.
- **`Mutex<T>`** — *mutual exclusion* lock. `.lock()` returns a guard giving exclusive access; other threads block until the guard drops (at end of scope). The lock is released automatically — no manual unlock.

Combined: **`Arc<Mutex<T>>`** is the canonical "shared mutable state across threads." Each thread gets an `Arc::clone`, locks the `Mutex` to touch the inner value, and the type system *forces* you to lock before access — you cannot reach the data without holding the lock.

```rust
let store = Arc::new(Mutex::new(TaskStore::new()));
let s = Arc::clone(&store);
thread::spawn(move || {
    let mut guard = s.lock().unwrap();
    guard.add("from thread");
});
```

## Analogy

`Arc` is a shared whiteboard with a check-in sheet — many people hold a key, and the board is erased only when the last key-holder leaves. `Mutex` is the single dry-erase marker sitting on the tray: to write, you must be holding the marker, and only one person can hold it at a time. Everyone else waits for the marker to hit the tray (the guard dropping) before they can grab it. You physically cannot write without the marker — that's the lock the compiler enforces.

## Workshop

**Setup:** The `tasker` project.

**Task:** Rework an operation to update a shared store from several threads:
1. Wrap a `TaskStore` in `Arc<Mutex<TaskStore>>`.
2. Spawn multiple threads (e.g. a concurrent variant of `import`, or several threads each adding a batch of tasks). Give each an `Arc::clone`; inside, `.lock()` and mutate.
3. Join all threads, then lock once on the main thread and confirm every task landed (count matches expected total).
4. Persist the final store with `save`.

## Acceptance Criteria / Edge Cases

- Threads share one `Arc<Mutex<TaskStore>>`; each locks before mutating.
- Final task count equals the sum of what every thread added — no lost updates.
- Guards are scoped tightly (lock, mutate, drop) so threads don't serialize longer than necessary.
- No deadlock: a thread never tries to lock the same `Mutex` twice while already holding it.

## Common Mistakes

- Cloning the *inner* `TaskStore` instead of the `Arc` — then each thread mutates its own copy and updates are lost. Clone the `Arc`, not the data.
- Holding the lock across a long or blocking operation, serializing all threads and killing concurrency. Lock late, release early.
- Locking the same mutex twice on one thread (e.g. a locked method calling another locked method) → self-deadlock. Keep critical sections small and non-nested.

## Ship vs Portfolio Note

**Ship a real tool:** a `.lock().unwrap()` panics if a holding thread panicked (poisoned lock). For a robust tool, handle the poisoned case or ensure critical sections can't panic. Note it now, harden in the capstone.

**Learning/portfolio:** `Arc<Mutex<T>>` is the shared-state pattern you'll see in nearly every concurrent Rust program. Understanding *why* the type forces lock-before-access is the whole lesson.

## Bridge

`tasker` is concurrent and correct — but how do you *know* it stays correct as you change it? Next: testing. Add unit and integration tests so the compiler's guarantees are backed by behavioral ones.
