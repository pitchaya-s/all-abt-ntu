"""Run direct service calls with one application and event loop per CLI invocation."""

import asyncio
import inspect
from contextlib import contextmanager
from contextvars import ContextVar

import click
import typer
from pydantic import ValidationError, validate_call

from shared.errors import OperationError, unexpected_error

from .common import fail

SESSION_LOOP = ContextVar("session_loop", default=None)
SESSION_APPLICATION = ContextVar("session_application", default=None)


@contextmanager
def application_scope():
    current = SESSION_APPLICATION.get()
    if current is not None:
        yield current
        return
    from application import Application

    application = Application()
    loop = asyncio.new_event_loop()
    app_token = SESSION_APPLICATION.set(application)
    loop_token = SESSION_LOOP.set(loop)
    try:
        yield application
    except (
        click.ClickException,
        click.exceptions.Exit,
        typer.BadParameter,
        typer.Exit,
        typer.Abort,
    ):
        raise
    except OperationError as error:
        fail(error)
    except Exception as error:
        fail(unexpected_error("CLI operation", error))
    finally:
        try:
            loop.run_until_complete(application.close())
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.run_until_complete(loop.shutdown_default_executor())
        finally:
            loop.close()
            SESSION_LOOP.reset(loop_token)
            SESSION_APPLICATION.reset(app_token)


async def execute(function, arguments, *, side_effect=False):
    try:
        result = validate_call(function)(**arguments)
        if inspect.isawaitable(result):
            result = await result
        return result
    except OperationError:
        raise
    except ValidationError as error:
        if error.title == getattr(function, "__qualname__", None):
            raise
        raise unexpected_error("CLI operation", error) from None
    except Exception as error:
        message = (
            "The action may have completed; check its outcome before retrying."
            if side_effect
            else None
        )
        raise unexpected_error("CLI operation", error, message=message) from None


def run(function, arguments, *, side_effect=False):
    loop = SESSION_LOOP.get()
    if loop is None:
        raise RuntimeError("Service calls require an application scope.")
    return loop.run_until_complete(
        execute(function, arguments, side_effect=side_effect)
    )
