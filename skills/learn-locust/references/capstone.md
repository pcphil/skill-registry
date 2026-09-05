# Capstone: Full Load-Test Suite

## Target

Use Locust's own quickstart demo/tutorial target so the learner needs zero infrastructure of their own. Locust's docs quickstart (docs.locust.io quickstart page) walks through a simple example target — confirm the current recommended target and host in Locust's own docs at teaching time (versions/paths can move; use a documentation lookup if unsure rather than assuming a hardcoded URL is still current). If the documented example ever becomes unavailable, fall back to having the learner run any trivial local Flask/FastAPI app with 2-3 endpoints as a substitute target — the lesson is about the load-test suite, not the target itself.

## Concept

This is not a new concept lesson — it's integration. The capstone locustfile should already contain (from Lessons 2-6): weighted tasks modeling a real usage ratio, a `SequentialTaskSet` for at least one real flow, response validation beyond HTTP status, and a deliberately chosen `LoadTestShape`.

**What makes this a capstone rather than "just run it again" is the results-interpretation gate**: the learner must commit to pass/fail thresholds *before* running, then hold the actual results against them. Skipping straight to "it ran, done" does not satisfy this lesson — that's the entire point of everything taught in Lesson 5.

## Task

1. Confirm the capstone locustfile integrates all prior lessons: multiple weighted tasks, one `SequentialTaskSet`, at least one validated (`catch_response=True`) request, and a custom `LoadTestShape`.
2. **Before running**, have the learner state explicit thresholds in writing:
   - Target p95 latency (e.g. "p95 under 500ms")
   - Acceptable failure rate (e.g. "under 1%")
   - Which test-type intent this run represents (load/stress/spike/soak, from Lesson 6)
3. Run the suite headless against the target: `locust -f locustfile.py --host <target> --headless -u <n> -r <rate> -t <duration>`.
4. Have the learner report actual RPS, p50/p95/p99 latency, and failure rate from the real output.
5. Have the learner explicitly state pass or fail against their stated thresholds, and why — including if the result is ambiguous or surprising.

## Acceptance Criteria

- Locustfile integrates weighting, sequencing, validation, and a load shape from prior lessons — not a fresh minimal file.
- Thresholds stated in writing *before* the run (RPS/p95/failure-rate expectations, test-type intent).
- Actual run completed, with real RPS/p50/p95/p99/failure-rate figures reported from that specific run's output.
- Explicit pass/fail verdict stated against the pre-committed thresholds, with reasoning — this is the gate that completes the capstone, not just having a locustfile that executes.

## Common Mistakes

- Setting thresholds after seeing the results ("well, 800ms p95 is fine actually") — defeats the purpose; push back if this happens and ask for the original stated threshold.
- Reporting only "it passed" without the actual numbers.
- Treating the capstone as complete once the file runs without errors, without ever reading or judging the output.

## On Capstone Complete

This is the final lesson. Follow the SKILL.md "On Complete" trigger: save final progress and a results summary to memory, state a completion summary including the actual pass/fail verdict, and ask if the learner wants to keep extending the suite or start something new.
