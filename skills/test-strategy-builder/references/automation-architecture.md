# Test automation architecture

Loaded when the strategy needs an explicit automation-architecture decision — the
structural choices that decide whether a suite scales or rots. Make these calls in
Phase A, sized to risk, before generating cases. Patterns are generic; login is a
worked example only. For concrete code shapes see `references/pytest.md` and
`references/playwright.md`.

## 1. Pyramid & layer split

Decide how much of each layer the suite carries, weighted by risk and cost:

- **Unit** (most) — pure logic, validators, hashing, token math. Fast, deterministic, cheap. Cover edge/permutation inputs here.
- **Integration / API** (middle) — boundary behavior: routes + DB/session, status codes, error shapes. Highest auth-risk concentration.
- **E2E / UI** (fewest) — a handful of critical user journeys only (login success, login fail, logout, reset).

**Push-down rule:** if a behavior can be proven one layer down, move it down. Never
verify validation permutations through the browser. Keep e2e thin — it is the
slowest and flakiest layer. An inverted pyramid (e2e-heavy) is the main scaling failure.

## 2. Page Object Model

### Page Object Model (e2e)

A page object models one screen and is the single place its selectors live. Rules:

1. **One page object per screen or component.**
2. **Locators defined once** — in the constructor, never inline in a spec.
3. **Methods express user intent** (`login(email, pwd)`), not mechanics (`fill`/`click`).
4. **A method that navigates returns the next page object** — page-transition chaining,
   so a spec reads as a journey.
5. **No assertions inside page objects** — they model the page; tests own the asserts.
6. **A `BasePage`** holds shared navigation / URL helpers; screens extend it.

```python
# pages/base_page.py
class BasePage:
    def __init__(self, page):
        self.page = page

# pages/login_page.py
class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.email = page.get_by_label("Email")
        self.password = page.get_by_label("Password")
        self.submit = page.get_by_role("button", name="Log in")

    def open(self):
        self.page.goto("/login")
        return self

    def login(self, email, password):
        self.email.fill(email)
        self.password.fill(password)
        self.submit.click()
        return DashboardPage(self.page)   # navigation returns the next page object

# tests/test_login.py — assertions live here, not in the page object
def test_e01_valid_login(page):
    dashboard = LoginPage(page).open().login("user@example.com", "Pass123!")
    expect(dashboard.user_email).to_have_text("user@example.com")
```

See `references/playwright.md` for the runnable binding-level detail (TS and Python).

### Integration boundary (not POM)

When there is no live server, model the edge as a small object returning `(status, body)`
— see `references/pytest.md`. Same assert shape swaps onto a real HTTP client later.

### Naming

Carry the case ID into the test name (`test_u01_...`, `test("E-01 ...")`) so the suite
maps back to the strategy table. Shared helpers in one place, no copy-paste.

## 3. Data & fixtures

The largest source of flake is shared, mutable, order-dependent state.

- **Fixtures for setup** — `conftest.py` fixtures (pytest) / `beforeEach` (Playwright)
  seed the minimum a case needs and tear it down after.
- **Factories for variation** — a `make_user(**overrides)` helper beats hand-built
  dicts when cases need slight variants; defaults sane, override only what matters.
- **Isolation** — each test owns its data; never depend on another test's residue or
  on execution order. Fresh state per test (or per worker) so tests can parallelize.
- **Determinism** — pin clocks/seeds/UUIDs where behavior depends on them (e.g. token
  expiry math); no real time, no random emails that collide.

## 4. CI, parallel & flake

- **Parallel / sharding** — design for isolation (above) so the runner can fan out
  (`pytest -n`, Playwright workers/shards). Parallel-safe data is the prerequisite.
- **Retries** — retry e2e on first failure only (`trace: on-first-retry`) to absorb
  genuine flake without masking real regressions; do not blanket-retry unit/integration.
- **Flake quarantine** — tag a known-flaky test, run it off the gating path, track it
  for fix — never delete silently and never let it block the pipeline.
- **Gating** — unit + integration block merge; e2e critical-path (the `smoke` set,
  select with `-m smoke`) blocks merge; the long-tail e2e can run post-merge / nightly.
- **Artifacts** — capture traces, screenshots, videos on failure for triage
  (`screenshot: only-on-failure`). Store them per run.

## 5. Test markers & selection

