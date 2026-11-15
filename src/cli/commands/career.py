"""Career service commands."""

import typer

from ..helpers import group
from ..execution import application_scope
from ..services import invoke

app = typer.Typer(no_args_is_help=True)
g_appointments = group(default=False)
app.add_typer(g_appointments, name="appointments")
g_auth = group(default=False)
app.add_typer(g_auth, name="auth")
g_employers = group(default=False)
app.add_typer(g_employers, name="employers")
g_events = group(default=False)
app.add_typer(g_events, name="events")
g_internships = group(default=False)
app.add_typer(g_internships, name="internships")
g_opportunities = group(default=False)
app.add_typer(g_opportunities, name="opportunities")
g_resources = group(default=False)
app.add_typer(g_resources, name="resources")


@g_auth.command("status")
def cmd_auth_status(json_output: bool = typer.Option(False, "--json", "-j")):
    """Report whether shared NTU keyring credentials can be read and whether this process has verified CareerAxis login; does not log in."""
    with application_scope() as application:
        return invoke(application.careeraxis_session.status, {}, json_output)


@g_opportunities.command("search")
def cmd_opportunities_search(
    query: str = typer.Argument(""),
    page: int = typer.Option(1, "--page", "-p"),
    limit: int = typer.Option(20, "--limit", "-l"),
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
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
    url: str,
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
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
    query: str = typer.Argument(""),
    page: int = typer.Option(1, "--page", "-p"),
    limit: int = typer.Option(20, "--limit", "-l"),
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
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
    query: str = typer.Argument(""),
    page: int = typer.Option(1, "--page", "-p"),
    limit: int = typer.Option(20, "--limit", "-l"),
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
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
    name: str = typer.Argument(""),
    current_opportunities_only: bool = typer.Option(False, "--current-only"),
    page: int = typer.Option(1, "--page", "-p"),
    limit: int = typer.Option(20, "--limit", "-l"),
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
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
    query: str = typer.Argument(""),
    page: int = typer.Option(1, "--page", "-p"),
    limit: int = typer.Option(20, "--limit", "-l"),
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
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
    query: str = typer.Argument(""),
    page: int = typer.Option(1, "--page", "-p"),
    limit: int = typer.Option(20, "--limit", "-l"),
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
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
    url: str,
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Read the visible details for a CareerAxis event, resource document, employer, appointment topic, or internship posting URL returned by a CareerAxis search tool."""
    with application_scope() as application:
        return invoke(
            application.careeraxis.get_portal_record,
            {"url": url, "refresh": refresh},
            json_output,
        )
