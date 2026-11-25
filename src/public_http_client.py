"""Pooled, bounded public HTTPS reads shared by NTU services."""

import logging
import time
import weakref
from collections import OrderedDict
from concurrent.futures import Future, wait
from contextlib import contextmanager
from datetime import datetime, timezone
from threading import BoundedSemaphore, Lock
from urllib.parse import urljoin, urlsplit

import httpx

from shared.errors import OperationError
from shared.http import (
    REDIRECT_STATUS,
    TRANSIENT_STATUS,
    NoCookies,
    allowed_https_url,
    failed_request_url,
    remaining_time,
    request_budget,
    request_timeout,
    retry_after_seconds,
    retryable_connection_error,
)
from shared.settings import SettingsError, setting_value

MAX_RESPONSE_BYTES = 8_000_000
MAX_RETRY_DELAY_SECONDS = 10.0
MAX_REDIRECTS = 5
MAX_ATTEMPTS = 2
REQUEST_CONCURRENCY = 2
REQUEST_INTERVAL_SECONDS = 0.25
REQUEST_TIMEOUT_SECONDS = 20.0
CACHE_TTL_SECONDS = 300.0
MAX_CACHE_ENTRIES = 64
MAX_CACHE_BYTES = 16_000_000
_SCHEDULERS_LOCK = Lock()
logger = logging.getLogger(__name__)


def _setting(name, default, cast, minimum, maximum):
    try:
        value = cast(setting_value(name, str(default)))
    except (TypeError, ValueError):
        raise SettingsError(
            f"{name} must be a number between {minimum} and {maximum}."
        ) from None
    if not minimum <= value <= maximum:
        raise SettingsError(f"{name} must be a number between {minimum} and {maximum}.")
    return value


def public_timeout() -> float:
    return _setting(
        "NTU_PUBLIC_HTTP_TIMEOUT_SECONDS", REQUEST_TIMEOUT_SECONDS, float, 1, 120
    )


def max_retry_delay() -> float:
    return _setting(
        "NTU_PUBLIC_HTTP_MAX_RETRY_DELAY_SECONDS", MAX_RETRY_DELAY_SECONDS, float, 0, 30
    )


class PublicRequestError(OperationError):
    def __init__(
        self, message, *, status=None, content_type=None, response_too_large=False
    ):
        super().__init__(message)
        self.status = status
        self.content_type = content_type
        self.response_too_large = response_too_large


class _HostScheduler:
    """Share concurrency and pacing between clients that call the same host."""

    def __init__(self, interval):
        concurrency = _setting(
            "NTU_PUBLIC_HTTP_CONCURRENCY", REQUEST_CONCURRENCY, int, 1, 8
        )
        self._slots = BoundedSemaphore(concurrency)
        self._interval = interval
        self._pace_lock = Lock()
        self._last_request = 0.0
        self._defer_until = 0.0

    @contextmanager
    def request_slot(self):
        if not self._slots.acquire(timeout=remaining_time()):
            raise PublicRequestError(
                "The upstream lookup ran out of time waiting for a connection."
            )
        try:
            with self._pace_lock:
                now = time.monotonic()
                if self._defer_until - now > max_retry_delay():
                    raise PublicRequestError(
                        "The upstream service requested a cooldown. Try again later.",
                        status=429,
                    )
                ready_at = max(
                    self._defer_until,
                    self._last_request + self._interval,
                )
                delay = max(0.0, ready_at - now)
                remaining = remaining_time()
                if remaining is not None and delay >= remaining:
                    raise PublicRequestError(
                        "The upstream lookup ran out of time waiting for a request slot."
                    )
                if delay:
                    time.sleep(delay)
                self._last_request = time.monotonic()
            yield
        finally:
            self._slots.release()

    def defer(self, seconds):
        if seconds <= 0:
            return
        with self._pace_lock:
            self._defer_until = max(self._defer_until, time.monotonic() + seconds)


_SCHEDULERS: dict[str, _HostScheduler] = {}


