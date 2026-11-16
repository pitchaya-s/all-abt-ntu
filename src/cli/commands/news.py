"""News service commands."""

from typing import Annotated, Literal, Optional

import typer

from ..execution import application_scope
from ..services import invoke

app = typer.Typer(no_args_is_help=True, help="Browse NTU news and articles.")


@app.command("search")
def cmd_search(
    query: str = typer.Argument("", help="Optional search text or keywords."),
    category_id: Optional[str] = typer.Option(
        None,
        "--category",
        help="The category ID returned by the relevant listing or details command.",
    ),
    sort: Annotated[
        Literal["latest", "oldest"],
        typer.Option(
            help="The order in which results should be returned. Choices: latest, oldest. Default: latest."
        ),
    ] = "latest",
    page: int = typer.Option(1, "--page", "-p", help="Result page number."),
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Search public NTU news by keyword and optional category, sorted latest or oldest."""
    with application_scope() as application:
        return invoke(
            application.news.search,
            {
                "query": query,
                "category_id": category_id,
                "sort": sort,
                "page": page,
                "refresh": refresh,
            },
            json_output,
        )


@app.command("categories")
def cmd_categories(
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """List current news category labels and filter IDs from NTU's official news form."""
    with application_scope() as application:
        return invoke(
            application.news.list_categories, {"refresh": refresh}, json_output
        )


@app.command("article")
def cmd_article(
    url: Annotated[
        str,
        typer.Argument(help="The URL of the record or article returned by a search."),
    ],
    offset: int = typer.Option(
        0, "--offset", help="Number of article characters to skip."
    ),
    max_chars: Annotated[
        int,
        typer.Option(
            help="Maximum number of text characters to return. Default: 12000."
        ),
    ] = 12000,
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Read the published text of an NTU /news/detail/ article URL returned by news_search."""
    with application_scope() as application:
        return invoke(
            application.news.get_article,
            {"url": url, "offset": offset, "max_chars": max_chars, "refresh": refresh},
            json_output,
        )
