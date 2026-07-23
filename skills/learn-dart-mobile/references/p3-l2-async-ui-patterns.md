# P3-L2: Async UI Patterns

## Concept

`FutureBuilder<T>` takes a `Future<T>` and a `builder` that receives an `AsyncSnapshot<T>` — check `snapshot.connectionState` (`waiting`, `done`) and `snapshot.hasError`/`snapshot.hasData` to render a loading spinner, an error message, or the real content, all from one widget. `StreamBuilder<T>` is the same idea for a `Stream` — useful for data that updates repeatedly (e.g., a live sync-status indicator), while `FutureBuilder` suits a one-shot async call.

The core UI rule: never leave a screen in an ambiguous state. Every async operation the user triggers (sync, load) should visibly show one of exactly three states — loading, error (with a retry option), or success — never a silent blank screen while something happens in the background.

## Analogy

`FutureBuilder` is like a food-delivery tracking screen: it explicitly shows "preparing" (waiting), "delivery failed, retry?" (error), or "delivered, here's your food" (data) — never just a blank screen while you wonder what's happening.

## Workshop

**Task:**
1. Wrap the "Sync now" flow from P3-L1 with explicit UI states: while `syncTask`/`fetchTasks` are in flight, show a loading indicator (e.g., disable the button + show a small spinner); on failure, show a `SnackBar` or inline error message with a "Retry" action; on success, show a brief confirmation (e.g., a `SnackBar` saying "Synced").
2. Use `FutureBuilder` for the initial `fetchTasks()` load on app start (if you choose to fetch remote tasks at launch) — show a spinner while `connectionState == ConnectionState.waiting`, an error view if `snapshot.hasError`, otherwise the list.
3. Ensure the loading state can't be triggered twice concurrently (disable the sync button while a sync is already in progress).

## Acceptance Criteria / Edge Cases

- Triggering sync shows a visible loading indicator, not a frozen-looking UI with no feedback.
- Simulating a failure (e.g., temporarily point at a bad URL) shows a clear error state with a retry option, not a silent failure or crash.
- Tapping "sync" rapidly multiple times doesn't launch overlapping sync operations.

## Common Mistakes

- Forgetting to check `snapshot.hasError` before assuming `snapshot.data` is populated — accessing `.data!` on an errored/waiting snapshot throws.
- Rebuilding the entire `FutureBuilder`'s `Future` on every widget rebuild (e.g., calling `fetchTasks()` directly inside `build()`) — causes an infinite refetch loop. Store the `Future` in `State` and create it once (e.g., in `initState`).
- Leaving the button enabled during an in-flight request, letting users queue up duplicate network calls.

## Ship vs Portfolio Note

**Ship a real app:** unclear loading/error states are one of the most common real-world App Store review complaints and support tickets ("app looks frozen") — this lesson's habits directly prevent that class of bug.

**Learning/portfolio:** this is a good moment to deliberately trigger the "Future recreated every rebuild" bug, see the app hammer the network repeatedly, then fix it — the failure mode is much more memorable than being told about it.

## Bridge

Sync now has proper loading/error feedback. Next: require a real login before the app can be used at all.
