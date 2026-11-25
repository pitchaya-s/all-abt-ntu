"""One Stop auth commands."""

import typer

from ...execution import application_scope
from ...helpers import group
from ...renderers import onestop as views
from ...services import invoke

app = group(default=False)


@app.command("status")
def cmd_auth_status(
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Sign in to One Stop and report whether access is verified."""
    with application_scope() as application:
        return invoke(
            application.onestop_session.verify,
            {},
            json_output,
            presenter=views.auth_status,
        )