def _scheduler_for(url):
    host = urlsplit(url).hostname
    if host is None:
        raise PublicRequestError(
            "The public service returned an unexpected URL; retrieval stopped."
        )
    host = host.lower()
    with _SCHEDULERS_LOCK:
        scheduler = _SCHEDULERS.get(host)
        if scheduler is None:
            # DR-NTU (Data) publishes a 60-second crawl delay. Be conservative
            # for API requests too, including calls from different clients.
            interval = _setting(
                "NTU_PUBLIC_HTTP_INTERVAL_SECONDS",
                REQUEST_INTERVAL_SECONDS,
                float,
                0,
                10,
            )
            if host == "researchdata.ntu.edu.sg":
                interval = max(interval, 60.0)
            scheduler = _HostScheduler(interval)
            _SCHEDULERS[host] = scheduler
        return scheduler


@contextmanager
def host_request_slot(url):
    """Apply the process-wide public request limit for the URL's host."""
    with _scheduler_for(url).request_slot():
        yield


def defer_host_requests(url, seconds):
    _scheduler_for(url).defer(seconds)


class _Redirects:
    def __init__(self, hosts):
        self.hosts = frozenset(host.lower() for host in hosts)

    def validate(self, url):
        if not allowed_https_url(url, self.hosts):
            raise PublicRequestError(
                "The public service returned an unexpected URL or redirect; retrieval stopped."
            )


