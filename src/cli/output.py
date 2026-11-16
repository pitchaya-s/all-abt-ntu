"""Terminal and machine-readable rendering of service results."""

import json
from dataclasses import asdict, is_dataclass

from pydantic import BaseModel
from rich.console import Console
from rich.table import Table
from rich.tree import Tree


def plain(value):
    if isinstance(value, BaseModel):
        return value.model_dump(mode="json")
    if is_dataclass(value) and not isinstance(value, type):
        return asdict(value)
    return value


_METADATA = {
    "retrieved_at",
    "source_url",
    "source_urls",
    "cached",
    "from_cache",
    "cache_age_seconds",
    "cache_ttl_seconds",
    "personal_cache_ttl_seconds",
    "session_storage",
    "next_offset",
    "next_page",
    "has_next_page",
    "has_more",
    "pages_checked",
    "directory_count",
    "local_count",
    "central_index_count",
}

_TABLE_FIELDS = {
    "name",
    "title",
    "course_code",
    "course_name",
    "course_type",
    "poi_id",
    "record_id",
    "item_id",
    "route_code",
    "stop_name",
    "stop_code",
    "routes",
    "eta",
    "next_eta",
    "published_date",
    "availability_label",
    "school",
    "email",
    "id",
    "content_id",
    "article_id",
    "attachment_id",
    "service_id",
    "index",
    "au",
    "vacancies_available",
    "waitlist_length",
    "status",
    "available",
}

_LONG_TEXT = {
    "summary",
    "description",
    "abstract",
    "details",
    "body",
    "content",
    "text",
    "excerpt",
}


def _label(name):
    return str(name).replace("_", " ").capitalize()


def _visible(value):
    if isinstance(value, dict):
        return {
            key: cleaned
            for key, item in value.items()
            if key not in _METADATA
            and (cleaned := _visible(item)) not in (None, "", [], {})
        }
    if isinstance(value, list):
        return [
            cleaned
            for item in value
            if (cleaned := _visible(item)) not in (None, "", [], {})
        ]
    return value


def _bus_view(value, data, related_stops=None):
    """Adapt bus records for display without changing the underlying result."""
    from omnibus.models import Routes, Stops

    if isinstance(value, Routes):
        data.pop("colors", None)
        for route in data["routes"]:
            route.pop("is_lta_service", None)
    elif isinstance(value, Stops):
        partial_page = data["total_count"] > len(data["stops"])
        if related_stops is not None:
            selected = {(stop["name"], stop["stop_code"]) for stop in data["stops"]}
            data["stops"] = [
                stop.model_dump(mode="json")
                for stop in related_stops
                if (stop.name, stop.stop_code) in selected
            ]
        grouped = {}
        for stop in data["stops"]:
            key = (stop["name"], stop["stop_code"])
            if key not in grouped:
                grouped[key] = {
                    "name": stop["name"],
                    "stop_code": stop["stop_code"],
                    "routes": [],
                }
            routes = grouped[key]["routes"]
            if stop["route_code"] not in routes:
                routes.append(stop["route_code"])
        data["stops"] = [
            {**stop, "routes": ", ".join(stop["routes"])} for stop in grouped.values()
        ]
        for stop in data["stops"]:
            if stop["name"] == stop["stop_code"]:
                del stop["stop_code"]
        data["total_stop_route_entries"] = data.pop("total_count")
        return partial_page and related_stops is None
    return False


def _tree_add(branch, value):
    if isinstance(value, dict):
        for key, item in value.items():
            if isinstance(item, list) and all(
                not isinstance(entry, (dict, list)) for entry in item
            ):
                branch.add(f"{_label(key)}: {', '.join(map(str, item))}")
            elif isinstance(item, (dict, list)):
                _tree_add(branch.add(_label(key)), item)
            else:
                branch.add(f"{_label(key)}: {item}")
    elif isinstance(value, list):
        for item in value:
            if isinstance(item, (dict, list)):
                _tree_add(branch.add("•"), item)
            else:
                branch.add(str(item))
    else:
        branch.add(str(value))


def _weeks(values):
    if not values or not all(isinstance(value, int) for value in values):
        return ", ".join(map(str, values))
    ordered = sorted(set(values))
    spans = []
    start = previous = ordered[0]
    for value in ordered[1:]:
        if value != previous + 1:
            spans.append(str(start) if start == previous else f"{start}–{previous}")
            start = value
        previous = value
    spans.append(str(start) if start == previous else f"{start}–{previous}")
    return ", ".join(spans)


