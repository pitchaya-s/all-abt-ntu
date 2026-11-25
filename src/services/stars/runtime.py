"""Runtime state for public STARS operations."""

from collections.abc import Callable, MutableMapping
from contextlib import contextmanager
from contextvars import ContextVar
from threading import Lock
from typing import Any, TypeVar, cast

import httpx


class StarsResources:
    def __init__(self, client: httpx.Client):
        self.client = client
        self._lock = Lock()
        self._caches: dict[str, tuple[Any, MutableMapping]] = {}

    def cache(self, name: str, factory):
        with self._lock:
            if name not in self._caches:
                self._caches[name] = Lock(), factory()
            return self._caches[name]

    def close(self):
        self.client.close()
        self._caches.clear()


_CURRENT: ContextVar[Callable[[], StarsResources] | None] = ContextVar(
    "stars_resources", default=None
)
_Cache = TypeVar("_Cache", bound=MutableMapping)


@contextmanager
def stars_scope(resources: Callable[[], StarsResources]):
    token = _CURRENT.set(resources)
    try:
        yield
    finally:
        _CURRENT.reset(token)


def current_resources() -> StarsResources | None:
    current = _CURRENT.get()
    return current() if current else None


def scoped_cache(name, default_lock, default_cache: _Cache) -> tuple[Any, _Cache]:
    resources = current_resources()
    if resources is None:
        return default_lock, default_cache
    lock, cache = resources.cache(name, type(default_cache))
    return lock, cast(_Cache, cache)
