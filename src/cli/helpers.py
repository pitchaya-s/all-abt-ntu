"""Shared parsing and group behavior for service commands."""

import json
from datetime import datetime
from pathlib import Path
from typing import Literal, Optional
from zoneinfo import ZoneInfo

import typer
import click
from typer.core import TyperGroup

Profile = Optional[Literal["public", "personal"]]


class DefaultGroup(TyperGroup):
    """A resource can have a default action and named subcommands."""

    def parse_args(self, ctx, args):
        if not args and not ctx.resilient_parsing:
            args = ["__default__"]
        return super().parse_args(ctx, args)

    def resolve_command(self, ctx, args):
        if args and args[0] not in self.commands:
            return "__default__", self.commands["__default__"], args
        return super().resolve_command(ctx, args)

    def format_help(self, ctx, formatter):
        super().format_help(ctx, formatter)
        default = self.commands.get("__default__")
        if default is not None:
            formatter.write_paragraph()
            description = (default.help or "Run the default command.").split("\n", 1)[0]
            formatter.write_text(
                "Default action (when no subcommand is supplied): " + description
            )
            default_context = click.Context(
                default, parent=ctx, info_name=ctx.info_name
            )
            default.format_options(default_context, formatter)


def group(*, default=False):
    return typer.Typer(
        cls=DefaultGroup if default else TyperGroup,
        no_args_is_help=not default,
        context_settings={"ignore_unknown_options": True, "allow_extra_args": True}
        if default
        else None,
    )


def read_json_file(path):
    try:
        source = Path(path).expanduser()
        if source.stat().st_size > 1024 * 1024:
            raise ValueError("JSON file exceeds 1 MiB.")
        return json.loads(source.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError) as error:
        raise typer.BadParameter(f"Cannot read JSON file: {error}") from None


def parse_json(value):
    try:
        return json.loads(value)
    except (TypeError, ValueError):
        raise typer.BadParameter("Expected a JSON value.") from None


def local_datetime(value: str | datetime | None) -> datetime | None:
    """Interpret a CLI date or naive timestamp in NTU's Singapore timezone."""
    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            raise typer.BadParameter("Use an ISO date or timestamp.") from None
    if value is not None and value.tzinfo is None:
        return value.replace(tzinfo=ZoneInfo("Asia/Singapore"))
    return value


def attachment_target(value, record_id=None):
    kind, separator, identifier = value.partition(":")
    if not separator or not identifier:
        raise typer.BadParameter(
            "Use request:ID, article:ID, or comment:ARTICLE/COMMENT."
        )
    if kind == "request":
        return {"kind": kind, "request_id": identifier, "record_id": record_id}
    if record_id is not None:
        raise typer.BadParameter("--record-id applies only to request targets.")
    if kind == "article":
        return {"kind": kind, "article_id": identifier}
    if kind == "draft":
        raise typer.BadParameter(
            "Draft attachments are managed inside the standalone request workflow."
        )
    if kind == "comment":
        article, slash, comment = identifier.partition("/")
        if slash and article and comment:
            return {
                "kind": "article_comment",
                "article_id": article,
                "comment_id": comment,
            }
    raise typer.BadParameter("Use request:ID, article:ID, or comment:ARTICLE/COMMENT.")
