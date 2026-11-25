"""Learn service commands."""

from typing import Annotated, Literal, Optional

from functools import partial
import re
from urllib.parse import parse_qs, unquote, urlsplit

import typer

from ..helpers import group, local_datetime, parse_json
from ..execution import application_scope
from ..services import invoke
from ..renderers import learn as views

app = typer.Typer(
    no_args_is_help=True, help="Browse your NTULearn courses, materials, and activity."
)
g_auth = group(default=False)
app.add_typer(g_auth, name="auth", help="Check NTULearn authentication.")
g_content = group(default=True)
app.add_typer(g_content, name="content", help="Browse course content and folders.")
g_courses = group(default=True)
app.add_typer(
    g_courses, name="courses", help="List enrolled courses or download materials."
)
g_files = group(default=False)
app.add_typer(g_files, name="files", help="Read or download course attachments.")
g_groups = group(default=True)
app.add_typer(g_groups, name="groups", help="List course groups and members.")
g_messages = group(default=False)
app.add_typer(g_messages, name="messages", help="List or read course messages.")
g_search = group(default=True)
app.add_typer(g_search, name="search", help="Search course content.")
g_videos = group(default=False)
app.add_typer(g_videos, name="videos", help="Download supported course videos.")


def is_content_url(value: str) -> bool:
    return "://" in value or value.lower().startswith("ntulearn.ntu.edu.sg/")


def content_reference(
    course_or_url: str, content_id: Optional[str], *, refresh: bool = False
) -> tuple[str, str]:
    """Resolve a content URL or a course reference and content ID."""
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
            from services.ntulearn.client.client import is_course_code

            supplied = course_or_url
            if is_course_code(supplied):
                with application_scope() as application:
                    supplied = invoke(
                        application.learn.resolve_course_id,
                        {"course_id": supplied, "refresh": refresh},
                        False,
                        show_result=False,
                    )
            if supplied != course:
                raise typer.BadParameter(
                    "The URL's course ID does not match the supplied course."
                )
        return course, item
    except ValueError:
        raise typer.BadParameter(
            "Provide a valid NTULearn document or lecture launch URL."
        ) from None


@g_auth.command("status")
def cmd_auth_status(
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Verify NTULearn access, reusing an existing session when available."""
    with application_scope() as application:
        return invoke(
            application.learn_session.verify,
            {},
            json_output,
            presenter=views.auth_status,
        )


@g_courses.command("__default__", hidden=True)
def cmd_courses_default(
    limit: int = typer.Option(50, "--limit", "-l", help="Maximum number of results."),
    offset: int = typer.Option(0, "--offset", help="Number of results to skip."),
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """List your enrolled NTULearn courses and organizations, including published availability and course IDs."""
    with application_scope() as application:
        return invoke(
            application.learn.list_courses,
            {"limit": limit, "offset": offset, "refresh": refresh},
            json_output,
            presenter=views.courses_default,
        )


@g_content.command("__default__", hidden=True)
def cmd_content_default(
    course_id: Annotated[
        str,
        typer.Argument(
            help="Course code or Blackboard course ID from ntu learn courses."
        ),
    ],
    parent_id: Optional[str] = typer.Option(
        None,
        "--parent",
        help="The ID of a parent folder. Omit it to browse the top level.",
    ),
    limit: int = typer.Option(50, "--limit", "-l", help="Maximum number of results."),
    offset: int = typer.Option(0, "--offset", help="Number of results to skip."),
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Read one level of course content."""
    with application_scope() as application:
        if parent_id and is_content_url(parent_id):
            course_id, parent_id = content_reference(
                course_id, parent_id, refresh=refresh
            )
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
            presenter=views.content_default,
        )


