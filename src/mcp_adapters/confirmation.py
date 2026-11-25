"""Ask the MCP host to confirm actions with external or local side effects."""

import inspect
import hashlib
import hmac
import json
import re
import secrets
from contextlib import nullcontext
from contextvars import ContextVar
from functools import partial, wraps
from typing import Annotated, get_type_hints

import anyio
from mcp.server.mcpserver.exceptions import ToolError
from mcp.server.mcpserver.resolve import Elicit, Resolve
from pydantic import BaseModel, StrictBool

from shared.action_review import ActionReview
from shared.errors import OperationError


class Confirmation(BaseModel):
    confirm: StrictBool


def _target_summary(arguments) -> str:
    entries = []
    for key, label in (
        ("plan_number", "Plan"),
        ("academic_year", "Academic year"),
        ("semester", "Semester"),
        ("quantity", "Quantity"),
    ):
        value = arguments.get(key)
        if type(value) is int:
            entries.append(f"{label} {value}")
    courses = arguments.get("courses")
    if isinstance(courses, list):
        entries.append(f"{len(courses)} course selections")
    for key in ("destination", "file_path"):
        path = arguments.get(key)
        if isinstance(path, str):
            name = re.split(r"[/\\]", path)[-1]
            entries.append(
                "File " + "".join(char for char in name if char.isprintable())[:90]
            )
    return ", ".join(entries)


def confirmed_tool(function, name, *, review=None, serialize=None, scope=nullcontext):
    """Require host confirmation without exposing a confirmation argument to the model."""
    signature = inspect.signature(function)
    confirmation_name = "confirmation_result"
    if confirmation_name in signature.parameters:
        raise ValueError("Confirmation result conflicts with tool arguments")
    if review and not serialize:
        raise ValueError("A reviewed action must serialize verification and execution.")

    secret = secrets.token_bytes(32)
    pending: ContextVar[str | None] = ContextVar("pending_confirmation", default=None)

    def describe(arguments):
        with scope():
            details = review(**arguments) if review else ActionReview("")
        payload = json.dumps(
            [arguments, details.state], default=str, ensure_ascii=True, sort_keys=True
        ).encode()
        digest = hmac.new(secret, payload, hashlib.sha256).hexdigest()[:24]
        summary = " ".join(
            "".join(
                char for char in details.summary if char.isprintable() or char.isspace()
            ).split()
        )[:420]
        if not summary:
            doc = inspect.getdoc(function) or ""
            summary = " ".join(doc.split(". ", 1)[0].split())[:240]
            target = _target_summary(arguments)
            if target:
                summary = f"{summary}\n{target}"
        return digest, summary

    async def ask(**arguments) -> Elicit[Confirmation]:
        try:
            digest, summary = await anyio.to_thread.run_sync(describe, arguments)
        except OperationError as error:
            raise ToolError(str(error)) from None
        pending.set(digest)
        return Elicit(
            f"Confirm this action: {name.replace('_', ' ')}\n"
            f"{summary}\nReview reference: {digest}",
            Confirmation,
        )

    ask.__signature__ = signature.replace(return_annotation=Elicit[Confirmation])
    ask.__annotations__ = {
        **get_type_hints(function, include_extras=True),
        "return": Elicit[Confirmation],
    }
    confirmation_type = Annotated[Confirmation, Resolve(ask)]

    @wraps(function)
    async def guarded(*args, **kwargs):
        confirmation = kwargs.pop(confirmation_name)
        approved = pending.get()
        pending.set(None)
        if confirmation.confirm is not True or not approved:
            raise ToolError("The action was not confirmed; nothing was changed.")
        if review:
            arguments = signature.bind(*args, **kwargs)
            arguments.apply_defaults()

            def checked():
                if describe(arguments.arguments)[0] != approved:
                    raise OperationError(
                        "The reviewed action changed. Review it again before confirming."
                    )
                return function(*args, **kwargs)

            return await anyio.to_thread.run_sync(serialize, checked)
        if inspect.iscoroutinefunction(function):
            return await function(*args, **kwargs)
        return await anyio.to_thread.run_sync(partial(function, *args, **kwargs))

    guarded.__annotations__ = {
        **get_type_hints(function, include_extras=True),
        confirmation_name: confirmation_type,
    }
    guarded.__signature__ = signature.replace(
        parameters=[
            *signature.parameters.values(),
            inspect.Parameter(
                confirmation_name,
                inspect.Parameter.KEYWORD_ONLY,
                annotation=confirmation_type,
            ),
        ]
    )
    return guarded
