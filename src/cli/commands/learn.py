"""Learn service commands."""

from typing import Literal, Optional

from functools import partial
import re
from urllib.parse import parse_qs, unquote, urlsplit

import typer

from ..helpers import group, local_datetime, parse_json
from ..execution import application_scope
from ..services import invoke

app = typer.Typer(no_args_is_help=True)
g_auth = group(default=False)
app.add_typer(g_auth, name="auth")
g_content = group(default=True)
app.add_typer(g_content, name="content")
g_courses = group(default=True)
app.add_typer(g_courses, name="courses")
g_files = group(default=False)
app.add_typer(g_files, name="files")
g_groups = group(default=True)
app.add_typer(g_groups, name="groups")
g_messages = group(default=False)
app.add_typer(g_messages, name="messages")
g_search = group(default=True)
app.add_typer(g_search, name="search")
g_videos = group(default=False)
app.add_typer(g_videos, name="videos")


def is_content_url(value: str) -> bool:
    return "://" in value or value.lower().startswith("ntulearn.ntu.edu.sg/")


def content_reference(course_or_url: str, content_id: Optional[str]) -> tuple[str, str]:
    """Resolve an NTULearn content URL or an explicit course and content ID."""
    candidate = (
        content_id if content_id and is_content_url(content_id) else course_or_url
    )
    if not is_content_url(candidate):
        if content_id is None:
            raise typer.BadParameter("Provide a content ID or an NTULearn content URL.")
        return course_or_url, content_id
    if candidate == course_or_url and content_id is not None:
        raise typer.BadParameter(
            "Provide either a content URL or a course and content ID."
        )
    try:
        url = urlsplit(candidate if "://" in candidate else "https://" + candidate)
        if (
            url.scheme != "https"
            or url.hostname != "ntulearn.ntu.edu.sg"
            or url.port not in (None, 443)
            or url.username is not None
            or url.password is not None
        ):
            raise ValueError
        match = re.fullmatch(
            r"/ultra/courses/([A-Za-z0-9_-]{1,80})/(document|lti/launchFrame)(?:/([A-Za-z0-9_-]{1,80}))?/?",
            url.path,
        )
        if not match:
            raise ValueError
        course, kind, item = match.groups()
        if kind == "document":
            if not item:
                raise ValueError
        else:
            if item:
                raise ValueError
            links = parse_qs(url.query).get("toolHref", [])
            if len(links) != 1:
                raise ValueError
            nested = urlsplit(unquote(re.sub(r"~([0-9a-fA-F]{2})", r"%\1", links[0])))
            if (
                nested.scheme != "https"
                or nested.hostname != "ntulearn.ntu.edu.sg"
                or nested.port not in (None, 443)
                or nested.username is not None
                or nested.password is not None
                or nested.path != "/webapps/blackboard/execute/blti/launchPlacement"
            ):
                raise ValueError
            params = parse_qs(nested.query)
            courses, items = params.get("course_id", []), params.get("content_id", [])
            if len(courses) != 1 or courses[0] != course or len(items) != 1:
                raise ValueError
            item = items[0]
            if not re.fullmatch(r"[A-Za-z0-9_-]{1,80}", item):
                raise ValueError
        if candidate == content_id and course_or_url != course:
            raise typer.BadParameter(
                "The URL's course ID does not match the supplied course ID."
            )
        return course, item
    except ValueError:
        raise typer.BadParameter(
            "Provide a valid NTULearn document or lecture launch URL."
        ) from None


@g_auth.command("status")
def cmd_auth_status(json_output: bool = typer.Option(False, "--json", "-j")):
    """Report credential configuration and this process's last verified login, without logging in."""
    with application_scope() as application:
        return invoke(application.learn_session.status, {}, json_output)


