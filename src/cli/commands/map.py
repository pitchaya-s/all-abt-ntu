"""Map service commands."""

from typing import Annotated, Literal, Optional

import typer

from ..execution import application_scope
from ..services import invoke

app = typer.Typer(
    no_args_is_help=True, help="Find campus places and walking directions."
)


@app.command("campuses")
def cmd_campuses(
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """List campuses in NTU's MazeMap collection with IDs and center coordinates."""
    with application_scope() as application:
        return invoke(
            application.mazemap.list_campuses, {"refresh": refresh}, json_output
        )


@app.command("buildings")
def cmd_buildings(
    campus_id: int = typer.Option(
        2123,
        "--campus",
        help="The campus ID; use the campus listing to find available IDs. Default: 2123.",
    ),
    query: Annotated[
        Optional[str],
        typer.Option(
            help="The search terms. Quote multiword text so the shell passes it as one argument."
        ),
    ] = None,
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
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
    query: str = typer.Argument(..., help="Search text or keywords."),
    campus_id: Optional[int] = typer.Option(
        None,
        "--campus",
        help="The campus ID; use the campus listing to find available IDs.",
    ),
    limit: int = typer.Option(10, "--limit", "-l", help="Maximum number of results."),
    offset: int = typer.Option(0, "--offset", help="Number of results to skip."),
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
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
    poi_id: Annotated[
        int, typer.Argument(help="The place's POI ID, returned by the place search.")
    ],
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
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
    from_poi_id: Annotated[
        int,
        typer.Argument(
            help="The starting place's POI ID, returned by the place search."
        ),
    ],
    to_poi_id: Annotated[
        int,
        typer.Argument(
            help="The destination place's POI ID, returned by the place search."
        ),
    ],
    constraint: Annotated[
        Literal["NO_CONSTRAINT", "PREFER_ACCESSIBLE", "REQUIRE_ACCESSIBLE"],
        typer.Option(
            help="The route accessibility constraint. Choices: NO_CONSTRAINT, PREFER_ACCESSIBLE, REQUIRE_ACCESSIBLE. Default: NO_CONSTRAINT."
        ),
    ] = "NO_CONSTRAINT",
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    accessible: bool = typer.Option(
        False,
        "--accessible",
        help="Require an accessible walking route. Use this or --constraint, not both.",
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
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
