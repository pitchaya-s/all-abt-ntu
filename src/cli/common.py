"""Shared command-line error reporting."""

import typer
from rich.console import Console


def fail(error: Exception) -> None:
    Console(stderr=True).print(f"Error: {error}", markup=False)
    raise typer.Exit(1)
