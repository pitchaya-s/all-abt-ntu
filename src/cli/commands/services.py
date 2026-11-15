"""Services service commands."""

from typing import Optional

import typer

from ..execution import application_scope
from ..services import invoke

app = typer.Typer(no_args_is_help=True)


@app.command("search")
def cmd_search(
    query: str = typer.Argument(""),
    type_id: Optional[str] = typer.Option(None, "--type"),
    category_id: Optional[str] = typer.Option(None, "--category"),
    location_contains: str = typer.Option("", "--location"),
    limit: int = typer.Option(20, "--limit", "-l"),
    offset: int = 0,
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
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
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """List official campus service type and category labels with filter IDs."""
    with application_scope() as application:
        return invoke(
            application.campus_services.list_filters, {"refresh": refresh}, json_output
        )
