# P2-L1: Widgets & Layout

## Concept

Everything visible in Flutter is a widget. `StatelessWidget` renders based only on the data passed into it (no internal mutable state) — use it when a screen/component never changes on its own. `StatefulWidget` pairs with a `State<T>` object that holds mutable data and calls `setState(() {...})` to trigger a rebuild when that data changes.

Layout is built from composition: `Scaffold` (screen skeleton: app bar, body, floating action button), `Column`/`Row` (vertical/horizontal stacking), `ListView.builder` (efficient scrolling list that only builds visible items), `Padding`/`SizedBox` (spacing). There's no CSS — every widget's size and position comes from its parent's constraints and the widget's own layout rules.

`ListView.builder(itemCount: ..., itemBuilder: (context, index) => ...)` is the standard way to render a list of items efficiently — it doesn't build all items upfront, only what's visible.

## Analogy

Widgets are like nesting dolls — a `Scaffold` contains a `Column`, which contains a `ListView`, which contains many list-item widgets. Each doll only knows how to hold the one inside it; the overall shape emerges from the nesting. `StatelessWidget` is a doll that's carved once and never changes; `StatefulWidget` is a doll with a small drawer inside (`State`) that can be opened and refilled, and every refill causes the doll to be redrawn.

## Workshop

**In `task_tracker/`:**

**Task:** Build the task list screen:
1. Create `lib/screens/task_list_screen.dart` with a `StatefulWidget` called `TaskListScreen`.
2. Its `State` holds `List<Task> tasks` (start with 3-4 hardcoded `Task` instances from `lib/models/task.dart`).
3. Render with `Scaffold(appBar: AppBar(title: Text("My Tasks")), body: ListView.builder(...))`, one row per task showing its title and status label (from `CompletionTracking.statusLabel()`).
4. Make `TaskListScreen` the `home:` of your `MaterialApp` in `main.dart`, replacing the placeholder text from lesson P1-L5.

## Acceptance Criteria / Edge Cases

- App builds and shows a scrolling list of the hardcoded tasks with title + status visible for each.
- Uses `ListView.builder`, not a manually unrolled `Column` of widgets (won't scale, and the lesson is about the builder pattern).
- Handles an empty task list gracefully (e.g., shows "No tasks yet" instead of a blank screen) — test this by temporarily setting `tasks` to `[]`.

## Common Mistakes

- Using `StatelessWidget` for `TaskListScreen` even though the task list will need to change later (add/edit/delete come next lesson) — should be `StatefulWidget` now to avoid a rewrite.
- Forgetting the `itemCount` parameter or setting it incorrectly (off-by-one, or hardcoding instead of `tasks.length`).
- Rebuilding the entire list from scratch outside `State` (e.g., as a local variable in `build()`) instead of storing it in `State` — loses data on every rebuild.

## Ship vs Portfolio Note

**Ship a real app:** `ListView.builder`'s lazy building matters once your task list is large — building all rows upfront (a plain `Column`) would visibly lag or crash on hundreds of items.

**Learning/portfolio:** this lesson is your first real "the compiler builds a UI from a widget tree" moment — take time to actually read the widget tree you wrote and trace which widget is the parent of which.

## Bridge

You can see your tasks, but you can't tap into one or add new ones yet. Next: navigation — a task-detail screen.
