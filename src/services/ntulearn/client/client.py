"""Typed academic reads using the authenticated user's own Blackboard permissions."""

import asyncio
import re
from datetime import datetime, timedelta, timezone
from functools import partial
from typing import Annotated

from pydantic import Field

from ..contracts import CourseReference, ID, LearnID, Offset, PageSize

from ..models import (
    Announcement,
    Announcements,
    Attachment,
    Attachments,
    Calendar,
    CalendarItem,
    Content,
    Contents,
    Download,
    Course,
    Courses,
    Grade,
    Gradebook,
    GradeColumn,
    LearnError,
)
from ..parser.response import records, required, text
from .session import Session

PREFIX = "/learn/api/public/v1"
_COURSE_CODE = re.compile(
    r"(?<![A-Za-z0-9])[A-Za-z]{2,4}[0-9]{4}[A-Za-z]?(?![A-Za-z0-9])"
)
_MAX_COURSE_PAGES = 20


def identifier(value):
    if not isinstance(value, str) or not re.fullmatch(ID, value):
        raise LearnError(
            "Use an NTULearn ID returned by another tool; slashes, URLs, and query strings are not allowed."
        )
    return value


def is_course_code(value: str) -> bool:
    return _COURSE_CODE.search(value) is not None


async def resolve_course_references(client, references, *, refresh=False, call=None):
    """Resolve codes against all pages of the authenticated enrollment list."""
    references = dict.fromkeys(identifier(value) for value in references)
    codes = {value: value.casefold() for value in references if is_course_code(value)}
    if not codes:
        return list(references)

    read_page = (
        client.list_courses if call is None else partial(call, client.list_courses)
    )
    matches: dict[str, set[str]] = {code: set() for code in codes.values()}
    exact_ids = set()
    offset = 0
    async with client.session.operation():
        generation = None
        for _ in range(_MAX_COURSE_PAGES):
            page = await read_page(limit=100, offset=offset, refresh=refresh)
            current_generation = client.session.auth.generation
            if generation is not None and generation != current_generation:
                raise LearnError(
                    "NTULearn authentication changed during course lookup. Retry the request."
                )
            generation = current_generation
            for course in page.courses:
                if course.id in references:
                    exact_ids.add(course.id)
                if course.organization is True or not course.course_code:
                    continue
                published = course.course_code.strip()
                aliases = {published.casefold()}
                aliases.update(
                    code.casefold() for code in _COURSE_CODE.findall(published)
                )
                for code in matches.keys() & aliases:
                    matches[code].add(identifier(course.id))
            if page.next_offset is None:
                break
            offset = page.next_offset
        else:
            raise LearnError(
                "NTULearn course lookup reached its page limit. Use a Blackboard course ID from the course list."
            )

    resolved = []
    for reference in references:
        if reference in exact_ids or reference not in codes:
            resolved.append(reference)
            continue
        candidates = matches[codes[reference]]
        if not candidates:
            raise LearnError(
                f"No enrolled NTULearn course matches {reference}. Check the code in the course list or use its Blackboard course ID."
            )
        if len(candidates) != 1:
            raise LearnError(
                f"More than one enrolled NTULearn course matches {reference}. Choose its Blackboard course ID from the course list."
            )
        resolved.append(next(iter(candidates)))
    return list(dict.fromkeys(resolved))


def page_parameters(limit, offset):
    if (
        type(limit) is not int
        or not 1 <= limit <= 100
        or type(offset) is not int
        or offset < 0
    ):
        raise LearnError(
            "limit must be 1–100 and offset must be a nonnegative integer."
        )
    return {"limit": limit, "offset": offset}


def mapping(item, key):
    value = item.get(key) or {}
    if not isinstance(value, dict):
        raise LearnError("NTULearn returned an unfamiliar nested academic field.")
    return value


def model(cls, **values):
    try:
        return cls(**values)
    except ValueError:
        raise LearnError(
            "NTULearn returned an unexpected academic-data format; no values were inferred."
        ) from None


