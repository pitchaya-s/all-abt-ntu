"""Route and live-bus operations."""

from typing import Any

from ..contracts import CampusRoute


from .. import parser
from ..models import BusPositions, OmnibusError, Routes


class RouteMethods:
    def get_live_buses(self: Any, route_code: CampusRoute = "Blue") -> BusPositions:
        "Get current live vehicle positions for one NTU campus shuttle route. An empty list means no positions were reported in this snapshot; source timestamps may be unavailable."
        data, url = self._post(
            "DataActionGetActiveBusServicesData",
            "MainFlow.Shuttle",
            screen_variables=dict(self._empty_map_variables(), RouteId=route_code),
            client_variables=self._client_variables(route_code),
        )
        buses, count, timestamp = parser.bus_positions(data)
        return BusPositions(
            retrieved_at=self._now(),
            source_urls=[url],
            route_code=route_code,
            reported_bus_count=count,
            source_timestamp=timestamp,
            buses=buses,
        )

    def list_routes(self: Any) -> Routes:
        "List public NTU shuttle routes and their published display colors. This does not include route path geometry."
        route_data, route_url = self._post(
            "DataActionGetRoutesList",
            "MainFlow.Shuttle",
            screen_variables=self._empty_map_variables(),
            client_variables=self._client_variables(),
        )
        color_data, color_url = self._post(
            "GetRoutesCodejson", "MainFlow.Shuttle", inputs={}
        )
        colors_text = color_data.get("Json")
        if not isinstance(colors_text, str):
            raise OmnibusError("NTU Omnibus returned no route-color data.")
        route_rows, colors = parser.routes(route_data, colors_text)
        return Routes(
            retrieved_at=self._now(),
            source_urls=[route_url, color_url],
            routes=route_rows,
            colors=colors,
        )