@g_content.command("tree")
def cmd_content_tree(
    course_id: Annotated[
        str,
        typer.Argument(
            help="Course code or Blackboard course ID from ntu learn courses."
        ),
    ],
    max_depth: Annotated[
        int, typer.Option(help="Maximum nesting depth to traverse. Default: 5.")
    ] = 5,
    max_nodes: Annotated[
        int,
        typer.Option(help="Maximum number of content nodes to examine. Default: 1000."),
    ] = 1000,
    max_requests: Annotated[
        int,
        typer.Option(
            help="Maximum number of upstream requests the operation may make. Default: 100."
        ),
    ] = 100,
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Read a course's nested content tree."""
    with application_scope() as application:
        from services.ntulearn.services import content

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
            presenter=views.content_tree,
        )


@app.command("attachments")
def cmd_attachments(
    course_id: str = typer.Argument(
        ...,
        metavar="COURSE_OR_URL",
        help="Course code, Blackboard course ID, or supported document or lecture URL.",
    ),
    content_id: Optional[str] = typer.Argument(
        None,
        help="The content ID returned when you browse the course. Where supported, a content URL can supply the course and content IDs.",
    ),
    limit: int = typer.Option(50, "--limit", "-l", help="Maximum number of results."),
    offset: int = typer.Option(0, "--offset", help="Number of results to skip."),
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """List attachments using a course and content ID, or an NTULearn content URL."""
    with application_scope() as application:
        course_id, content_id = content_reference(
            course_id, content_id, refresh=refresh
        )
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
            presenter=views.attachments,
        )


@g_files.command("read")
def cmd_files_read(
    course_id: str = typer.Argument(
        ...,
        metavar="COURSE_OR_URL",
        help="Course code, Blackboard course ID, or supported document or lecture URL.",
    ),
    content_id: str = typer.Argument(
        ...,
        metavar="CONTENT_OR_ATTACHMENT_ID",
        help="Content ID when using a course ID, or attachment ID when using a URL.",
    ),
    attachment_id: Optional[str] = typer.Argument(
        None, help="The attachment ID returned by the attachment listing."
    ),
    max_chars: Annotated[
        int,
        typer.Option(
            help="Maximum number of text characters to return. Default: 20000."
        ),
    ] = 20000,
    max_pages: Annotated[
        int, typer.Option(help="Maximum number of document pages to read. Default: 20.")
    ] = 20,
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Read an attachment as text. Supply course and content IDs, or a content URL, plus the attachment ID."""
    with application_scope() as application:
        from services.ntulearn.services import files

        if attachment_id is None:
            attachment_id = content_id
            course_id, content_id = content_reference(course_id, None)
        else:
            course_id, content_id = content_reference(course_id, content_id)
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
            presenter=views.files_read,
        )


@g_files.command("download")
def cmd_files_download(
    course_id: str = typer.Argument(
        ...,
        metavar="COURSE_OR_URL",
        help="Course code, Blackboard course ID, or supported document or lecture URL.",
    ),
    content_id: str = typer.Argument(
        ...,
        metavar="CONTENT_OR_ATTACHMENT_ID",
        help="Content ID when using a course ID, or attachment ID when using a URL.",
    ),
    attachment_id: Optional[str] = typer.Argument(
        None, help="The attachment ID returned by the attachment listing."
    ),
    destination: str = typer.Option(
        ...,
        "--output",
        "-o",
        help="The local destination path. Follow the command description for file or directory requirements.",
    ),
    max_bytes: int = typer.Option(
        20_000_000, help="Maximum file size in bytes (up to 20 MB)."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Download an attachment using course and content IDs, or a content URL, plus the attachment ID."""
    with application_scope() as application:
        if attachment_id is None:
            attachment_id = content_id
            course_id, content_id = content_reference(course_id, None)
        else:
            course_id, content_id = content_reference(course_id, content_id)
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
            presenter=views.files_download,
        )


