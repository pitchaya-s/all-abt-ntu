"""Adapt shared operation registrations to MCP tools."""

import inspect
from dataclasses import asdict
from functools import wraps

from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import ToolAnnotations

from shared.confirmation import confirmed_tool
from shared.operation import OperationError, unexpected_error


def translate_errors(function, name, *, failure_message=None):
    if inspect.iscoroutinefunction(function):

        @wraps(function)
        async def async_call(*args, **kwargs):
            try:
                return await function(*args, **kwargs)
            except OperationError as error:
                raise ToolError(str(error)) from None
            except Exception as error:
                raise ToolError(
                    str(unexpected_error(name, error, message=failure_message))
                ) from None

        return async_call

    @wraps(function)
    def call(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except OperationError as error:
            raise ToolError(str(error)) from None
        except Exception as error:
            raise ToolError(
                str(unexpected_error(name, error, message=failure_message))
            ) from None

    return call


class MCPAdapter:
    def __init__(self, server, app=None, *, public_only=False):
        if app is None:
            from application import Application

            app = Application()
        self.server = server
        self.app = app
        self.public_only = public_only

    def tool(self, *, name, annotations, **kwargs):
        def register(function):
            if self.public_only and annotations.read_only_hint is not True:
                raise ValueError("Public MCP registrations must be read-only.")
            confirmation = annotations.confirmation
            function = translate_errors(
                function,
                name,
                failure_message=annotations.uncertain_message
                or annotations.failure_message,
            )
            if confirmation:
                function = confirmed_tool(function, confirmation)
            hints = asdict(annotations)
            hints.pop("confirmation")
            hints.pop("failure_message")
            hints.pop("uncertain_message")
            return self.server.tool(
                name=name, annotations=ToolAnnotations(**hints), **kwargs
            )(function)

        return register
