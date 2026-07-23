# P2-L4: Local Persistence

## Concept

`sqflite` gives you a real SQL database on-device — good fit here since tasks are structured records with a stable shape. (`hive` is a valid lighter-weight NoSQL alternative if you'd rather store objects directly without SQL; either is acceptable, but these notes assume `sqflite`.)

The pattern: a `DatabaseHelper` (or similar) class wraps the raw `sqflite` API — opening the database, creating the `tasks` table on first run, and exposing `insertTask`, `getTasks`, `updateTask`, `deleteTask` methods that convert between your `Task` class and database rows (`Map<String, dynamic>`). Your `TaskProvider` from the last lesson calls into this helper instead of only holding an in-memory list — on app start, it loads from the database; every mutation writes through to the database too.

This is also where `Task` needs `toMap()` and `fromMap()` methods — the serialization boundary between your Dart objects and the raw database rows.

## Analogy

An in-memory list is a whiteboard — fast to write on, but wiped clean when the office closes (app restarts). A local database is a filing cabinet — slightly slower to open a drawer and write a page, but it's still there tomorrow. Your `TaskProvider` is the office assistant who keeps a whiteboard for quick reference during the day but always also files a copy in the cabinet.

## Workshop

**Task:**
1. Add `sqflite` and `path` packages to `pubspec.yaml`, `flutter pub get`.
2. Add `toMap()` and `Task.fromMap(Map<String, dynamic> map)` to `lib/models/task.dart`.
3. Create `lib/services/database_helper.dart`: opens/creates a `tasks` table (`id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, notes TEXT, done INTEGER`), with methods `insertTask`, `getAllTasks`, `updateTask`, `deleteTask`.
4. Update `TaskProvider` to load tasks from `DatabaseHelper` on construction (or an explicit `loadTasks()` call from `main.dart` before `runApp`), and to call the corresponding database method inside `addTask`/`toggleDone`/`deleteTask` in addition to updating the in-memory list.
5. Verify persistence: add a task, fully close and relaunch the app, confirm it's still there.

## Acceptance Criteria / Edge Cases

- Tasks survive a full app restart (not just hot reload — hot reload keeps memory state, which would give a false pass).
- `done` (a `bool` in Dart) is correctly converted to/from `INTEGER` (0/1) for SQLite, which has no native boolean type.
- Deleting a task removes it from the database, not just the in-memory list (verify by restarting after a delete).
- App still shows the empty-state message correctly when the database has zero rows.

## Common Mistakes

- Storing `bool done` directly without converting to `0`/`1` — `sqflite` will error or silently misbehave since SQLite has no boolean column type.
- Forgetting to `await` database calls, causing the UI to update optimistically but the database write to lose a race with a subsequent read.
- Not handling the first-run case where the `tasks` table doesn't exist yet (must create it in the database's `onCreate` callback).

## Ship vs Portfolio Note

**Ship a real app:** this is the point where data loss becomes a real user-facing bug if done wrong — test the restart-persistence scenario explicitly, don't assume it works because hot reload looked fine.

**Learning/portfolio:** understanding *why* hot reload can mask a persistence bug (it preserves Dart memory state across reloads) is itself a valuable lesson about Flutter's dev tooling.

## Bridge

Tasks now survive restarts, but every task still needs the floating-action-button placeholder. Next: a real add-task form with validation.
