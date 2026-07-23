# P3-L2: Concurrency — Threads & Channels

## Concept

`std::thread::spawn(|| { ... })` runs a closure on a new OS thread and returns a `JoinHandle`. Call `.join()` to wait for it and collect its result. A spawned thread may outlive the current scope, so its closure must not borrow locals that could vanish — you `move` owned data into it: `thread::spawn(move || ...)`.

To communicate, use a **channel** — `std::sync::mpsc::channel()` gives a `(Sender, Receiver)` pair (mpsc = *multi-producer, single-consumer*). Producers `tx.send(value)` (which **moves** the value across the thread boundary); the consumer `rx.recv()` or iterates `for msg in rx`. Clone the `Sender` to have multiple producers. When all senders drop, the receiver's iteration ends.

The key insight: Rust's ownership rules make this **safe at compile time**. A value sent down a channel is moved — the sender can't touch it afterward, so there's no shared-mutable-state data race. The `Send` marker trait (auto-implemented) is the compiler's proof a type is safe to move between threads.

## Analogy

Threads are extra workers you hire; each needs its own copy of the materials (`move`) because you can't have two people writing on the same sheet at once. A channel is a one-way pneumatic tube between desks: a worker drops a finished item in the tube (`send`) and it's *gone from their desk* — physically can't be double-handled — and the receiving desk pulls items out one at a time (`recv`). Ownership moving through the tube is exactly what prevents two workers clobbering the same item.

## Workshop

**Setup:** The `tasker` project.

**Task:** Add a `import <file>` command that bulk-parses many task lines concurrently:
1. Read a text file of task lines (one `"<id>|<title>"` per line — reuse your L4 parser).
2. Split the lines into a few chunks. `spawn` a worker thread per chunk that parses its lines and `send`s each resulting `Task` (or a parse error) down a channel. `move` each chunk into its thread.
3. The main thread collects everything from the `Receiver` into the store, then `join`s the workers.
4. Report how many imported and how many failed. Save the store.

(A handful of threads over a small file is illustrative, not a real speedup — the goal is the *pattern*: move data in, send results out, join.)

## Acceptance Criteria / Edge Cases

- Worker closures use `move`; no borrow of a local that outlives the thread.
- Results travel by channel; parsed tasks land in the store on the main thread.
- All handles are `join`ed — no thread silently dropped.
- An empty file or a file with some malformed lines is handled (report failures, don't panic).

## Common Mistakes

- Forgetting `move` on the closure → "closure may outlive borrowed value" compile error.
- Holding onto a `Sender` (or not dropping the original) so the receiver's `for msg in rx` loop never ends — deadlock. Drop or scope senders so the loop terminates.
- Trying to share the `Vec<Task>` directly across threads by reference — that's next lesson's job (`Arc`/`Mutex`). Here, send *owned* results through the channel instead.

## Ship vs Portfolio Note

**Ship a real tool:** for real parallel speedup on CPU-bound work you'd reach for `rayon` (`par_iter`) rather than hand-spawning threads. Know the manual pattern first so `rayon` isn't magic.

**Learning/portfolio:** "fearless concurrency" is Rust's headline claim, and this workshop shows why — the borrow checker turns data races into compile errors. That guarantee is the payoff for everything in Phase 1.

## Bridge

Channels move *owned* data between threads. But sometimes threads must share *one* mutable thing. Next: `Arc<Mutex<T>>` — safe shared state, letting multiple threads update the same task store.
