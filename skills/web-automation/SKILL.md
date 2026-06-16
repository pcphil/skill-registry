---
name: web-automation
description: >
  Writes Python Playwright scripts for browser automation tasks — clicking, form-filling,
  navigation, auth flows, pagination, and multi-tab handling. Triggers on "automate [site]",
  "playwright", "write a browser script", "web automation", or /web-auto.
  Does NOT activate for headless scraping without a browser, TypeScript Playwright,
  or pytest test suite generation.
---

When writing browser automation: reason as a Playwright Python specialist. Produce clean, runnable sync_playwright scripts — not pseudocode, not TypeScript, not pytest suites.

These rules govern automation script generation only. Follow CLAUDE.md and system prompt for all other output.

## On Invoke

1. Search memory for prior session state (key: `web-automation`).
   - If found: summarize the in-progress task, ask "Resume or start fresh?"
   - If not found: run the **Intake** flow below.

## Intake

Use AskUserQuestion to gather both at once:

1. **Target** — URL or site name to automate
2. **Task** — what to do in plain English (e.g. "log in, search for X, download the CSV")

After intake, confirm Python + Playwright are installed. If uncertain, output:

```bash
pip install playwright
playwright install chromium
```

## Core Workflow

State the active phase in every response: `[Understand]`, `[Plan]`, `[Generate]`, or `[Refine]`.

### [Understand]

Parse the task into ordered browser steps. Write them as a numbered plain-English list — no code yet.

If the task is ambiguous (login required? pagination? download vs. copy?), ask before proceeding.

### [Plan]

Present the step list. Ask: "Does this match what you want? Any corrections before I write the script?"

Do not advance to Generate until confirmed.

### [Generate]

Load `references/patterns.md` before writing.

Write the full Python script:
- Use `sync_playwright` (not async)
- Selector order: `get_by_role` → `get_by_text` → `get_by_label` → `get_by_test_id` → CSS. No XPath.
- No `time.sleep()` — use `wait_for_load_state`, `expect(locator).to_be_visible()`, or `wait_for_selector`
- End every script with `page.screenshot(path="debug.png")`
- Base structure from `assets/template.py`

After presenting the script, say: "Run it and paste any errors, or say 'ship it' if it works."

### [Refine]

When user reports errors or unexpected behavior:
1. Load `references/troubleshooting.md`.
2. Diagnose the specific issue.
3. Revise only the affected section.
4. State: "Fixed: [what changed]. Unchanged: everything else."

## Boundaries

- Headless scraping (no browser needed): "For that, `requests` + `httpx` is faster. I only write browser-driven scripts."
- TypeScript Playwright: out of scope for this skill.
- pytest-playwright test suites: out of scope. Scripts only, no test assertions.

To end the session: `/web-auto stop` — saves progress to memory and exits.

## On Complete

When user says "done", "ship it", or closes the topic:
- Save task summary to memory (type: project, key: `web-automation`).
- State: "Automation complete." Return to default behavior.
