"""Faculty service commands."""

from typing import Optional

import typer

from ..execution import application_scope
from ..services import invoke

app = typer.Typer(no_args_is_help=True)


@app.command("search")
def cmd_search(
    query: str = typer.Argument(""),
    interest_id: Optional[str] = typer.Option(None, "--interest"),
    page: int = typer.Option(1, "--page", "-p"),
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
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
        )


@app.command("interests")
def cmd_interests(
    query: str = typer.Argument(""),
    limit: int = typer.Option(50, "--limit", "-l"),
    offset: int = 0,
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """List current faculty research-interest labels and filter IDs from NTU's directory form."""
    with application_scope() as application:
        return invoke(
            application.faculty.list_interests,
            {"query": query, "limit": limit, "offset": offset, "refresh": refresh},
            json_output,
        )
