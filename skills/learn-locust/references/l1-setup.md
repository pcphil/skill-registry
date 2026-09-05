# Lesson 1: Setup

## Concept

Locust is a Python load-testing tool: you describe simulated users as Python code, and Locust spawns many of them concurrently against a target. Unlike most load-testing tools, test logic is plain Python — no proprietary DSL.

Core pieces at a glance:
- `pip install locust` — it's a regular Python package.
- A **locustfile** (conventionally `locustfile.py`) defines simulated user behavior.
- Running `locust` starts a local web UI (default `http://localhost:8089`) where you set user count, spawn rate, and target host, then watch live stats.

## Task

1. Create a project directory for this course, e.g. `locust-course/`.
2. Install Locust: `pip install locust` (recommend a virtualenv if the learner hasn't set one up).
3. Create an empty `locustfile.py` in that directory with just:
   ```python
   from locust import HttpUser, task

   class PlaceholderUser(HttpUser):
       pass
   ```
4. Run `locust -f locustfile.py` from that directory and confirm the web UI comes up at `localhost:8089` (don't start a test yet — just confirm it launches without error).
5. Say "done" once the UI loads.

## Acceptance Criteria

- `locust` command runs without import/syntax errors.
- Web UI is reachable and shows the "Start new load test" screen.

## Common Mistakes

- Running `locust` from the wrong directory (it looks for `locustfile.py` in the cwd by default, or needs `-f <path>`).
- Forgetting the virtualenv is active when `pip install` was run somewhere else — `locust: command not found`.
