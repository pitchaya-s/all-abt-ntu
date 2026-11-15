"""Unified local command line for NTU services and the MCP server."""

import typer

from .manage import auth, cli_setup, config_app, mcp
from .commands import register
from shared.version import VERSION


def create_app():
    """Build the CLI without loading MCP configuration."""
    app = typer.Typer(
        invoke_without_command=True,
        help="NTU services, local configuration, and MCP server.",
        context_settings={"help_option_names": ["-h", "--help"]},
    )
    app.add_typer(mcp, name="mcp")
    app.add_typer(auth, name="auth")
    app.add_typer(cli_setup, name="cli")
    app.add_typer(config_app, name="config")
    register(app)

    @app.callback()
    def root(
        ctx: typer.Context,
        version: bool = typer.Option(False, "--version", is_eager=True),
    ):
        if version:
            typer.echo(VERSION)
            raise typer.Exit()
        if ctx.invoked_subcommand is None:
            typer.echo(ctx.get_help())
            raise typer.Exit()

    return app


def main():
    create_app()()
