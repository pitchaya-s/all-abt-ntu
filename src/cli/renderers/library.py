"""Terminal views for library commands."""

from .common import detail, listing, pagination, table

search = listing(
    "Library resources",
    "records",
    (
        "record_id",
        "title",
        "authors",
        "publication_dates",
        "resource_types",
        "availability_label",
    ),
)
record = detail(
    "Library record",
    (
        "record_id",
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
    ),
    nested="record",
)
map_availability = listing(
    "Facility availability", "spaces", ("space_id", "name", "status")
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
        ("library", "name", "space_id", "location_id", "group_id", "map_slug", "url"),
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
            space.get("name") or str(space.get("item_id") or "Facility"),
            space.get("slots"),
            ("start", "end", "status"),
        )
    if data.get("window_end"):
        console.print("The facility's booking window ends on this date.")
    pagination(console, data)
