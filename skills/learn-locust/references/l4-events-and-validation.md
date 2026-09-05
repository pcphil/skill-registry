# Lesson 4: Events & Validation

## Concept

By default Locust only counts a request as "failed" on HTTP-level errors (connection errors, timeouts). A `200 OK` response with the wrong body, missing field, or business-logic error looks like a success unless you validate it yourself.

Key mechanics:
- `catch_response=True` on a request call (e.g. `self.client.get("/", catch_response=True)`) gives you a response object where you control pass/fail:
  ```python
  with self.client.get("/", catch_response=True) as resp:
      if "expected text" not in resp.text:
          resp.failure("expected text missing")
  ```
- Locust's event hooks (`locust.event`, e.g. `request` event) let you run custom code on every request — useful for logging or custom metrics, not required for basic validation.

## Task

Pick one existing task from the locustfile and add real validation:
1. Convert it to use `catch_response=True`.
2. Check something beyond HTTP status — e.g. response body contains expected content, or JSON response has an expected key.
3. Call `resp.failure("<reason>")` when validation fails, with a specific message (not just "failed").
4. Run a test and confirm: (a) it still reports success when the check passes, and (b) temporarily breaking the check (e.g. checking for text that doesn't exist) shows up as a failure in the stats table, not just as a false success.

## Acceptance Criteria

- At least one task uses `catch_response=True` with an explicit content/business-logic check, not just relying on HTTP status.
- `resp.failure(...)` is called with a specific, useful message.
- Learner has demonstrated (by temporarily breaking the check) that the validation actually catches a failure Locust's default behavior would have missed.

## Common Mistakes

- Using `catch_response=True` but never calling `resp.success()` or `resp.failure()` — Locust then reports it as neither, or defaults confusingly.
- Checking status code only inside `catch_response` — that's redundant with Locust's default behavior and doesn't add real validation value.
- Forgetting the `with` block — `catch_response` responses need the context manager to auto-report if you don't explicitly call success/failure.
