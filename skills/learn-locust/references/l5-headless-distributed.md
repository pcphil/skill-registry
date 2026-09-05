# Lesson 5: Headless & Distributed Runs

## Concept

The web UI is great for exploring, but real load tests are usually run headless (no browser, scriptable, CI-friendly) and, for large loads, distributed across multiple worker processes.

Key mechanics:
- Headless: `locust -f locustfile.py --host <host> --headless -u <users> -r <spawn-rate> -t <duration>` — e.g. `-u 50 -r 5 -t 1m` ramps to 50 users at 5/sec, runs for 1 minute, then stops and prints a summary.
- Distributed: `locust --master` on one process, `locust --worker --master-host=<ip>` on one or more others — the master coordinates, workers generate load. Only useful once a single process can't generate enough load itself.
- `--csv=<prefix>` writes stats to CSV files for later analysis; `--html=<file>` writes an HTML report.

**Reading the results table is the actual skill here** — running Locust is easy, knowing whether the numbers are good or bad is the point:
- **RPS (requests/sec)** — throughput. Compare against what you expected to sustain.
- **p50 (median) latency** — typical-case response time. A p50 that looks fine can hide a bad tail.
- **p95 / p99 latency** — tail latency. This is usually what actually matters for user experience — the p95 is how slow it is for 1 in 20 requests, not the "average" everyone imagines.
- **Failure rate** — percentage of requests that failed (HTTP errors + anything you marked failed in Lesson 4). Non-zero isn't automatically bad, but should be understood, not ignored.

A single average-latency number without percentiles is close to useless for load testing — it hides exactly the tail behavior you're testing for.

## Task

1. Run the locustfile headless: `locust -f locustfile.py --host <demo-host> --headless -u 20 -r 5 -t 30s`.
2. After it finishes, read the printed summary table and report back: total RPS, p50, p95, p99 latency, and failure rate — in your own words, not just pasted numbers.
3. State whether the p95 looks acceptable to you and why (there's no single "right" answer here — the point is forming an opinion from the data).
4. (Optional, if the learner wants to try it) Start a `--master` in one terminal and one `--worker` in another against the same locustfile, confirm the worker connects and load is generated from both.

## Acceptance Criteria

- A completed headless run with a printed summary table.
- Learner correctly identifies RPS, p50, p95, p99, and failure rate from their own output (not guessed).
- Learner states an opinion on whether the p95 is acceptable, with reasoning tied to the actual number.

## Common Mistakes

- Reading only the average/median and ignoring p95/p99 — this is the single most common load-testing mistake and worth calling out directly if the learner does it.
- Treating any non-zero failure rate as automatically bad without checking what actually failed and why.
- Running `--worker` without a reachable `--master-host`, then being confused why no load appears.
