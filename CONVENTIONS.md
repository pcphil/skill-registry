# Task Tracker — Learning Project Conventions

This file documents the conventions for `task_tracker/`, a Flutter app built incrementally while learning Dart and Flutter. Aider has no agentic workflow or memory system — these are static conventions for whichever phase of the app you're currently editing, not a tutoring script. The human developer drives which phase/lesson is active; ask them if it's unclear from the current files.

## Stack

- Language: Dart (null safety on, no `dynamic` unless justified)
- Framework: Flutter (mobile targets only — no web/desktop)
- State management: Provider (`ChangeNotifier` + `context.watch`/`context.read`)
- Local persistence: sqflite
- Networking: `http` package + `dart:convert`
- Auth: Firebase Auth or an explicitly-labeled mock service for learning purposes

## Code Style

- Domain data uses typed classes (e.g. `Task`), never loose `Map<String, dynamic>` passed around as if it were a model.
- Named constructor parameters (`Task({required this.title, this.notes, this.done = false})`), not positional.
- Prefer `.where()`/`.map()`/`.fold()` over hand-rolled loops for simple collection transforms.
- `watch` in `build()` methods only; `read` inside event handlers (`onPressed`, `onTap`).

## Patterns to Follow

- Every async operation the user can trigger (sync, login, save) shows one of exactly three UI states: loading, error with retry, or success — never a silent blank screen.
- Read credentials, API keys, and tokens from environment/config (`String.fromEnvironment`), never as literal strings in source.
- Give every persisted `Task` an `updatedAt` timestamp; sync/merge logic compares by this field, not by title.

## Patterns to Avoid

- Do not store raw passwords anywhere (local storage, database, logs) — only a session token/flag.
- Do not recreate a `Future` inside a `FutureBuilder`'s `build()` call on every rebuild — store it once in `State`.
- Do not bypass `TaskProvider`'s methods to mutate the task list directly from a screen.

## Commit Style

- Format: `feat(phase-lesson): message` (e.g. `feat(p2-l3): add Provider-based task state`)
- Keep subject line under 72 characters

## Testing

- Widget tests in `test/`, named `<screen>_test.dart`
- Run: `flutter test`
- At minimum: one widget test for the empty-task-list state, one unit test for `Task.toMap`/`fromMap` round-trip

## Out of Scope

- This file does not cover web or desktop Flutter targets, or backend/server-side Dart — the project is mobile-only.
- Full curriculum detail (concepts, analogies, per-lesson acceptance criteria) lives in the Claude Code version of this skill at `skills/learn-dart-mobile/`, not duplicated here.
