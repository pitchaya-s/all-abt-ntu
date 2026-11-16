"""Career service commands."""

from typing import Annotated

import typer

from ..helpers import group
from ..execution import application_scope
from ..services import invoke

app = typer.Typer(
    no_args_is_help=True, help="Explore CareerAxis opportunities and career resources."
)
g_appointments = group(default=False)
app.add_typer(g_appointments, name="appointments", help="Find career-coaching topics.")
g_auth = group(default=False)
app.add_typer(g_auth, name="auth", help="Check CareerAxis authentication.")
g_employers = group(default=False)
app.add_typer(g_employers, name="employers", help="Search employers.")
g_events = group(default=False)
app.add_typer(g_events, name="events", help="Search career events.")
g_internships = group(default=False)
app.add_typer(g_internships, name="internships", help="Search the internship board.")
g_opportunities = group(default=False)
app.add_typer(
    g_opportunities, name="opportunities", help="Search and inspect job opportunities."
)
g_resources = group(default=False)
app.add_typer(g_resources, name="resources", help="Search career resources.")


@g_auth.command("status")
def cmd_auth_status(
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Sign in to CareerAxis and report whether access is verified."""
    with application_scope() as application:
        return invoke(application.careeraxis_session.verify, {}, json_output)


@g_opportunities.command("search")
def cmd_opportunities_search(
    query: str = typer.Argument("", help="Optional search text or keywords."),
    page: int = typer.Option(1, "--page", "-p", help="Result page number."),
    limit: int = typer.Option(20, "--limit", "-l", help="Maximum number of results."),
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Search your authenticated NTU CareerAxis job and internship listings by keyword."""
    with application_scope() as application:
        return invoke(
            application.careeraxis.search_opportunities,
            {"query": query, "page": page, "limit": limit, "refresh": refresh},
            json_output,
        )


@g_opportunities.command("show")
def cmd_opportunities_show(
    url: Annotated[
        str,
        typer.Argument(help="The URL of the record or article returned by a search."),
    ],
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Read the full visible text for an opportunity URL returned by careeraxis_search_opportunities, including HTTPS application links."""
    with application_scope() as application:
        return invoke(
            application.careeraxis.get_opportunity,
            {"url": url, "refresh": refresh},
            json_output,
        )


@g_events.command("search")
def cmd_events_search(
    query: str = typer.Argument("", help="Optional search text or keywords."),
    page: int = typer.Option(1, "--page", "-p", help="Result page number."),
    limit: int = typer.Option(20, "--limit", "-l", help="Maximum number of results."),
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Search authenticated CareerAxis events by keyword."""
    with application_scope() as application:
        return invoke(
            application.careeraxis.search_events,
            {"query": query, "page": page, "limit": limit, "refresh": refresh},
            json_output,
        )


@g_resources.command("search")
def cmd_resources_search(
    query: str = typer.Argument("", help="Optional search text or keywords."),
    page: int = typer.Option(1, "--page", "-p", help="Result page number."),
    limit: int = typer.Option(20, "--limit", "-l", help="Maximum number of results."),
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Search CareerAxis career resources and training documents by keyword."""
    with application_scope() as application:
        return invoke(
            application.careeraxis.search_resources,
            {"query": query, "page": page, "limit": limit, "refresh": refresh},
            json_output,
        )


@g_employers.command("search")
def cmd_employers_search(
    name: str = typer.Argument(
        "", help="The name of the item, setting or field to use."
    ),
    current_opportunities_only: bool = typer.Option(
        False,
        "--current-only",
        help="Limit employers to those with current opportunities.",
    ),
    page: int = typer.Option(1, "--page", "-p", help="Result page number."),
    limit: int = typer.Option(20, "--limit", "-l", help="Maximum number of results."),
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Search CareerAxis employer profiles by name, optionally limiting results to employers with current opportunities."""
    with application_scope() as application:
        return invoke(
            application.careeraxis.search_organisations,
            {
                "name": name,
                "current_opportunities_only": current_opportunities_only,
                "page": page,
                "limit": limit,
                "refresh": refresh,
            },
            json_output,
        )


@g_appointments.command("topics")
def cmd_appointments_topics(
    query: str = typer.Argument("", help="Optional search text or keywords."),
    page: int = typer.Option(1, "--page", "-p", help="Result page number."),
    limit: int = typer.Option(20, "--limit", "-l", help="Maximum number of results."),
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Search CareerAxis career-coaching appointment topics such as internship strategy, interview practice, and resume critique."""
    with application_scope() as application:
        return invoke(
            application.careeraxis.search_appointment_topics,
            {"query": query, "page": page, "limit": limit, "refresh": refresh},
            json_output,
        )


@g_internships.command("search")
def cmd_internships_search(
    query: str = typer.Argument("", help="Optional search text or keywords."),
    page: int = typer.Option(1, "--page", "-p", help="Result page number."),
    limit: int = typer.Option(20, "--limit", "-l", help="Maximum number of results."),
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Search the authenticated CareerAxis Internship workgroup job board by keyword across its visible internship postings."""
    with application_scope() as application:
        return invoke(
            application.careeraxis.search_internship_jobs,
            {"query": query, "page": page, "limit": limit, "refresh": refresh},
            json_output,
        )


@app.command("record")
def cmd_record(
    url: Annotated[
        str,
        typer.Argument(help="The URL of the record or article returned by a search."),
    ],
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Read the visible details for a CareerAxis event, resource document, employer, appointment topic, or internship posting URL returned by a CareerAxis search tool."""
    with application_scope() as application:
        return invoke(
            application.careeraxis.get_portal_record,
            {"url": url, "refresh": refresh},
            json_output,
        )
