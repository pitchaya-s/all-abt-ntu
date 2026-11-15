"""Register each service's explicit CLI commands."""

from . import (
    bus,
    career,
    faculty,
    learn,
    library,
    map,
    news,
    onestop,
    research,
    services,
    stars,
)


def register(app):
    for name, module in (
        ("stars", stars),
        ("learn", learn),
        ("career", career),
        ("map", map),
        ("research", research),
        ("library", library),
        ("faculty", faculty),
        ("news", news),
        ("services", services),
        ("bus", bus),
        ("onestop", onestop),
    ):
        app.add_typer(module.app, name=name)
