"""Safe service errors shared by the CLI and MCP interfaces."""


class OperationError(RuntimeError):
    """A safe, user-facing operation failure."""


def invalid_arguments(error, known_fields) -> str:
    """Report schema fields without exposing submitted values or user-supplied keys."""
    fields = sorted(
        {
            location[0]
            for issue in error.errors(include_input=False, include_context=False)
            if (location := issue["loc"]) and location[0] in known_fields
        }
    )
    return (
        "Invalid arguments. Check: " + ", ".join(fields) + "."
        if fields
        else "Invalid arguments. Check the accepted fields and types."
    )


def unexpected_error(
    name: str, error: Exception, *, message: str | None = None
) -> OperationError:
    """Hide untrusted exception details while retaining service-specific guidance."""
    import logging

    logging.getLogger(__name__).warning(
        "Operation %s failed with %s", name, type(error).__name__
    )
    return OperationError(message or "The NTU operation failed unexpectedly.")
