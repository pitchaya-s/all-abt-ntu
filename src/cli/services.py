"""Shared CLI operation discovery, validation and dispatch."""

import sys
import inspect
from functools import partial

import typer

from .common import fail
from .execution import run
from .output import render


def invoke(
    operation,
    arguments,
    json_output,
    *,
    side_effect=False,
    show_result=True,
    presenter=None,
):
    try:

        def has_password(value):
            if isinstance(value, dict):
                return any(
                    "password" in str(key).lower() or has_password(item)
                    for key, item in value.items()
                )
            if isinstance(value, list):
                return any(has_password(item) for item in value)
            return False

        if has_password(arguments):
            raise ValueError("Passwords are not accepted as command arguments.")
        if side_effect:
            action = operation
            while isinstance(action, partial):
                action = action.func
            description = (
                (inspect.getdoc(action) or "this action").split(". ", 1)[0].rstrip(".")
            )
            if (
                not sys.stdin.isatty()
                or not sys.stderr.isatty()
                or not typer.confirm(f"Confirm: {description}?", err=True)
            ):
                raise ValueError("Action was not confirmed; nothing was changed.")
        result = run(operation, arguments, side_effect=side_effect)
        if show_result:
            render(result, json_output, presenter=presenter)
        return result
    except Exception as error:
        fail(error)
