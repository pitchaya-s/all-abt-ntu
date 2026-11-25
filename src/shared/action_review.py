"""User-facing information bound to a confirmation."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ActionReview:
    summary: str
    state: object = None
