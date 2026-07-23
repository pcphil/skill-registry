# P1-L5: Project Scaffold

## Concept

`flutter create task_tracker` generates a runnable starter app with the standard structure:

```
task_tracker/
├── lib/
│   └── main.dart       # entry point — runApp(...)
├── pubspec.yaml        # dependencies + metadata
├── android/, ios/       # platform-specific projects
└── test/               # widget/unit tests
```

`pubspec.yaml` is where you declare dependencies (used starting Phase 2 for state management, persistence, HTTP). `lib/main.dart` calls `runApp(MyApp())`, and `MyApp` is typically a `MaterialApp` wrapping your first screen.

From this lesson forward, every workshop modifies files inside this same `task_tracker/` project — there are no more standalone scripts.

## Analogy

Running `flutter create` is like a general contractor pouring the foundation and framing a house before you move in any furniture — plumbing and electrical (the platform folders) are already roughed in; you're about to start on the rooms (screens) and what goes in them.

## Workshop

**Task:**
1. Run `flutter create task_tracker` (requires the Flutter SDK installed — if not installed, install it first per the official Flutter docs for your OS).
2. `cd task_tracker && flutter run` to confirm the default counter-demo app launches on a simulator/emulator/device.
3. Move your `Task` class (and `CompletionTracking` mixin) from the Phase 1 scripts into `lib/models/task.dart` as the first file in the real project.
4. Replace the default `lib/main.dart` app title/home widget text so it says "Task Tracker" instead of the Flutter demo counter app — confirms you can find and edit the entry point.

## Acceptance Criteria / Edge Cases

- `flutter run` launches successfully with no build errors.
- `lib/models/task.dart` exists and contains the `Task` class + `CompletionTracking` mixin, compiling cleanly when imported.
- App title/home screen text visibly reflects "Task Tracker" instead of the default demo.

## Common Mistakes

- Not having the Flutter SDK/Android or iOS toolchain set up before this lesson — `flutter doctor` is the fastest way to diagnose missing setup pieces.
- Editing the wrong file (there can be confusion between `lib/main.dart` and platform-specific `MainActivity`/`AppDelegate` files — you only need `lib/main.dart` for this).
- Forgetting to update the import path when moving `Task` into `lib/models/task.dart`.

## Ship vs Portfolio Note

**Ship a real app:** get comfortable with `flutter doctor`, `flutter run`, and `flutter build` now — you'll use all three continuously through the rest of the curriculum and beyond.

**Learning/portfolio:** this is the moment the "app" becomes real and visible — worth taking a screenshot of the very first run for your own before/after record as the app grows.

## Bridge

You have a running (nearly empty) Flutter app with your `Task` model already inside it. Phase 2 starts building the actual UI — the task list screen.
