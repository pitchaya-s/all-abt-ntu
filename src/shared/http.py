"""Request limits and retry policy shared by upstream clients."""

import math
import ssl
import time
from contextlib import contextmanager
from contextvars import ContextVar
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from http.cookiejar import DefaultCookiePolicy
from urllib.parse import urlsplit

import httpx

from .errors import OperationError

TRANSIENT_STATUS = frozenset({429, 500, 502, 503, 504})
REDIRECT_STATUS = frozenset({301, 302, 303, 307, 308})
_DEADLINE: ContextVar[float | None] = ContextVar("ntu_request_deadline", default=None)


class NoCookies(DefaultCookiePolicy):
    def set_ok(self, cookie, request):
        return False

    def return_ok(self, cookie, request):
        return False


@contextmanager
def request_budget(seconds: float = 120):
    if _DEADLINE.get() is not None:
        yield
        return
    token = _DEADLINE.set(time.monotonic() + seconds)
    try:
        yield
    finally:
        _DEADLINE.reset(token)


def remaining_time() -> float | None:
    deadline = _DEADLINE.get()
    if deadline is None:
        return None
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise OperationError(
            "The lookup timed out. Try a narrower request or retry later."
        )
    return remaining


def request_timeout(seconds: float) -> httpx.Timeout:
    remaining = remaining_time()
    if remaining is not None:
        seconds = min(seconds, remaining)
    return httpx.Timeout(seconds, connect=min(10.0, seconds))


def retry_after_seconds(value: str | None, default: float) -> float:
    if not value:
        return default
    try:
        delay = float(value)
    except ValueError:
        try:
            date = parsedate_to_datetime(value)
            if date.tzinfo is None:
                date = date.replace(tzinfo=timezone.utc)
            delay = (date - datetime.now(timezone.utc)).total_seconds()
        except (TypeError, ValueError, OverflowError):
            return default
    return max(0.0, delay) if math.isfinite(delay) else default


def retryable_connection_error(error: httpx.RequestError) -> bool:
    cause: BaseException | None = error
    while cause is not None:
        if isinstance(cause, ssl.SSLError):
            return False
        cause = cause.__cause__
    return isinstance(
        error, (httpx.TimeoutException, httpx.NetworkError, httpx.RemoteProtocolError)
    )


def failed_request_url(error: httpx.RequestError, default: str) -> str:
    try:
        return str(error.request.url)
    except RuntimeError:
        return default


def allowed_https_url(url: str, hosts) -> bool:
    try:
        parsed = urlsplit(url)
        return (
            parsed.scheme == "https"
            and parsed.hostname in hosts
            and parsed.port in (None, 443)
            and parsed.username is None
            and parsed.password is None
            and not parsed.fragment
        )
    except (TypeError, ValueError):
        return False
