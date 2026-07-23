# P3-L4: Cloud Sync

## Concept

Cloud sync means reconciling two sources of truth: the local `sqflite` database (works offline, instant) and a remote store (Firestore or a REST backend — shared across the user's devices). The core challenge is merging, not just fetching: what happens when a task was edited locally while offline, and the remote copy also changed?

A workable starter strategy: give every `Task` an `updatedAt` timestamp. On sync, compare local and remote copies of the same task by ID — whichever has the newer `updatedAt` wins ("last write wins"). This isn't the most sophisticated approach (real production apps often need more careful conflict resolution), but it's a correct, understandable starting point.

Sync should run: on app start (pull remote changes down), after any local mutation (push the change up), and via the manual "Sync now" button from P3-L1/P3-L2 as a fallback.

## Analogy

Think of two people editing the same shared shopping list from different rooms of a house, then comparing notes. "Last write wins" is the simple rule of "whoever wrote their note most recently is assumed to be right" — not perfect (the other room's edit is lost if it's older), but way better than the two lists silently diverging forever.

## Workshop

**Task:**
1. Add `updatedAt` (a `DateTime`) to the `Task` model, updated on every local mutation (add, edit, toggle, delete-as-tombstone if you want to sync deletions too — or just handle add/edit/toggle for this lesson and note deletion sync as a known simplification).
2. Extend `ApiService` (P3-L1) with `fetchRemoteTasks()` (already scaffolded conceptually in P1-L4) and `pushTask(Task task)`.
3. Write a `SyncService` with a `sync()` method: fetch remote tasks, compare each by ID against local tasks using `updatedAt`, keep the newer version locally (write it to `sqflite` via `DatabaseHelper`) and push any locally-newer tasks to remote.
4. Call `sync()` on app start (after login) and wire it into the existing manual "Sync now" button, using the loading/error UI pattern from P3-L2.

## Acceptance Criteria / Edge Cases

- A task edited locally while "offline" (simulate by just not calling sync) and then synced correctly overwrites an older remote copy of the same task, and vice versa.
- A brand-new task that only exists locally gets pushed to remote and picks up whatever ID scheme remote uses (or keeps a local ID if your backend supports client-assigned IDs — be consistent).
- Running `sync()` twice in a row with no changes in between is a no-op — doesn't create duplicate tasks or thrash the UI.

## Common Mistakes

- Comparing tasks by title instead of a stable ID — two tasks with the same title get incorrectly merged or duplicated.
- Forgetting to update `updatedAt` on every local mutation path — a real edit gets incorrectly treated as older than a stale remote copy.
- Running sync on every widget rebuild instead of on explicit triggers (app start, mutation, manual button) — same class of bug as P3-L2's Future-recreation mistake, but at the network-call level this time.

## Ship vs Portfolio Note

**Ship a real app:** "last write wins" is a real, shippable starting strategy — plenty of production apps use it. Just document the tradeoff (silent data loss on true concurrent edits) rather than pretending it's perfect.

**Learning/portfolio:** this lesson is the most conceptually complex one in the curriculum — if it doesn't click on the first pass, that's expected; sync/conflict resolution is genuinely one of the harder problems in real app development.

## Bridge

The app now works fully offline-first with cloud sync. The capstone lesson polishes what you've built rather than adding a new concept.
