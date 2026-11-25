"""Public LTA stops from BusRouter SG and estimates from ArriveLah."""

import json
import re
from contextlib import contextmanager

from public_http_client import PublicHTTPClient

from ..contracts import LTA_SERVICES
from ..models import LtaArrival, OmnibusError, Stop

SERVICES_URL = "https://data.busrouter.sg/v1/services.min.json"
STOPS_URL = "https://data.busrouter.sg/v1/stops.min.json"
ARRIVAL_URL = "https://arrivelah2.busrouter.sg/"


def _is_stop_code(value):
    return isinstance(value, str) and re.fullmatch(r"[0-9]{5}", value) is not None


class LTAClient:
    def __init__(self, *, transport=None):
        self.http = PublicHTTPClient(
            "LTA bus data",
            {"data.busrouter.sg", "arrivelah2.busrouter.sg"},
            {"application/json"},
            transport=transport,
        )

    @contextmanager
    def _object(self, url, source, *, refresh=False):
        with self.http.parsed_response(url, refresh=refresh) as (body, snapshot):
            try:
                data = json.loads(body)
            except (ValueError, UnicodeError):
                raise OmnibusError(f"{source} returned invalid JSON.") from None
            if not isinstance(data, dict) or not data:
                raise OmnibusError(f"{source} returned an unexpected response.")
            yield data, snapshot

    def list_stops(self, service_no):
        with self._object(SERVICES_URL, "BusRouter SG") as (services, service_snapshot):
            if service_no not in services:
                return [], (SERVICES_URL,), service_snapshot["retrieved_at"]
            service = services[service_no]
            if not isinstance(service, dict) or not isinstance(
                service.get("routes"), list
            ):
                raise OmnibusError(
                    "BusRouter SG returned an unexpected service record."
                )
            codes = {}
            for route in service["routes"]:
                if not isinstance(route, list) or not all(map(_is_stop_code, route)):
                    raise OmnibusError(
                        "BusRouter SG returned an invalid route stop list."
                    )
                codes.update(dict.fromkeys(route))
            if not codes:
                return [], (SERVICES_URL,), service_snapshot["retrieved_at"]
            name = service.get("name")
            if not isinstance(name, str):
                raise OmnibusError("BusRouter SG returned an invalid service name.")

        records = []
        with self._object(STOPS_URL, "BusRouter SG") as (stops, stop_snapshot):
            for code in codes:
                stop = stops.get(code)
                if (
                    not isinstance(stop, list)
                    or len(stop) < 3
                    or not isinstance(stop[2], str)
                    or not stop[2].strip()
                ):
                    raise OmnibusError(
                        "BusRouter SG omitted a stop referenced by the route."
                    )
                records.append(
                    Stop(
                        name=stop[2].strip(),
                        stop_code=code,
                        route_code=service_no,
                        is_lta_service=True,
                        route_long_name=name or None,
                    )
                )
        return (
            records,
            (SERVICES_URL, STOPS_URL),
            min(service_snapshot["retrieved_at"], stop_snapshot["retrieved_at"]),
        )

    def predictions(self, stop_code):
        if not _is_stop_code(stop_code):
            raise OmnibusError("Use a five-digit LTA bus stop code.")
        url = f"{ARRIVAL_URL}?id={stop_code}"
        with self._object(url, "ArriveLah", refresh=True) as (data, _):
            services = data.get("services")
            if not isinstance(services, list):
                raise OmnibusError("ArriveLah returned an unexpected service list.")
            result: dict[str, list[tuple[int, str | None]]] = {}
            for service in services:
                if not isinstance(service, dict) or not isinstance(
                    service.get("no"), str
                ):
                    raise OmnibusError("ArriveLah returned an invalid service record.")
                if service["no"] not in LTA_SERVICES:
                    continue
                service_predictions = result.setdefault(service["no"], [])
                upcoming = (
                    service.get("next"),
                    service.get("next2", service.get("subsequent")),
                    service.get("next3"),
                )
                for bus in upcoming:
                    if bus is None:
                        continue
                    if (
                        not isinstance(bus, dict)
                        or type(bus.get("duration_ms")) is not int
                    ):
                        raise OmnibusError(
                            "ArriveLah returned an invalid arrival estimate."
                        )
                    load = bus.get("load")
                    service_predictions.append(
                        (
                            bus["duration_ms"],
                            load if load in ("SEA", "SDA", "LSD") else None,
                        )
                    )
            for estimates in result.values():
                estimates.sort(key=lambda estimate: estimate[0])
            return result, url

    @staticmethod
    def arrival(stop, estimates):
        duration, load = estimates[0] if estimates else (None, None)
        following = estimates[1][0] if len(estimates) > 1 else None
        seconds = _seconds(duration)
        next_seconds = _seconds(following)
        return LtaArrival(
            service_no=stop.route_code,
            stop_name=stop.name,
            stop_code=stop.stop_code,
            eta_minutes=_minutes(seconds),
            eta_seconds=seconds,
            next_eta_minutes=_minutes(next_seconds),
            next_eta_seconds=next_seconds,
            load=load,
        )


def _seconds(duration_ms):
    return None if duration_ms is None else max(0, (duration_ms + 999) // 1000)


def _minutes(seconds):
    return None if seconds is None else str((seconds + 59) // 60)
