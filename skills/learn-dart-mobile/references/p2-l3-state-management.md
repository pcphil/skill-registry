# P2-L3: State Management

## Concept

`setState()` works for state owned by a single widget, but it doesn't scale once multiple screens need to read or modify the same data (e.g., the list screen and detail screen both need the current task list). This is where a state-management approach earns its keep.

**Provider** (or Riverpod, its successor) is the most common approach taught here: define a class extending `ChangeNotifier` that holds your app's shared state (the task list) and exposes methods like `addTask()`, `toggleDone()`, `deleteTask()` — each calling `notifyListeners()` after mutating. Wrap your app (or the relevant subtree) in a `ChangeNotifierProvider`, and widgets that need the data use `context.watch<TaskProvider>()` (rebuilds on change) or `context.read<TaskProvider>()` (one-time read, e.g., inside a button's `onPressed`).

The key rule: `watch` in `build()` methods (so the widget rebuilds when data changes), `read` in event handlers (so you don't accidentally rebuild while just calling a method).

## Analogy

`setState` is like a sticky note only you can see and update. A shared state provider is a whiteboard in a shared office — anyone (any screen) can read it, and when someone updates it, everyone looking at the whiteboard sees the new version immediately without you having to walk around and tell each person individually.

## Workshop

**Task:**
1. Add the `provider` package to `pubspec.yaml` and run `flutter pub get`.
2. Create `lib/providers/task_provider.dart`: a `TaskProvider extends ChangeNotifier` holding `List<Task> _tasks`, with a getter `tasks`, and methods `addTask(Task task)`, `toggleDone(int index)`, `deleteTask(int index)` — each calling `notifyListeners()`.
3. Wrap `MaterialApp` in `main.dart` with `ChangeNotifierProvider(create: (_) => TaskProvider(), child: MaterialApp(...))`.
4. Update `TaskListScreen` to read tasks via `context.watch<TaskProvider>().tasks` instead of local hardcoded state.
5. Add a floating action button that calls `context.read<TaskProvider>().addTask(...)` with a new hardcoded task (a real add-task form comes in lesson P2-L5).
6. Add a checkbox or tap-to-toggle on each row calling `toggleDone(index)`, and a delete (swipe or button) calling `deleteTask(index)`.

## Acceptance Criteria / Edge Cases

- Adding a task via the floating action button immediately updates the visible list (no manual refresh needed).
- Toggling done/deleting updates both the list screen and, if the detail screen is open for that task, reflects correctly on return.
- Uses `watch` in `build()` and `read` inside `onPressed`/`onTap` handlers — not the reverse (using `read` in `build` won't rebuild on changes; using `watch` in a handler is unnecessary and can cause warnings).
- Deleting the last remaining task results in the empty-state message from lesson P2-L1, not a crash.

## Common Mistakes

- Using `context.watch` inside an `onPressed` callback (works but rebuilds unnecessarily and can throw in some contexts) — should be `context.read` there.
- Forgetting to call `notifyListeners()` after mutating `_tasks` — UI silently doesn't update, the classic "state changed but nothing happened" bug.
- Mutating `_tasks` from outside `TaskProvider` (e.g., a screen directly modifying the list) instead of going through the provider's methods — breaks the single-source-of-truth pattern.

## Ship vs Portfolio Note

**Ship a real app:** this shared-state pattern is what lets local persistence (next lesson) and cloud sync (Phase 3) plug in later without rewriting every screen — the provider becomes the one place that talks to storage.

**Learning/portfolio:** if `setState` felt fine for one screen, this lesson is the moment to feel *why* it stops being enough the instant a second screen needs the same data.

## Bridge

Tasks now live in shared state, but they vanish on app restart. Next: local persistence so tasks survive between sessions.
