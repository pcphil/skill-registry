# P1-L3: OOP in Dart

## Concept

Dart classes look like most OOP languages: fields, constructors, methods. Dart adds a few idioms worth knowing early:
- **Named constructor shorthand**: `Task({required this.title, this.done = false});` assigns constructor parameters directly to fields — no manual `this.title = title` body needed.
- **Mixins** (`mixin`, `with`): add behavior to a class without inheritance. A mixin can't be instantiated on its own; it's "mixed in" to a class via `with`.
- **Interfaces implicitly**: any Dart class can be used as an interface via `implements` — there's no separate `interface` keyword.
- **Immutability**: mark fields `final` when they shouldn't change after construction. Prefer immutable data classes where practical — easier to reason about, fewer accidental-mutation bugs.

## Analogy

A class is a blueprint (a cookie cutter); each instance is a cookie made from it. A mixin is like a stamp you can press onto any cookie to add a design — it doesn't care what shape the cookie is, it just adds the same decoration to whichever ones request it.

## Workshop

**Continue in the same Dart project (no Flutter yet).**

**Task:** Replace the `Map`-based task model from lesson 2 with a real class:
- Define `class Task` with `final String title`, `final String? notes`, and `bool done`.
- Define `mixin CompletionTracking` with a method `String statusLabel()` that a class using it can call — it should read a `done` field the mixin doesn't itself define (i.e., the mixin references `done`, and `Task` provides it).
- Make `Task` use the mixin: `class Task with CompletionTracking { ... }`.
- Rewrite lesson 2's `incompleteTitles` to accept `List<Task>` instead of `List<Map<String, dynamic>>`.

## Acceptance Criteria / Edge Cases

- `Task` compiles and instantiates with named constructor parameters (`Task(title: "Buy milk")`).
- `CompletionTracking.statusLabel()` returns something like `"✓ done"` or `"○ pending"` based on the task's `done` value.
- `incompleteTitles` works identically to lesson 2 but operates on `List<Task>` now — type-safe, no string-key typos possible.

## Common Mistakes

- Trying to give the mixin its own `done` field instead of relying on the field from the class it's mixed into (causes ambiguity or shadowing bugs).
- Forgetting `required` on constructor parameters that have no default — Dart will let a nullable field default to `null` silently if you're not careful.
- Making `done` `final` — it needs to be mutable since marking a task complete changes it after creation.

## Ship vs Portfolio Note

**Ship a real app:** this `Task` class becomes your app's core domain model for the rest of the curriculum — every later lesson (local storage, forms, API sync) serializes and deserializes this exact shape. Getting the fields right now saves rework later.

**Learning/portfolio:** this is a good moment to see why "we'll just use a Map for now" from lesson 2 breaks down as an app grows — the class version is self-documenting and typo-proof.

## Bridge

Your `Task` model is solid, but everything so far runs synchronously and instantly. Real apps wait on things — network calls, disk reads. Next: async Dart.
