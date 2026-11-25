"""Browser setup shared by the offline Chromium contract tests."""

import os
import unittest


def launch_chromium(playwright):
    try:
        return playwright.chromium.launch(headless=True)
    except Exception:
        if os.environ.get("NTU_TEST_REQUIRE_CHROMIUM") == "1":
            raise
        raise unittest.SkipTest("Optional Chromium is unavailable") from None
