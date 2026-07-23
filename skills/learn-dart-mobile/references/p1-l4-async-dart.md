# P1-L4: Async Dart

## Concept

Dart is single-threaded but non-blocking via an event loop. `Future<T>` represents a value that will be available later (or an error). `async`/`await` let you write asynchronous code that reads top-to-bottom like synchronous code, instead of nesting `.then()` callbacks.

A function marked `async` always returns a `Future`, even if you write `return 5;` inside it — Dart wraps it as `Future<int>`. `await` pauses execution of that function (not the whole app) until the awaited `Future` completes.

`Stream<T>` is the async equivalent of an `Iterable` — a sequence of values delivered over time instead of all at once (e.g., a live task-count updating as items are added). You'll use Streams more in Phase 2/3 with `StreamBuilder`; for now, just understand a Stream can emit 0, 1, or many values before completing.

## Analogy

A `Future` is like a food delivery order confirmation — you get a receipt immediately (the `Future` object), but the actual food (the value) arrives later. `await` is you waiting at the door instead of doing something else, but everyone else in the building (the rest of the app) keeps moving. A `Stream` is like a subscription box — instead of one delivery, you get several over time.

## Workshop

**Continue in the same Dart project.**

**Task:** Simulate an async task-sync operation without a real network call yet:
- Write `Future<List<Task>> fetchRemoteTasks()` that uses `Future.delayed(Duration(seconds: 1), () => [...])` to simulate network latency, returning a hardcoded list of 2-3 `Task` objects (reuse the class from lesson 3).
- Write an `async` function `printSyncedTasks()` that calls `await fetchRemoteTasks()` and prints each task's title and status label.
- Add basic error simulation: make `fetchRemoteTasks` randomly throw an exception (e.g., 1-in-4 chance) and wrap the call in `printSyncedTasks` with a `try`/`catch` that prints a friendly error message instead of crashing.

## Acceptance Criteria / Edge Cases

- `fetchRemoteTasks` returns `Future<List<Task>>`, not `List<Task>` directly.
- `printSyncedTasks` correctly awaits before printing — output should not appear until after the simulated delay.
- The `try`/`catch` actually catches the simulated failure at least once across a few runs (verify by running it several times) and doesn't crash the program.

## Common Mistakes

- Forgetting `async` on the function while still using `await` inside it (compile error) — or using `await` on something that isn't a `Future`.
- Not awaiting the `Future` at all, causing the print to run before data arrives (or silently doing nothing with an unawaited Future).
- Catching `Exception` too broadly and hiding real bugs — catch what you expect, log/print the rest.

## Ship vs Portfolio Note

**Ship a real app:** every real API/network call fails sometimes — timeouts, no connection, server errors. The `try`/`catch` habit you're building now is exactly what production sync code needs; Phase 3 builds directly on this pattern with a real HTTP call.

**Learning/portfolio:** the goal here is comfort with `async`/`await` and `Future` before Flutter adds UI state on top of it — debugging async UI bugs is much harder if the underlying async fundamentals aren't solid.

## Bridge

You can now simulate async data fetching. Next lesson: stop writing plain Dart scripts and scaffold the actual Flutter project — this is where your continuous app begins.