@g_videos.command("download")
def cmd_videos_download(
    course_id: str = typer.Argument(
        ...,
        metavar="COURSE_OR_URL",
        help="Course code, Blackboard course ID, or supported document or lecture URL.",
    ),
    content_id: Optional[str] = typer.Argument(
        None,
        help="The content ID returned when you browse the course. Where supported, a content URL can supply the course and content IDs.",
    ),
    destination: str = typer.Option(
        ...,
        "--output",
        "-o",
        help="The local destination path. Follow the command description for file or directory requirements.",
    ),
    max_mb: Annotated[
        int, typer.Option(help="Maximum video size in megabytes. Default: 1000.")
    ] = 1000,
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Download a Kaltura video using course and content IDs, or an NTULearn content URL."""
    with application_scope() as application:
        from services.ntulearn.services import videos

        course_id, content_id = content_reference(course_id, content_id)
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
            presenter=views.videos_download,
        )


@g_courses.command("download")
def cmd_courses_download(
    course_id: Annotated[
        str,
        typer.Argument(
            help="Course code or Blackboard course ID from ntu learn courses."
        ),
    ],
    destination: str = typer.Option(
        ...,
        "--output",
        "-o",
        help="The local destination path. Follow the command description for file or directory requirements.",
    ),
    max_depth: Annotated[
        int, typer.Option(help="Maximum nesting depth to traverse. Default: 5.")
    ] = 5,
    max_nodes: Annotated[
        int,
        typer.Option(help="Maximum number of content nodes to examine. Default: 1000."),
    ] = 1000,
    max_files: Annotated[
        int, typer.Option(help="Maximum number of files to download. Default: 100.")
    ] = 100,
    max_total_mb: Annotated[
        int,
        typer.Option(help="Maximum total download size in megabytes. Default: 200."),
    ] = 200,
    max_requests: Annotated[
        int,
        typer.Option(
            help="Maximum number of upstream requests the operation may make. Default: 200."
        ),
    ] = 200,
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Recursively save readable Blackboard attachments under destination/course_id with content folder names and stable file IDs."""
    with application_scope() as application:
        from services.ntulearn.services import files

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
            presenter=views.courses_download,
        )


@app.command("announcements")
def cmd_announcements(
    course_id: Annotated[
        str,
        typer.Argument(
            help="Course code or Blackboard course ID from ntu learn courses."
        ),
    ],
    limit: int = typer.Option(50, "--limit", "-l", help="Maximum number of results."),
    offset: int = typer.Option(0, "--offset", help="Number of results to skip."),
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
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
            presenter=views.announcements,
        )


@app.command("grades")
def cmd_grades(
    course_id: Annotated[
        str,
        typer.Argument(
            help="Course code or Blackboard course ID from ntu learn courses."
        ),
    ],
    limit: int = typer.Option(50, "--limit", "-l", help="Maximum number of results."),
    offset: int = typer.Option(0, "--offset", help="Number of results to skip."),
    grades_offset: int = typer.Option(
        0, "--grades-offset", help="Number of grades to skip."
    ),
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
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
            presenter=views.grades,
        )


@app.command("calendar")
def cmd_calendar(
    since: Annotated[
        Optional[str],
        typer.Option(help="Start of the date or time range in ISO format."),
    ] = None,
    until: Annotated[
        Optional[str], typer.Option(help="End of the date or time range in ISO format.")
    ] = None,
    course_id: Optional[str] = typer.Option(
        None,
        "--course",
        help="Course code or Blackboard course ID from ntu learn courses.",
    ),
    limit: int = typer.Option(50, "--limit", "-l", help="Maximum number of results."),
    offset: int = typer.Option(0, "--offset", help="Number of results to skip."),
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
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
            presenter=views.calendar,
        )


