# Copilot Instructions — Task Tracker (Dart/Flutter learning project)

Copilot has no multi-step workflow or memory system, so these are static coding conventions for the app being built while learning Dart and Flutter — not a tutoring script. A human is following an external curriculum; these instructions keep Copilot's suggestions consistent with it.

## Stack

- Language: Dart, null safety on
- Framework: Flutter (mobile only)
- State: Provider (`ChangeNotifier`)
- Persistence: sqflite
- Networking: `http` + `dart:convert`

## Code Style

- Domain data as typed classes (e.g. `Task`), not loose `Map<String, dynamic>`.
- Named constructor parameters, not positional.
- `watch` in `build()`, `read` in event handlers.

## Preferred Patterns

- Every async user action (sync, login, save) shows loading, error-with-retry, or success — never a silent blank state.
- Credentials/API keys read from environment/config (`String.fromEnvironment`), never hardcoded.
- `Task.updatedAt` drives sync/merge comparisons.

## Patterns to Avoid

- Storing raw passwords anywhere — only a session token/flag.
- Recreating a `Future` inside `FutureBuilder`'s `build()` on every rebuild.
- Mutating the task list outside `TaskProvider`'s own methods.

## Testing

- Tests in `test/`, named `<screen>_test.dart`
- Run: `flutter test`

## Scope

These instructions apply to `lib/`, `pubspec.yaml`, and `test/` in this Flutter project only — not to web/desktop targets or backend code.
