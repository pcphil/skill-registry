# P1-L1: Dart Syntax & Types

## Concept

Dart is statically typed with type inference — `var name = "Alice"` infers `String`, but the type is fixed after that. Dart has been null-safe by default since Dart 2.12: every type is non-nullable unless you explicitly mark it with `?` (e.g., `String? nickname`). The compiler forces you to handle the null case before using a nullable value — either with a null check, `??` (if-null), or `!` (assert non-null, use sparingly).

Functions are values in Dart. You can assign them to variables, pass them as arguments, and write them as arrow functions for one-liners: `int square(int x) => x * x;`.

Key types you'll use constantly: `int`, `double`, `String`, `bool`, `List`, `Map`, `Set`. Dart also has `dynamic` (opts out of static typing entirely) — avoid it unless there's a specific reason; it defeats the point of null safety and type checking.

## Analogy

Think of Dart's type system like labeled storage containers. A `String` container can only ever hold text — you can't accidentally put a number in it and have it silently work. Null safety is like a container having a "this container might be empty" sticker (`?`) — if it's not stickered, the compiler guarantees there's always something inside, so you never have to check.

## Workshop

**Setup:** No Flutter project yet — write plain Dart in a `.dart` file (e.g., `dart_basics.dart`), run with `dart run dart_basics.dart`.

**Task:** Write a function `describeTask(String title, {String? notes})` that:
- Takes a required `title` and an optional `notes` parameter.
- Returns a formatted string: `"Task: <title>"` if notes is null, or `"Task: <title> — <notes>"` if notes is provided.
- Uses null-safe access (`??` or explicit null check) — no `!` assertions.

Call it with at least 3 different inputs (with and without notes) and print the results.

## Acceptance Criteria / Edge Cases

- Compiles with null safety enabled (default in modern Dart) — no `!` used to force-unwrap `notes`.
- Handles `notes` being `null`, an empty string `""`, and a non-empty string correctly (empty string is not null — it should still print the dash).
- Function signature uses named optional parameter syntax correctly: `{String? notes}`.

## Common Mistakes

- Forgetting the `?` on `notes` and having the compiler reject calls without it.
- Using `notes!` to force-unwrap instead of `??` or a null check — works until it doesn't.
- Confusing `String?` (nullable) with `String` (non-nullable, must always have a value).

## Ship vs Portfolio Note

**Ship a real app:** null safety isn't optional in production Flutter — a `NoSuchMethodError` on null from unsafe code crashes the app in front of real users. Get comfortable with `??`, `?.`, and null checks now.

**Learning/portfolio:** focus on understanding *why* Dart forces this — it's less about avoiding crashes right now and more about building the habit of thinking through "can this ever be null?" for every value.

## Bridge

You now have a way to describe a single task. Next: collections — you'll hold many tasks in a list and start filtering/transforming them.
