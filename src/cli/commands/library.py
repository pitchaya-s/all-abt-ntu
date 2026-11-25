"""Library service commands."""

from typing import Annotated, Literal, Optional

import typer

from ..helpers import group
from ..execution import application_scope
from ..services import invoke
from ..renderers import library as views

app = typer.Typer(
    no_args_is_help=True, help="Search library resources and explore facilities."
)
g_facilities = group(default=True)
app.add_typer(
    g_facilities, name="facilities", help="Explore library facilities and schedules."
)
g_map = group(default=False)
app.add_typer(g_map, name="map", help="Check public facility map availability.")


@app.command("search")
def cmd_search(
    query: str = typer.Argument(..., help="Search text or keywords."),
    field: Annotated[
        Literal["any", "title", "creator", "isbn", "issn", "sub"],
        typer.Option(help="Which field to search, such as title, creator, or ISBN."),
    ] = "any",
    match: Annotated[
        Literal["contains", "exact"],
        typer.Option(
            help="How the search should match the selected field. Choices: contains, exact. Default: contains."
        ),
    ] = "contains",
    resource_type: Annotated[
        Optional[str], typer.Option(help="The published resource-type facet token.")
    ] = None,
    limit: int = typer.Option(10, "--limit", "-l", help="Maximum number of results."),
    offset: int = typer.Option(0, "--offset", help="Number of results to skip."),
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Search NTU OneSearch for books, articles, journals and other catalogue resources."""
    with application_scope() as application:
        return invoke(
            application.library.search,
            {
                "query": query,
                "field": field,
                "match": match,
                "resource_type": resource_type,
                "limit": limit,
                "offset": offset,
                "refresh": refresh,
            },
            json_output,
            presenter=views.search,
        )


@app.command("record")
def cmd_record(
    record_id: Annotated[
        str,
        typer.Argument(help="Record ID from ntu library search."),
    ],
    context: Annotated[
        Literal["L", "PC"],
        typer.Option(
            help="The library search context: local catalogue (L) or broader discovery (PC). Choices: L, PC. Default: L."
        ),
    ] = "L",
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Read a OneSearch record's bibliographic metadata, descriptions, subjects, identifiers and published access links."""
    with application_scope() as application:
        return invoke(
            application.library.get_record,
            {"record_id": record_id, "context": context, "refresh": refresh},
            json_output,
            presenter=views.record,
        )


@app.command("availability")
def cmd_availability(
    record_id: Annotated[
        str,
        typer.Argument(help="Record ID from ntu library search."),
    ],
    context: Annotated[
        Literal["L", "PC"],
        typer.Option(
            help="The library search context: local catalogue (L) or broader discovery (PC). Choices: L, PC. Default: L."
        ),
    ] = "L",
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Read published physical holdings with library, location, call number and status, plus institutional full-text service links and access notes."""
    with application_scope() as application:
        return invoke(
            application.library.get_availability,
            {"record_id": record_id, "context": context, "refresh": refresh},
            json_output,
            presenter=views.availability,
        )


@g_facilities.command("__default__", hidden=True)
def cmd_facilities_default(
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """List NTU Library facility categories, library/floor maps and closure notices."""
    with application_scope() as application:
        return invoke(
            application.library_facilities.list_facilities,
            {"refresh": refresh},
            json_output,
            presenter=views.facilities_default,
        )


@g_map.command("availability")
def cmd_map_availability(
    map_slug: Annotated[
        str, typer.Argument(help="The library map slug returned by facility discovery.")
    ],
    date: str = typer.Option(..., "--date", help="Date in YYYY-MM-DD format."),
    time: str = typer.Option(..., "--time", help="Time in 24-hour HH:MM format."),
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Read seat/room booking statuses for a library map at date YYYY-MM-DD and time HH:MM in Singapore."""
    with application_scope() as application:
        return invoke(
            application.library_facilities.get_map_availability,
            {"map_slug": map_slug, "date": date, "time": time, "refresh": refresh},
            json_output,
            presenter=views.map_availability,
        )


@g_facilities.command("schedule")
def cmd_facilities_schedule(
    date: str = typer.Option(..., "--date", help="Date in YYYY-MM-DD format."),
    space_id: Optional[int] = typer.Option(
        None,
        "--space",
        help="The space ID returned by the relevant listing or details command.",
    ),
    location_id: Optional[int] = typer.Option(
        None,
        "--location",
        help="The location ID returned by the relevant listing or details command.",
    ),
    group_id: Optional[int] = typer.Option(
        None,
        "--group",
        help="The group ID returned by the relevant listing or details command.",
    ),
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Read a day's LibFacilities room/seat time grid, room description and source status classes."""
    with application_scope() as application:
        return invoke(
            application.library_session.get_schedule,
            {
                "date": date,
                "space_id": space_id,
                "location_id": location_id,
                "group_id": group_id,
                "refresh": refresh,
            },
            json_output,
            presenter=views.facilities_schedule,
        )


g_facilities.command("list")(cmd_facilities_default)
