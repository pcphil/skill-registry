# P2-L2: Navigation & Routing

## Concept

Flutter navigation is stack-based: `Navigator.push(context, route)` pushes a new screen on top, `Navigator.pop(context)` returns to the previous one. `MaterialPageRoute` is the standard route type — it gives you the platform-appropriate transition animation for free.

To pass data to the next screen, pass it as a constructor argument to the destination widget (e.g., `TaskDetailScreen(task: tasks[index])`). To pass data *back* when popping, `Navigator.pop(context, someValue)` and `await` the result of the original `push` call.

Named routes (`Navigator.pushNamed`) exist for larger apps with many screens, but explicit `MaterialPageRoute` pushes are simpler and clearer for now — stick with explicit pushes for this curriculum.

## Analogy

Navigation is a stack of index cards. Pushing a new screen is like placing a new card on top of the pile — you can only see and interact with the top card. Popping removes the top card, revealing the one underneath again. Passing data back is like writing a note on the card before you remove it, so the card below can read what you wrote.

## Workshop

**Task:**
1. Create `lib/screens/task_detail_screen.dart` — a `StatelessWidget` (it just displays one `Task`, no need for internal state yet) that shows the task's title, notes, and status label in a `Scaffold`.
2. In `task_list_screen.dart`, wrap each list row in a `GestureDetector` or use `ListTile`'s `onTap`, and on tap: `Navigator.push(context, MaterialPageRoute(builder: (_) => TaskDetailScreen(task: tasks[index])))`.
3. Add a back button behavior check: confirm the platform back button/gesture and an explicit `AppBar` back arrow both correctly return to the list.

## Acceptance Criteria / Edge Cases

- Tapping any task row navigates to a detail screen showing that specific task's data (not always the first task — a common indexing bug).
- Detail screen correctly displays a task with no `notes` (null) without crashing or showing the literal word "null".
- Back navigation (both gesture/button and AppBar arrow) returns to the list screen with the list state intact (no tasks lost or duplicated).

## Common Mistakes

- Passing the wrong task (e.g., always `tasks[0]` due to a closure capturing the wrong loop variable in older Dart, or hardcoding an index instead of using the builder's `index` parameter).
- Forgetting to handle `notes == null` in the detail screen's `Text()` widget — interpolating null directly into a string shows `"null"` literally.
- Not using `MaterialPageRoute` and instead trying to swap widgets in place — loses the native transition and proper back-stack behavior.

## Ship vs Portfolio Note

**Ship a real app:** users expect back gestures/buttons to always work predictably — test on a real device or simulator, not just hot-reload, since navigation edge cases (double-back, rapid taps) show up more clearly there.

**Learning/portfolio:** this is a good place to intentionally break the indexing (hardcode `tasks[0]`) and observe the bug, then fix it — seeing the wrong-data bug firsthand makes the correct pattern stick.

## Bridge

You can view a task's details, but you still can't add, edit, or delete anything — the list is static. Next: real state management for add/edit/delete.
