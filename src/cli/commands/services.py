"""Services service commands."""

from typing import Optional

import typer

from ..execution import application_scope
from ..services import invoke

app = typer.Typer(no_args_is_help=True, help="Find campus food, shops, and services.")


@app.command("search")
def cmd_search(
    query: str = typer.Argument("", help="Optional search text or keywords."),
    type_id: Optional[str] = typer.Option(
        None,
        "--type",
        help="The type ID returned by the relevant listing or details command.",
    ),
    category_id: Optional[str] = typer.Option(
        None,
        "--category",
        help="The category ID returned by the relevant listing or details command.",
    ),
    location_contains: str = typer.Option(
        "", "--location", help="Match this text in the published location."
    ),
    limit: int = typer.Option(20, "--limit", "-l", help="Maximum number of results."),
    offset: int = typer.Option(0, "--offset", help="Number of results to skip."),
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Find NTU food outlets, shops, clinics and campus services by name/address keyword and optional location substring."""
    with application_scope() as application:
        return invoke(
            application.campus_services.search,
            {
                "query": query,
                "type_id": type_id,
                "category_id": category_id,
                "location_contains": location_contains,
                "limit": limit,
                "offset": offset,
                "refresh": refresh,
            },
            json_output,
        )


@app.command("filters")
def cmd_filters(
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """List official campus service type and category labels with filter IDs."""
    with application_scope() as application:
        return invoke(
            application.campus_services.list_filters, {"refresh": refresh}, json_output
        )
