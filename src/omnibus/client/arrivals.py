"""Live arrival and service-status operations."""

from typing import Any

from ..contracts import (
    ArrivalSource,
    CAMPUS_ROUTES,
    CampusRoute,
    LTA_SERVICES,
    Query,
    RouteFilter,
)


from .. import parser
from ..models import Arrivals, OmnibusError, ServiceStatus


class ArrivalMethods:
    def get_arrivals(
        self: Any,
        route_filter: RouteFilter | None = None,
        stop_query: Query = "",
        source: ArrivalSource = "all",
    ) -> Arrivals:
        "Get arrival estimates for NTU shuttles and LTA services 179, 179A, 179B, and 199. Filter by route and stop name or code. A call can fetch up to 20 matching route-stop pairs. LTA estimates come from ArriveLah. Missing estimates are null."
        self._query(stop_query)
        if source not in {"all", "shuttle", "lta"}:
            raise OmnibusError("Choose all, shuttle, or lta arrival sources.")
        codes = list(
            CAMPUS_ROUTES
            if source == "shuttle"
            else LTA_SERVICES
            if source == "lta"
            else CAMPUS_ROUTES + LTA_SERVICES
        )
        if route_filter:
            if route_filter not in codes:
                raise OmnibusError(
                    "The selected route does not match the arrival source; choose the matching shuttle or lta source."
                )
            codes = [route_filter]
        stops, source_urls, _, _, uncovered = self._stop_records(codes)
        query = stop_query.strip().casefold()
        stops = [
            stop
            for stop in stops
            if not query
            or query in stop.name.casefold()
            or query in stop.stop_code.casefold()
        ]
        if len(stops) > 20:
            raise OmnibusError(
                "More than 20 stops match this request. Choose one route or a more specific stop name for live arrivals."
            )
        shuttle_rows: list[Any] = []
        lta_rows: list[Any] = []
        predictions_by_stop = {}
        for stop in stops:
            if stop.is_lta_service:
                if stop.stop_code not in predictions_by_stop:
                    predictions, url = self._lta.predictions(stop.stop_code)
                    predictions_by_stop[stop.stop_code] = predictions
                    source_urls.append(url)
                estimates = predictions_by_stop[stop.stop_code].get(stop.route_code, ())
                lta_rows.append(self._lta.arrival(stop, estimates))
                continue
            data, url = self._post(
                "GetETAAndNextETA_FMS",
                "MainFlow.Shuttle",
                inputs={"BusStopCode": stop.stop_code, "RouteCode": stop.route_code},
            )
            shuttle_rows.append(parser.stop_arrival(data, stop))
            source_urls.append(url)
        return Arrivals(
            retrieved_at=self._now(),
            source_urls=list(dict.fromkeys(source_urls)),
            route_filter=route_filter,
            stop_query=stop_query,
            shuttle_arrivals=shuttle_rows,
            lta_arrivals=lta_rows,
            routes_without_stop_data=uncovered,
        )

    def get_service_status(
        self: Any, route_code: CampusRoute = "Blue"
    ) -> ServiceStatus:
        "Get the published first/last bus schedule, public-holiday/special-day flags, and temporary notices for an NTU campus shuttle route."
        schedule_data, schedule_url = self._post(
            "GetRoutesMinMax", "MainFlow.Shuttle", inputs={"RouteCode": route_code}
        )
        special_data, special_url = self._post(
            "CheckPHSpecialDay", "MainFlow.Shuttle", inputs={"RouteCode": route_code}
        )
        message_data, message_url = self._post(
            "GetTempMessages", "MainFlow.Shuttle", inputs={}
        )
        try:
            schedules = parser.schedules(schedule_data, route_code)
            result = message_data["Result"]
            if not isinstance(result, dict):
                raise TypeError
            is_local = schedule_data["IsFromLocalDB"]
            is_holiday = special_data["IsTodayPublicHoliday"]
            is_special = special_data["IsTodaySpecialDay"]
            has_message = result["IsShowTemp"]
            for value in (is_local, is_holiday, is_special, has_message):
                if type(value) is not bool:
                    raise TypeError
        except (KeyError, TypeError):
            raise OmnibusError(
                "NTU Omnibus returned an unexpected service-status response."
            ) from None
        return ServiceStatus(
            retrieved_at=self._now(),
            source_urls=[schedule_url, special_url, message_url],
            route_code=route_code,
            schedules=schedules,
            schedule_from_local_db=is_local,
            is_public_holiday=is_holiday,
            is_special_day=is_special,
            special_day_notice=parser.optional_text(
                special_data.get("SpecialDayTextVal")
            ),
            has_temporary_message=has_message,
            temporary_message=parser.optional_text(result.get("TempMessageContent")),
            no_active_bus_message=parser.optional_text(result.get("MsgNoActiveBus")),
            no_operations_message=parser.optional_text(result.get("MsgNoOperations")),
        )
