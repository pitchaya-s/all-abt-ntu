"""Faculty service commands."""

from typing import Optional

import typer

from ..execution import application_scope
from ..services import invoke
from ..renderers import faculty as views

app = typer.Typer(no_args_is_help=True, help="Find NTU faculty and research interests.")


@app.command("search")
def cmd_search(
    query: str = typer.Argument("", help="Optional search text or keywords."),
    interest_id: Optional[str] = typer.Option(
        None,
        "--interest",
        help="The interest ID returned by the relevant listing or details command.",
    ),
    page: int = typer.Option(1, "--page", "-p", help="Result page number."),
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Search NTU's public faculty directory by name, optionally filtered by one research interest."""
    with application_scope() as application:
        return invoke(
            application.faculty.search,
            {
                "query": query,
                "interest_id": interest_id,
                "page": page,
                "refresh": refresh,
            },
            json_output,
            presenter=views.search,
        )


@app.command("interests")
def cmd_interests(
    query: str = typer.Argument("", help="Optional search text or keywords."),
    limit: int = typer.Option(50, "--limit", "-l", help="Maximum number of results."),
    offset: int = typer.Option(0, "--offset", help="Number of results to skip."),
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """List current faculty research-interest labels and filter IDs from NTU's directory form."""
    with application_scope() as application:
        return invoke(
            application.faculty.list_interests,
            {"query": query, "limit": limit, "offset": offset, "refresh": refresh},
            json_output,
            presenter=views.interests,
        )
