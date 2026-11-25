"""One Stop profile commands."""

from typing import Annotated, Literal

import typer

from ...execution import application_scope
from ...helpers import group
from ...renderers import onestop as views
from ...services import invoke

app = group(default=True)


@app.command("__default__", hidden=True)
def cmd_profile_default(
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Read your own displayed profile fields, editable flags, preferences/choices, notification setting and picture-upload capability."""
    with application_scope() as application:
        return invoke(
            application.onestop_portal.get_profile,
            {},
            json_output,
            presenter=views.profile_default,
        )


@app.command("set")
def cmd_profile_set(
    field_name: Annotated[str, typer.Argument(help="The name of the field to update.")],
    value: Annotated[
        str, typer.Argument(help="The value to set for the named field or preference.")
    ],
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Update one displayed editable own-profile field through its native inline editor."""
    with application_scope() as application:
        return invoke(
            application.onestop_portal.update_profile,
            {"field_name": field_name, "value": value},
            json_output,
            side_effect=True,
            presenter=views.profile_set,
        )


@app.command("picture")
def cmd_profile_picture(
    file_path: Annotated[str, typer.Argument(help="Path to the file to upload.")],
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Upload the explicitly selected local image as your own ServiceNow profile picture using the native file input."""
    with application_scope() as application:
        return invoke(
            application.onestop_portal.update_picture,
            {"file_path": file_path},
            json_output,
            side_effect=True,
            presenter=views.profile_picture,
        )


@app.command("notifications")
def cmd_profile_notifications(
    enabled: Annotated[
        Literal["on", "off"],
        typer.Argument(
            help="Choose on to enable the setting or off to disable it. Choices: on, off."
        ),
    ],
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Enable or disable your ServiceNow notification preference."""
    with application_scope() as application:
        return invoke(
            application.onestop_portal.set_notifications,
            {"enabled": enabled == "on"},
            json_output,
            side_effect=True,
            presenter=views.profile_notifications,
        )


@app.command("preference")
def cmd_profile_preference(
    name: Annotated[
        Literal[
            "accessibility",
            "voice_input",
            "analytics",
            "timezone",
            "language",
            "communication_channels",
        ],
        typer.Argument(
            help="The name of the item, setting or field to use. Choices: accessibility, voice_input, analytics, timezone, language, communication_channels."
        ),
    ],
    value: Annotated[
        str, typer.Argument(help="The value to set for the named field or preference.")
    ],
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Set an enabled own preference returned by get_profile."""
    with application_scope() as application:
        return invoke(
            application.onestop_portal.set_preference,
            {"name": name, "value": value},
            json_output,
            side_effect=True,
            presenter=views.profile_preference,
        )
