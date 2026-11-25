"""Public course-code/title search, with cached results shared across pages."""

from copy import deepcopy
from datetime import datetime, timezone
import re
from threading import Lock
import time
from typing import Literal

from ..runtime import scoped_cache
from .cache import cache_ttl_seconds, CACHE_TTL_SECONDS, MAX_CACHE_ENTRIES
from .courses import _fetch_html
from .http import NTURequestError
from .validation import _academic_term
from ..parser.search import parse_course_search
from ..parser.common import NTUPageError
from ..schemas import SearchCoursesResult


_cache_lock = Lock()
_cache: dict[tuple[int, str, str, str], tuple[float, SearchCoursesResult]] = {}


def search_courses(
    query: str,
    academic_year: int,
    semester: int | str,
    study_mode: Literal["full_time", "part_time"] = "full_time",
    limit: int = 20,
    offset: int = 0,
) -> SearchCoursesResult:
    ttl = cache_ttl_seconds(CACHE_TTL_SECONDS)
    lock, cache = scoped_cache("search.search_courses", _cache_lock, _cache)
    query = " ".join(query.split()).upper()
    if not 2 <= len(query) <= 80 or not re.fullmatch(
        r"[A-Z0-9][A-Z0-9 &'()+,./:-]*", query
    ):
        raise ValueError(
            "Search query must be 2–80 characters, starting with a letter or digit; use course codes or title words without wildcards."
        )
    if study_mode not in {"full_time", "part_time"}:
        raise ValueError("Study mode must be full_time or part_time.")
    if (
        type(limit) is not int
        or not 1 <= limit <= 100
        or type(offset) is not int
        or offset < 0
    ):
        raise ValueError(
            "Search limit must be 1–100 and offset must be a nonnegative integer."
        )
    year, term, acadsem = _academic_term(academic_year, semester)
    key = (year, term, query, study_mode)
    result = None
    if ttl:
        with lock:
            cached = cache.get(key)
            if cached and time.monotonic() - cached[0] < ttl:
                result = deepcopy(cached[1])
    if result is None:
        html, source = _fetch_html(
            acadsem, query, study_mode="F" if study_mode == "full_time" else "P"
        )
        try:
            courses = parse_course_search(html, year, term)
        except NTUPageError as error:
            raise NTURequestError(
                f"Could not safely parse NTU's course search: {error}"
            ) from error
        result = {
            "query": query,
            "academic_year": year,
            "semester": term,
            "study_mode": study_mode,
            "total_count": len(courses),
            "offset": 0,
            "has_more": False,
            "courses": courses,
            "source_url": source,
            "retrieved_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        }
        if ttl:
            with lock:
                now = time.monotonic()
                for expired in [
                    k for k, (created, _) in cache.items() if now - created >= ttl
                ]:
                    del cache[expired]
                if key not in cache and len(cache) >= MAX_CACHE_ENTRIES:
                    del cache[min(cache, key=lambda k: cache[k][0])]
                cache[key] = (now, deepcopy(result))
    return {
        **result,
        "courses": result["courses"][offset : offset + limit],
        "offset": offset,
        "has_more": offset + limit < result["total_count"],
    }
