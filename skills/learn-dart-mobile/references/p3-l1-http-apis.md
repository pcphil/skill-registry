# P3-L1: HTTP & APIs

## Concept

The `http` package provides simple request methods: `http.get(uri)`, `http.post(uri, body: ...)`, each returning a `Future<Response>` with `.statusCode` and `.body` (raw JSON string). Use `dart:convert`'s `jsonDecode`/`jsonEncode` to convert between JSON strings and Dart `Map`/`List` structures.

The typical flow: encode your `Task` to JSON (reuse `toMap()` from P2-L4, then `jsonEncode(map)`), POST it, check `statusCode` is in the 200 range, and for GET requests, `jsonDecode(response.body)` then map each JSON object through `Task.fromMap()`.

Never hardcode API keys, tokens, or credentials directly in source — read them from environment/config (e.g., `--dart-define=API_KEY=...` at build time, read via `String.fromEnvironment('API_KEY')`) so they aren't committed to version control or visible in the compiled app source.

## Analogy

An HTTP request is like mailing a letter to an office and waiting for a reply envelope. `jsonEncode`/`jsonDecode` are the shared language both sides agree to write in so the letter's contents (your `Task` data) can be understood regardless of which programming language wrote or reads it.

## Workshop

**Task:** (Use a free mock API like `jsonplaceholder.typicode.com` or a simple local mock server — no real backend needed yet, that's next lesson.)

1. Add the `http` package to `pubspec.yaml`.
2. Create `lib/services/api_service.dart` with `Future<void> syncTask(Task task)` — POSTs the task's JSON to the mock endpoint, checks the status code, throws a descriptive exception on failure.
3. Add `Future<List<Task>> fetchTasks()` — GETs from the mock endpoint, decodes the JSON array, maps each entry through `Task.fromMap()`.
4. Read any API key/token via `String.fromEnvironment(...)`, not a literal string in the code — even if the mock API doesn't require one, build the habit now.
5. Wire a manual "Sync now" button in the app (doesn't need to auto-run yet) that calls `syncTask` for each local task and prints success/failure per task.

## Acceptance Criteria / Edge Cases

- Handles a non-200 status code by throwing/logging a clear error, not silently continuing as if it succeeded.
- Handles malformed/unexpected JSON in the response without crashing the whole app (wrap `jsonDecode` in a try/catch or validate expected keys exist).
- No literal API key/token/secret string appears anywhere in the committed source.

## Common Mistakes

- Treating any non-thrown response as success — a 404 or 500 still returns a `Response` object, it doesn't throw automatically; you must check `statusCode` yourself.
- Forgetting `Content-Type: application/json` header on POST requests, causing the server to misinterpret the body.
- Hardcoding a real API key directly for "just testing" and forgetting to remove it before committing.

## Ship vs Portfolio Note

**Ship a real app:** credential hygiene here isn't optional — a key baked into a compiled APK can be extracted by anyone. `--dart-define` plus a secrets-management process for CI is the minimum bar.

**Learning/portfolio:** using a public mock API is fine for this lesson; the `String.fromEnvironment` habit still matters because it's the pattern you'll carry into any real backend later.

## Bridge

You can sync data manually, but there's no loading/error feedback in the UI yet, and no real auth. Next: async UI patterns for loading and error states.
