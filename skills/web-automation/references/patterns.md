# Playwright Python Patterns

Load this file before writing any automation script.

---

## 1. Selector Hierarchy

Prefer in this order. Stop at the first method that uniquely identifies the element.

```python
# 1. Role (most semantic, most stable)
page.get_by_role("button", name="Submit")
page.get_by_role("link", name="Next page")
page.get_by_role("textbox", name="Email")

# 2. Text (good for labels and headings)
page.get_by_text("Sign in")
page.get_by_text("Confirm order", exact=True)

# 3. Label (best for form fields with visible labels)
page.get_by_label("Password")
page.get_by_label("Search")

# 4. Test ID (when the app uses data-testid attributes)
page.get_by_test_id("submit-btn")

# 5. CSS (last resort — fragile, breaks on refactors)
page.locator("button.btn-primary")
page.locator("#email-input")

# Never: XPath — too brittle
```

---

## 2. Wait Strategies

Never use `time.sleep()`. Use Playwright's built-in waits.

```python
# Wait for page load
page.goto("https://example.com")
page.wait_for_load_state("networkidle")   # all network activity settled
page.wait_for_load_state("domcontentloaded")  # faster, DOM ready only

# Wait for a specific element before interacting
expect(page.get_by_role("button", name="Submit")).to_be_visible()
page.get_by_role("button", name="Submit").click()

# Wait for element to appear (returns locator when found)
page.wait_for_selector(".result-item")

# Wait for navigation after a click
with page.expect_navigation():
    page.get_by_role("button", name="Go").click()

# Increase default timeout globally (ms)
page.set_default_timeout(15000)
```

---

## 3. Auth / Session Reuse

Avoid logging in on every run. Save and reuse browser storage state.

```python
# First run: log in and save state
import os
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://example.com/login")
    page.get_by_label("Email").fill(os.environ["SITE_EMAIL"])
    page.get_by_label("Password").fill(os.environ["SITE_PASSWORD"])
    page.get_by_role("button", name="Log in").click()
    page.wait_for_load_state("networkidle")

    context.storage_state(path="auth.json")  # save cookies + localStorage
    browser.close()

# Subsequent runs: load saved state (skip login)
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(storage_state="auth.json")
    page = context.new_page()
    page.goto("https://example.com/dashboard")
    # already logged in
```

---

## 4. Form Interaction

```python
# Text input
page.get_by_label("First name").fill("Alice")

# Dropdown (select by visible text)
page.get_by_label("Country").select_option("Canada")

# Dropdown (select by value)
page.get_by_label("Size").select_option(value="xl")

# Checkbox
page.get_by_label("I agree to terms").check()
page.get_by_label("Subscribe to newsletter").uncheck()

# Radio button
page.get_by_label("Credit card").check()

# Key press
page.get_by_role("textbox").press("Enter")
page.keyboard.press("Tab")

# File upload
page.get_by_label("Upload file").set_input_files("report.pdf")

# Clear and retype
field = page.get_by_label("Search")
field.clear()
field.fill("new query")
```

---

## 5. Pagination

```python
while True:
    # Process current page content here
    items = page.locator(".item").all()
    for item in items:
        print(item.inner_text())

    # Check for next page
    next_btn = page.get_by_role("link", name="Next")
    if not next_btn.is_visible():
        break

    next_btn.click()
    page.wait_for_load_state("networkidle")
```

---

## 6. Multi-Tab / Popups

```python
# Capture a new tab opened by a click
with context.expect_page() as new_page_info:
    page.get_by_role("link", name="Open in new tab").click()

new_page = new_page_info.value
new_page.wait_for_load_state("domcontentloaded")
new_page.bring_to_front()

# Do work on new_page, then close it
new_page.close()
page.bring_to_front()  # return to original

# Handle popup dialog (alert/confirm)
page.on("dialog", lambda dialog: dialog.accept())
page.get_by_role("button", name="Delete").click()
```

---

## 7. Screenshots & Debugging

```python
# End-of-script screenshot (always include)
page.screenshot(path="debug.png")

# Screenshot at a specific step
page.screenshot(path="after-login.png")

# Full-page screenshot
page.screenshot(path="full.png", full_page=True)

# Screenshot of a single element
page.get_by_role("table").screenshot(path="table.png")

# Pause execution for manual inspection (headed mode only)
page.pause()  # opens Playwright Inspector — remove before final run
```
