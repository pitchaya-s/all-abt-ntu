"""Pooled public HTML requests for STARS data endpoints."""

import atexit
import logging
import time
from concurrent.futures import Future
from threading import BoundedSemaphore, Lock
from urllib.parse import urljoin, urlsplit
from urllib.request import Request

import httpx

from public_http_client import (
    defer_host_requests,
    host_request_slot,
    max_retry_delay,
    public_timeout,
    schedule_host_retry,
)
from shared.http import (
    REDIRECT_STATUS,
    allowed_https_url,
    failed_request_url,
    remaining_time,
    request_budget,
    request_timeout,
    retryable_connection_error,
)
from shared.http import NoCookies as _NoCookies
from ..runtime import current_resources, scoped_cache

USER_AGENT = "all-abt-ntu-mcp/0.1 (NTU timetable lookup)"
REQUEST_TIMEOUT_SECONDS = 20
MAX_RESPONSE_BYTES = 5_000_000
MAX_RETRIES = 2
MIN_REQUEST_INTERVAL_SECONDS = 1.0
MAX_CONCURRENT_REQUESTS = 2
MAX_REDIRECTS = 5
_ALLOWED_HOSTS = frozenset({"wis.ntu.edu.sg", "wish.wis.ntu.edu.sg"})

_READ_FORMS = frozenset(
    {
        "aus_schedule_new.main_display1",
        "aus_subj_cont.main_display1",
        "aus_vacancy.check_vacancy2",
        "exam_timetable_und.mainsubmit",
        "exam_timetable_und.query_page",
        "exam_timetable_und.get_detail",
    }
)


class NTURequestError(RuntimeError):
    pass


def create_public_client() -> httpx.Client:
    client = httpx.Client(
        timeout=httpx.Timeout(REQUEST_TIMEOUT_SECONDS, connect=10.0),
        follow_redirects=False,
        headers={"User-Agent": USER_AGENT, "Accept": "text/html"},
    )
    client.cookies.jar.set_policy(_NoCookies())
    return client


_public_client: httpx.Client | None = None
_client_lock = Lock()


def _request_client() -> httpx.Client:
    resources = current_resources()
    if resources is not None:
        return resources.client
    global _public_client
    with _client_lock:
        if _public_client is None:
            _public_client = create_public_client()
            atexit.register(_public_client.close)
        return _public_client


_request_slots = BoundedSemaphore(MAX_CONCURRENT_REQUESTS)
_pace_lock = Lock()
_last_request_started = 0.0
_inflight_lock = Lock()
_inflight: dict[tuple[object, ...], Future[str]] = {}


def _wait_for_request_slot() -> None:
    global _last_request_started
    with _pace_lock:
        delay = MIN_REQUEST_INTERVAL_SECONDS - (
            time.monotonic() - _last_request_started
        )
        if delay > 0:
            time.sleep(delay)
        _last_request_started = time.monotonic()


def _validate_url(url: str) -> None:
    if not allowed_https_url(url, _ALLOWED_HOSTS):
        raise NTURequestError(
            "NTU returned an unexpected URL or redirect; retrieval stopped."
        )


