"""Library service commands."""

from typing import Literal, Optional

import typer

from ..helpers import group
from ..execution import application_scope
from ..services import invoke

app = typer.Typer(no_args_is_help=True)
g_facilities = group(default=True)
app.add_typer(g_facilities, name="facilities")
g_map = group(default=False)
app.add_typer(g_map, name="map")


@app.command("search")
def cmd_search(
    query: str,
    field: Literal["any", "title", "creator", "isbn", "issn", "sub"] = "any",
    match: Literal["contains", "exact"] = "contains",
    resource_type: Optional[str] = None,
    limit: int = typer.Option(10, "--limit", "-l"),
    offset: int = 0,
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
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
        )


@app.command("record")
def cmd_record(
    record_id: str,
    context: Literal["L", "PC"] = "L",
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Read a OneSearch record's bibliographic metadata, descriptions, subjects, identifiers and published access links."""
    with application_scope() as application:
        return invoke(
            application.library.get_record,
            {"record_id": record_id, "context": context, "refresh": refresh},
            json_output,
        )


@app.command("availability")
def cmd_availability(
    record_id: str,
    context: Literal["L", "PC"] = "L",
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Read published physical holdings with library, location, call number and status, plus institutional full-text service links and access notes."""
    with application_scope() as application:
        return invoke(
            application.library.get_availability,
            {"record_id": record_id, "context": context, "refresh": refresh},
            json_output,
        )


@g_facilities.command("__default__", hidden=True)
def cmd_facilities_default(
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """List NTU Library facility categories, library/floor maps and closure notices."""
    with application_scope() as application:
        return invoke(
            application.library_facilities.list_facilities,
            {"refresh": refresh},
            json_output,
        )


@g_map.command("availability")
def cmd_map_availability(
    map_slug: str,
    date: str = typer.Option(..., "--date"),
    time: str = typer.Option(..., "--time"),
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Read seat/room booking statuses for a library map at date YYYY-MM-DD and time HH:MM in Singapore."""
    with application_scope() as application:
        return invoke(
            application.library_facilities.get_map_availability,
            {"map_slug": map_slug, "date": date, "time": time, "refresh": refresh},
            json_output,
        )


@g_facilities.command("schedule")
def cmd_facilities_schedule(
    date: str = typer.Option(..., "--date"),
    space_id: Optional[int] = typer.Option(None, "--space"),
    location_id: Optional[int] = typer.Option(None, "--location"),
    group_id: Optional[int] = typer.Option(None, "--group"),
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
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
        )


g_facilities.command("list")(cmd_facilities_default)
