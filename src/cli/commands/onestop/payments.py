"""One Stop payments commands."""

from typing import Annotated

import typer

from ...execution import application_scope
from ...helpers import group
from ...renderers import onestop as views
from ...services import invoke

app = group(default=False)


@app.command("services")
def cmd_payments_services(
    query: str = typer.Argument("", help="Optional search text or keywords."),
    limit: int = typer.Option(20, "--limit", "-l", help="Maximum number of results."),
    offset: int = typer.Option(0, "--offset", help="Number of results to skip."),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Search/browse services in the student's native payment directory, preserving its active/category/access filter."""
    with application_scope() as application:
        return invoke(
            application.onestop_portal.list_payment_services,
            {"query": query, "limit": limit, "offset": offset},
            json_output,
            presenter=views.payments_services,
        )


@app.command("service")
def cmd_payments_service(
    service_id: Annotated[
        str,
        typer.Argument(
            help="The service ID returned by the relevant listing or details command."
        ),
    ],
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Read a visible payment service's native fixed-amount information."""
    with application_scope() as application:
        return invoke(
            application.onestop_portal.get_payment_service,
            {"service_id": service_id},
            json_output,
            presenter=views.payments_service,
        )


@app.command("checkout-link")
def cmd_payments_checkout_link(
    service_id: Annotated[
        str,
        typer.Argument(
            help="The service ID returned by the relevant listing or details command."
        ),
    ],
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Ask One Stop to prepare a checkout link for a visible payment service."""
    with application_scope() as application:
        return invoke(
            application.onestop_portal.prepare_payment,
            {"service_id": service_id},
            json_output,
            side_effect=True,
            presenter=views.payments_checkout_link,
        )
