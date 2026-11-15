"""Register the local MCP server with selected client applications."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from ..config import ConfigError

NAME = "all-abt-ntu-mcp"
COMMAND = ["uvx", "--from", "all-abt-ntu-mcp[mcp,personal]@latest", "ntu", "mcp"]


def register_command(provider: str) -> None:
    import questionary

    try:
        existing = subprocess.run(
            [provider, "mcp", "get", NAME], capture_output=True, text=True, check=False
        )
    except OSError as error:
        raise ConfigError(f"Could not run {provider}: {error}") from error
    if existing.returncode == 0:
        if provider == "claude":
            print(f"{NAME} is already configured in Claude Code; left unchanged.")
            return
        if not questionary.confirm(
            f"Replace the existing {NAME} configuration in Codex?", default=False
        ).unsafe_ask():
            print("Existing Codex configuration left unchanged.")
            return
    command = [provider, "mcp", "add"]
    if provider == "claude":
        command += ["--scope", "user"]
    elif sys.platform.startswith("linux"):
        address = os.environ.get("DBUS_SESSION_BUS_ADDRESS")
        if not address:
            runtime = os.environ.get("XDG_RUNTIME_DIR") or f"/run/user/{os.getuid()}"
            address = f"unix:path={runtime}/bus"
        command += ["--env", f"DBUS_SESSION_BUS_ADDRESS={address}"]
    command += [NAME, "--", *COMMAND]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=False)
    except OSError as error:
        raise ConfigError(f"Could not run {provider}: {error}") from error
    if result.returncode:
        detail = (result.stderr or result.stdout).strip()
        raise ConfigError(f"Could not configure {provider}: {detail}")
    print(f"Configured {NAME} in {provider}.")


def register_opencode() -> None:
    directory = (
        Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config") / "opencode"
    )
    path = directory / "opencode.json"
    if (directory / "opencode.jsonc").exists():
        raise ConfigError(
            "OpenCode uses opencode.jsonc; add the server manually to preserve its comments. See the README."
        )
    try:
        data = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
        if not isinstance(data, dict) or not isinstance(data.get("mcp", {}), dict):
            raise ValueError("expected an object with an MCP object")
        servers = data.setdefault("mcp", {})
        entry = {
            "type": "local",
            "command": COMMAND,
            "enabled": True,
            "timeout": 240000,
        }
        if NAME in servers:
            if servers[NAME] == entry:
                print(f"{NAME} is already configured in OpenCode.")
                return
            import questionary

            if not questionary.confirm(
                f"Replace the existing {NAME} configuration in OpenCode?", default=False
            ).unsafe_ask():
                print("Existing OpenCode configuration left unchanged.")
                return
        servers[NAME] = entry
        directory.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=directory, delete=False
        ) as output:
            temporary = Path(output.name)
            json.dump(data, output, indent=2, ensure_ascii=False)
            output.write("\n")
        try:
            if path.exists():
                os.chmod(temporary, path.stat().st_mode & 0o777)
            os.replace(temporary, path)
        finally:
            temporary.unlink(missing_ok=True)
    except (OSError, ValueError) as error:
        raise ConfigError(f"Could not configure OpenCode: {error}") from error
    print(f"Configured {NAME} in {path}.")


def configure_clients() -> None:
    import questionary

    providers = questionary.checkbox(
        "Which MCP clients should be configured?",
        instruction="(space to select, enter to continue; select none to skip)",
        choices=[
            questionary.Choice("Codex", value="codex"),
            questionary.Choice("Claude Code", value="claude"),
            questionary.Choice("OpenCode", value="opencode"),
        ],
    ).unsafe_ask()
    if providers is None:
        raise ConfigError("Client configuration cancelled; tool choices were saved.")
    failures = []
    for provider in providers:
        try:
            if provider == "opencode":
                register_opencode()
            else:
                register_command(provider)
        except ConfigError as error:
            failures.append(str(error))
    if failures:
        raise ConfigError("\n".join(failures))
