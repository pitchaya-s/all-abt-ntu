"""One Stop catalog commands."""

from typing import Annotated, Literal, Optional

import typer

from ...execution import application_scope
from ...helpers import group
from ...renderers import onestop as views
from ...services import invoke

app = group(default=False)


@app.command("categories")
def cmd_catalog_categories(
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """List the signed-in student's visible One Stop catalog categories and subcategories, parent IDs and published item counts."""
    with application_scope() as application:
        return invoke(
            application.onestop.list_categories,
            {"refresh": refresh},
            json_output,
            presenter=views.catalog_categories,
        )


@app.command("search")
def cmd_catalog_search(
    query: str = typer.Argument("", help="Optional search text or keywords."),
    category_id: Optional[str] = typer.Option(
        None,
        "--category",
        help="The category ID returned by the relevant listing or details command.",
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
    """Search the student's One Stop service catalog with query, or browse one category_id."""
    with application_scope() as application:
        return invoke(
            application.onestop.list_catalog_items,
            {
                "query": query,
                "category_id": category_id,
                "limit": limit,
                "offset": offset,
                "refresh": refresh,
            },
            json_output,
            presenter=views.catalog_search,
        )


@app.command("item")
def cmd_catalog_item(
    item_id: Annotated[
        str,
        typer.Argument(
            help="The item ID returned by the relevant listing or details command."
        ),
    ],
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Read a native One Stop form's description, current visible field labels/types, mandatory flags and choices."""
    with application_scope() as application:
        return invoke(
            application.onestop.get_catalog_item,
            {"item_id": item_id, "refresh": refresh},
            json_output,
            presenter=views.catalog_item,
        )


@app.command("favourite")
def cmd_catalog_favourite(
    item_id: Annotated[
        str,
        typer.Argument(
            help="The item ID returned by the relevant listing or details command."
        ),
    ],
    category_id: str = typer.Option(
        ...,
        "--category",
        help="The category ID returned by the relevant listing or details command.",
    ),
    favourite: Literal["on", "off"] = typer.Option(
        ..., "--state", help="The requested favourite state. Choices: on, off."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Set a catalog item's favourite state through its category's native control."""
    with application_scope() as application:
        return invoke(
            application.onestop_favourites.set_catalog_favourite,
            {
                "category_id": category_id,
                "item_id": item_id,
                "favourite": favourite == "on",
            },
            json_output,
            side_effect=True,
            presenter=views.catalog_favourite,
        )
