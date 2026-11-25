"""MCP tool registration, policies, dependency binding, and error handling."""

import inspect
from dataclasses import dataclass
from contextlib import nullcontext
from functools import wraps
from typing import Any, Optional, Protocol, get_type_hints

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError, UnexpectedToolError
from mcp.types import ToolAnnotations
from pydantic import ValidationError

from mcp_adapters.confirmation import confirmed_tool
from shared.errors import OperationError, invalid_arguments, unexpected_error
from shared.http import request_budget


class NTUMCPServer(MCPServer):
    async def call_tool(self, name, arguments, context=None):
        try:
            return await super().call_tool(name, arguments, context)
        except ToolError as error:
            if isinstance(error, UnexpectedToolError) or not isinstance(
                error.__cause__, ValidationError
            ):
                raise
            tool = next(
                (tool for tool in await self.list_tools() if tool.name == name), None
            )
            fields = tool.input_schema.get("properties", {}) if tool else {}
            raise ToolError(invalid_arguments(error.__cause__, fields)) from None


@dataclass
class ToolPolicy:
    read_only_hint: Optional[bool] = None
    idempotent_hint: Optional[bool] = None
    destructive_hint: Optional[bool] = None
    open_world_hint: Optional[bool] = None
    confirmation: Optional[str] = None
    failure_message: Optional[str] = None
    uncertain_message: Optional[str] = None
    review: Any = None
    serialize_reviewed: Any = None


class ToolRegistrar(Protocol):
    app: Any

    def tool(self, *, name: str, annotations: ToolPolicy, **kwargs: Any) -> Any: ...


def bind_argument(function, argument):
    """Bind a workflow's first argument without exposing it as a tool input."""
    signature = inspect.signature(function)
    parameters = tuple(signature.parameters.values())
    if not parameters:
        raise ValueError("The workflow has no argument to bind.")

    if inspect.iscoroutinefunction(function):

        @wraps(function)
        async def bound(*args, **kwargs):
            return await function(argument, *args, **kwargs)
    else:

        @wraps(function)
        def bound(*args, **kwargs):
            return function(argument, *args, **kwargs)

    hints = get_type_hints(function, include_extras=True)
    bound.__signature__ = signature.replace(
        parameters=[
            parameter.replace(
                annotation=hints.get(parameter.name, parameter.annotation)
            )
            for parameter in parameters[1:]
        ],
        return_annotation=hints.get("return", signature.return_annotation),
    )
    bound.__annotations__ = {
        name: annotation
        for name, annotation in hints.items()
        if name != parameters[0].name
    }
    return bound


def translate_errors(function, name, *, failure_message=None, scope=nullcontext):
    if inspect.iscoroutinefunction(function):

        @wraps(function)
        async def async_call(*args, **kwargs):
            try:
                with scope(), request_budget():
                    return await function(*args, **kwargs)
            except ToolError:
                raise
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
            with scope(), request_budget():
                return function(*args, **kwargs)
        except ToolError:
            raise
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
            scope = getattr(self.app, "operation", nullcontext)
            if confirmation:
                function = confirmed_tool(
                    function,
                    confirmation,
                    review=annotations.review,
                    serialize=annotations.serialize_reviewed,
                    scope=scope,
                )
            function = translate_errors(
                function,
                name,
                failure_message=annotations.uncertain_message
                or annotations.failure_message,
                scope=scope,
            )
            return self.server.tool(
                name=name,
                annotations=ToolAnnotations(
                    read_only_hint=annotations.read_only_hint,
                    idempotent_hint=annotations.idempotent_hint,
                    destructive_hint=annotations.destructive_hint,
                    open_world_hint=annotations.open_world_hint,
                ),
                **kwargs,
            )(function)

        return register
