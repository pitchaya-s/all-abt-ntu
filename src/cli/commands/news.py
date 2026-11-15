"""News service commands."""

from typing import Literal, Optional

import typer

from ..execution import application_scope
from ..services import invoke

app = typer.Typer(no_args_is_help=True)


@app.command("search")
def cmd_search(
    query: str = typer.Argument(""),
    category_id: Optional[str] = typer.Option(None, "--category"),
    sort: Literal["latest", "oldest"] = "latest",
    page: int = typer.Option(1, "--page", "-p"),
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
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
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """List current news category labels and filter IDs from NTU's official news form."""
    with application_scope() as application:
        return invoke(
            application.news.list_categories, {"refresh": refresh}, json_output
        )


@app.command("article")
def cmd_article(
    url: str,
    offset: int = 0,
    max_chars: int = 12000,
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Read the published text of an NTU /news/detail/ article URL returned by news_search."""
    with application_scope() as application:
        return invoke(
            application.news.get_article,
            {"url": url, "offset": offset, "max_chars": max_chars, "refresh": refresh},
            json_output,
        )