@g_courses.command("__default__", hidden=True)
def cmd_courses_default(
    limit: int = typer.Option(50, "--limit", "-l"),
    offset: int = 0,
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """List your enrolled NTULearn courses and organizations, including published availability and course IDs."""
    with application_scope() as application:
        return invoke(
            application.learn.list_courses,
            {"limit": limit, "offset": offset, "refresh": refresh},
            json_output,
        )


@g_content.command("__default__", hidden=True)
def cmd_content_default(
    course_id: str,
    parent_id: Optional[str] = typer.Option(None, "--parent"),
    limit: int = typer.Option(50, "--limit", "-l"),
    offset: int = 0,
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Read one level of course content."""
    if parent_id and is_content_url(parent_id):
        _, parent_id = content_reference(course_id, parent_id)
    with application_scope() as application:
        return invoke(
            application.learn.get_course_contents,
            {
                "course_id": course_id,
                "parent_id": parent_id,
                "limit": limit,
                "offset": offset,
                "refresh": refresh,
            },
            json_output,
        )


@g_content.command("tree")
def cmd_content_tree(
    course_id: str,
    max_depth: int = 5,
    max_nodes: int = 1000,
    max_requests: int = 100,
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Read a course's nested content tree."""
    with application_scope() as application:
        from ntulearn.services import content

        return invoke(
            partial(content.get_content_tree, application.learn),
            {
                "course_id": course_id,
                "max_depth": max_depth,
                "max_nodes": max_nodes,
                "max_requests": max_requests,
                "refresh": refresh,
            },
            json_output,
        )


@app.command("attachments")
def cmd_attachments(
    course_id: str = typer.Argument(..., metavar="COURSE_ID_OR_URL"),
    content_id: Optional[str] = typer.Argument(None),
    limit: int = typer.Option(50, "--limit", "-l"),
    offset: int = 0,
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """List attachments using a course and content ID, or an NTULearn content URL."""
    course_id, content_id = content_reference(course_id, content_id)
    with application_scope() as application:
        return invoke(
            application.learn.get_content_attachments,
            {
                "course_id": course_id,
                "content_id": content_id,
                "limit": limit,
                "offset": offset,
                "refresh": refresh,
            },
            json_output,
        )


@g_files.command("read")
def cmd_files_read(
    course_id: str = typer.Argument(..., metavar="COURSE_ID_OR_URL"),
    content_id: str = typer.Argument(..., metavar="CONTENT_OR_ATTACHMENT_ID"),
    attachment_id: Optional[str] = typer.Argument(None),
    max_chars: int = 20000,
    max_pages: int = 20,
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Read an attachment as text. Supply course and content IDs, or a content URL, plus the attachment ID."""
    if attachment_id is None:
        attachment_id = content_id
        course_id, content_id = content_reference(course_id, None)
    else:
        course_id, content_id = content_reference(course_id, content_id)
    with application_scope() as application:
        from ntulearn.services import files

        return invoke(
            partial(files.read_file_content, application.learn),
            {
                "course_id": course_id,
                "content_id": content_id,
                "attachment_id": attachment_id,
                "max_chars": max_chars,
                "max_pages": max_pages,
            },
            json_output,
        )


@g_files.command("download")
def cmd_files_download(
    course_id: str = typer.Argument(..., metavar="COURSE_ID_OR_URL"),
    content_id: str = typer.Argument(..., metavar="CONTENT_OR_ATTACHMENT_ID"),
    attachment_id: Optional[str] = typer.Argument(None),
    destination: str = typer.Option(..., "--output", "-o"),
    max_bytes: int = typer.Option(
        20_000_000, help="Maximum file size in bytes (up to 20 MB)."
    ),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Download an attachment using course and content IDs, or a content URL, plus the attachment ID."""
    if attachment_id is None:
        attachment_id = content_id
        course_id, content_id = content_reference(course_id, None)
    else:
        course_id, content_id = content_reference(course_id, content_id)
    with application_scope() as application:
        return invoke(
            application.learn.download_file,
            {
                "course_id": course_id,
                "content_id": content_id,
                "attachment_id": attachment_id,
                "destination": destination,
                "max_bytes": max_bytes,
            },
            json_output,
            side_effect=True,
        )


@g_videos.command("download")
def cmd_videos_download(
    course_id: str = typer.Argument(..., metavar="COURSE_ID_OR_URL"),
    content_id: Optional[str] = typer.Argument(None),
    destination: str = typer.Option(..., "--output", "-o"),
    max_mb: int = 1000,
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Download a Kaltura video using course and content IDs, or an NTULearn content URL."""
    course_id, content_id = content_reference(course_id, content_id)
    with application_scope() as application:
        from ntulearn.services import videos

        return invoke(
            partial(videos.download_video, application.learn),
            {
                "course_id": course_id,
                "content_id": content_id,
                "destination": destination,
                "max_mb": max_mb,
            },
            json_output,
            side_effect=True,
        )


@g_courses.command("download")
def cmd_courses_download(
    course_id: str,
    destination: str = typer.Option(..., "--output", "-o"),
    max_depth: int = 5,
    max_nodes: int = 1000,
    max_files: int = 100,
    max_total_mb: int = 200,
    max_requests: int = 200,
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Recursively save readable Blackboard attachments under destination/course_id with content folder names and stable file IDs."""
    with application_scope() as application:
        from ntulearn.services import files

        return invoke(
            partial(files.download_course, application.learn),
            {
                "course_id": course_id,
                "destination": destination,
                "max_depth": max_depth,
                "max_nodes": max_nodes,
                "max_files": max_files,
                "max_total_mb": max_total_mb,
                "max_requests": max_requests,
                "refresh": refresh,
            },
            json_output,
            side_effect=True,
        )


@app.command("announcements")
def cmd_announcements(
    course_id: str,
    limit: int = typer.Option(50, "--limit", "-l"),
    offset: int = 0,
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Read published announcements for one enrolled course."""
    with application_scope() as application:
        return invoke(
            application.learn.get_announcements,
            {
                "course_id": course_id,
                "limit": limit,
                "offset": offset,
                "refresh": refresh,
            },
            json_output,
        )


@app.command("grades")
def cmd_grades(
    course_id: str,
    limit: int = typer.Option(50, "--limit", "-l"),
    offset: int = 0,
    grades_offset: int = 0,
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Read visible gradebook columns and your own scores/status."""
    with application_scope() as application:
        return invoke(
            application.learn.get_gradebook,
            {
                "course_id": course_id,
                "limit": limit,
                "offset": offset,
                "grades_offset": grades_offset,
                "refresh": refresh,
            },
            json_output,
        )


@app.command("calendar")
def cmd_calendar(
    since: Optional[str] = None,
    until: Optional[str] = None,
    course_id: Optional[str] = typer.Option(None, "--course"),
    limit: int = typer.Option(50, "--limit", "-l"),
    offset: int = 0,
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Read calendar entries and published deadlines, across your courses or for one course."""
    with application_scope() as application:
        return invoke(
            application.learn.get_calendar,
            {
                "since": local_datetime(since),
                "until": local_datetime(until),
                "course_id": course_id,
                "limit": limit,
                "offset": offset,
                "refresh": refresh,
            },
            json_output,
        )


@app.command("upcoming")
def cmd_upcoming(
    since: Optional[str] = None,
    until: Optional[str] = None,
    course_ids: Optional[str] = typer.Option(None, "--course-ids", help="JSON value."),
    item_type: Optional[str] = None,
    max_requests: int = 100,
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Collect all calendar pages across your enrolled courses."""
    with application_scope() as application:
        from ntulearn.services import overview

        return invoke(
            partial(overview.get_upcoming, application.learn),
            {
                "since": local_datetime(since),
                "until": local_datetime(until),
                "course_ids": (
                    parse_json(course_ids) if course_ids is not None else None
                ),
                "item_type": item_type,
                "max_requests": max_requests,
                "refresh": refresh,
            },
            json_output,
        )


@app.command("digest")
def cmd_digest(
    since: Optional[str] = None,
    until: Optional[str] = None,
    course_ids: Optional[str] = typer.Option(None, "--course-ids", help="JSON value."),
    max_items: int = 200,
    max_requests: int = 100,
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Digest of recent announcements, upcoming calendar items and your gradebook across courses."""
    with application_scope() as application:
        from ntulearn.services import overview

        return invoke(
            partial(overview.whats_new, application.learn),
            {
                "since": local_datetime(since),
                "until": local_datetime(until),
                "course_ids": (
                    parse_json(course_ids) if course_ids is not None else None
                ),
                "max_items": max_items,
                "max_requests": max_requests,
                "refresh": refresh,
            },
            json_output,
        )


@g_messages.command("list")
def cmd_messages_list(
    folder: Literal["inbox", "sent"] = "inbox",
    course_id: Optional[str] = typer.Option(None, "--course"),
    since: Optional[str] = None,
    unread_only: bool = typer.Option(False, "--unread-only"),
    limit: int = typer.Option(50, "--limit", "-l"),
    offset: int = 0,
    max_requests: int = 100,
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """List Blackboard inbox/sent messages through readable course conversations, without marking them read."""
    with application_scope() as application:
        from ntulearn.services import messages

        return invoke(
            partial(messages.list_messages, application.learn),
            {
                "folder": folder,
                "course_id": course_id,
                "since": local_datetime(since),
                "unread_only": unread_only,
                "limit": limit,
                "offset": offset,
                "max_requests": max_requests,
                "refresh": refresh,
            },
            json_output,
        )


@g_messages.command("read")
def cmd_messages_read(
    message_id: str,
    course_id: Optional[str] = typer.Option(None, "--course"),
    conversation_id: Optional[str] = None,
    max_requests: int = 100,
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Read a message's full body and published conversation recipients."""
    with application_scope() as application:
        from ntulearn.services import messages

        return invoke(
            partial(messages.read_message, application.learn),
            {
                "message_id": message_id,
                "course_id": course_id,
                "conversation_id": conversation_id,
                "max_requests": max_requests,
                "refresh": refresh,
            },
            json_output,
        )


@app.command("users")
def cmd_users(
    course_id: str,
    limit: int = typer.Option(50, "--limit", "-l"),
    offset: int = 0,
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """List course users visible to your account, with their published names and roles."""
    with application_scope() as application:
        from ntulearn.services import people

        return invoke(
            partial(people.list_course_users, application.learn),
            {
                "course_id": course_id,
                "limit": limit,
                "offset": offset,
                "refresh": refresh,
            },
            json_output,
        )


@g_groups.command("__default__", hidden=True)
def cmd_groups_default(
    course_id: str,
    limit: int = typer.Option(50, "--limit", "-l"),
    offset: int = 0,
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """List groups and group sets defined in a course."""
    with application_scope() as application:
        from ntulearn.services import people

        return invoke(
            partial(people.list_course_groups, application.learn),
            {
                "course_id": course_id,
                "limit": limit,
                "offset": offset,
                "refresh": refresh,
            },
            json_output,
        )


@g_groups.command("members")
def cmd_groups_members(
    course_id: str,
    group_id: str,
    limit: int = typer.Option(50, "--limit", "-l"),
    offset: int = 0,
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """List visible members of a course group through Blackboard's browser membership API."""
    with application_scope() as application:
        from ntulearn.services import people

        return invoke(
            partial(people.get_group_members, application.learn),
            {
                "course_id": course_id,
                "group_id": group_id,
                "limit": limit,
                "offset": offset,
                "refresh": refresh,
            },
            json_output,
        )


@g_search.command("__default__", hidden=True)
def cmd_search_default(
    course_id: str,
    query: str,
    max_depth: int = 5,
    max_nodes: int = 1000,
    max_results: int = 50,
    max_requests: int = 100,
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Recursively search one course's content titles, body and description for a case-insensitive substring."""
    with application_scope() as application:
        from ntulearn.services import content

        return invoke(
            partial(content.search_course_content, application.learn),
            {
                "course_id": course_id,
                "query": query,
                "max_depth": max_depth,
                "max_nodes": max_nodes,
                "max_results": max_results,
                "max_requests": max_requests,
                "refresh": refresh,
            },
            json_output,
        )


@g_search.command("all")
def cmd_search_all(
    query: str,
    course_ids: Optional[str] = typer.Option(None, "--course-ids", help="JSON value."),
    max_depth: int = 5,
    max_nodes: int = 1000,
    max_results: int = 50,
    max_requests: int = 100,
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Recursively search content across available enrolled courses, or selected course_ids."""
    with application_scope() as application:
        from ntulearn.services import content

        return invoke(
            partial(content.search_all_courses, application.learn),
            {
                "query": query,
                "course_ids": (
                    parse_json(course_ids) if course_ids is not None else None
                ),
                "max_depth": max_depth,
                "max_nodes": max_nodes,
                "max_results": max_results,
                "max_requests": max_requests,
                "refresh": refresh,
            },
            json_output,
        )


g_courses.command("list")(cmd_courses_default)
g_content.command("show")(cmd_content_default)
g_groups.command("list")(cmd_groups_default)
g_search.command("course")(cmd_search_default)
