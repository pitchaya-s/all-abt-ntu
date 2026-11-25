"""Start a configured MCP server without requiring the CLI interface."""

from functools import partial

from .config import ConfigError, load_config, service_environment


def run_server(profile=None):
    try:
        current = load_config()
        from .tools.commands import effective_disabled
        from server import main

        selected = profile or current["profile"]
        with service_environment(current):
            main(
                selected,
                select_disabled_tools=partial(effective_disabled, current, selected),
            )
    except ConfigError as error:
        raise ValueError(str(error)) from None
