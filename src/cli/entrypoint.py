"""Select the requested interface without importing its optional dependencies."""

import argparse
from importlib.util import find_spec
import os
import sys

from shared.version import VERSION


def _missing(extra, purpose):
    print(
        f"{purpose} requires the {extra} extra. Install "
        f"'all-abt-ntu-mcp[{extra}]' or run with uvx --from "
        f"'all-abt-ntu-mcp[{extra}]' ntu ...",
        file=sys.stderr,
    )
    raise SystemExit(1)


def _run_cli(*, mcp_management=False):
    if find_spec("typer") is None or find_spec("rich") is None:
        _missing("cli,mcp" if mcp_management else "cli", "This command")
    if mcp_management and find_spec("mcp") is None:
        _missing("cli,mcp", "MCP setup and tool management")
    from .cli import main

    main()


def _run_mcp(arguments):
    parser = argparse.ArgumentParser(
        prog="ntu mcp",
        description="Run the MCP server; setup and tool management require the CLI and MCP extras.",
    )
    parser.add_argument("--profile", choices=("public", "personal"))
    parser.add_argument("command", nargs="?", choices=("setup", "tools"))
    parser.add_argument("arguments", nargs=argparse.REMAINDER)
    options = parser.parse_args(arguments)
    if options.command:
        _run_cli(mcp_management=True)
        return
    if options.arguments:
        parser.error("unexpected arguments: " + " ".join(options.arguments))
    if find_spec("mcp") is None:
        _missing("mcp", "The MCP server")
    from .mcp import run_server

    try:
        run_server(options.profile)
    except (ValueError, RuntimeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        raise SystemExit(1) from None


def main():
    arguments = sys.argv[1:]
    if any(
        name.endswith("_COMPLETE") and name.startswith("_NTU") for name in os.environ
    ):
        _run_cli()
    elif arguments[:1] == ["mcp"]:
        _run_mcp(arguments[1:])
    elif arguments == ["--version"]:
        print(VERSION)
    elif not arguments or arguments in (["--help"], ["-h"]):
        if find_spec("typer") is not None and find_spec("rich") is not None:
            _run_cli()
        else:
            print(
                "Usage: ntu [OPTIONS] COMMAND [ARGS]...\n\nNTU services and MCP server.\n\n"
                "Install all-abt-ntu-mcp[cli] for service commands, or "
                "all-abt-ntu-mcp[mcp] for ntu mcp."
            )
    else:
        _run_cli()
