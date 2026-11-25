"""Terminal views for NTULearn commands."""

from rich.tree import Tree

from .common import auth_status as auth_status
from .common import (
    detail,
    details,
    download,
    file_size,
    listing,
    notices,
    pagination,
    sections,
    table,
    text,
)

courses_default = listing(
    "Courses", "courses", ("course_code", "name", "id", "available")
)
attachments = listing("Attachments", "attachments", ("file_name", "id"))
announcements = sections("Announcements", "announcements", date="created")
users = listing("Participants", "users", ("name", "role"))
groups_default = listing("Groups", "groups", ("name", "id", "available"))
groups_members = listing("Group members", "users", ("name", "role"))
search_default = listing(
    "Content matches", "matches", ("title", "breadcrumb", "course_id", "content_id")
)
search_all = search_default
calendar = listing(
    "Calendar", "items", ("title", "calendar_name", "start", "end", "location")
)
upcoming = calendar
files_read = detail(
    "File", ("file_name", "text", "truncated", "pages_read", "total_pages")
)
files_download = download
videos_download = download


def content_tree(console, data):
    root = Tree("Course content")

    def add(parent, nodes):
        for node in nodes:
            title = node.get("title") or "Untitled"
            identifier = node.get("id")
            branch = parent.add(f"{title} ({identifier})" if identifier else title)
            add(branch, node.get("children") or [])
            if node.get("children_complete") is False:
                branch.add("Some items could not be read.")

    add(root, data.get("contents") or [])
    console.print(root)
    notices(console, data)


def messages_list(console, data):
    messages = [
        {**message, "sender": (message.get("sender") or {}).get("name")}
        for message in data.get("messages") or []
    ]
    table(
        console,
        "Messages",
        messages,
        ("subject", "sender", "created", "read", "id", "course_id"),
    )
    pagination(console, data)


def content_default(console, data):
    entries = data.get("contents") or []
    table(console, "Course content", entries, ("title", "id", "type", "has_children"))
    for entry in entries:
        if entry.get("body") or entry.get("description"):
            details(
                console, entry.get("title") or "Content", entry, ("body", "description")
            )
    pagination(console, data)


def grades(console, data):
    grades_by_column = {grade["column_id"]: grade for grade in data.get("grades", [])}
    rows = []
    for column in data.get("columns", []):
        grade = grades_by_column.get(column["id"], {})
        rows.append(
            {
                "name": column.get("name"),
                "score": grade.get("score"),
                "possible_score": column.get("possible_score"),
                "status": grade.get("status"),
                "due": column.get("due"),
            }
        )
    known_columns = {column["id"] for column in data.get("columns", [])}
    for grade in data.get("grades", []):
        if grade["column_id"] not in known_columns:
            rows.append(
                {
                    "name": "Unnamed grade item",
                    "score": grade.get("score"),
                    "status": grade.get("status"),
                }
            )
    table(console, "Grades", rows, ("name", "score", "possible_score", "status", "due"))
    names = {
        column["id"]: column.get("name") or "Unnamed grade item"
        for column in data.get("columns", [])
    }
    for grade in data.get("grades", []):
        if grade.get("text") or grade.get("feedback") or grade.get("exempt"):
            details(
                console,
                names.get(grade["column_id"], "Unnamed grade item"),
                grade,
                ("text", "feedback", "exempt"),
            )
    pagination(console, data)
    if data.get("grades_next_offset") is not None:
        console.print(f"More grades: --grades-offset {data['grades_next_offset']}")


def messages_read(console, data):
    message = data.get("message") or {}
    console.rule(text(message.get("subject") or "Message"), style="bold")
    sender = message.get("sender") or {}
    if sender.get("name"):
        console.print(f"From: {sender['name']}")
    if message.get("created"):
        console.print(f"Created: {message['created']}")
    if data.get("body"):
        console.print(text(data["body"]), markup=False)
    recipients = data.get("recipients") or []
    names = [person["name"] for person in recipients if person.get("name")]
    if len(names) < len(recipients):
        names.append(f"{len(recipients) - len(names)} without a published name")
    if names:
        console.print("Recipients: " + ", ".join(names))
    notices(console, data)


def courses_download(console, data):
    table(
        console,
        "Downloaded files",
        [
            {**file, "size": file_size(file.get("bytes_written"))}
            for file in data.get("files") or []
        ],
        ("path", "status", "size"),
    )
    if data.get("destination"):
        console.print(f"Destination: {data['destination']}")
    if data.get("bytes_written") is not None:
        console.print(f"Total size: {file_size(data['bytes_written'])}")
    notices(console, data)


def digest(console, data):
    sections("Announcements", "announcements", date="created")(console, data)
    table(
        console,
        "Upcoming",
        data.get("upcoming"),
        ("title", "calendar_name", "start", "end", "location"),
    )
    rows = []
    for entry in data.get("grades", []):
        column, grade = entry.get("column") or {}, entry.get("grade") or {}
        rows.append(
            {
                "course_id": entry.get("course_id"),
                "name": column.get("name"),
                "score": grade.get("score"),
                "possible_score": column.get("possible_score"),
                "status": grade.get("status"),
            }
        )
    table(
        console,
        "Grades",
        rows,
        ("course_id", "name", "score", "possible_score", "status"),
    )
    if data.get("grade_change_note"):
        console.print(data["grade_change_note"])
