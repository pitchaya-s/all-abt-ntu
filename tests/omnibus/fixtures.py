"""Fictional shuttle, BusRouter SG, and ArriveLah responses."""

import json

import httpx

from services.omnibus.client import OmnibusClient
from services.omnibus.client.lta import ARRIVAL_URL, SERVICES_URL, STOPS_URL


RESPONSES = {
    "DataActionGetRoutesList": {
        "RouteList": {
            "List": [
                {"Route": "Blue", "RouteDescription": "Campus loop", "IsSBS": False}
            ]
        }
    },
    "GetRoutesCodejson": {
        "Json": "{'data':[{'route_code':'Blue','color_code':'0054A6','Order':'1'}]}"
    },
    "DataActionGetActiveBusServicesData": {
        "Response": {
            "ActiveBusResult": {
                "Activebus": {
                    "List": [
                        {
                            "Vehplate": "TEST123",
                            "Lat": "1.35",
                            "Lng": "103.68",
                            "Speed": "0",
                            "LoadInfo": {
                                "Capacity": "40",
                                "Ridership": "5",
                                "CrowdLevel": "Low",
                            },
                        }
                    ]
                },
                "ActiveBusCount": "1",
                "TimeStamp": "1900-01-01T00:00:00",
            }
        }
    },
    "DataActionGetPickupCheckPoints": {},
    "GetETAAndNextETA_FMS": {"ETA": "3", "NextETA": "10"},
    "GetRoutesMinMax": {
        "IsFromLocalDB": False,
        "FMS_RouteMinMaxTime": {
            "List": [
                {
                    "Json": json.dumps(
                        {
                            "RouteMinMaxTimeResult": {
                                "RouteMinMaxTime": [
                                    {
                                        "Route": "Blue",
                                        "FirstTime": "07:00",
                                        "LastTime": "23:00",
                                    }
                                ]
                            }
                        }
                    )
                }
            ]
        },
    },
    "CheckPHSpecialDay": {"IsTodayPublicHoliday": False, "IsTodaySpecialDay": False},
    "GetTempMessages": {"Result": {"IsShowTemp": False}},
}

LTA_SERVICES = {
    "179": {"name": "Example Loop", "routes": [["12345", "12345"]]},
    "179B": {"name": "Example Branch", "routes": [["12345"]]},
}
LTA_STOPS = {"12345": [103.68, 1.35, "Example Gate", "Example Road"]}
LTA_PREDICTIONS = {
    "services": [
        {"no": "179", "next": {"duration_ms": 600000, "load": "LSD"}},
        {
            "no": "179",
            "next": {"duration_ms": 285500, "load": "SEA"},
            "next2": {"duration_ms": 900000, "load": "SDA"},
            "subsequent": {"duration_ms": 900000, "load": "SDA"},
        },
        {"no": "179B", "next": None, "next2": None, "next3": None},
    ]
}


class FixtureClient(OmnibusClient):
    def __init__(self):
        super().__init__(lta_transport=httpx.MockTransport(self._lta_request))
        self.calls = []
        self.lta_calls = []

    def _lta_request(self, request):
        url = str(request.url)
        self.lta_calls.append(url)
        if url == SERVICES_URL:
            return httpx.Response(200, json=LTA_SERVICES)
        if url == STOPS_URL:
            return httpx.Response(200, json=LTA_STOPS)
        if url == ARRIVAL_URL + "?id=12345":
            return httpx.Response(200, json=LTA_PREDICTIONS)
        raise AssertionError("Unexpected LTA URL")

    def _post(self, name, view_name, **kwargs):
        self.calls.append((name, view_name, kwargs))
        data = RESPONSES[name]
        if name == "DataActionGetPickupCheckPoints":
            route = kwargs["screen_variables"]["RouteId"]
            values = {
                "Blue": [{"Pickupname": "Example Hall", "Busstopcode": "EX1"}]
            }.get(route, [])
            data = {
                "ServiceId": "NTU",
                "PickupPoints": {
                    "PickupPointResult": {"Pickuppoint": {"List": values}}
                },
            }
        return data, "https://apps.ntu.edu.sg/NTUOmnibus/screenservices/example/" + name
