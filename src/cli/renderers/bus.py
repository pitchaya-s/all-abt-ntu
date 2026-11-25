"""Terminal views for shuttle and bus commands."""

from .common import listing, table

routes = listing("Routes", "routes", ("route_code", "description", "long_name"))


def stops(console, data, *, related_stops=None):
    page = data.get("stops") or []
    selected = {(stop.get("name"), stop.get("stop_code")) for stop in page}
    records = related_stops if related_stops is not None else page
    grouped = {}
    for item in records:
        stop = item.model_dump(mode="json") if hasattr(item, "model_dump") else item
        key = (stop.get("name"), stop.get("stop_code"))
        if key not in selected:
            continue
        if key not in grouped:
            grouped[key] = {
                "name": key[0],
                "stop_code": key[1] if key[1] != key[0] else None,
                "routes": [],
            }
        route = stop.get("route_code")
        if route and route not in grouped[key]["routes"]:
            grouped[key]["routes"].append(route)
    table(console, "Stops", grouped.values(), ("name", "stop_code", "routes"))
    if data.get("total_count") is not None:
        console.print(f"Total stop-route entries: {data['total_count']}")
    if data.get("next_offset") is not None:
        console.print(f"More results: --offset {data['next_offset']}")
    if related_stops is None and data.get("total_count", 0) > len(page):
        console.print(
            "Routes shown are from this page; more routes may appear on later pages."
        )


def arrivals(console, data):
    shuttle = data.get("shuttle_arrivals") or []
    lta = data.get("lta_arrivals") or []
    if shuttle:
        table(
            console,
            "Shuttle arrivals",
            shuttle,
            ("route_code", "stop_name", "eta", "next_eta"),
        )
    if lta:
        table(
            console,
            "Bus arrivals",
            lta,
            (
                "service_no",
                "stop_name",
                "stop_code",
                "eta_minutes",
                "next_eta_minutes",
                "load",
            ),
        )
    if not shuttle and not lta:
        console.print("Arrivals: No estimates available.")


def live(console, data):
    table(
        console,
        "Live buses",
        data.get("buses"),
        ("vehicle_plate", "latitude", "longitude", "speed", "crowd_level", "occupancy"),
    )
    if data.get("reported_bus_count") is not None:
        console.print(f"Buses reported: {data['reported_bus_count']}")


def status(console, data):
    table(
        console,
        "Operating schedule",
        data.get("schedules"),
        ("route_code", "day_type", "schedule_type", "first_bus", "last_bus"),
    )
    for field in (
        "special_day_notice",
        "temporary_message",
        "no_active_bus_message",
        "no_operations_message",
    ):
        if data.get(field):
            console.print(data[field])
