"""Terminal views for MazeMap commands."""

from math import ceil

from .common import detail, listing, pagination, table, text

campuses = listing("Campuses", "campuses", ("name", "campus_id"))
search = listing(
    "Places", "places", ("name", "building_name", "floor_name", "identifier", "poi_id")
)
place = detail(
    "Place",
    (
        "name",
        "identifier",
        "building_name",
        "floor_name",
        "categories",
        "description",
        "capacity",
        "map_url",
        "poi_id",
    ),
    nested="place",
)


def buildings(console, data):
    buildings_data = data.get("buildings") or []
    if not buildings_data:
        console.print("Buildings: No results.")
    for building in buildings_data:
        table(
            console,
            building.get("name") or "Building",
            building.get("floors"),
            ("name", "level"),
        )


def directions(console, data):
    routes = data.get("routes") or []
    if not routes:
        console.print("Directions: No routes found.")
    for route in routes:
        distance = route.get("distance_metres")
        title = "Walking route"
        if distance is not None:
            distance_label = (
                f"{distance / 1000:.2f} km" if distance >= 1000 else f"{distance:g} m"
            )
            title += f" — {distance_label}"
        console.rule(title, style="bold")
        duration = route.get("duration_seconds")
        if duration is not None:
            duration_label = (
                f"{ceil(duration / 60)} min"
                if duration >= 60
                else f"{ceil(duration)} sec"
            )
            console.print(f"Estimated walk: {duration_label}")
        if route.get("accessible") is not None:
            console.print(f"Accessible: {text(route['accessible'])}")
        if route.get("uncertain"):
            console.print("Accessibility or route details are uncertain.")
        for instruction in route.get("instructions") or []:
            console.print(f"• {instruction}")
        for issue in route.get("issues") or []:
            console.print(f"Notice: {issue}")
    pagination(console, data)