def _request_html(
    client: httpx.Client,
    request: Request,
    page_description: str,
    attempt: int,
    attempts: int,
):
    current_url = request.full_url
    method = request.get_method()
    content = request.data
    if content is not None and not isinstance(content, (str, bytes)):
        raise NTURequestError(
            f"NTU request body for {page_description} is not a supported encoded form."
        )
    headers = dict(request.header_items())

    for _ in range(MAX_REDIRECTS + 1):
        _validate_url(current_url)
        with _request_slots:
            _wait_for_request_slot()
            with (
                host_request_slot(current_url),
                client.stream(
                    method,
                    current_url,
                    content=content,
                    headers=headers,
                    timeout=request_timeout(public_timeout()),
                ) as response,
            ):
                if response.status_code in REDIRECT_STATUS:
                    location = response.headers.get("location")
                    if not location:
                        raise NTURequestError(
                            f"NTU returned an incomplete redirect for {page_description}."
                        )
                    next_url = urljoin(current_url, location)
                    _validate_url(next_url)
                    if response.status_code in {301, 302, 303} and method not in {
                        "GET",
                        "HEAD",
                    }:
                        method, content = "GET", None
                        headers = {
                            name: value
                            for name, value in headers.items()
                            if name.casefold() not in {"content-length", "content-type"}
                        }
                    current_url = next_url
                    continue

                status = response.status_code
                response_headers = response.headers
                if status >= 400:
                    retry = schedule_host_retry(
                        current_url,
                        response,
                        fallback=min(4.0, 2.0**attempt),
                        may_retry=attempt + 1 < attempts,
                        retry_limit=max_retry_delay(),
                    )
                    return status, response_headers, b"", retry

                content_type = (
                    response_headers.get("content-type", "")
                    .split(";", 1)[0]
                    .strip()
                    .lower()
                )
                if content_type != "text/html":
                    raise NTURequestError(
                        f"NTU returned {content_type!r}; expected HTML for {page_description}."
                    )
                length = response_headers.get("content-length")
                if length and length.isdigit() and int(length) > MAX_RESPONSE_BYTES:
                    raise NTURequestError(
                        f"NTU's {page_description} page exceeded the 5 MB safety limit."
                    )
                body = bytearray()
                for chunk in response.iter_bytes():
                    remaining_time()
                    if len(body) + len(chunk) > MAX_RESPONSE_BYTES:
                        raise NTURequestError(
                            f"NTU's {page_description} page exceeded the 5 MB safety limit."
                        )
                    body.extend(chunk)
                return status, response_headers, bytes(body), False

    raise NTURequestError(
        f"NTU returned too many redirects for {page_description}; retrieval stopped."
    )


def _decode_html(body: bytes, headers: httpx.Headers) -> str:
    charset = None
    for parameter in headers.get("content-type", "").split(";")[1:]:
        name, separator, value = parameter.strip().partition("=")
        if separator and name.casefold() == "charset":
            charset = value.strip().strip("\"'")
            break
    try:
        return body.decode(charset or "windows-1252", errors="replace")
    except LookupError:
        return body.decode("windows-1252", errors="replace")


def _await_inflight(flight: Future[str]) -> str:
    return flight.result(timeout=remaining_time())


def _fetch_html_request(
    request: Request, page_description: str, client: httpx.Client | None = None
) -> str:
    with request_budget():
        return _fetch_shared(request, page_description, client)


def _fetch_shared(request, page_description, client):
    request_client = client or _request_client()
    lock, flights = scoped_cache("http.inflight", _inflight_lock, _inflight)
    key = (
        id(request_client),
        request.get_method(),
        request.full_url,
        request.data,
        page_description,
        tuple(
            sorted((name.casefold(), value) for name, value in request.header_items())
        ),
    )
    with lock:
        flight = flights.get(key)
        owner = flight is None
        if owner:
            flight = Future()
            flights[key] = flight
    if flight is None:
        raise RuntimeError("The STARS request flight was not initialized.")

    if not owner:
        return _await_inflight(flight)

    try:
        result = _fetch_html_request_once(request, page_description, request_client)
    except BaseException as error:
        with lock:
            if flights.get(key) is flight:
                del flights[key]
            flight.set_exception(error)
        raise
    with lock:
        if flights.get(key) is flight:
            del flights[key]
        flight.set_result(result)
    return result


def _fetch_html_request_once(
    request: Request, page_description: str, request_client: httpx.Client
) -> str:
    last_error = "network error"
    path = urlsplit(request.full_url).path.lower().rsplit("/", 1)[-1]
    safe_read = request.get_method() in {"GET", "HEAD"} or path in _READ_FORMS
    attempts = MAX_RETRIES + 1 if safe_read else 1

    for attempt in range(attempts):
        try:
            status, headers, body, retry = _request_html(
                request_client, request, page_description, attempt, attempts
            )
        except httpx.RequestError as error:
            if not retryable_connection_error(error) or attempt + 1 == attempts:
                break
            failure_url = failed_request_url(error, request.full_url)
            defer_host_requests(failure_url, min(4.0, 2.0**attempt))
            continue
        if status < 400:
            return _decode_html(body, headers)
        if status == 429:
            logging.getLogger(__name__).warning("STARS upstream returned HTTP 429")
        last_error = f"HTTP {status}"
        if not retry:
            break

    raise NTURequestError(
        f"Could not retrieve {page_description} from NTU after {attempt + 1} attempt(s): {last_error}."
    )
