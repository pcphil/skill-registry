from playwright.sync_api import sync_playwright, expect


def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://example.com")
    page.wait_for_load_state("networkidle")

    # automation steps here

    page.screenshot(path="debug.png")
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
