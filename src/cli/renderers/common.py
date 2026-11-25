"""Small presentation primitives shared by service-specific renderers."""

from collections.abc import Callable, Mapping, Sequence
from typing import Any

from rich.console import Console
from rich.filesize import decimal
from rich.table import Table
from rich.tree import Tree

Data = Mapping[str, Any]
Renderer = Callable[[Console, Data], None]


def label(name: str) -> str:
    words = name.replace("_", " ").split()
    abbreviations = {
        "id": "ID",
        "url": "URL",
        "au": "AU",
        "eta": "ETA",
        "poi": "POI",
        "lta": "LTA",
        "xml": "XML",
    }
    return " ".join(
        abbreviations.get(
            word.lower(), word.capitalize() if index == 0 else word.lower()
        )
        for index, word in enumerate(words)
    )


def value_at(data: Data, path: str):
    if path in data:
        return data[path]
    value: Any = data
    for part in path.split("."):
        if not isinstance(value, Mapping):
            return None
        value = value.get(part)
    return value


def text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, (list, tuple)):
        return ", ".join(text(item) for item in value)
    if isinstance(value, bool):
        return "Yes" if value else "No"
    return str(value)


def file_size(bytes_count: int | None) -> str | None:
    return decimal(bytes_count) if bytes_count is not None else None


def table(console: Console, title: str, rows, fields: Sequence[str]) -> None:
    rows = list(rows or [])
    if not rows:
        console.print(f"{title}: No results.")
        return
    fields = [
        field
        for field in fields
        if any(value_at(row, field) not in (None, "", [], {}) for row in rows)
    ]
    if not fields:
        console.print(f"{title}: No displayable results.")
        return
    result = Table(title=title)
    for field in fields:
        minimum = None
        if field.endswith("_id") or field == "id":
            minimum = min(36, max(len(text(value_at(row, field))) for row in rows))
        result.add_column(
            label(field.split(".")[-1]), min_width=minimum, overflow="fold"
        )
    for row in rows:
        result.add_row(*(text(value_at(row, field)) for field in fields))
    console.print(result)


def add_tree(branch: Tree, value) -> None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            if item is None or item == "" or item == [] or item == {}:
                continue
            if isinstance(item, (Mapping, list)):
                add_tree(branch.add(label(key)), item)
            else:
                branch.add(f"{label(key)}: {text(item)}")
    elif isinstance(value, list):
        for item in value:
            if isinstance(item, (Mapping, list)):
                title = next(
                    (
                        str(item[key])
                        for key in ("name", "title", "course_code", "id")
                        if isinstance(item, Mapping) and item.get(key)
                    ),
                    "•",
                )
                add_tree(branch.add(title), item)
            else:
                branch.add(text(item))
    else:
        branch.add(text(value))


def details(console: Console, title: str, data: Data, fields: Sequence[str]) -> None:
    selected = {field: value_at(data, field) for field in fields}
    selected = {
        key: value
        for key, value in selected.items()
        if value is not None and value != "" and value != [] and value != {}
    }
    if not selected:
        console.print(f"{title}: No details available.")
        return
    tree = Tree(title)
    add_tree(tree, selected)
    console.print(tree)


def notices(console: Console, data: Data) -> None:
    if data.get("complete") is False or data.get("truncated") is True:
        console.print("Results may be incomplete.")
    for issue in data.get("issues") or []:
        if isinstance(issue, Mapping):
            message = issue.get("message") or issue.get("reason") or issue.get("error")
            if message:
                console.print(f"Notice: {message}")
        elif issue:
            console.print(f"Notice: {text(issue)}")


def pagination(console: Console, data: Data) -> None:
    total = data.get("total_count")
    pagination_data = data.get("pagination")
    if total is None and isinstance(pagination_data, Mapping):
        total = pagination_data.get("total_elements")
        if total is None:
            total = pagination_data.get("complete_list_size")
    if total is not None:
        console.print(f"Total: {total}")
    next_offset = data.get("next_offset")
    if next_offset is not None:
        console.print(f"More results: --offset {next_offset}")
    elif data.get("has_more") is True:
        console.print("More results are available; use --offset.")
    elif data.get("next_page") is not None:
        console.print(f"More results: --page {data['next_page']}")
    elif data.get("has_next_page") is True:
        console.print("More results are available; use --page.")
    elif (
        isinstance(pagination_data, Mapping)
        and pagination_data.get("next_page") is not None
    ):
        console.print(f"More results: --page {pagination_data['next_page']}")
    elif (
        isinstance(pagination_data, Mapping)
        and pagination_data.get("next_offset") is not None
    ):
        console.print(f"More results: --offset {pagination_data['next_offset']}")
    elif isinstance(pagination_data, Mapping) and pagination_data.get(
        "resumption_token"
    ):
        console.print(f"More results: --token {pagination_data['resumption_token']}")
    notices(console, data)


def listing(title: str, key: str, fields: Sequence[str]) -> Renderer:
    def show(console: Console, data: Data) -> None:
        table(console, title, data.get(key), fields)
        pagination(console, data)

    return show


def detail(title: str, fields: Sequence[str], *, nested: str | None = None) -> Renderer:
    def show(console: Console, data: Data) -> None:
        record = data.get(nested) if nested else data
        details(console, title, record if isinstance(record, Mapping) else {}, fields)
        pagination(console, data)

    return show


def sections(
    title: str,
    key: str,
    *,
    heading: str = "title",
    body: str = "body",
    date: str | None = None,
) -> Renderer:
    def show(console: Console, data: Data) -> None:
        rows = data.get(key) or []
        if not rows:
            console.print(f"{title}: No results.")
        for row in rows:
            console.rule(text(row.get(heading) or title), style="bold")
            if date and row.get(date):
                console.print(f"{label(date)}: {text(row[date])}")
            if row.get(body):
                console.print(text(row[body]), markup=False)
        pagination(console, data)

    return show


auth_status = detail(
    "Authentication",
    (
        "session_verified",
        "authentication_method",
        "credential_error",
        "credentials_configured",
    ),
)
action = detail(
    "Result", ("outcome", "message", "verified", "resource_id", "references")
)


def download(console, data):
    details(
        console,
        "Download",
        {"path": data.get("path"), "size": file_size(data.get("bytes_written"))},
        ("path", "size"),
    )