class LearnClient:
    def __init__(self, session: Session):
        self.session = session
        self._user_id: str | None = None
        self._user_id_generation: int | None = None
        self._user_id_lock = asyncio.Lock()

    async def _own_user_id(self) -> str:
        generation = self.session.auth.generation
        if self._user_id is not None and self._user_id_generation == generation:
            return self._user_id
        async with self._user_id_lock:
            generation = self.session.auth.generation
            if self._user_id is not None and self._user_id_generation == generation:
                return self._user_id
            for attempt in range(2):
                generation = self.session.auth.generation
                user, _ = await self.session.get(
                    PREFIX + "/users/me", refresh=bool(attempt)
                )
                user_id = identifier(required(user, "id"))
                current_generation = self.session.auth.generation
                if generation == current_generation:
                    self._user_id = user_id
                    self._user_id_generation = current_generation
                    return user_id
            raise LearnError(
                "NTULearn authentication changed while identifying the current user; retry the request."
            )

    async def list_records(self, path, limit, offset, refresh=False, **params):
        data, freshness = await self.session.get(
            path, {**page_parameters(limit, offset), **params}, refresh
        )
        rows, next_offset = records(data, path)
        if data.get("courseErrors"):
            raise LearnError(
                "NTULearn reported errors for part of this request; narrow the calendar window or select a single course."
            )
        if next_offset is not None and next_offset <= offset:
            raise LearnError(
                "NTULearn returned a pagination loop; no further pages were followed."
            )
        return rows, next_offset, freshness

    async def list_courses(
        self, limit: PageSize = 50, offset: Offset = 0, refresh: bool = False
    ) -> Courses:
        "List your enrolled NTULearn courses and organizations, including published availability and course IDs."
        rows, next_offset, freshness = await self.list_records(
            PREFIX + "/users/me/courses", limit, offset, refresh, expand="course"
        )
        courses = []
        for row in rows:
            course = mapping(row, "course")
            courses.append(
                model(
                    Course,
                    id=required(course, "id"),
                    name=required(course, "name"),
                    course_code=course.get("courseId"),
                    available=mapping(course, "availability").get("available"),
                    role=row.get("courseRoleId"),
                    organization=course.get("organization"),
                )
            )
        return model(
            Courses,
            courses=courses,
            offset=offset,
            next_offset=next_offset,
            **freshness,
        )

    async def resolve_course_id(
        self, course_id: CourseReference, refresh: bool = False
    ) -> str:
        return (await resolve_course_references(self, [course_id], refresh=refresh))[0]

    async def get_course_contents(
        self,
        course_id: CourseReference,
        parent_id: LearnID | None = None,
        limit: PageSize = 50,
        offset: Offset = 0,
        refresh: bool = False,
    ) -> Contents:
        "Read one level of course content. Omit parent_id for the root; use an item's ID to open a folder. HTML body/description are returned as text."
        parent_id = identifier(parent_id) if parent_id is not None else None
        course_id = await self.resolve_course_id(course_id, refresh)
        path = f"{PREFIX}/courses/{course_id}/contents"
        if parent_id is not None:
            path += f"/{parent_id}/children"
        rows, next_offset, freshness = await self.list_records(
            path, limit, offset, refresh
        )
        contents = [
            model(
                Content,
                id=required(row, "id"),
                title=required(row, "title"),
                parent_id=row.get("parentId"),
                has_children=row.get("hasChildren"),
                type=mapping(row, "contentHandler").get("id"),
                body=text(row.get("body")),
                description=text(row.get("description")),
                modified=row.get("modified"),
            )
            for row in rows
        ]
        return model(
            Contents,
            course_id=course_id,
            contents=contents,
            offset=offset,
            next_offset=next_offset,
            **freshness,
        )

    async def get_content_record(self, course_id, content_id):
        """Return a fresh content record for internal parsing of supported embeds."""
        course_id, content_id = identifier(course_id), identifier(content_id)
        data, _ = await self.session.get(
            f"{PREFIX}/courses/{course_id}/contents/{content_id}", refresh=True
        )
        if not isinstance(data, dict) or data.get("id") not in (None, content_id):
            raise LearnError("NTULearn returned an unfamiliar course content record.")
        return data

    async def get_announcements(
        self,
        course_id: CourseReference,
        limit: PageSize = 50,
        offset: Offset = 0,
        refresh: bool = False,
    ) -> Announcements:
        "Read published announcements for one enrolled course. An empty list is distinct from denied access."
        course_id = await self.resolve_course_id(course_id, refresh)
        rows, next_offset, freshness = await self.list_records(
            f"{PREFIX}/courses/{course_id}/announcements", limit, offset, refresh
        )
        announcements = [
            model(
                Announcement,
                id=required(row, "id"),
                title=required(row, "title"),
                body=text(row.get("body")),
                created=row.get("created"),
                modified=row.get("modified"),
            )
            for row in rows
        ]
        return model(
            Announcements,
            course_id=course_id,
            announcements=announcements,
            offset=offset,
            next_offset=next_offset,
            **freshness,
        )

    async def get_calendar(
        self,
        since: datetime | None = None,
        until: datetime | None = None,
        course_id: CourseReference | None = None,
        limit: PageSize = 50,
        offset: Offset = 0,
        refresh: bool = False,
    ) -> Calendar:
        "Read calendar entries and published deadlines, across your courses or for one course. Defaults to the next 14 days. Supply timezone-aware timestamps and a window no longer than 112 days."
        since = since or datetime.now(timezone.utc)
        until = until or since + timedelta(days=14)
        if (
            since.tzinfo is None
            or until.tzinfo is None
            or not timedelta(0) < until - since <= timedelta(days=112)
        ):
            raise LearnError(
                "Use timezone-aware calendar times with an end after the start and a window of at most 112 days."
            )
        params = {"since": since.isoformat(), "until": until.isoformat()}
        if course_id is not None:
            params["courseId"] = await self.resolve_course_id(course_id, refresh)
        rows, next_offset, freshness = await self.list_records(
            PREFIX + "/calendars/items", limit, offset, refresh, **params
        )
        items = [
            model(
                CalendarItem,
                id=required(row, "id"),
                title=required(row, "title"),
                type=row.get("type"),
                calendar_name=row.get("calendarName"),
                course_id=mapping(row, "dynamicCalendarItemProps").get("courseId"),
                start=row.get("start"),
                end=row.get("end"),
                description=text(row.get("description")),
                location=row.get("location"),
            )
            for row in rows
        ]
        return model(
            Calendar,
            since=since,
            until=until,
            items=items,
            offset=offset,
            next_offset=next_offset,
            **freshness,
        )

    async def get_gradebook(
        self,
        course_id: CourseReference,
        limit: PageSize = 50,
        offset: Offset = 0,
        grades_offset: Offset = 0,
        refresh: bool = False,
    ) -> Gradebook:
        "Read visible gradebook columns and your own scores/status. Missing scores remain null. Columns and grades paginate independently with offset and grades_offset."
        async with self.session.operation():
            course_id = await self.resolve_course_id(course_id, refresh)
            columns_result, user_id_result = await asyncio.gather(
                self.list_records(
                    f"{PREFIX}/courses/{course_id}/gradebook/columns",
                    limit,
                    offset,
                    refresh,
                ),
                self._own_user_id(),
            )
            columns, next_offset, freshness = columns_result
            user_id = user_id_result
            grades, grades_next_offset, grade_freshness = await self.list_records(
                f"{PREFIX}/courses/{course_id}/gradebook/users/{user_id}",
                limit,
                grades_offset,
                refresh,
            )
            columns = [
                model(
                    GradeColumn,
                    id=required(row, "id"),
                    name=required(row, "name"),
                    possible_score=mapping(row, "score").get("possible"),
                    due=mapping(row, "grading").get("due"),
                    available=mapping(row, "availability").get("available"),
                    content_id=row.get("contentId"),
                )
                for row in columns
            ]
            grades = [
                model(
                    Grade,
                    column_id=required(row, "columnId"),
                    score=row.get("score"),
                    text=row.get("text"),
                    status=row.get("status") or row.get("gradingStatus"),
                    exempt=row.get("exempt"),
                    feedback=text(row.get("feedback")),
                    modified=row.get("modified") or row.get("lastGraded"),
                )
                for row in grades
            ]
            freshness = {
                "retrieved_at": min(
                    freshness["retrieved_at"], grade_freshness["retrieved_at"]
                ),
                "from_cache": freshness["from_cache"] and grade_freshness["from_cache"],
                "cache_age_seconds": max(
                    freshness["cache_age_seconds"], grade_freshness["cache_age_seconds"]
                ),
            }
            return model(
                Gradebook,
                course_id=course_id,
                columns=columns,
                grades=grades,
                offset=offset,
                grades_offset=grades_offset,
                next_offset=next_offset,
                grades_next_offset=grades_next_offset,
                **freshness,
            )

    async def get_content_attachments(
        self,
        course_id: CourseReference,
        content_id: LearnID,
        limit: PageSize = 50,
        offset: Offset = 0,
        refresh: bool = False,
    ) -> Attachments:
        "List files attached to a course content item. Use a leaf content ID rather than a folder. Some external/LTI content has no downloadable Blackboard attachment."
        content_id = identifier(content_id)
        course_id = await self.resolve_course_id(course_id, refresh)
        rows, next_offset, freshness = await self.list_records(
            f"{PREFIX}/courses/{course_id}/contents/{content_id}/attachments",
            limit,
            offset,
            refresh,
        )
        attachments = [
            model(
                Attachment,
                id=required(row, "id"),
                file_name=required(row, "fileName"),
                mime_type=row.get("mimeType"),
            )
            for row in rows
        ]
        return model(
            Attachments,
            course_id=course_id,
            content_id=content_id,
            attachments=attachments,
            offset=offset,
            next_offset=next_offset,
            **freshness,
        )

    async def download_file(
        self,
        course_id: CourseReference,
        content_id: LearnID,
        attachment_id: LearnID,
        destination: str,
        max_bytes: Annotated[int, Field(ge=1, le=20000000, strict=True)] = 20000000,
    ) -> Download:
        "Download a Blackboard attachment to an explicit local file path, up to 20 MB. Never overwrites an existing file. Does not modify NTULearn or forward university cookies to file-delivery hosts."
        content_id, attachment_id = identifier(content_id), identifier(attachment_id)
        course_id = await self.resolve_course_id(course_id)
        path = f"{PREFIX}/courses/{course_id}/contents/{content_id}/attachments/{attachment_id}/download"
        return await self.session.download(path, destination, max_bytes=max_bytes)
