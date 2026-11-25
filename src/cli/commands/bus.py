"""Bus service commands."""

from typing import Annotated, Literal, Optional
from functools import partial

import typer

from omnibus.contracts import RouteFilter

from ..execution import application_scope
from ..output import render
from ..services import invoke
from ..renderers import bus as views

app = typer.Typer(
    no_args_is_help=True, help="Check shuttle routes, stops, arrivals, and status."
)


@app.command("routes")
def cmd_routes(
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """List public NTU shuttle routes and their published display colors."""
    with application_scope() as application:
        return invoke(
            application.omnibus.list_routes, {}, json_output, presenter=views.routes
        )


@app.command("stops")
def cmd_stops(
    query: str = typer.Argument("", help="Optional search text or keywords."),
    route_code: Optional[RouteFilter] = typer.Option(
        None,
        "--route",
        help="Campus shuttle route or supported LTA service.",
    ),
    limit: int = typer.Option(20, "--limit", "-l", help="Maximum number of results."),
    offset: int = typer.Option(0, "--offset", help="Number of results to skip."),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Search NTU shuttle and LTA bus stops by stop name or code, optionally limited to a route/service."""
    with application_scope() as application:
        arguments = {
            "query": query,
            "route_code": route_code,
            "limit": limit,
            "offset": offset,
        }
        page = invoke(
            application.omnibus.list_stops, arguments, json_output, show_result=False
        )
        if json_output or not page.stops:
            render(page, json_output=json_output, presenter=views.stops)
            return page
        if offset == 0 and page.next_offset is None:
            render(page, presenter=partial(views.stops, related_stops=page.stops))
            return page

        # Stop records are paginated by route. Collect cached pages so each stop
        # on the requested page can show all of its matching routes.
        related = []
        cursor = 0
        for _ in range(100):
            batch = invoke(
                application.omnibus.list_stops,
                {**arguments, "limit": 100, "offset": cursor},
                False,
                show_result=False,
            )
            related.extend(batch.stops)
            if batch.next_offset is None:
                break
            if batch.next_offset <= cursor:
                raise ValueError(
                    "The bus service returned an invalid pagination cursor."
                )
            cursor = batch.next_offset
        else:
            raise ValueError("The bus service returned too many pages of stops.")
        render(page, presenter=partial(views.stops, related_stops=related))
        return page


@app.command("arrivals")
def cmd_arrivals(
    route_filter: Optional[RouteFilter] = typer.Option(
        None,
        "--route",
        help="Campus shuttle route or supported LTA service.",
    ),
    stop_query: str = typer.Option("", "--stop", help="Search by stop name."),
    source: Annotated[
        Literal["all", "shuttle", "lta"],
        typer.Option(
            help="Which arrival-data source to use. Choices: all, shuttle, lta. Default: all."
        ),
    ] = "all",
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Get arrival estimates for NTU shuttles and LTA buses."""
    with application_scope() as application:
        return invoke(
            application.omnibus.get_arrivals,
            {"route_filter": route_filter, "stop_query": stop_query, "source": source},
            json_output,
            presenter=views.arrivals,
        )


@app.command("live")
def cmd_live(
    route_code: Literal["Blue", "Brown", "Green", "Grey", "Red"] = typer.Option(
        "Blue",
        "--route",
        help="The published shuttle route or supported bus service. Choices: Blue, Brown, Green, Grey, Red. Default: Blue.",
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Get current live vehicle positions for one NTU campus shuttle route."""
    with application_scope() as application:
        return invoke(
            application.omnibus.get_live_buses,
            {"route_code": route_code},
            json_output,
            presenter=views.live,
        )


@app.command("status")
def cmd_status(
    route_code: Literal["Blue", "Brown", "Green", "Grey", "Red"] = typer.Option(
        "Blue",
        "--route",
        help="The published shuttle route or supported bus service. Choices: Blue, Brown, Green, Grey, Red. Default: Blue.",
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Get the published first/last bus schedule, public-holiday/special-day flags, and temporary notices for an NTU campus shuttle route."""
    with application_scope() as application:
        return invoke(
            application.omnibus.get_service_status,
            {"route_code": route_code},
            json_output,
            presenter=views.status,
        )