def _table(console, name, rows):
    if all(
        {"course_code", "day", "start_time", "end_time"} <= row.keys() for row in rows
    ):
        from stars.parser.course import parse_teaching_weeks

        schedules = []
        for row in rows:
            schedule = {
                **{
                    key: value
                    for key, value in row.items()
                    if key not in {"start_time", "end_time", "group"}
                },
                "time": f"{row['start_time']}–{row['end_time']}",
                "lesson_type": " ".join(
                    str(part)
                    for part in (row.get("lesson_type"), row.get("group"))
                    if part
                ),
                "teaching_weeks": _weeks(row.get("teaching_weeks", [])),
            }
            remarks = row.get("remarks")
            if isinstance(remarks, str):
                parsed = parse_teaching_weeks(remarks)
                if parsed is not None and list(parsed) == row.get("teaching_weeks"):
                    schedule.pop("remarks", None)
            schedules.append(schedule)
        rows = schedules
    if rows and any("TIME\\DAY" in row for row in rows):
        occupied = [
            row
            for row in rows
            if any(
                str(value).strip() for key, value in row.items() if key != "TIME\\DAY"
            )
        ]
        if not occupied:
            console.print(f"{_label(name)}: No scheduled sessions.")
            return
        rows = occupied
    scalars = list(
        dict.fromkeys(
            key
            for row in rows
            for key, value in row.items()
            if not isinstance(value, (dict, list))
        )
    )
    if "TIME\\DAY" in scalars:
        columns = scalars
    elif all({"course_code", "day", "time"} <= row.keys() for row in rows):
        columns = [
            key
            for key in (
                "course_code",
                "day",
                "time",
                "lesson_type",
                "venue",
                "teaching_weeks",
            )
            if key in scalars
        ]
    else:
        columns = [key for key in scalars if key in _TABLE_FIELDS][:4]
    if not columns:
        columns = [key for key in scalars if "url" not in key and "link" not in key][:4]
    if not columns:
        tree = Tree(_label(name))
        _tree_add(tree, rows)
        console.print(tree)
        return
    table = Table(title=_label(name))
    for column in columns:
        min_width = None
        if column.endswith("_id"):
            min_width = min(36, max(len(str(row.get(column, ""))) for row in rows))
        table.add_column(_label(column), min_width=min_width, overflow="fold")
    shortened = False
    for row in rows:
        cells = []
        for column in columns:
            item = str(row.get(column, ""))
            if column in _LONG_TEXT and len(item) > 180:
                item = item[:177].rstrip() + "..."
                shortened = True
            cells.append(item)
        table.add_row(*cells)
    console.print(table)
    for index, row in enumerate(rows, 1):
        details = {}
        nested_tables = []
        for key, item in row.items():
            if key in columns:
                continue
            if key == "headers" and isinstance(row.get("records"), list):
                continue
            if (
                isinstance(item, list)
                and item
                and all(isinstance(entry, dict) for entry in item)
            ):
                nested_tables.append((key, item))
                continue
            if key in _LONG_TEXT and isinstance(item, str) and len(item) > 180:
                item = item[:177].rstrip() + "..."
                shortened = True
            details[key] = item
        if details:
            tree = Tree(f"{_label(name)} {index}")
            _tree_add(tree, details)
            console.print(tree)
        for key, items in nested_tables:
            _table(console, f"{name} {index} — {key}", items)
    if shortened:
        console.print("Long descriptions are shortened; use --json for complete text.")


def render(value, json_output: bool = False, *, related_stops=None) -> None:
    data = plain(value)
    if json_output:
        print(json.dumps(data, default=str, ensure_ascii=False))
        return
    console = Console(markup=False)
    if isinstance(data, list):
        items = _visible(data)
        if not items:
            console.print("No results.")
        elif all(isinstance(item, dict) for item in items):
            _table(console, "Results", items)
        else:
            tree = Tree("Results")
            _tree_add(tree, items)
            console.print(tree)
        return
    if not isinstance(data, dict):
        console.print(data)
        return

    bus_more_routes = _bus_view(value, data, related_stops)
    more_results = data.get("next_offset") is not None or data.get("has_more") is True
    pagination = data.get("pagination")
    more_pages = (
        data.get("next_page") is not None
        or data.get("has_next_page") is True
        or (isinstance(pagination, dict) and pagination.get("next_page") is not None)
    )
    cleaned = _visible(data)
    if not cleaned:
        console.print("No results.")
        return

    tables = [
        (name, items)
        for name, items in cleaned.items()
        if isinstance(items, list)
        and items
        and all(isinstance(item, dict) for item in items)
    ]
    if tables:
        for name, items in tables:
            _table(console, name, items)
        details = {
            name: item
            for name, item in cleaned.items()
            if name not in dict(tables)
            and name not in {"query", "offset", "page", "route_filter"}
        }
        if details:
            tree = Tree("Details")
            _tree_add(tree, details)
            console.print(tree)
    else:
        tree = Tree("Result")
        _tree_add(tree, cleaned)
        console.print(tree)
    if more_results:
        console.print("More results available; use --offset to see the next page.")
    elif more_pages:
        console.print("More results available; use --page to see the next page.")
    if bus_more_routes:
        console.print(
            "Routes shown are from this page; more routes may appear on later pages."
        )
