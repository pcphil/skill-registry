# Lesson 6: Load Shapes

## Concept

`-u`/`-r` gives you a flat ramp-then-hold pattern. `LoadTestShape` (a class you define and register with `@locust.tag`-free custom class extending `LoadTestShape`) lets you control user count over time arbitrarily — step patterns, spikes, custom ramps.

**Pick the shape based on what you're actually trying to find out, not because a shape looks interesting.** The standard test-type vocabulary:

- **Load test** — expected normal traffic, sustained. Answers: "does this hold up under everyday load?" Shape: ramp to target, hold flat.
- **Stress test** — push well past expected load until something breaks. Answers: "where's the breaking point, and what fails first?" Shape: step up in stages beyond normal capacity.
- **Spike test** — sudden jump in traffic, then back down. Answers: "does the system survive a traffic spike (product launch, news mention) without falling over?" Shape: flat baseline → sharp spike → back to baseline.
- **Soak test** — moderate load sustained for a long time. Answers: "do things degrade over time — memory leaks, connection exhaustion, slow-growing queues?" Shape: flat, long duration.

Mechanics:
```python
from locust import LoadTestShape

class StepLoadShape(LoadTestShape):
    def tick(self):
        run_time = self.get_run_time()
        # return (user_count, spawn_rate) or None to stop the test
        ...
```
`tick()` is called repeatedly by Locust; returning `None` ends the test.

## Task

1. Before writing code, state which test type you're building (load/stress/spike/soak) and why — what question does it answer that a flat `-u`/`-r` run wouldn't?
2. Implement a `LoadTestShape` subclass matching that choice (e.g. a spike shape: low baseline, sudden jump, back down).
3. Run it and confirm the web UI's user-count graph actually shows the shape you intended (flat, spike, steps — whichever you built).

## Acceptance Criteria

- Stated test-type intent before implementation, with reasoning (not "picked spike because it sounded fun").
- Working `LoadTestShape` subclass whose `tick()` implements that intent.
- Confirmed (via the UI graph or headless output) that the actual user-count-over-time matches the intended shape.

## Common Mistakes

- Building a shape that doesn't match the stated intent (e.g. saying "spike test" but writing a flat ramp).
- Forgetting `tick()` must return `None` eventually, or the test never stops on its own.
- Confusing spawn *rate* (how fast users ramp) with target user *count* — a shape needs both at each step.
