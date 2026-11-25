"""Defaults and validation for public STARS caches."""

from shared.settings import SettingsError, setting_value

CACHE_TTL_SECONDS = 3600
MAX_CACHE_ENTRIES = 128


def cache_ttl_seconds(default: int = CACHE_TTL_SECONDS) -> int:
    try:
        value = int(setting_value("NTU_CACHE_TTL_SECONDS", str(default)))
    except ValueError:
        value = -1
    if value < 0:
        raise SettingsError("NTU_CACHE_TTL_SECONDS must be a nonnegative integer.")
    return value
