"""Terminal views for MazeMap commands."""

from .common import detail, listing, pagination, table, text

campuses = listing("Campuses", "campuses", ("campus_id", "name"))
search = listing(
    "Places", "places", ("poi_id", "name", "building_name", "floor_name", "identifier")
)
place = detail(
    "Place",
    (
        "poi_id",
        "name",
        "identifier",
        "building_name",
        "floor_name",
        "categories",
        "description",
        "capacity",
        "map_url",
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
            f"{building.get('name') or 'Building'} ({building.get('building_id')})",
            building.get("floors"),
            ("floor_id", "name", "level"),
        )


def directions(console, data):
    routes = data.get("routes") or []
    if not routes:
        console.print("Directions: No routes found.")
    for route in routes:
        distance = route.get("distance_metres")
        title = (
            f"Walking route — {distance:g} m"
            if distance is not None
            else "Walking route"
        )
        console.rule(title, style="bold")
        if route.get("duration_seconds") is not None:
            console.print(f"Estimated duration: {route['duration_seconds']} seconds")
        if route.get("accessible") is not None:
            console.print(f"Accessible: {text(route['accessible'])}")
        if route.get("uncertain"):
            console.print("Accessibility or route details are uncertain.")
        for instruction in route.get("instructions") or []:
            console.print(f"• {instruction}")
        for issue in route.get("issues") or []:
            console.print(f"Notice: {issue}")
    pagination(console, data)
