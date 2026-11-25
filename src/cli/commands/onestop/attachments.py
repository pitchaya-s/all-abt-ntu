"""One Stop attachments commands."""

from typing import Annotated, Optional

import typer

from ...execution import application_scope
from ...helpers import attachment_target, group
from ...renderers import onestop as views
from ...services import invoke

app = group(default=False)


@app.command("list")
def cmd_attachments_list(
    target: Annotated[
        str,
        typer.Argument(
            help="Target: request:ID, article:ID, or comment:ARTICLE/COMMENT."
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
    """List attachments on a verified own request/item, a readable knowledge article/comment, or an active local draft."""
    with application_scope() as application:
        target = attachment_target(target, record_id)
        return invoke(
            application.onestop_files.list,
            {"target": target},
            json_output,
            presenter=views.attachments_list,
        )


@app.command("upload")
def cmd_attachments_upload(
    target: Annotated[
        str,
        typer.Argument(
            help="Target: request:ID, article:ID, or comment:ARTICLE/COMMENT."
        ),
    ],
    file_path: Annotated[str, typer.Argument(help="Path to the file to upload.")],
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
    """Upload an explicitly selected file from the configured One Stop upload directory to the verified target."""
    with application_scope() as application:
        target = attachment_target(target, record_id)
        return invoke(
            application.onestop_files.upload,
            {"target": target, "file_path": file_path},
            json_output,
            side_effect=True,
            presenter=views.attachments_upload,
        )


@app.command("download")
def cmd_attachments_download(
    target: Annotated[
        str,
        typer.Argument(
            help="Target: request:ID, article:ID, or comment:ARTICLE/COMMENT."
        ),
    ],
    attachment_id: Annotated[
        str, typer.Argument(help="Attachment ID returned by attachments list.")
    ],
    destination: str = typer.Option(
        ...,
        "--output",
        "-o",
        help="The local destination path. Follow the command description for file or directory requirements.",
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
    """Download a listed attachment of the verified target to a new explicit absolute file path, up to 20 MB."""
    with application_scope() as application:
        target = attachment_target(target, record_id)
        return invoke(
            application.onestop_files.download,
            {
                "target": target,
                "attachment_id": attachment_id,
                "destination": destination,
            },
            json_output,
            side_effect=True,
            presenter=views.attachments_download,
        )


@app.command("delete")
def cmd_attachments_delete(
    target: Annotated[
        str,
        typer.Argument(
            help="Target: request:ID, article:ID, or comment:ARTICLE/COMMENT."
        ),
    ],
    attachment_id: Annotated[
        str, typer.Argument(help="Attachment ID returned by attachments list.")
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
    """Delete an attachment only when it is listed on the verified target and native editing is allowed."""
    with application_scope() as application:
        target = attachment_target(target, record_id)
        return invoke(
            application.onestop_files.delete,
            {"target": target, "attachment_id": attachment_id},
            json_output,
            side_effect=True,
            presenter=views.attachments_delete,
        )


@app.command("rename")
def cmd_attachments_rename(
    target: Annotated[
        str,
        typer.Argument(
            help="Target: request:ID, article:ID, or comment:ARTICLE/COMMENT."
        ),
    ],
    attachment_id: Annotated[
        str, typer.Argument(help="Attachment ID returned by attachments list.")
    ],
    file_name: Annotated[str, typer.Argument(help="New attachment filename.")],
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
    """Rename a listed editable attachment using the native attachment service."""
    with application_scope() as application:
        target = attachment_target(target, record_id)
        return invoke(
            application.onestop_files.rename,
            {"target": target, "attachment_id": attachment_id, "file_name": file_name},
            json_output,
            side_effect=True,
            presenter=views.attachments_rename,
        )
