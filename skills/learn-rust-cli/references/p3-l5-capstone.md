# P3-L5: Capstone / Polish

## Concept

`tasker` works. This lesson turns "works on my machine" into "I'd hand this to someone." Three tools do most of the work:

- **`cargo clippy`** — Rust's linter. It catches non-idiomatic code, needless clones, redundant patterns, and common mistakes the compiler allows but shouldn't ship. Aim for a **clippy-clean** build (`cargo clippy -- -D warnings` treats lints as errors).
- **`cargo fmt`** — the standard formatter. One run makes the whole codebase consistent.
- **`cargo build --release`** — an optimized build. The binary lands in `target/release/tasker` and runs far faster than the debug build. This is the artifact you'd actually distribute.

Beyond tooling: audit error handling (any `.unwrap()` left on a user-reachable path?), confirm exit codes are correct, tighten the `Display`/help output, and update the data-file location if you flagged it earlier.

## Analogy

The whole course built and wired the car; the capstone is the pre-delivery inspection. Clippy is the mechanic pointing out sloppy wiring that runs but shouldn't; `fmt` is the detailing; `--release` is tuning the engine for the road instead of the workshop. You don't add new parts — you make sure nothing rattles before handing over the keys.

## Workshop

**Setup:** The `tasker` project. This is the final lesson — frame it by the saved goal.

**Task (both goals):**
1. Run `cargo clippy` and resolve every warning (or justify any you suppress with a comment). Run `cargo fmt`.
2. Audit for `.unwrap()`/`.expect()` on any path reachable from user input; replace with proper `Result` handling. Confirm errors print to stderr and the process exits non-zero on failure.
3. Run the full `cargo test` suite green.
4. Write a short `README.md`: what `tasker` does, the commands, and how to build/run it.

**If goal = ship a real tool:** build `cargo build --release`, run the release binary directly (`./target/release/tasker list`), and fix the data-file location (store `tasks.json` in a proper data/config dir rather than the cwd). Confirm `--help` and `--version` read well.

**If goal = learning/portfolio:** focus the pass on clean idiomatic code — clippy-clean, well-named modules, documented public items (`///` doc comments), and a README that explains *what you learned building it*. A release build is optional.

## Acceptance Criteria / Edge Cases

- `cargo clippy` is clean (or suppressions are justified); `cargo fmt` applied; `cargo test` green.
- No `.unwrap()` reachable from user input; failures → clear stderr message + non-zero exit.
- `README.md` documents commands and build/run steps.
- (Ship goal) a working `--release` binary; sane data-file location.

## Common Mistakes

- Blanket-`#[allow]`ing clippy lints to silence them instead of fixing the underlying issue. Suppress only with a reason.
- Leaving a `.unwrap()` on `lock()` or file I/O that a real user can trigger — the exact crash the whole course taught you to avoid.
- Shipping a `tasks.json` written to the cwd, so the tool "loses" tasks when run from a different directory.

## Ship vs Portfolio Note

**Ship a real tool:** a clippy-clean, release-built, correctly-exiting CLI with a README is genuinely publishable — consider `cargo publish` or a GitHub release. You've built a real Unix citizen.

**Learning/portfolio:** you've now traversed Rust's core: ownership, borrowing, traits, generics, iterators, error handling, modules, serde, concurrency, and testing — all in one coherent project. That's a portfolio piece that demonstrates the whole language.

## On Complete

`tasker` is complete. Summarize the features built (task CRUD, persistence, concurrent import, shared state, tests, polished CLI) and the Rust concepts each exercised. Ask whether to keep extending `tasker` (e.g. `rayon` for real parallelism, an async network sync, a TUI) or move to a new topic.
