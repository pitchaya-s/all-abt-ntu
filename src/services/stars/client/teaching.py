"""One bounded, cached term-wide read for each public undergraduate study mode."""

import time
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor
from contextvars import copy_context
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from threading import Lock

from ..domain.models import Course
from ..parser.common import NTUPageError
from ..parser.schedule import parse_teaching_schedule
from ..runtime import scoped_cache
from .cache import cache_ttl_seconds, CACHE_TTL_SECONDS
from .courses import BASE_URL, _fetch_html
from .http import NTURequestError
from .validation import _academic_term


@dataclass(frozen=True)
class TeachingSnapshot:
    academic_year: int
    semester: str
    courses: tuple[Course, ...]
    retrieved_at: str
    source_url: str = BASE_URL
    cached: bool = False


_lock = Lock()
_cache: OrderedDict[tuple[int, str], tuple[float, TeachingSnapshot]] = OrderedDict()


def get_teaching_snapshot(academic_year, semester, refresh=False):
    ttl = cache_ttl_seconds(CACHE_TTL_SECONDS)
    lock, cache = scoped_cache("teaching.get_teaching_snapshot", _lock, _cache)
    year, term, acadsem = _academic_term(academic_year, semester)
    key = year, term
    with lock:
        cached = cache.get(key)
        if not refresh and ttl and cached and time.monotonic() - cached[0] < ttl:
            cache.move_to_end(key)
            return replace(cached[1], cached=True)
        retrieved = datetime.now(timezone.utc).isoformat(timespec="seconds")
        with ThreadPoolExecutor(
            max_workers=2, thread_name_prefix="ntu-teaching"
        ) as pool:
            pages = [
                pool.submit(
                    copy_context().run, _fetch_html, acadsem, "", study_mode=mode
                )
                for mode in ("F", "P")
            ]
            html_pages = [future.result()[0] for future in pages]
        courses = []
        for html in html_pages:
            try:
                courses.extend(parse_teaching_schedule(html, year, term))
            except NTUPageError as error:
                raise NTURequestError(
                    f"Could not safely read the complete teaching schedule: {error}"
                ) from None
        if not courses:
            raise NTURequestError(
                "NTU has no published undergraduate teaching schedules for this term; no room availability was inferred."
            )
        result = TeachingSnapshot(year, term, tuple(courses), retrieved)
        if ttl:
            cache[key] = time.monotonic(), result
            cache.move_to_end(key)
            while len(cache) > 4:
                cache.popitem(last=False)
        return result
