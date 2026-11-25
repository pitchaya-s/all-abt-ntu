"""Pooled, rate-limited and read-only HTTP transport for NTULearn."""

import asyncio
import json
import logging
import re
from contextlib import asynccontextmanager
from pathlib import Path
from time import monotonic
from typing import Any, AsyncIterator
from urllib.parse import urljoin, urlsplit

import anyio
import httpx

# HTTPX's INFO messages include complete URLs, including signed file-download
# query strings. HTTPCore's debug logs can include request headers and cookies.
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)

from shared.http import (
    TRANSIENT_STATUS,
    REDIRECT_STATUS,
    remaining_time,
    retry_after_seconds,
)

from ..models import LearnError
from .browser_cookies import BASE_URL, NTULEARN_HOST, SessionCookie, install_cookies
from .config import SessionConfig
from .videos.kaltura import download_kaltura_file as _download_kaltura_file

MAX_JSON_BYTES = 5_000_000
MAX_FILE_BYTES = 20_000_000
MAX_RETRY_DELAY_SECONDS = 60
MAX_ATTEMPTS = 3
_ID = r"[A-Za-z0-9_-]{1,80}"
READ_PATH = re.compile(
    rf"(?:/learn/api/public/v1/(?:users/me(?:/courses)?|calendars/items|courses/{_ID}"
    rf"(?:/announcements|/users|/groups|/gradebook/(?:columns|users/{_ID})"
    rf"|/contents(?:/{_ID}(?:/children|/attachments(?:/{_ID}/download)?)?)?)?)"
    rf"|/learn/api/v1/(?:messages/summary|courses/{_ID}/(?:conversations(?:/{_ID})?|memberships)))"
)
_RETRYABLE = TRANSIENT_STATUS
_REDIRECTS = REDIRECT_STATUS


class AuthGenerationChanged(Exception):
    """Authentication changed before a queued request reached the transport."""


def allowed_read_path(path: str) -> bool:
    return READ_PATH.fullmatch(path) is not None


class RequestScheduler:
    """A shared concurrency cap and minimum start interval for all requests."""

    def __init__(self, concurrency: int, interval_seconds: float):
        self._slots = asyncio.Semaphore(concurrency)
        self._interval = interval_seconds
        self._next_start = 0.0
        self._defer_until: dict[str, float] = {}

    def defer(self, host: str, delay: float) -> None:
        if delay > 0:
            self._defer_until[host] = max(
                self._defer_until.get(host, 0.0), monotonic() + delay
            )

    def _delay(self, host: str, now: float) -> float:
        deferred = self._defer_until.get(host, 0.0) - now
        if deferred > MAX_RETRY_DELAY_SECONDS:
            raise LearnError(
                "NTULearn requested a retry delay. Try this read again later."
            )
        return max(deferred, self._next_start - now)

    @asynccontextmanager
    async def slot(self, host: str) -> AsyncIterator[None]:
        while True:
            delay = self._delay(host, monotonic())
            if delay > 0:
                await asyncio.sleep(delay)
                continue
            async with self._slots:
                now = monotonic()
                if self._delay(host, now) > 0:
                    continue
                self._defer_until.pop(host, None)
                self._next_start = now + self._interval
                yield
                return


