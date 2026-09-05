# Lesson 2: User & Task Basics

## Concept

`HttpUser` is Locust's base class for simulating one user making HTTP requests. Each `@task`-decorated method is something that user does. `wait_time` controls the pause between tasks for a single simulated user — it's what keeps a load test from hammering the target with zero delay.

Key mechanics:
- `class MyUser(HttpUser): host = "https://example.com"` — or set the host in the web UI / `--host` flag instead of hardcoding it.
- `self.client.get("/path")` inside a task — `self.client` is a wrapped `requests`-like session scoped to this simulated user.
- `wait_time = between(1, 3)` (from `locust import between`) — random pause in seconds between tasks.

## Task

Replace the placeholder `PlaceholderUser` in `locustfile.py` with a real user that:
1. Is named `WebsiteUser(HttpUser)`.
2. Sets `wait_time = between(1, 3)`.
3. Has one `@task` method that does `self.client.get("/")` against a real target (use Locust's own quickstart demo — the reference in `references/capstone.md` has the host).
4. Run `locust -f locustfile.py --host <demo-host>`, start a test with 1-2 users in the web UI, and confirm requests show up in the stats table.

## Acceptance Criteria

- `WebsiteUser` class exists, inherits `HttpUser`, has `wait_time` set.
- At least one `@task` method issues a real request via `self.client`.
- A live run in the web UI shows non-zero request count with 0 failures for this endpoint.

## Common Mistakes

- Forgetting `self.` — calling `client.get(...)` instead of `self.client.get(...)`.
- Omitting `wait_time` — Locust still runs but hammers the target with no pacing between requests.
- Setting `host` to a URL that includes a path — `host` should be the origin only (e.g. `https://example.com`, not `https://example.com/api`).
