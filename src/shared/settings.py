"""Application-scoped NTU service settings."""

import os
from collections.abc import Mapping
from contextlib import contextmanager
from contextvars import ContextVar
from typing import TypeVar

from .errors import OperationError

# Each entry maps a friendly key to its existing environment variable, type and limits.
SETTINGS: dict[
    str, dict[str, tuple[str, type, int | float | None, int | float | None]]
] = {
    "stars": {
        "cache_ttl_seconds": ("NTU_CACHE_TTL_SECONDS", int, 0, None),
        "personal_cache_ttl_seconds": ("NTU_PERSONAL_CACHE_TTL_SECONDS", int, 0, 86400),
    },
    "ntulearn": {
        "cache_ttl_seconds": ("NTULEARN_CACHE_TTL_SECONDS", int, 0, 86400),
        "headless": ("NTULEARN_HEADLESS", bool, None, None),
        "browser_cookies": ("NTULEARN_BROWSER_COOKIES", bool, None, None),
        "request_concurrency": ("NTULEARN_REQUEST_CONCURRENCY", int, 1, 8),
        "request_interval_seconds": ("NTULEARN_REQUEST_INTERVAL_SECONDS", float, 0, 5),
        "timeout_seconds": ("NTULEARN_TIMEOUT_SECONDS", float, 1, 120),
    },
    "careeraxis": {
        "cache_ttl_seconds": ("CAREERAXIS_CACHE_TTL_SECONDS", int, 0, 3600),
        "headless": ("CAREERAXIS_HEADLESS", bool, None, None),
    },
    "onestop": {"upload_dir": ("NTU_ONESTOP_UPLOAD_DIR", str, None, None)},
    "public_http": {
        "concurrency": ("NTU_PUBLIC_HTTP_CONCURRENCY", int, 1, 8),
        "interval_seconds": ("NTU_PUBLIC_HTTP_INTERVAL_SECONDS", float, 0, 10),
        "timeout_seconds": ("NTU_PUBLIC_HTTP_TIMEOUT_SECONDS", float, 1, 120),
        "max_retry_delay_seconds": (
            "NTU_PUBLIC_HTTP_MAX_RETRY_DELAY_SECONDS",
            float,
            0,
            30,
        ),
    },
    "browser": {"browsers_path": ("PLAYWRIGHT_BROWSERS_PATH", str, None, None)},
}

_NAMES = frozenset(
    entry[0] for section in SETTINGS.values() for entry in section.values()
)
_SETTINGS: ContextVar[Mapping[str, str] | None] = ContextVar(
    "ntu_settings", default=None
)


class SettingsError(OperationError):
    """A service setting has an invalid value."""


def resolved_settings(defaults: Mapping[str, str] | None = None) -> dict[str, str]:
    current = _SETTINGS.get()
    if current is not None and defaults is None:
        return dict(current)
    return {
        name: value
        for name, value in {**(defaults or {}), **os.environ}.items()
        if name in _NAMES
    }


@contextmanager
def settings_scope(settings: Mapping[str, str]):
    token = _SETTINGS.set(settings)
    try:
        yield
    finally:
        _SETTINGS.reset(token)


_Default = TypeVar("_Default", str, None)


def setting_value(name: str, default: _Default) -> str | _Default:
    settings = _SETTINGS.get()
    return (os.environ if settings is None else settings).get(name, default)
