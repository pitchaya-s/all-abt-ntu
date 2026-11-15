"""Check the browser installed for the active Playwright environment."""

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def chromium_installed() -> bool:
    # Playwright's synchronous API cannot start in a running asyncio loop.
    def inspect_browser():
        from playwright.sync_api import sync_playwright

        with sync_playwright() as playwright:
            return Path(playwright.chromium.executable_path).is_file()

    try:
        with ThreadPoolExecutor(max_workers=1) as executor:
            return executor.submit(inspect_browser).result()
    except Exception:
        return False