class PublicHTTPClient:
    def __init__(
        self,
        service,
        hosts,
        content_types,
        *,
        transport: httpx.BaseTransport | None = None,
    ):
        self.service = service
        self.content_types = frozenset(value.lower() for value in content_types)
        self.redirects = _Redirects(hosts)
        self._timeout = public_timeout()
        self._max_retry_delay = max_retry_delay()
        self.client = httpx.Client(
            timeout=httpx.Timeout(self._timeout, connect=min(10.0, self._timeout)),
            follow_redirects=False,
            transport=transport,
            headers={
                "User-Agent": "all-abt-ntu-mcp/0.1 (public NTU lookup)",
                "Accept": ", ".join(sorted(self.content_types)),
            },
        )
        self.client.cookies.jar.set_policy(NoCookies())
        self._lock = Lock()
        self._cache: OrderedDict[str, tuple[float, bytes, datetime]] = OrderedDict()
        self._inflight: dict[tuple[str, bool], Future[tuple[bytes, datetime]]] = {}
        self._latest_started: dict[str, int] = {}
        self._next_sequence = 0
        self._closed = False
        self._finalizer = weakref.finalize(self, self.client.close)

    def get(self, url, refresh=False):
        with request_budget():
            return self._get(url, refresh)

    def _get(self, url, refresh):
        self.redirects.validate(url)
        key = (url, bool(refresh))
        with self._lock:
            if self._closed:
                raise PublicRequestError(
                    f"The {self.service} HTTP client is closed; restart the MCP server."
                )
            cached = self._cache.get(url)
            if (
                not refresh
                and cached is not None
                and time.monotonic() - cached[0] < CACHE_TTL_SECONDS
            ):
                self._cache.move_to_end(url)
                return cached[1], self._snapshot(url, cached[2], cached=True)
            flight = self._inflight.get(key)
            owner = flight is None
            if owner:
                flight = Future()
                self._inflight[key] = flight
                self._next_sequence += 1
                sequence = self._next_sequence
                self._latest_started[url] = sequence

        if not owner:
            try:
                body, retrieved = flight.result(timeout=remaining_time())
            except TimeoutError:
                raise PublicRequestError(
                    "The upstream lookup ran out of time."
                ) from None
            return body, self._snapshot(url, retrieved, cached=True)

        try:
            body, retrieved = self._fetch(url)
        except BaseException as error:
            with self._lock:
                if self._inflight.get(key) is flight:
                    del self._inflight[key]
                if (url, False) not in self._inflight and (
                    url,
                    True,
                ) not in self._inflight:
                    self._latest_started.pop(url, None)
                flight.set_exception(error)
            raise

        with self._lock:
            if self._latest_started.get(url) == sequence:
                self._cache[url] = (time.monotonic(), body, retrieved)
                self._cache.move_to_end(url)
                while (
                    len(self._cache) > MAX_CACHE_ENTRIES
                    or sum(len(entry[1]) for entry in self._cache.values())
                    > MAX_CACHE_BYTES
                ):
                    self._cache.popitem(last=False)
            if self._inflight.get(key) is flight:
                del self._inflight[key]
            if (url, False) not in self._inflight and (url, True) not in self._inflight:
                self._latest_started.pop(url, None)
            flight.set_result((body, retrieved))
        return body, self._snapshot(url, retrieved, cached=False)

    @staticmethod
    def _snapshot(url, retrieved, *, cached):
        return dict(retrieved_at=retrieved, source_url=url, cached=cached)

    @contextmanager
    def parsed_response(self, url, refresh=False):
        """Evict this response if validation inside the block fails."""
        body, snapshot = self.get(url, refresh)
        try:
            yield body, snapshot
        except Exception:
            self.invalidate(url, retrieved_at=snapshot.get("retrieved_at"))
            raise

    def invalidate(self, url, *, retrieved_at=None):
        with self._lock:
            cached = self._cache.get(url)
            if cached is not None and (
                retrieved_at is None or cached[2] == retrieved_at
            ):
                self._cache.pop(url, None)

    def _fetch(self, url):
        for attempt in range(MAX_ATTEMPTS):
            try:
                status, headers, body, response_url = self._request_chain(url)
            except httpx.RequestError as error:
                if attempt + 1 < MAX_ATTEMPTS and retryable_connection_error(error):
                    defer_host_requests(
                        failed_request_url(error, url), min(4.0, 2.0**attempt)
                    )
                    continue
                raise PublicRequestError(
                    f"Could not reach {self.service}; try again later."
                ) from None
            except httpx.HTTPError:
                raise PublicRequestError(
                    f"{self.service} returned an invalid HTTP response; retrieval stopped."
                ) from None

            if status == 429:
                logger.warning("%s upstream returned HTTP 429", self.service)
            if status in TRANSIENT_STATUS:
                advertised = headers.get("retry-after")
                delay = retry_after_seconds(advertised, 1.0)
                retry = attempt + 1 < MAX_ATTEMPTS and delay <= self._max_retry_delay
                if retry or advertised or status == 429:
                    defer_host_requests(response_url, delay)
                if retry:
                    continue
            if status >= 400:
                raise PublicRequestError(
                    f"{self.service} returned HTTP {status}; check the request or try again later.",
                    status=status,
                )
            retrieved = datetime.now(timezone.utc)
            return body, retrieved
        raise PublicRequestError(
            f"Could not reach {self.service} after two attempts; try again later."
        )

    def _request_chain(self, url):
        current_url = url
        for _ in range(MAX_REDIRECTS + 1):
            self.redirects.validate(current_url)
            with (
                host_request_slot(current_url),
                self.client.stream(
                    "GET", current_url, timeout=request_timeout(self._timeout)
                ) as response,
            ):
                if response.status_code in REDIRECT_STATUS:
                    location = response.headers.get("location")
                    if not location:
                        raise PublicRequestError(
                            f"{self.service} returned an incomplete redirect; retrieval stopped."
                        )
                    current_url = urljoin(current_url, location)
                    self.redirects.validate(current_url)
                    continue

                headers = response.headers
                status = response.status_code
                if status >= 400:
                    return status, headers, b"", current_url
                content_type = (
                    headers.get("content-type", "").split(";", 1)[0].strip().lower()
                )
                if content_type not in self.content_types:
                    raise PublicRequestError(
                        f"{self.service} returned an unexpected content type; no data was inferred.",
                        content_type=content_type,
                    )
                length = headers.get("content-length")
                if length and length.isdigit() and int(length) > MAX_RESPONSE_BYTES:
                    raise PublicRequestError(
                        f"{self.service} response exceeded the 8 MB safety limit.",
                        response_too_large=True,
                    )
                body = bytearray()
                for chunk in response.iter_bytes():
                    remaining_time()
                    if len(body) + len(chunk) > MAX_RESPONSE_BYTES:
                        raise PublicRequestError(
                            f"{self.service} response exceeded the 8 MB safety limit.",
                            response_too_large=True,
                        )
                    body.extend(chunk)
                return status, headers, bytes(body), current_url
        raise PublicRequestError(
            f"{self.service} returned too many redirects; retrieval stopped."
        )

    def close(self):
        with self._lock:
            if self._closed:
                return
            self._closed = True
            flights = tuple(self._inflight.values())
        wait(flights)
        try:
            self.client.close()
        finally:
            self._finalizer.detach()
