"""Bounded public HTTP transport for Omnibus."""

import logging
from urllib.parse import urljoin

import httpx

from public_http_client import (
    defer_host_requests,
    host_request_slot,
    max_retry_delay,
    public_timeout,
)
from shared.http import (
    REDIRECT_STATUS,
    TRANSIENT_STATUS,
    allowed_https_url,
    failed_request_url,
    remaining_time,
    request_budget,
    request_timeout,
    retry_after_seconds,
    retryable_connection_error,
)
from ..models import OmnibusError
from .constants import (
    _ALLOWED_HOSTS,
    _MAX_ATTEMPTS,
    _MAX_REDIRECTS,
    _MAX_RESPONSE_BYTES,
)


class HTTPMethods:
    def _read(self, url, *, body=None, headers=None, safe_read=False):
        with request_budget():
            return self._request(url, body, headers, safe_read or body is None)

    def _request(self, url, body, headers, retryable):
        self._validate_url(url, redirect=False)
        if self._closed:
            raise OmnibusError(
                "The NTU Omnibus HTTP client is closed; restart the MCP server."
            )
        request_headers = {
            "OutSystems-client-env": "browser",
        }
        if headers:
            request_headers.update(headers)
        method = "POST" if body is not None else "GET"
        attempts = _MAX_ATTEMPTS if retryable else 1
        for attempt in range(attempts):
            try:
                status, payload, response_headers, response_url = self._request_chain(
                    url, method, body, request_headers
                )
            except httpx.RequestError as error:
                if attempt + 1 < attempts and retryable_connection_error(error):
                    failure_url = failed_request_url(error, url)
                    defer_host_requests(failure_url, min(4.0, 2.0**attempt))
                    continue
                raise OmnibusError(
                    "Could not reach NTU Omnibus; try again later."
                ) from None
            except httpx.HTTPError:
                raise OmnibusError(
                    "NTU Omnibus returned an invalid HTTP response; retrieval stopped."
                ) from None

            if status == 429:
                logging.getLogger(__name__).warning(
                    "NTU Omnibus upstream returned HTTP 429"
                )
            if status in TRANSIENT_STATUS:
                advertised = response_headers.get("retry-after")
                delay = retry_after_seconds(advertised, min(4.0, 2.0**attempt))
                retry = attempt + 1 < attempts and delay <= max_retry_delay()
                if retry or advertised or status == 429:
                    defer_host_requests(response_url, delay)
                if retry:
                    continue
            if status >= 400:
                return status, payload
            return payload
        raise OmnibusError(
            "Could not reach NTU Omnibus after two attempts; try again later."
        )

    @staticmethod
    def _validate_url(url, *, redirect=True):
        if not allowed_https_url(url, _ALLOWED_HOSTS):
            message = (
                "NTU Omnibus returned an unexpected redirect; retrieval stopped."
                if redirect
                else ("NTU Omnibus returned an unexpected URL; retrieval stopped.")
            )
            raise OmnibusError(message)

    def _request_chain(self, url, method, body, headers):
        current_url = url
        for _ in range(_MAX_REDIRECTS + 1):
            self._validate_url(current_url)
            with (
                host_request_slot(current_url),
                self._http.stream(
                    method,
                    current_url,
                    content=body,
                    headers=headers,
                    timeout=request_timeout(public_timeout()),
                ) as response,
            ):
                response_url = str(response.url)
                self._validate_url(response_url)
                if response.status_code in REDIRECT_STATUS:
                    location = response.headers.get("location")
                    if not location:
                        raise OmnibusError(
                            "NTU Omnibus returned an incomplete redirect; retrieval stopped."
                        )
                    current_url = urljoin(current_url, location)
                    self._validate_url(current_url)
                    if response.status_code in {301, 302, 303} and method not in {
                        "GET",
                        "HEAD",
                    }:
                        method, body = "GET", None
                        headers = {
                            name: value
                            for name, value in headers.items()
                            if name.casefold() not in {"content-length", "content-type"}
                        }
                    continue

                payload = bytearray()
                for chunk in response.iter_bytes():
                    remaining_time()
                    if len(payload) + len(chunk) > _MAX_RESPONSE_BYTES:
                        raise OmnibusError(
                            "NTU Omnibus response exceeded the 8 MB limit."
                        )
                    payload.extend(chunk)
                return (
                    response.status_code,
                    bytes(payload),
                    response.headers,
                    response_url,
                )
        raise OmnibusError(
            "NTU Omnibus returned too many redirects; retrieval stopped."
        )

    def close(self):
        with self._lock:
            if self._closed:
                return
            self._closed = True
            self._http.close()
            self._finalizer.detach()
        self._lta.http.close()

    def _get_bytes(self, url):
        response = self._read(url)
        if isinstance(response, tuple):
            code, _ = response
            raise OmnibusError(
                f"NTU Omnibus returned HTTP {code} while loading public app data."
            )
        return response
