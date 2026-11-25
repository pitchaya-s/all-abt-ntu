"""MCP, authentication, and configuration commands."""

import sys
import subprocess
import warnings
from getpass import GetPassWarning, getpass
from importlib.util import find_spec
from typing import Annotated
import typer

from shared.browser import chromium_installed
from shared.credentials import (
    CredentialError,
    credential_status,
    delete_credentials,
    save_credentials,
)
from .common import fail
from .config import (
    SETTINGS,
    ConfigError,
    apply_config_env,
    load_config,
    save_config,
    service_environment,
    setting_entry,
)
from .helpers import Profile
from .output import render

mcp = typer.Typer(invoke_without_command=True, help="Run and configure the MCP server.")
auth = typer.Typer(
    no_args_is_help=True, help="Manage credentials in the native OS keyring."
)
config_app = typer.Typer(
    no_args_is_help=True, help="Manage settings shared by the CLI and MCP."
)
tools_app = typer.Typer(no_args_is_help=True, help="Manage MCP tools.")
cli_setup = typer.Typer(no_args_is_help=True, help="Set up the CLI.")
mcp.add_typer(tools_app, name="tools")


@cli_setup.command("setup")
def setup_cli(ctx: typer.Context):
    """Optionally save credentials and install Chromium for personal services."""
    if not all(stream.isatty() for stream in (sys.stdin, sys.stdout, sys.stderr)):
        fail(ConfigError("CLI setup requires an interactive terminal."))

    import questionary

    try:
        ctx.with_resource(service_environment())
        status = credential_status()
        if status["credential_error"]:
            print(
                f"Could not check saved NTU credentials: {status['credential_error']}",
                file=sys.stderr,
            )
        configured = status["credentials_configured"]
        save = questionary.confirm(
            "Replace the NTU credentials saved in your OS keyring?"
            if configured
            else "Save NTU account credentials in your OS keyring?",
            default=configured is False and not status["credential_error"],
        ).unsafe_ask()
        if save is None:
            raise ConfigError("CLI setup cancelled.")
        if save:
            save_auth()
        if chromium_installed():
            print("Playwright Chromium is already installed.")
            print("CLI setup complete.")
            return
        install = questionary.confirm(
            "Install Playwright Chromium for browser-based personal services?",
            default=False,
        ).unsafe_ask()
        if install is None:
            raise ConfigError("CLI setup cancelled.")
        if install:
            if find_spec("playwright") is None:
                raise ConfigError(
                    "Chromium installation requires the personal extra. "
                    "Install 'all-abt-ntu[cli,personal]' and rerun ntu cli setup."
                )
            result = subprocess.run(
                [sys.executable, "-m", "playwright", "install", "chromium"],
                check=False,
            )
            if result.returncode or not chromium_installed():
                raise ConfigError(
                    "Chromium installation failed; rerun ntu cli setup to retry."
                )
            print("Playwright Chromium is ready.")
        print("CLI setup complete.")
    except KeyboardInterrupt:
        fail(ConfigError("CLI setup cancelled."))
    except (ConfigError, OSError) as error:
        fail(error)


@mcp.callback()
def mcp_main(
    ctx: typer.Context,
    profile: Profile = typer.Option(None, help="Server profile: public or personal."),
):
    if profile not in (None, "public", "personal"):
        raise typer.BadParameter("Choose public or personal.")
    try:
        apply_config_env(load_config())
    except ConfigError as error:
        fail(error)
    ctx.obj = profile
    if ctx.invoked_subcommand is None:
        from .mcp import run_server

        try:
            run_server(profile)
        except (ConfigError, ValueError, RuntimeError) as error:
            fail(error)


@mcp.command()
def setup(ctx: typer.Context):
    """Choose an MCP profile, tools, and client applications interactively."""
    from .tools.commands import setup as setup_tools
    from .tools.clients import configure_clients

    try:
        assert ctx.parent is not None
        if setup_tools(ctx.parent.obj):
            save_auth()
        configure_clients()
    except (ConfigError, RuntimeError) as error:
        fail(error)


@tools_app.command("list")
def list_tools(
    ctx: typer.Context,
    all_tools: bool = typer.Option(
        False, "--all", help="Show individual tools instead of families."
    ),
):
    """List enabled and disabled tools for the active MCP profile."""
    from .tools.commands import tools_command

    try:
        assert ctx.parent is not None and ctx.parent.parent is not None
        tools_command("list", [], ctx.parent.parent.obj, all_tools=all_tools)
    except (ConfigError, RuntimeError) as error:
        fail(error)


