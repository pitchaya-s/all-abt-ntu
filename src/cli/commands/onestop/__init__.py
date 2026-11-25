"""Commands for the One Stop student portal."""

import typer

from ...execution import application_scope
from ...renderers import onestop as views
from ...services import invoke
from . import (
    appointments,
    attachments,
    auth,
    cart,
    catalog,
    favourites,
    knowledge,
    payments,
    profile,
    requests,
)

app = typer.Typer(
    no_args_is_help=True,
    help="Access One Stop requests, appointments, and account services.",
)
app.add_typer(
    appointments.app, name="appointments", help="List appointments or book from a form."
)
app.add_typer(
    attachments.app, name="attachments", help="List, download, or manage attachments."
)
app.add_typer(auth.app, name="auth", help="Check One Stop authentication.")
app.add_typer(
    cart.app, name="cart", help="View or manage the shopping cart and checkout."
)
app.add_typer(catalog.app, name="catalog", help="Browse catalog categories and forms.")
app.add_typer(
    favourites.app, name="favourites", help="View or manage catalog favourites."
)
app.add_typer(
    knowledge.app, name="knowledge", help="Search and interact with knowledge articles."
)
app.add_typer(
    payments.app,
    name="payments",
    help="Explore payment services and prepare checkout links.",
)
app.add_typer(profile.app, name="profile", help="View or update your profile.")
app.add_typer(
    requests.app, name="requests", help="Browse requests or apply for a service."
)


@app.command("dashboard")
def cmd_dashboard(
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Read your One Stop homepage announcements, actions/payment links, upcoming appointments and popular links."""
    with application_scope() as application:
        return invoke(
            application.onestop_portal.dashboard,
            {},
            json_output,
            presenter=views.dashboard,
        )


@app.command("announcements")
def cmd_announcements(
    limit: int = typer.Option(20, "--limit", "-l", help="Maximum number of results."),
    offset: int = typer.Option(0, "--offset", help="Number of results to skip."),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Read One Stop announcements, summaries and links from the native announcements collection with local pagination."""
    with application_scope() as application:
        return invoke(
            application.onestop_portal.list_announcements,
            {"limit": limit, "offset": offset},
            json_output,
            presenter=views.announcements,
        )


@app.command("actions")
def cmd_actions(
    limit: int = typer.Option(20, "--limit", "-l", help="Maximum number of results."),
    offset: int = typer.Option(0, "--offset", help="Number of results to skip."),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Read your One Stop to-do/billing actions and their published due dates and payment links."""
    with application_scope() as application:
        return invoke(
            application.onestop_portal.list_actions,
            {"limit": limit, "offset": offset},
            json_output,
            presenter=views.actions,
        )


@app.command("links")
def cmd_links(
    limit: int = typer.Option(20, "--limit", "-l", help="Maximum number of results."),
    offset: int = typer.Option(0, "--offset", help="Number of results to skip."),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """List links on One Stop's Popular Sites page, preserving native catalog, knowledge and external destinations."""
    with application_scope() as application:
        return invoke(
            application.onestop_portal.list_popular_links,
            {"limit": limit, "offset": offset},
            json_output,
            presenter=views.links,
        )
