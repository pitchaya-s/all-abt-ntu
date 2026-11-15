"""Map service commands."""

from typing import Literal, Optional

import typer

from ..execution import application_scope
from ..services import invoke

app = typer.Typer(no_args_is_help=True)


@app.command("campuses")
def cmd_campuses(
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """List campuses in NTU's MazeMap collection with IDs and center coordinates."""
    with application_scope() as application:
        return invoke(
            application.mazemap.list_campuses, {"refresh": refresh}, json_output
        )


@app.command("buildings")
def cmd_buildings(
    campus_id: int = typer.Option(2123, "--campus"),
    query: Optional[str] = None,
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """List campus buildings and their floor IDs/names/levels."""
    with application_scope() as application:
        return invoke(
            application.mazemap.list_buildings,
            {"campus_id": campus_id, "query": query, "refresh": refresh},
            json_output,
        )


@app.command("search")
def cmd_search(
    query: str,
    campus_id: Optional[int] = typer.Option(None, "--campus"),
    limit: int = typer.Option(10, "--limit", "-l"),
    offset: int = 0,
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Search NTU rooms, venues and amenities by code, name or category, including aliases such as TR+7."""
    with application_scope() as application:
        return invoke(
            application.mazemap.search_places,
            {
                "query": query,
                "campus_id": campus_id,
                "limit": limit,
                "offset": offset,
                "refresh": refresh,
            },
            json_output,
        )


@app.command("place")
def cmd_place(
    poi_id: int,
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Read one NTU place's location, aliases, building, floor, categories and published description/capacity."""
    with application_scope() as application:
        return invoke(
            application.mazemap.get_place,
            {"poi_id": poi_id, "refresh": refresh},
            json_output,
        )


@app.command("directions")
def cmd_directions(
    from_poi_id: int,
    to_poi_id: int,
    constraint: Literal[
        "NO_CONSTRAINT", "PREFER_ACCESSIBLE", "REQUIRE_ACCESSIBLE"
    ] = "NO_CONSTRAINT",
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    accessible: bool = typer.Option(False, "--accessible"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Get walking routes between two NTU POIs, estimated metres/seconds and English instructions where available."""
    with application_scope() as application:
        if accessible:
            if constraint != "NO_CONSTRAINT":
                raise typer.BadParameter("Use --accessible or --constraint, not both.")
            constraint = "REQUIRE_ACCESSIBLE"
        return invoke(
            application.mazemap.get_directions,
            {
                "from_poi_id": from_poi_id,
                "to_poi_id": to_poi_id,
                "constraint": constraint,
                "refresh": refresh,
            },
            json_output,
        )
