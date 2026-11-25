"""Bounded in-memory cache for validated NTULearn JSON responses."""

import time
from collections import OrderedDict
from copy import deepcopy
from typing import Any


class ResponseCache:
    def __init__(
        self, ttl_seconds: int, max_entries: int = 128, max_bytes: int = 16_000_000
    ):
        self.ttl_seconds = ttl_seconds
        self.max_entries = max_entries
        self.max_bytes = max_bytes
        self._bytes = 0
        self._entries: OrderedDict[tuple, tuple[float, Any, Any, int]] = OrderedDict()

    def get(self, key: tuple, *, refresh: bool = False):
        if refresh or not self.ttl_seconds:
            return None
        entry = self._entries.get(key)
        if entry is None:
            return None
        created, data, retrieved_at, size = entry
        age = time.monotonic() - created
        if age >= self.ttl_seconds:
            del self._entries[key]
            self._bytes -= size
            return None
        self._entries.move_to_end(key)
        return deepcopy(data), {
            "retrieved_at": retrieved_at,
            "from_cache": True,
            "cache_age_seconds": int(age),
        }

    def put(self, key: tuple, data: Any, retrieved_at: Any, *, size: int) -> None:
        if not self.ttl_seconds:
            return
        previous = self._entries.pop(key, None)
        if previous is not None:
            self._bytes -= previous[3]
        if size > self.max_bytes:
            return
        self._entries[key] = (time.monotonic(), deepcopy(data), retrieved_at, size)
        self._bytes += size
        self._entries.move_to_end(key)
        while len(self._entries) > self.max_entries or self._bytes > self.max_bytes:
            _, entry = self._entries.popitem(last=False)
            self._bytes -= entry[3]

    def clear(self) -> None:
        self._entries.clear()
        self._bytes = 0
