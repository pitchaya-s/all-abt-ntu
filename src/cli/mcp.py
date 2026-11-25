"""Start a configured MCP server without requiring the CLI interface."""

from functools import partial

from .config import ConfigError, apply_config_env, load_config


def run_server(profile=None):
    try:
        current = load_config()
        apply_config_env(current)
        from .tools.commands import effective_disabled
        from server import main

        selected = profile or current["profile"]
        main(
            selected,
            select_disabled_tools=partial(effective_disabled, current, selected),
        )
    except ConfigError as error:
        raise ValueError(str(error)) from None
