# P2-L5: Forms & Validation

## Concept

Flutter's `Form` widget wraps a set of form fields and coordinates validation across all of them via a `GlobalKey<FormState>`. Each `TextFormField` takes a `validator: (value) => ...` function returning an error string (shown under the field) or `null` (valid). Calling `formKey.currentState!.validate()` runs every field's validator and returns `true` only if all pass.

`TextEditingController` holds the live text of a field so you can read its current value on submit without relying on `setState` for every keystroke. Always `dispose()` controllers in the widget's `dispose()` method to avoid memory leaks.

## Analogy

A `Form` is like a paper application form with multiple boxes — each box (`TextFormField`) has its own small-print rule ("must not be empty"), but you don't find out which boxes failed until you hit "submit" (`validate()`), at which point every box highlights its own problem at once rather than one at a time.

## Workshop

**Task:**
1. Create `lib/screens/add_task_screen.dart`: a form with a `TextFormField` for `title` (required, validator: non-empty) and one for `notes` (optional, no validator needed).
2. On submit (a button, or `AppBar` action), call `formKey.currentState!.validate()`; if valid, build a `Task` from the field values and call `context.read<TaskProvider>().addTask(...)`, then `Navigator.pop(context)` back to the list.
3. Replace the floating-action-button placeholder from lesson P2-L3 (which added a hardcoded task) — it should now navigate to `AddTaskScreen` instead.
4. Dispose both `TextEditingController`s properly.

## Acceptance Criteria / Edge Cases

- Submitting with an empty title shows a validation error under the field and does not add a task or navigate away.
- Submitting with a valid title (with or without notes) adds the task and returns to the list, which now shows it.
- Notes field being empty is treated as "no notes" (`null` or empty string, consistent with how `p1-l1` and the detail screen already handle a missing notes value) — not a validation failure.
- Controllers are disposed — no "used after dispose" warnings/errors when navigating away and back repeatedly.

## Common Mistakes

- Forgetting to check the `validate()` return value before proceeding — adding the task even when a field is invalid.
- Reading field values via `setState`-tracked strings instead of `TextEditingController.text` — works but is unnecessarily complex; use the controller.
- Leaking controllers by not overriding `dispose()` — small in a demo app, real problem at scale.

## Ship vs Portfolio Note

**Ship a real app:** validation is a user-trust feature — a form that silently accepts garbage (or crashes on empty input) is a common cause of real bug reports. Get the empty-title case right; it's the one users will hit constantly.

**Learning/portfolio:** this lesson closes the loop on Phase 2 — you now have full CRUD (create via this form, read via the list/detail screens, update via toggle-done, delete via the delete action) backed by real persistence.

## Bridge

Phase 2 is complete — full CRUD with persistence, all local. Phase 3 connects this app to the outside world: real HTTP calls, authentication, and cloud sync.
