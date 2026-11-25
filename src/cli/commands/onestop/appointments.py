"""One Stop appointments commands."""

from typing import Annotated

import typer

from ...execution import application_scope
from ...helpers import group
from ...renderers import onestop as views
from ...services import invoke
from .workflows import _add_draft_attachments, _choose, _fill_draft, _show_workflow

app = group(default=True)


@app.command("__default__", hidden=True)
def cmd_appointments_default(
    limit: int = typer.Option(20, "--limit", "-l", help="Maximum number of results."),
    offset: int = typer.Option(0, "--offset", help="Number of results to skip."),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Read your native upcoming appointment list with appointment numbers, published dates/times and locations."""
    with application_scope() as application:
        return invoke(
            application.onestop_appointments.list,
            {"limit": limit, "offset": offset},
            json_output,
            presenter=views.appointments_default,
        )


@app.command("book")
def cmd_appointments_book(
    item_id: Annotated[
        str, typer.Argument(help="Catalog item ID for an appointment form.")
    ],
):
    """Prepare an appointment form, choose a slot and book it in one session."""
    with application_scope() as application:
        from ...session import session_scope

        with session_scope():
            draft = invoke(
                application.onestop_forms.prepare,
                {"item_id": item_id},
                False,
                show_result=False,
                side_effect=True,
            )
            _show_workflow(draft, views.draft_preview)
            draft = _fill_draft(draft, allow_appointment=True)
            draft = _add_draft_attachments(draft)
            configuration = invoke(
                application.onestop_appointments.configuration,
                {"draft_id": draft.draft_id},
                False,
                show_result=False,
            )
            _show_workflow(configuration, views.appointment_preview)
            if not configuration.enabled:
                raise typer.BadParameter(
                    "The native form does not offer appointment booking."
                )
            date = typer.prompt("Appointment date (YYYY-MM-DD)", err=True)
            slots = invoke(
                application.onestop_appointments.slots,
                {"draft_id": draft.draft_id, "date": date},
                False,
                show_result=False,
            )
            if not slots.slots:
                raise typer.BadParameter(
                    "No appointment slots were returned for that date."
                )
            slot = _choose(slots.slots, "Choose a time").slot_id
            return invoke(
                application.onestop_appointments.book,
                {"draft_id": draft.draft_id, "slot_id": slot},
                False,
                side_effect=True,
                presenter=views.appointments_book,
            )