@app.command("upcoming")
def cmd_upcoming(
    since: Annotated[
        Optional[str],
        typer.Option(help="Start of the date or time range in ISO format."),
    ] = None,
    until: Annotated[
        Optional[str], typer.Option(help="End of the date or time range in ISO format.")
    ] = None,
    course_ids: Optional[str] = typer.Option(
        None, "--course-ids", help="JSON array of course codes or Blackboard IDs."
    ),
    item_type: Annotated[
        Optional[str],
        typer.Option(help="Restrict calendar results to the selected item type."),
    ] = None,
    max_requests: Annotated[
        int,
        typer.Option(
            help="Maximum number of upstream requests the operation may make. Default: 100."
        ),
    ] = 100,
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Collect all calendar pages across your enrolled courses."""
    with application_scope() as application:
        from services.ntulearn.services import overview

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
            presenter=views.upcoming,
        )


@app.command("digest")
def cmd_digest(
    since: Annotated[
        Optional[str],
        typer.Option(help="Start of the date or time range in ISO format."),
    ] = None,
    until: Annotated[
        Optional[str], typer.Option(help="End of the date or time range in ISO format.")
    ] = None,
    course_ids: Optional[str] = typer.Option(
        None, "--course-ids", help="JSON array of course codes or Blackboard IDs."
    ),
    max_items: Annotated[
        int, typer.Option(help="Maximum number of items to include. Default: 200.")
    ] = 200,
    max_requests: Annotated[
        int,
        typer.Option(
            help="Maximum number of upstream requests the operation may make. Default: 100."
        ),
    ] = 100,
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Digest of recent announcements, upcoming calendar items and your gradebook across courses."""
    with application_scope() as application:
        from services.ntulearn.services import overview

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
            presenter=views.digest,
        )


@g_messages.command("list")
def cmd_messages_list(
    folder: Annotated[
        Literal["inbox", "sent"],
        typer.Option(
            help="Choose the inbox or sent message folder. Choices: inbox, sent. Default: inbox."
        ),
    ] = "inbox",
    course_id: Optional[str] = typer.Option(
        None,
        "--course",
        help="Course code or Blackboard course ID from ntu learn courses.",
    ),
    since: Annotated[
        Optional[str],
        typer.Option(help="Start of the date or time range in ISO format."),
    ] = None,
    unread_only: bool = typer.Option(
        False, "--unread-only", help="Restrict messages to unread items."
    ),
    limit: int = typer.Option(50, "--limit", "-l", help="Maximum number of results."),
    offset: int = typer.Option(0, "--offset", help="Number of results to skip."),
    max_requests: Annotated[
        int,
        typer.Option(
            help="Maximum number of upstream requests the operation may make. Default: 100."
        ),
    ] = 100,
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """List Blackboard inbox/sent messages through readable course conversations, without marking them read."""
    with application_scope() as application:
        from services.ntulearn.services import messages

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
            presenter=views.messages_list,
        )


@g_messages.command("read")
def cmd_messages_read(
    message_id: Annotated[
        str,
        typer.Argument(
            help="The message ID returned by the relevant listing or details command."
        ),
    ],
    course_id: Optional[str] = typer.Option(
        None,
        "--course",
        help="Course code or Blackboard course ID from ntu learn courses.",
    ),
    conversation_id: Annotated[
        Optional[str],
        typer.Option(
            help="The conversation ID returned by the relevant listing or details command."
        ),
    ] = None,
    max_requests: Annotated[
        int,
        typer.Option(
            help="Maximum number of upstream requests the operation may make. Default: 100."
        ),
    ] = 100,
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Read a message's full body and published conversation recipients."""
    with application_scope() as application:
        from services.ntulearn.services import messages

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
            presenter=views.messages_read,
        )


