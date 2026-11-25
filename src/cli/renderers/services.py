"""Terminal views for campus-services commands."""

from .common import listing, table

search = listing(
    "Campus services",
    "locations",
    ("name", "address", "operating_hours", "phone", "map_url"),
)


def filters(console, data):
    table(console, "Service types", data.get("types"), ("id", "name"))
    table(console, "Categories", data.get("categories"), ("id", "name"))
