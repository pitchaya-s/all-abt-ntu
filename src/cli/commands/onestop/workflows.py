"""Interactive One Stop workflow prompts."""

import typer

from ...execution import application_scope
from ...output import render
from ...renderers import onestop as views
from ...services import invoke


def _show_workflow(value, presenter):
    """Display a review without exposing temporary workflow identifiers."""
    if hasattr(value, "model_dump"):
        render(value, presenter=presenter)
    else:
        render(value)


def _choose(choices, label):
    for index, choice in enumerate(choices, 1):
        typer.echo(f"{index}. {choice.label}", err=True)
    number = typer.prompt(label, type=int, err=True)
    if not 1 <= number <= len(choices):
        raise typer.BadParameter("Choose a number from the displayed list.")
    return choices[number - 1]


def _fill_draft(draft, *, allow_appointment=False):
    """Fill required fields, optionally edit others, and show each native preview."""
    with application_scope() as application:
        for _ in range(10):
            missing = set(draft.missing_fields) | set(draft.invalid_fields)
            if allow_appointment:
                missing.discard("appointment")
            if not missing:
                editable = [field for field in draft.fields if not field.read_only]
                if not editable or not typer.confirm(
                    "Edit another field?", default=False, err=True
                ):
                    return draft
                typer.echo(
                    "Editable fields: "
                    + ", ".join(f"{field.name} ({field.label})" for field in editable),
                    err=True,
                )
                name = typer.prompt("Field name", err=True)
                if name not in {field.name for field in editable}:
                    raise typer.BadParameter(
                        "Choose a currently visible editable field."
                    )
                missing.add(name)
            values = {}
            for field in draft.fields:
                if field.name not in missing or field.read_only:
                    continue
                if getattr(field, "reference", False):
                    query = typer.prompt(f"Search {field.label}", err=True)
                    matches = invoke(
                        application.onestop_forms.search_references,
                        {
                            "draft_id": draft.draft_id,
                            "field_name": field.name,
                            "query": query,
                        },
                        False,
                        show_result=False,
                    )
                    if not matches.choices:
                        raise typer.BadParameter(
                            f"No choices were returned for {field.label}."
                        )
                    values[field.name] = _choose(
                        matches.choices, f"Choose {field.label}"
                    ).value
                    continue
                if field.choices:
                    values[field.name] = _choose(
                        field.choices, f"Choose {field.label}"
                    ).value
                else:
                    values[field.name] = typer.prompt(field.label, err=True)
            if not values:
                raise typer.BadParameter(
                    "The form needs a field that cannot be filled here; use the One Stop portal."
                )
            draft = invoke(
                application.onestop_forms.update,
                {"draft_id": draft.draft_id, "values": values},
                False,
                show_result=False,
                side_effect=True,
            )
            _show_workflow(draft, views.draft_preview)
        raise typer.BadParameter(
            "The form still has missing or invalid fields after ten updates."
        )


def _add_draft_attachments(draft):
    """Upload only files explicitly selected during this workflow."""
    with application_scope() as application:
        for _ in range(20):
            if not typer.confirm(
                "Add an attachment to this draft?", default=False, err=True
            ):
                return draft
            path = typer.prompt(
                "Absolute path in the configured One Stop upload directory", err=True
            )
            invoke(
                application.onestop_files.upload,
                {
                    "target": {"kind": "draft", "draft_id": draft.draft_id},
                    "file_path": path,
                },
                False,
                side_effect=True,
            )
            draft = invoke(
                application.onestop_forms.get,
                {"draft_id": draft.draft_id},
                False,
                show_result=False,
            )
            _show_workflow(draft, views.draft_preview)
        typer.echo("Reached the limit of 20 attachments for this workflow.", err=True)
        return draft
