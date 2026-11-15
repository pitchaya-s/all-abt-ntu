"""MCP tool registration, policies, dependency binding, and error handling."""

import inspect
from dataclasses import asdict, dataclass
from functools import wraps
from typing import Any, Optional, Protocol, get_type_hints

from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import ToolAnnotations

from shared.confirmation import confirmed_tool
from shared.errors import OperationError, unexpected_error


@dataclass
class ToolPolicy:
    read_only_hint: Optional[bool] = None
    idempotent_hint: Optional[bool] = None
    destructive_hint: Optional[bool] = None
    open_world_hint: Optional[bool] = None
    confirmation: Optional[str] = None
    failure_message: Optional[str] = None
    uncertain_message: Optional[str] = None


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
