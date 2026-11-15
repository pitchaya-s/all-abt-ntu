"""Transport-independent operation metadata and safe service errors."""

from dataclasses import dataclass
from functools import wraps
import inspect
from typing import Any, Optional, Protocol, get_type_hints


class OperationError(RuntimeError):
    """A safe, user-facing operation failure."""


def unexpected_error(
    name: str, error: Exception, *, message: str | None = None
) -> OperationError:
    """Hide untrusted exception details while retaining service-specific guidance."""
    import logging

    logging.getLogger(__name__).warning(
        "Operation %s failed with %s", name, type(error).__name__
    )
    return OperationError(message or "The NTU operation failed unexpectedly.")


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
