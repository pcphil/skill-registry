# Playwright codegen patterns (e2e / UI)

Loaded when the user names **Playwright** as the target framework for e2e/UI cases.
Turn the Phase B e2e rows into a browser-driving suite. Patterns are generic — login
is a worked example only. e2e proves the real user journey, so these specs need a
**running app**; they cannot run against an in-memory mock.

Playwright has two first-class bindings — pick the one matching the project's stack:

- **TypeScript** (`@playwright/test`, npm) — `*.spec.ts`.
- **Python** (`pytest-playwright`, pip) — `test_*.py` using the `page` fixture; runs
  under pytest, so e2e slots into the same run as the unit/integration suite from
  `references/pytest.md`.

The conventions below are identical across bindings: one case row → one test, case ID
in the test name, accessible locators, explicit final assertion, e2e kept thin.

## File layout

**TypeScript**
```
<suite>/
├── e2e/<flow>.spec.ts     # one spec file per user flow
├── playwright.config.ts   # baseURL + browser projects
└── package.json           # @playwright/test devDependency
```

`playwright.config.ts` — point `baseURL` at the running app:

```ts
import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./e2e",
  use: {
    baseURL: process.env.BASE_URL ?? "http://localhost:3000",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
  },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
});
```

**Python**
```
<suite>/
├── e2e/test_<flow>.py     # one file per user flow; uses the `page` fixture
└── pytest.ini             # [pytest] addopts/base-url config
```

`pytest.ini` — set the base URL (or pass `--base-url` on the CLI):

```ini
[pytest]
addopts = --base-url http://localhost:3000 --screenshot only-on-failure --tracing retain-on-failure
```

## Case row → spec

One e2e table row → one test. Put the case ID in the test name so it maps back.

| Table column | Goes to |
|--------------|---------|
| ID + Title | test name `E-01 valid login lands on dashboard` |
| Preconditions | seeded data / per-test navigation |
| Steps / Inputs | page actions (`fill`, `click`) |
| Expected result | assertion on URL / visible text / network |

**TypeScript**
```ts
import { test, expect } from "@playwright/test";

test("E-01 valid login lands on dashboard", async ({ page }) => {
  await page.goto("/login");
  await page.getByLabel(/email/i).fill("user@example.com");
  await page.getByLabel(/password/i).fill("Pass123!");
  await page.getByRole("button", { name: /sign in|log in/i }).click();
  await expect(page).toHaveURL(/.*dashboard/);
});
```

**Python** (`page` fixture is provided by `pytest-playwright`; `--base-url` makes
`page.goto("/login")` relative)
```python
import re
from playwright.sync_api import Page, expect

# E-01 valid login lands on dashboard
def test_e01_valid_login_lands_on_dashboard(page: Page):
    page.goto("/login")
    page.get_by_label(re.compile("email", re.I)).fill("user@example.com")
    page.get_by_label(re.compile("password", re.I)).fill("Pass123!")
    page.get_by_role("button", name=re.compile("sign in|log in", re.I)).click()
    expect(page).to_have_url(re.compile(r".*dashboard"))
```

## Selector strategy

Prefer accessible, resilient locators over CSS/XPath, in either binding:

- TS: `getByRole("button", { name })`, `getByLabel(/email/i)`, `getByText(...)`.
- Python: `get_by_role("button", name=...)`, `get_by_label(...)`, `get_by_text(...)`.
- Fall back to `getByTestId` / `get_by_test_id` only when no accessible name exists.
- Note in the test that routes (`/login`, `/dashboard`) and selectors must be adjusted
  to the app's real markup — generated selectors are a starting point.

## Asserting "no request sent" (client-side validation rows)

For a case like "empty submit blocked client-side", assert the network stayed quiet.

**TypeScript**
```ts
test("E-05 empty submit blocked", async ({ page }) => {
  await page.goto("/login");
  let posted = false;
  page.on("request", (r) => {
    if (r.url().includes("/login") && r.method() === "POST") posted = true;
  });
  await page.getByRole("button", { name: /sign in|log in/i }).click();
  await expect(page.getByText(/required/i)).toBeVisible();
  expect(posted).toBe(false);
});
```

**Python**
```python
def test_e05_empty_submit_blocked(page: Page):
    page.goto("/login")
    posted = {"v": False}
    def _seen(req):
        if "/login" in req.url and req.method == "POST":
            posted["v"] = True
    page.on("request", _seen)
    page.get_by_role("button", name=re.compile("sign in|log in", re.I)).click()
    expect(page.get_by_text(re.compile("required", re.I))).to_be_visible()
    assert posted["v"] is False
```

## Tooling

Recommend, do not auto-install. e2e also needs the app running.

**TypeScript**
```bash
npm install
npx playwright install chromium
BASE_URL=http://localhost:3000 npm run test:e2e
```

**Python**
```bash
pip install pytest-playwright
playwright install chromium
pytest e2e/ --base-url http://localhost:3000
```

## Coverage discipline

- One e2e row → one test; keep e2e to the few critical journeys (the table's P0/P1 flows).
- Every test ends on an explicit assertion for the stated expected result.
- Push exhaustive input/edge permutations down to unit/integration — keep e2e thin.
