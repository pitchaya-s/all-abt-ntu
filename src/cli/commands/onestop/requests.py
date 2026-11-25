"""One Stop requests commands."""

from typing import Annotated, Literal, Optional

import typer

from ...execution import application_scope
from ...helpers import group
from ...renderers import onestop as views
from ...services import invoke
from .workflows import _add_draft_attachments, _fill_draft, _show_workflow

app = group(default=False)


@app.command("list")
def cmd_requests_list(
    status: Annotated[
        Literal["all", "open", "closed"],
        typer.Option(
            help="Restrict the listing to the selected status. Choices: all, open, closed. Default: all."
        ),
    ] = "all",
    kind: Annotated[
        Literal["all", "case", "request"],
        typer.Option(
            help="Restrict the listing to the selected kind of request. Choices: all, case, request. Default: all."
        ),
    ] = "all",
    limit: int = typer.Option(20, "--limit", "-l", help="Maximum number of results."),
    offset: int = typer.Option(0, "--offset", help="Number of results to skip."),
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Read your own open/closed One Stop cases and service requests, expanding native lists up to 500 records."""
    with application_scope() as application:
        return invoke(
            application.onestop.list_my_requests,
            {
                "status": status,
                "kind": kind,
                "limit": limit,
                "offset": offset,
                "refresh": refresh,
            },
            json_output,
            presenter=views.requests_list,
        )


@app.command("show")
def cmd_requests_show(
    request_id: Annotated[
        str,
        typer.Argument(
            help="The request ID returned by the relevant listing or details command."
        ),
    ],
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Read one of your requests after checking request_id against your retrieved personal lists."""
    with application_scope() as application:
        return invoke(
            application.onestop.get_my_request,
            {"request_id": request_id, "refresh": refresh},
            json_output,
            presenter=views.requests_show,
        )


@app.command("activity")
def cmd_requests_activity(
    request_id: Annotated[
        str,
        typer.Argument(
            help="The request ID returned by the relevant listing or details command."
        ),
    ],
    record_id: Annotated[
        Optional[str],
        typer.Option(
            help="A record ID for a request target when the request contains multiple records."
        ),
    ] = None,
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Read visible comments and attachment events on a verified own request/item, plus current reply/upload/state-action permissions."""
    with application_scope() as application:
        return invoke(
            application.onestop_tickets.activity,
            {"request_id": request_id, "record_id": record_id},
            json_output,
            presenter=views.requests_activity,
        )


@app.command("reply")
def cmd_requests_reply(
    request_id: Annotated[
        str,
        typer.Argument(
            help="The request ID returned by the relevant listing or details command."
        ),
    ],
    text: str = typer.Option(
        ..., "--text", help="The text to send. Quote multiword text in the shell."
    ),
    record_id: Annotated[
        Optional[str],
        typer.Option(
            help="A record ID for a request target when the request contains multiple records."
        ),
    ] = None,
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Post a real additional comment to a verified own ticket/item when its current native state permits replying."""
    with application_scope() as application:
        return invoke(
            application.onestop_tickets.reply,
            {"request_id": request_id, "text": text, "record_id": record_id},
            json_output,
            side_effect=True,
            presenter=views.requests_reply,
        )


@app.command("action")
def cmd_requests_action(
    request_id: Annotated[
        str,
        typer.Argument(
            help="The request ID returned by the relevant listing or details command."
        ),
    ],
    action: Annotated[
        Literal["close", "reopen", "accept-solution", "reject-solution"],
        typer.Argument(
            help="The native action to perform; inspect the record for the actions currently available. Choices: close, reopen, accept-solution, reject-solution."
        ),
    ],
    record_id: Annotated[
        Optional[str],
        typer.Option(
            help="A record ID for a request target when the request contains multiple records."
        ),
    ] = None,
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Execute a state action currently offered by the native own-ticket page."""
    with application_scope() as application:
        return invoke(
            application.onestop_tickets.take_action,
            {
                "request_id": request_id,
                "action": action.replace("-", "_"),
                "record_id": record_id,
            },
            json_output,
            side_effect=True,
            presenter=views.requests_action,
        )


@app.command("apply")
def cmd_requests_apply(
    item_id: Annotated[
        str, typer.Argument(help="Catalog item ID returned by catalog search.")
    ],
):
    """Prepare, fill, review and submit a native request in one session."""
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
            draft = _fill_draft(draft)
            draft = _add_draft_attachments(draft)
            if not draft.ready:
                raise typer.BadParameter("The native form is not ready for submission.")
            return invoke(
                application.onestop_forms.submit,
                {"draft_id": draft.draft_id, "action": "submit"},
                False,
                side_effect=True,
                presenter=views.requests_apply,
            )