def change_tools(ctx, action, names):
    from .tools.commands import tools_command

    try:
        assert ctx.parent is not None and ctx.parent.parent is not None
        tools_command(action, names, ctx.parent.parent.obj)
    except (ConfigError, RuntimeError) as error:
        fail(error)


@tools_app.command("enable")
def enable_tools(
    ctx: typer.Context,
    names: list[str] = typer.Argument(
        ..., help="Tool family names or individual MCP tool names."
    ),
):
    """Enable MCP tool families or individual tools."""
    change_tools(ctx, "enable", names)


@tools_app.command("disable")
def disable_tools(
    ctx: typer.Context,
    names: list[str] = typer.Argument(
        ..., help="Tool family names or individual MCP tool names."
    ),
):
    """Disable MCP tool families or individual tools."""
    change_tools(ctx, "disable", names)


@auth.command("save")
def save_auth():
    """Save or replace your NTU account credentials in the native OS keyring."""
    try:
        if not sys.stdin.isatty() or not sys.stderr.isatty():
            raise CredentialError(
                "Credential setup requires an interactive terminal; piped input is refused."
            )
        username = input("NTU network username or email: ")
        with warnings.catch_warnings():
            warnings.simplefilter("error", GetPassWarning)
            password = getpass("NTU password: ")
        save_credentials(username, password)
        print("Credentials saved in the OS keyring.")
    except GetPassWarning:
        fail(CredentialError("Cannot hide password input; no credentials were saved."))
    except (CredentialError, EOFError, KeyboardInterrupt) as error:
        fail(error)


@auth.command("status")
def auth_status():
    """Check the local keyring without signing in to an NTU service."""
    try:
        status = credential_status()
        if status["credential_error"]:
            raise CredentialError(status["credential_error"])
        print(
            "Credentials stored: "
            + ("yes" if status["credentials_configured"] else "no")
        )
    except CredentialError as error:
        fail(error)


@auth.command("delete")
def auth_delete():
    """Confirm and delete the saved NTU account credentials."""
    if not sys.stdin.isatty() or not typer.confirm("Delete stored NTU credentials?"):
        fail(CredentialError("Credential deletion was not confirmed."))
    try:
        delete_credentials()
        print("Credentials deleted from the OS keyring.")
    except CredentialError as error:
        fail(error)


@config_app.command("list")
def config_list():
    """Show saved service settings as JSON."""
    try:
        render(load_config(validate_mcp=False)["env"], json_output=True)
    except ConfigError as error:
        fail(error)


@config_app.command("set")
def config_set(
    name: Annotated[
        str, typer.Argument(help="Setting name, such as ntulearn.headless.")
    ],
    value: Annotated[
        str, typer.Argument(help="Value to save for this service setting.")
    ],
):
    """Set a service setting for the CLI and MCP."""
    try:
        section, separator, key = name.partition(".")
        if not separator or not section or not key:
            raise ConfigError("Use a setting name such as ntulearn.headless.")
        if "password" in key.lower() or "secret" in key.lower():
            raise ConfigError("Credentials cannot be stored in configuration.")
        _, rendered = setting_entry(section, key, value, parse=True)
        kind = SETTINGS[section][key][1] if section != "other" else str
        parsed = rendered == "true" if kind is bool else kind(rendered)
        current = load_config(validate_mcp=False)
        current["env"].setdefault(section, {})[key] = parsed
        path = save_config(current)
        print(f"Updated setting in {path}.")
    except ConfigError as error:
        fail(error)


@config_app.command("unset")
def config_unset(
    name: Annotated[
        str, typer.Argument(help="Setting name, such as ntulearn.headless.")
    ],
):
    """Remove a saved service setting."""
    try:
        section, separator, key = name.partition(".")
        if not separator or not section or not key:
            raise ConfigError("Use a setting name such as ntulearn.headless.")
        current = load_config(validate_mcp=False)
        values = current["env"].get(section, {})
        values.pop(key, None)
        if not values:
            current["env"].pop(section, None)
        path = save_config(current)
        print(f"Updated setting in {path}.")
    except ConfigError as error:
        fail(error)
