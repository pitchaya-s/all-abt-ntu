"""Safe service errors shared by the CLI and MCP interfaces."""


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
