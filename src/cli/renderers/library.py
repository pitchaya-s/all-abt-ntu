"""Terminal views for library commands."""

from .common import detail, listing, pagination, table

search = listing(
    "Library resources",
    "records",
    (
        "title",
        "authors",
        "publication_dates",
        "resource_types",
        "availability_label",
        "record_id",
        "context",
    ),
)
record = detail(
    "Library record",
    (
        "title",
        "authors",
        "resource_types",
        "publication_dates",
        "publishers",
        "editions",
        "languages",
        "subjects",
        "descriptions",
        "identifiers",
        "links",
        "catalogue_url",
        "record_id",
        "context",
    ),
    nested="record",
)
map_availability = listing(
    "Facility availability", "spaces", ("name", "status", "space_id")
)


def availability(console, data):
    table(
        console,
        "Holdings",
        data.get("holdings"),
        ("library", "location", "call_number", "availability"),
    )
    table(
        console,
        "Electronic access",
        data.get("electronic_services"),
        ("name", "url", "notes"),
    )


def facilities_default(console, data):
    table(
        console,
        "Library facilities",
        data.get("facilities"),
        ("name", "library", "map_slug", "space_id", "location_id", "group_id", "url"),
    )
    for notice in data.get("notices") or []:
        console.print(f"Notice: {notice}")


def facilities_schedule(console, data):
    if data.get("title"):
        console.print(data["title"])
    if data.get("description"):
        console.print(data["description"])
    spaces = data.get("spaces") or []
    if not spaces:
        console.print("Facility schedule: No results.")
    for space in spaces:
        table(
            console,
            space.get("name") or "Facility",
            space.get("slots"),
            ("start", "end", "status"),
        )
    if data.get("window_end") and data.get("date"):
        console.print(f"Booking window ends on {data['date']}.")
    pagination(console, data)
