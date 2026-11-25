"""Input constraints for NTU shuttle and public bus lookups."""

from typing import Annotated, Literal, get_args

from pydantic import Field

CampusRoute = Literal["Blue", "Brown", "Green", "Grey", "Red"]
LtaService = Literal["179", "179A", "179B", "199"]
RouteFilter = Literal[CampusRoute, LtaService]
CAMPUS_ROUTES = get_args(CampusRoute)
LTA_SERVICES = get_args(LtaService)
ArrivalSource = Literal["all", "shuttle", "lta"]
Query = Annotated[str, Field(max_length=120)]
