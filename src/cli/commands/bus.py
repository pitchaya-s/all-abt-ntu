"""Bus service commands."""

from typing import Literal, Optional

import typer

from ..execution import application_scope
from ..services import invoke

app = typer.Typer(no_args_is_help=True)


@app.command("routes")
def cmd_routes(json_output: bool = typer.Option(False, "--json", "-j")):
    """List public NTU shuttle routes and their published display colors."""
    with application_scope() as application:
        return invoke(application.omnibus.list_routes, {}, json_output)


@app.command("stops")
def cmd_stops(
    query: str = typer.Argument(""),
    route_code: Optional[
        Literal["Blue", "Brown", "Green", "Grey", "Red", "179", "179A", "199"]
    ] = typer.Option(None, "--route"),
    limit: int = typer.Option(20, "--limit", "-l"),
    offset: int = 0,
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Search NTU shuttle and LTA bus stops by stop name or code, optionally limited to a route/service."""
    with application_scope() as application:
        return invoke(
            application.omnibus.list_stops,
            {
                "query": query,
                "route_code": route_code,
                "limit": limit,
                "offset": offset,
            },
            json_output,
        )


@app.command("arrivals")
def cmd_arrivals(
    route_filter: Optional[
        Literal["Blue", "Brown", "Green", "Grey", "Red", "179", "179A", "199"]
    ] = typer.Option(None, "--route"),
    stop_query: str = typer.Option("", "--stop"),
    source: Literal["all", "shuttle", "lta"] = "all",
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Get arrival estimates for NTU shuttles and/or LTA services 179, 179A, and 199."""
    with application_scope() as application:
        return invoke(
            application.omnibus.get_arrivals,
            {"route_filter": route_filter, "stop_query": stop_query, "source": source},
            json_output,
        )


@app.command("live")
def cmd_live(
    route_code: Literal["Blue", "Brown", "Green", "Grey", "Red"] = typer.Option(
        "Blue", "--route"
    ),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Get current live vehicle positions for one NTU campus shuttle route."""
    with application_scope() as application:
        return invoke(
            application.omnibus.get_live_buses, {"route_code": route_code}, json_output
        )


@app.command("status")
def cmd_status(
    route_code: Literal["Blue", "Brown", "Green", "Grey", "Red"] = typer.Option(
        "Blue", "--route"
    ),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Get the published first/last bus schedule, public-holiday/special-day flags, and temporary notices for an NTU campus shuttle route."""
    with application_scope() as application:
        return invoke(
            application.omnibus.get_service_status,
            {"route_code": route_code},
            json_output,
        )