class LearnHTTP:
    def __init__(
        self,
        config: SessionConfig,
        *,
        transport: httpx.AsyncBaseTransport | None = None,
        external_transport: httpx.AsyncBaseTransport | None = None,
    ):
        timeout = httpx.Timeout(
            config.timeout_seconds,
            connect=min(config.timeout_seconds, 10.0),
        )
        limits = httpx.Limits(
            max_connections=config.request_concurrency,
            max_keepalive_connections=config.request_concurrency,
        )
        self.client = httpx.AsyncClient(
            base_url=BASE_URL,
            headers={"Accept": "application/json"},
            timeout=timeout,
            follow_redirects=False,
            limits=limits,
            transport=transport,
            trust_env=False,
        )
        # File delivery hosts never receive NTULearn cookies or inherited auth.
        self.external_client = httpx.AsyncClient(
            timeout=timeout,
            follow_redirects=False,
            limits=limits,
            transport=external_transport,
            trust_env=False,
        )
        self.scheduler = RequestScheduler(
            config.request_concurrency,
            config.request_interval_seconds,
        )
        self._external_lock = asyncio.Lock()
        self._auth_generation: int | None = None
        self._auth_cookies: tuple[Any, ...] = ()

    def set_cookies(self, cookies: tuple[SessionCookie, ...], generation: int) -> None:
        install_cookies(self.client.cookies.jar, cookies)
        self._auth_generation = generation
        self._snapshot_auth_cookies()

    def clear_cookies(self, generation: int | None = None) -> None:
        self.client.cookies.clear()
        self._auth_generation = generation
        self._auth_cookies = ()

    def _snapshot_auth_cookies(self) -> None:
        self._auth_cookies = tuple(self.client.cookies.jar)

    def _restore_auth_cookies(self) -> None:
        jar = self.client.cookies.jar
        jar.clear()
        for cookie in self._auth_cookies:
            jar.set_cookie(cookie)

    async def get(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        *,
        expected_generation: int | None = None,
    ) -> httpx.Response:
        if not allowed_read_path(path):
            raise LearnError(
                "This NTULearn endpoint is not in the read-only allowlist."
            )
        try:
            with anyio.fail_after(remaining_time()):
                return await self._get_json(
                    BASE_URL + path, params, expected_generation
                )
        except TimeoutError:
            raise LearnError(
                "The NTULearn lookup timed out. Try a narrower request or retry later."
            ) from None

    async def _get_json(self, url, params, expected_generation):
        for attempt in range(MAX_ATTEMPTS):
            async with self.stream(
                self.client, url, params=params, expected_generation=expected_generation
            ) as response:
                if (
                    response.status_code not in _RETRYABLE
                    or attempt == MAX_ATTEMPTS - 1
                ):
                    return await self._read_json_response(response, expected_generation)
                delay = retry_delay(response, attempt)
                paced = server_cooldown(response) >= 0
            if not paced:
                await asyncio.sleep(delay)
        raise LearnError("NTULearn is temporarily unavailable.")

    async def _read_json_response(self, response, expected_generation):
        body = bytearray()
        if (
            response.status_code == 200
            and "application/json" in response.headers.get("content-type", "").lower()
        ):
            async for chunk in response.aiter_bytes(chunk_size=64 * 1024):
                if len(body) + len(chunk) > MAX_JSON_BYTES:
                    raise LearnError(
                        "NTULearn JSON exceeded the response limit. Reduce the page size or narrow the request."
                    )
                body.extend(chunk)
        if (
            expected_generation is not None
            and expected_generation != self._auth_generation
        ):
            raise AuthGenerationChanged
        headers = response.headers.copy()
        headers.pop("content-encoding", None)
        headers.pop("content-length", None)
        return httpx.Response(
            response.status_code,
            headers=headers,
            content=bytes(body),
            request=response.request,
        )

    @asynccontextmanager
    async def stream(
        self,
        client: httpx.AsyncClient,
        url: str,
        *,
        expected_generation: int | None = None,
        headers: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
    ) -> AsyncIterator[httpx.Response]:
        host = urlsplit(url).hostname or NTULEARN_HOST
        try:
            if client is self.external_client:
                async with self._external_lock:
                    client.cookies.clear()
                    try:
                        async with self.scheduler.slot(host):
                            async with client.stream(
                                "GET", url, headers=headers
                            ) as response:
                                self._observe_cooldown(host, response)
                                yield response
                    finally:
                        # A vendor response cannot set cookies for another
                        # external request, even when its domain is shared.
                        client.cookies.clear()
            else:
                async with self.scheduler.slot(host):
                    if (
                        expected_generation is not None
                        and expected_generation != self._auth_generation
                    ):
                        raise AuthGenerationChanged
                    async with client.stream(
                        "GET", url, headers=headers, params=params
                    ) as response:
                        self._observe_cooldown(host, response)
                        if (
                            expected_generation is not None
                            and expected_generation != self._auth_generation
                        ):
                            self._restore_auth_cookies()
                            raise AuthGenerationChanged
                        self._snapshot_auth_cookies()
                        yield response
        except httpx.HTTPError:
            raise LearnError(
                "NTULearn connection failed or timed out; retry later."
            ) from None

    def _observe_cooldown(self, host: str, response: httpx.Response) -> None:
        if response.status_code in _RETRYABLE:
            self.scheduler.defer(host, server_cooldown(response))

    async def download_bytes(
        self,
        path: str,
        max_bytes: int,
        *,
        expected_generation: int | None = None,
    ) -> bytes:
        if not allowed_read_path(path) or not path.endswith("/download"):
            raise LearnError("Use a Blackboard attachment download endpoint.")
        url = BASE_URL + path
        for _ in range(4):
            parsed = urlsplit(url)
            if (
                parsed.scheme != "https"
                or parsed.username
                or parsed.password
                or parsed.fragment
            ):
                raise LearnError(
                    "The attachment redirect is not a supported secure download URL."
                )
            host = parsed.hostname or ""
            if parsed.port not in (None, 443) or parsed.netloc.lower() not in {
                host.lower(),
                f"{host.lower()}:443",
            }:
                raise LearnError(
                    "The attachment redirect is not a supported secure download URL."
                )
            if parsed.hostname == NTULEARN_HOST:
                request_client = self.client
                authenticated = True
            else:
                if host.endswith((".blackboard.com", ".blackboardcdn.com")):
                    request_client = self.external_client
                    authenticated = False
                else:
                    raise LearnError(
                        "The file requires an unsupported external download host; open it in NTULearn manually."
                    )

            redirected = False
            for attempt in range(MAX_ATTEMPTS):
                response_status = None
                retry_delay_seconds = None
                redirect = None
                body = bytearray()
                async with self.stream(
                    request_client,
                    url,
                    expected_generation=expected_generation if authenticated else None,
                ) as response:
                    response_status = response.status_code
                    if authenticated and response_status == 401:
                        from .auth import SessionExpired

                        raise SessionExpired
                    if response_status in _RETRYABLE and attempt < MAX_ATTEMPTS - 1:
                        retry_delay_seconds = retry_delay(response, attempt)
                    elif response_status in _REDIRECTS:
                        location = response.headers.get("location", "")
                        redirect = urljoin(url, location) if location else None
                    elif response_status != 200:
                        raise LearnError(
                            f"NTULearn could not download this attachment (HTTP {response_status})."
                        )
                    else:
                        content_type = response.headers.get("content-type", "").lower()
                        if (
                            "text/html" in content_type
                            or "application/json" in content_type
                        ):
                            raise LearnError(
                                "NTULearn returned a login/error page or unsupported HTML/JSON attachment; no file was saved."
                            )
                        length = response.headers.get("content-length")
                        if (
                            length
                            and length.isdigit()
                            and int(length) > min(MAX_FILE_BYTES, max_bytes)
                        ):
                            raise LearnError(
                                "This attachment exceeds the 20 MB file limit or remaining batch limit; no file was saved."
                            )
                        async for chunk in response.aiter_bytes():
                            body.extend(chunk)
                            if len(body) > min(MAX_FILE_BYTES, max_bytes):
                                raise LearnError(
                                    "This attachment exceeds the 20 MB file limit or remaining batch limit; no file was saved."
                                )
                if retry_delay_seconds is not None:
                    await asyncio.sleep(retry_delay_seconds)
                    continue
                if response_status in _REDIRECTS:
                    if redirect is None:
                        raise LearnError(
                            "NTULearn returned too many or incomplete file redirects; no file was saved."
                        )
                    url = redirect
                    redirected = True
                    break
                return bytes(body)
            if not redirected:
                raise LearnError(
                    "NTULearn could not complete the attachment download; retry later."
                )
        raise LearnError(
            "NTULearn returned too many file redirects; no file was saved."
        )

    async def download_kaltura_file(
        self,
        url: str,
        destination: Path,
        max_bytes: int,
        referer: str,
    ) -> int:
        return await _download_kaltura_file(self, url, destination, max_bytes, referer)

    async def aclose(self) -> None:
        await self.client.aclose()
        await self.external_client.aclose()


def server_cooldown(response: httpx.Response) -> float:
    fallback = 1.0 if response.status_code == 429 else -1.0
    return retry_after_seconds(response.headers.get("retry-after"), fallback)


def retry_delay(response: httpx.Response, attempt: int) -> float:
    fallback = 1.0 if response.status_code == 429 else float(2**attempt)
    delay = retry_after_seconds(response.headers.get("retry-after"), fallback)
    if delay > MAX_RETRY_DELAY_SECONDS:
        raise LearnError(
            "NTULearn requested a retry delay longer than one minute; retry this read later."
        )
    return delay


def json_body(response: httpx.Response) -> Any:
    if "application/json" not in response.headers.get("content-type", "").lower():
        raise LearnError(
            "NTULearn returned a non-JSON page instead of academic data; no data was inferred."
        )
    body = response.content
    if len(body) > MAX_JSON_BYTES:
        raise LearnError(
            "NTULearn's response exceeded the 5 MB limit; request a smaller page."
        )
    try:
        return json.loads(body)
    except (ValueError, UnicodeError):
        raise LearnError(
            "NTULearn returned malformed JSON; no data was inferred."
        ) from None
