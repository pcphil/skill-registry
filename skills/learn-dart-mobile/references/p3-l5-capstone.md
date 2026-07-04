# P3-L5: Capstone / Polish

## Concept

No new Dart/Flutter concept here — this lesson is a deliberate polish pass over the whole app, and the specific polish checklist depends on the learner's stated goal from the Assessment:

**Ship a real app** goal — production-readiness pass:
- Error handling audit: every `await` that can throw (network, database, auth) has a corresponding user-visible error state, not just a console print.
- Basic testing: at least one widget test (e.g., `TaskListScreen` renders the empty state correctly) and one unit test (e.g., `Task.fromMap`/`toMap` round-trip correctly).
- Release build: run `flutter build apk` (Android) or `flutter build ios` (iOS, requires macOS/Xcode) at least once, resolve any release-mode-only issues (these sometimes differ from debug-mode behavior).
- App icon, name, and basic metadata in `pubspec.yaml`/platform folders reflect "Task Tracker" rather than defaults.

**Learning/portfolio** goal — presentation pass:
- Clean up any leftover debug prints, hardcoded test data, or commented-out code from earlier lessons.
- Write a short README describing the app and which concepts each phase covered (useful as a portfolio artifact).
- Take a few screenshots of the key screens (list, detail, add-task form, login) for a portfolio entry.
- Optionally: pick one "next feature" you'd add if continuing (e.g., due dates, categories, reminders) and note it — shows forward thinking without requiring more curriculum time.

## Analogy

If the whole curriculum has been building a house room by room, this lesson is the final walkthrough before moving in (ship goal: an inspector checking wiring and locks) or before showing it to guests (portfolio goal: staging the rooms and taking photos) — no new rooms are built, but what's there gets finished properly.

## Workshop

**Task:** Complete the checklist matching your stated goal (above). There's no single "correct" file to review — the Review step for this lesson should check whichever concrete artifacts the checklist produced (test files, a release build log, a README, screenshots) against the checklist items for the learner's goal.

## Acceptance Criteria / Edge Cases

- Ship-a-real-app: at least one passing widget test and one passing unit test exist and run via `flutter test`; a release build completes without errors.
- Learning/portfolio: a README exists describing the app and curriculum; no leftover debug artifacts (stray `print()` calls, hardcoded test tasks) remain in the shipped screens.
- Either goal: the app, end to end, supports login → view tasks → add/edit/complete/delete a task → sync → logout, without crashing at any step.

## Common Mistakes

- Treating "polish" as optional busywork and skipping it — for the ship-a-real-app track especially, this is where real bugs (untested edge cases, release-mode-only crashes) actually surface.
- Writing tests that only check the happy path — include at least one test for an edge case already identified earlier in the curriculum (e.g., empty task list, null notes).
- For portfolio polish: forgetting to remove any real credentials or test account details before sharing screenshots or a repo publicly.

## Ship vs Portfolio Note

This lesson *is* the ship-vs-portfolio branch point made explicit — there's no generic "next lesson" content beyond this; the branch itself is the final lesson.

## Bridge

This is the last lesson. On completion, follow the skill's On Complete behavior: summarize what was built across all three phases, and ask if the learner wants to keep extending the app or start a new topic.
