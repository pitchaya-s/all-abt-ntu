"""Input constraints for NTU shuttle and public bus lookups."""

from typing import Annotated, Literal

from pydantic import Field

CampusRoute = Literal["Blue", "Brown", "Green", "Grey", "Red"]
RouteFilter = Literal["Blue", "Brown", "Green", "Grey", "Red", "179", "179A", "199"]
ArrivalSource = Literal["all", "shuttle", "lta"]
Query = Annotated[str, Field(max_length=120)]
