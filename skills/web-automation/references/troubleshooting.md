# Playwright Python Troubleshooting

Load this file when the user reports errors or unexpected script behavior.

---

## Element Not Found / TimeoutError

**Symptom:** `TimeoutError: Timeout 30000ms exceeded` on a locator action.

**Causes and fixes:**

1. **Wrong wait strategy** — the element exists but isn't visible/ready yet.
   ```python
   # Add an explicit wait before interacting
   expect(page.get_by_role("button", name="Submit")).to_be_visible()
   page.get_by_role("button", name="Submit").click()
   ```

2. **Wrong selector** — the element is there but the selector doesn't match.
   ```python
   # Debug: print all matching elements
   print(page.locator("button").all_inner_texts())
   # Or pause and inspect manually
   page.pause()
   ```

3. **Timeout too short** — slow network or heavy page.
   ```python
   page.set_default_timeout(60000)  # increase to 60s globally
   ```

---

## Flaky Selector (Works Sometimes, Fails Others)

**Symptom:** Script passes on first run, fails intermittently on subsequent runs.

**Fix:** Replace fragile CSS/position-based selectors with semantic ones.

```python
# Fragile — breaks when class names change or order shifts
page.locator(".btn:nth-child(2)").click()
page.locator("div > span.label").click()

# Stable — tied to visible text and ARIA role
page.get_by_role("button", name="Confirm").click()
page.get_by_text("Confirm", exact=True).click()
```

Also ensure you're waiting for the element before acting on it — race conditions are a common source of flakiness.

---

## Navigation Timeout

**Symptom:** `TimeoutError` during `page.goto()` or after clicking a link.

```python
# Increase navigation timeout specifically
page.goto("https://example.com", timeout=60000)

# Or wait for a specific load state
page.goto("https://example.com")
page.wait_for_load_state("networkidle")

# After a click that triggers navigation
with page.expect_navigation(timeout=60000):
    page.get_by_role("button", name="Next").click()
```

---

## Login Wall (Redirected to Login on Every Run)

**Symptom:** Script navigates to a protected page but keeps landing on the login screen.

**Fix:** Use `storage_state` to persist the session (see `patterns.md` section 3).

If the session expires frequently, add a login-check at the start:

```python
page.goto("https://example.com/dashboard")
page.wait_for_load_state("networkidle")

if page.url.startswith("https://example.com/login"):
    # Session expired — log in again and re-save state
    page.get_by_label("Email").fill("user@example.com")
    page.get_by_label("Password").fill("secret")
    page.get_by_role("button", name="Log in").click()
    page.wait_for_load_state("networkidle")
    page.context.storage_state(path="auth.json")
```

---

## Content Inside an iframe

**Symptom:** Selector finds nothing even though the element is visible on screen.

**Cause:** Element lives inside an `<iframe>` — Playwright doesn't cross frame boundaries by default.

```python
# Target the iframe first, then locate within it
frame = page.frame_locator("iframe[name='content-frame']")
frame.get_by_role("button", name="Submit").click()

# Or by iframe src
frame = page.frame_locator("iframe[src*='checkout']")
frame.get_by_label("Card number").fill("4111111111111111")
```

---

## Dynamic Content Not Loaded

**Symptom:** Script reads empty or stale data from a page that loads content via JavaScript.

```python
# Wait for all network requests to finish
page.wait_for_load_state("networkidle")

# Or wait for a specific element that signals content is ready
page.wait_for_selector(".data-table tbody tr")

# Or wait for a specific response (useful for API-driven pages)
with page.expect_response("**/api/results**") as response_info:
    page.get_by_role("button", name="Search").click()
response = response_info.value
print(response.json())
```

---

## StaleElementError / Element Detached

**Symptom:** `Error: strict mode violation` or element reference becomes invalid mid-script.

**Fix:** Re-query the element after any navigation or DOM mutation instead of caching it.

```python
# Don't cache locators across navigations
# Bad
btn = page.get_by_role("button", name="Next")
page.reload()
btn.click()  # stale — page reloaded

# Good — re-query after navigation
page.reload()
page.get_by_role("button", name="Next").click()
```