@app.command("users")
def cmd_users(
    course_id: Annotated[
        str,
        typer.Argument(
            help="Course code or Blackboard course ID from ntu learn courses."
        ),
    ],
    limit: int = typer.Option(50, "--limit", "-l", help="Maximum number of results."),
    offset: int = typer.Option(0, "--offset", help="Number of results to skip."),
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """List course users visible to your account, with their published names and roles."""
    with application_scope() as application:
        from services.ntulearn.services import people

        return invoke(
            partial(people.list_course_users, application.learn),
            {
                "course_id": course_id,
                "limit": limit,
                "offset": offset,
                "refresh": refresh,
            },
            json_output,
            presenter=views.users,
        )


@g_groups.command("__default__", hidden=True)
def cmd_groups_default(
    course_id: Annotated[
        str,
        typer.Argument(
            help="Course code or Blackboard course ID from ntu learn courses."
        ),
    ],
    limit: int = typer.Option(50, "--limit", "-l", help="Maximum number of results."),
    offset: int = typer.Option(0, "--offset", help="Number of results to skip."),
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """List groups and group sets defined in a course."""
    with application_scope() as application:
        from services.ntulearn.services import people

        return invoke(
            partial(people.list_course_groups, application.learn),
            {
                "course_id": course_id,
                "limit": limit,
                "offset": offset,
                "refresh": refresh,
            },
            json_output,
            presenter=views.groups_default,
        )


@g_groups.command("members")
def cmd_groups_members(
    course_id: Annotated[
        str,
        typer.Argument(
            help="Course code or Blackboard course ID from ntu learn courses."
        ),
    ],
    group_id: Annotated[
        str,
        typer.Argument(
            help="The group ID returned by the relevant listing or details command."
        ),
    ],
    limit: int = typer.Option(50, "--limit", "-l", help="Maximum number of results."),
    offset: int = typer.Option(0, "--offset", help="Number of results to skip."),
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """List visible members of a course group through Blackboard's browser membership API."""
    with application_scope() as application:
        from services.ntulearn.services import people

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
            presenter=views.groups_members,
        )


@g_search.command("__default__", hidden=True)
def cmd_search_default(
    course_id: Annotated[
        str,
        typer.Argument(
            help="Course code or Blackboard course ID from ntu learn courses."
        ),
    ],
    query: str = typer.Argument(..., help="Search text or keywords."),
    max_depth: Annotated[
        int, typer.Option(help="Maximum nesting depth to traverse. Default: 5.")
    ] = 5,
    max_nodes: Annotated[
        int,
        typer.Option(help="Maximum number of content nodes to examine. Default: 1000."),
    ] = 1000,
    max_results: Annotated[
        int,
        typer.Option(
            help="Maximum number of matching results to collect. Default: 50."
        ),
    ] = 50,
    max_requests: Annotated[
        int,
        typer.Option(
            help="Maximum number of upstream requests the operation may make. Default: 100."
        ),
    ] = 100,
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Recursively search one course's content titles, body and description for a case-insensitive substring."""
    with application_scope() as application:
        from services.ntulearn.services import content

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
            presenter=views.search_default,
        )


@g_search.command("all")
def cmd_search_all(
    query: str = typer.Argument(..., help="Search text or keywords."),
    course_ids: Optional[str] = typer.Option(
        None, "--course-ids", help="JSON array of course codes or Blackboard IDs."
    ),
    max_depth: Annotated[
        int, typer.Option(help="Maximum nesting depth to traverse. Default: 5.")
    ] = 5,
    max_nodes: Annotated[
        int,
        typer.Option(help="Maximum number of content nodes to examine. Default: 1000."),
    ] = 1000,
    max_results: Annotated[
        int,
        typer.Option(
            help="Maximum number of matching results to collect. Default: 50."
        ),
    ] = 50,
    max_requests: Annotated[
        int,
        typer.Option(
            help="Maximum number of upstream requests the operation may make. Default: 100."
        ),
    ] = 100,
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Recursively search content across available enrolled courses, or selected course_ids."""
    with application_scope() as application:
        from services.ntulearn.services import content

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
            presenter=views.search_all,
        )


g_courses.command("list")(cmd_courses_default)
g_content.command("show")(cmd_content_default)
g_groups.command("list")(cmd_groups_default)
g_search.command("course")(cmd_search_default)
