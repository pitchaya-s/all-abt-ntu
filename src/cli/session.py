"""Scoped service session for a single interactive workflow."""

import sys
from contextlib import contextmanager

from .common import fail
from .execution import application_scope


@contextmanager
def session_scope():
    if not sys.stdin.isatty() or not sys.stderr.isatty():
        fail(ValueError("This workflow requires an interactive terminal."))
    with application_scope() as application:
        yield application
