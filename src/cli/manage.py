"""MCP, authentication, and configuration commands."""

import sys
import warnings
from getpass import GetPassWarning, getpass
import typer

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
    setting_entry,
)
from .helpers import Profile
from .output import render

mcp = typer.Typer(invoke_without_command=True, help="Run and configure the MCP server.")
auth = typer.Typer(
    no_args_is_help=True, help="Manage credentials in the native OS keyring."
)
config_app = typer.Typer(no_args_is_help=True, help="Manage MCP settings.")
tools_app = typer.Typer(no_args_is_help=True, help="Manage MCP tools.")
mcp.add_typer(tools_app, name="tools")


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
        from server import main as server_main
        from .tools.commands import effective_disabled

        try:
            current = load_config()
            selected = profile or current["profile"]
            server_main(
                selected, disabled_tools=sorted(effective_disabled(current, selected))
            )
        except (ConfigError, RuntimeError) as error:
            fail(error)


@mcp.command()
def setup(ctx: typer.Context):
    from .tools.commands import setup as setup_tools

    try:
        assert ctx.parent is not None
        if setup_tools(ctx.parent.obj):
            save_auth()
    except (ConfigError, RuntimeError) as error:
        fail(error)


@tools_app.command("list")
def list_tools(ctx: typer.Context, all_tools: bool = typer.Option(False, "--all")):
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
def enable_tools(ctx: typer.Context, names: list[str] = typer.Argument(...)):
    change_tools(ctx, "enable", names)


@tools_app.command("disable")
def disable_tools(ctx: typer.Context, names: list[str] = typer.Argument(...)):
    change_tools(ctx, "disable", names)


@auth.command("save")
def save_auth():
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
        print("Credentials saved in the OS keyring. Automatic login enabled.")
    except GetPassWarning:
        fail(CredentialError("Cannot hide password input; no credentials were saved."))
    except (CredentialError, EOFError, KeyboardInterrupt) as error:
        fail(error)


@auth.command("status")
def auth_status():
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
    if not sys.stdin.isatty() or not typer.confirm("Delete stored NTU credentials?"):
        fail(CredentialError("Credential deletion was not confirmed."))
    try:
        delete_credentials()
        print("Stored credentials deleted. Automatic login disabled.")
    except CredentialError as error:
        fail(error)


@config_app.command("list")
def config_list():
    render(load_config()["env"], json_output=True)


@config_app.command("set")
def config_set(name: str, value: str):
    try:
        section, separator, key = name.partition(".")
        if not separator or not section or not key:
            raise ConfigError("Use a setting name such as ntulearn.headless.")
        if "password" in key.lower() or "secret" in key.lower():
            raise ConfigError("Credentials cannot be stored in configuration.")
        _, rendered = setting_entry(section, key, value, parse=True)
        kind = SETTINGS[section][key][1] if section != "other" else str
        parsed = rendered == "true" if kind is bool else kind(rendered)
        current = load_config()
        current["env"].setdefault(section, {})[key] = parsed
        path = save_config(current)
        print(f"Updated setting in {path}.")
    except ConfigError as error:
        fail(error)


@config_app.command("unset")
def config_unset(name: str):
    try:
        section, separator, key = name.partition(".")
        if not separator or not section or not key:
            raise ConfigError("Use a setting name such as ntulearn.headless.")
        current = load_config()
        values = current["env"].get(section, {})
        values.pop(key, None)
        if not values:
            current["env"].pop(section, None)
        path = save_config(current)
        print(f"Updated setting in {path}.")
    except ConfigError as error:
        fail(error)
