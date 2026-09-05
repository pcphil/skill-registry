# Lesson 3: Weights & Sequences

## Concept

Real users don't do every action equally often. Locust's `@task(weight)` lets you assign relative frequency: `@task(3)` runs three times as often as `@task(1)` on average across the simulated population. `SequentialTaskSet` (or `TaskSet` for unordered grouping) lets you model a fixed sequence of steps, like "browse → add to cart → checkout", instead of independent random tasks.

**This is where load testing becomes about the target system, not just the API.** A locustfile with realistic weights tells you something about real traffic; one with arbitrary weights just tells you Locust works. Before writing weights, the learner should be able to answer: "if 1,000 real users hit this site right now, what's the rough ratio of browse-only vs. buy vs. search?" — the weights should approximate that ratio, not be picked at random.

**Think time vs. `wait_time`**: `wait_time` is the pause *between* a user's tasks (modeling "user reads the page before clicking again"). Think time is the same idea by a different name in performance-testing vocabulary generally — the point is that a load test with zero or unrealistic think time will report throughput numbers that don't reflect how the target behaves under real usage patterns.

## Task

Extend `WebsiteUser` from Lesson 2:
1. Add at least 3 `@task`s with different weights (e.g. `@task(5)` for a common read, `@task(1)` for a rarer write/search action).
2. Before writing the weights, state in one sentence what real-world ratio you're modeling (e.g. "5:1 browse-to-search, because most visits are browsing").
3. Group at least 2 of the tasks into a `SequentialTaskSet` representing a fixed real-world flow (e.g. view item → view cart).
4. Run the test again and confirm the stats table shows the expected rough ratio of request counts between the weighted tasks.

## Acceptance Criteria

- At least 3 weighted tasks with a stated, plausible real-world justification for the ratio (not "I picked these numbers").
- One `SequentialTaskSet` modeling an ordered real flow.
- Live run shows request-count ratios roughly matching the stated weights.

## Common Mistakes

- Weights that don't sum to anything meaningful — remember weights are *relative*, `@task(2)` and `@task(1)` behave the same as `@task(20)` and `@task(10)`.
- Confusing `TaskSet` (unordered pool) with `SequentialTaskSet` (strict order) when the real flow requires order.
- Setting `wait_time` to near-zero "to make the test faster" — this destroys the realism of the throughput numbers; push back on this if the learner suggests it without justification.
