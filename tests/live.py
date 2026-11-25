"""Helpers for opt-in MCP checks against real services."""

import os
import sys
from pathlib import Path

from mcp.client.stdio import StdioServerParameters


def local_stdio(profile="public"):
    """Use the project interpreter and an explicit profile for live requests."""
    overrides = {}
    if profile == "personal":
        for name in (
            "DBUS_SESSION_BUS_ADDRESS",
            "XDG_RUNTIME_DIR",
            "PLAYWRIGHT_BROWSERS_PATH",
            "NTU_PERSONAL_CACHE_TTL_SECONDS",
        ):
            if name in os.environ:
                overrides[name] = os.environ[name]
    return StdioServerParameters(
        command=sys.executable,
        args=["-c", "import sys; from server import main; main(sys.argv[1])", profile],
        env=overrides,
        cwd=str(Path(__file__).resolve().parents[1]),
    )


def failure_kind(result):
    # Tool errors can contain upstream text. Classify them without emitting it.
    message = " ".join(getattr(item, "text", "") for item in result.content).lower()
    if any(word in message for word in ("mfa", "captcha", "interactive")):
        return "interactive authentication or upstream challenge"
    if any(
        word in message
        for word in ("login", "sign in", "keyring", "credentials", "sso")
    ):
        return "authentication or session failure"
    if any(word in message for word in ("timed out", "connection", "http ")):
        return "upstream or network failure"
    return "tool failure"