Tag tests with markers so the suite slices by purpose, not just by directory or layer.
Register every marker in `pytest.ini` — an unregistered mark is a silent typo:

```ini
[pytest]
markers =
    smoke: fast P0 critical-path, gate every push
    regression: full coverage, run nightly / pre-release
    api: integration / API-layer tests (the boundary suite)
    slow: long-running, opt-in
    flaky: known-unstable, quarantined off the gate
```

```python
import pytest

@pytest.mark.smoke
def test_e01_valid_login(page):
    ...

@pytest.mark.api
def test_i02_login_wrong_password(api):
    ...

@pytest.mark.regression
@pytest.mark.slow
def test_password_reset_email_flow(page):
    ...
```

Select at run time with `-m`:

```bash
pytest -m smoke                      # fast gate, every push
pytest -m api                        # just the boundary suite
pytest -m "regression and not flaky" # full set, skip quarantined
pytest -m "not slow"                 # everything quick
```

Marker discipline:
- **smoke** = a few P0 journeys, seconds-fast; it composes across layers (one unit, one
  `api` integration, one e2e happy path), not a whole layer.
- **regression** = the exhaustive set; runs nightly / pre-release, not on every push.
- **api** marks the integration boundary suite so it can run without spinning browsers.
- **flaky** routes a test off the gate (ties to flake quarantine in section 4) — never
  delete, track for fix.

Playwright (TS) has no `pytest.mark`; tag tests in the title (`@smoke`) and select with
`--grep @smoke` — see `references/playwright.md`.

## 6. Synchronization (no sleeps)

Fixed waits are the #1 e2e flake source. Never `time.sleep` / `page.wait_for_timeout`.

- Use **web-first assertions** that auto-retry until a timeout: `expect(locator).to_be_visible()`,
  `expect(page).to_have_url(...)`. Playwright also auto-waits for actionability before
  acting (visible, enabled, stable).
- Wait on a **condition**, not a duration: `page.wait_for_url(...)`,
  `page.wait_for_load_state(...)`, or an `expect` that encodes the state you need.
- If you reach for a sleep, you are missing the assertion that describes what you're
  waiting for — write that instead.

## 7. Auth & state reuse (speed)

Logging in through the UI on every test is slow and flaky. Log in **once**, reuse the
session.

- Save `storageState` (cookies + localStorage) after a login, then start tests
  authenticated:

```python
# session fixture: authenticate once, persist storage
context = browser.new_context()
LoginPage(context.new_page()).open().login(EMAIL, PASSWORD)
context.storage_state(path=".auth/state.json")

# each test: skip the UI login
context = browser.new_context(storage_state=".auth/state.json")
```

- Better still, authenticate via **API/token** and seed storage instead of driving the UI.
  The UI login is proven once (E-01); everywhere else, reuse state.
- General rule: **set up state via API, assert via UI** — fast and focused.

## 8. Reporting & artifacts

Make failures triageable and CI-readable.

- **CI report:** JUnit XML (`pytest --junitxml=report.xml`); a human report via
  `pytest-html` or Allure.
- **On failure:** Playwright trace (`--tracing retain-on-failure`, open in the trace
  viewer) plus screenshot / video. See `references/playwright.md` for wiring.
- Publish artifacts per run; track flake rate over time so quarantine (section 4) is data-driven.

## 9. Environments & secrets

Run the same suite against any environment without code changes.

- Drive `base_url` and credentials from the environment (`BASE_URL`, `.env` / CI secrets);
  keep one config per environment (dev / staging / prod-readonly).
- **Never hardcode** credentials or tokens in tests — read them from env / a secret store;
  CI injects secrets at run time.
- A config matrix lets one suite target dev locally and staging in CI from the same code.

## 10. Specialized checks

### Visual regression
`expect(page).to_have_screenshot()` diffs against a committed baseline. Commit baselines,
review diffs on change, mask dynamic regions (dates, avatars). Gate selectively — fonts
and rendering differ across OS/CI, so visual tests flake easily.

### Accessibility
Run axe-core as an assertion on key screens (`axe-playwright-python` /
`@axe-core/playwright`); fail the test on new violations. Cheap, high-value coverage that
unit/integration can't give.

## Output of this step

A short architecture decision recorded in the Phase A test plan: pyramid split,
suite structure, data strategy, marker scheme (smoke gate), sync & auth-reuse strategy,
and CI/flake approach — each one line, justified by risk. Then proceed to the case table.
