"""Terminal views for shuttle and bus commands."""

from .common import listing, table

routes = listing("Routes", "routes", ("route_code", "description", "long_name"))
_LOAD_LABELS = {"SEA": "Seats available", "SDA": "Standing", "LSD": "Limited standing"}


def _stop_coverage(console, data):
    uncovered = data.get("routes_without_stop_data")
    if uncovered:
        console.print("No stop data available for: " + ", ".join(uncovered))


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
                "routes": [],
            }
        route = stop.get("route_code")
        if route and route not in grouped[key]["routes"]:
            grouped[key]["routes"].append(route)
    table(console, "Stops", grouped.values(), ("name", "routes"))
    _stop_coverage(console, data)
    if data.get("next_offset") is not None:
        console.print(f"More stops: --offset {data['next_offset']}")
    if related_stops is None and data.get("total_count", 0) > len(page):
        console.print(
            "Routes shown are from this page; more routes may appear on later pages."
        )


def _eta(minutes):
    if minutes is None:
        return None
    return "Due" if minutes == "0" else f"{minutes} min"


def arrivals(console, data):
    shuttle = data.get("shuttle_arrivals") or []
    lta = data.get("lta_arrivals") or []
    if shuttle:
        table(
            console,
            "Shuttle arrivals",
            [
                {
                    **row,
                    "eta": _eta(row.get("eta")) or "-",
                    "next_eta": _eta(row.get("next_eta")),
                }
                for row in shuttle
            ],
            ("route_code", "stop_name", "eta", "next_eta"),
        )
    if lta:
        table(
            console,
            "Bus arrivals",
            [
                {
                    **row,
                    "eta": _eta(row.get("eta_minutes")) or "-",
                    "next_eta": _eta(row.get("next_eta_minutes")),
                    "crowding": _LOAD_LABELS.get(row.get("load"), row.get("load")),
                }
                for row in lta
            ],
            (
                "service_no",
                "stop_name",
                "eta",
                "next_eta",
                "crowding",
            ),
        )
    if not shuttle and not lta:
        route = data.get("route_filter")
        uncovered = data.get("routes_without_stop_data") or []
        if route not in uncovered:
            query = (data.get("stop_query") or "").strip()
            route_name = f" on route {route}" if route else ""
            if query:
                console.print(f'No stops match "{query}"{route_name}.', markup=False)
                route_option = f" --route {route}" if route else ""
                console.print(f"Find stop names with: ntu bus stops{route_option}")
            elif not uncovered:
                console.print(f"No stops found{route_name}.")
    _stop_coverage(console, data)


def live(console, data):
    buses = [
        {
            **bus,
            "location": f"{bus['latitude']:.5f}, {bus['longitude']:.5f}",
        }
        for bus in data.get("buses") or []
        if bus.get("latitude") is not None and bus.get("longitude") is not None
    ]
    table(
        console,
        "Live buses",
        buses,
        ("location", "crowd_level", "occupancy"),
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
