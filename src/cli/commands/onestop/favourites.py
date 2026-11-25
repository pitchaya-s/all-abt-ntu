"""One Stop favourites commands."""

from typing import Annotated

import typer

from ...execution import application_scope
from ...helpers import group
from ...renderers import onestop as views
from ...services import invoke

app = group(default=True)


@app.command("__default__", hidden=True)
def cmd_favourites_default(
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Read your saved catalog favourites and which are pinned to the homepage."""
    with application_scope() as application:
        return invoke(
            application.onestop_favourites.list,
            {},
            json_output,
            presenter=views.favourites_default,
        )


@app.command("pin")
def cmd_favourites_pin(
    favourite_id: Annotated[
        str,
        typer.Argument(
            help="The favourite ID returned by the relevant listing or details command."
        ),
    ],
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Pin a saved favourite to the homepage."""
    with application_scope() as application:
        return invoke(
            application.onestop_favourites.update,
            {"favourite_id": favourite_id, "action": "pin"},
            json_output,
            side_effect=True,
            presenter=views.favourites_pin,
        )


@app.command("unpin")
def cmd_favourites_unpin(
    favourite_id: Annotated[
        str,
        typer.Argument(
            help="The favourite ID returned by the relevant listing or details command."
        ),
    ],
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Unpin a favourite from the homepage."""
    with application_scope() as application:
        return invoke(
            application.onestop_favourites.update,
            {"favourite_id": favourite_id, "action": "unpin"},
            json_output,
            side_effect=True,
            presenter=views.favourites_unpin,
        )


@app.command("remove")
def cmd_favourites_remove(
    favourite_id: Annotated[
        str,
        typer.Argument(
            help="The favourite ID returned by the relevant listing or details command."
        ),
    ],
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Remove a saved favourite."""
    with application_scope() as application:
        return invoke(
            application.onestop_favourites.update,
            {"favourite_id": favourite_id, "action": "remove"},
            json_output,
            side_effect=True,
            presenter=views.favourites_remove,
        )


@app.command("clear")
def cmd_favourites_clear(
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Remove eligible saved favourites."""
    with application_scope() as application:
        return invoke(
            application.onestop_favourites.update,
            {"action": "clear"},
            json_output,
            side_effect=True,
            presenter=views.favourites_clear,
        )
