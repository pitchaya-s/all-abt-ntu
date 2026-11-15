"""Register the local MCP server with selected client applications."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from ..config import ConfigError

NAME = "all-abt-ntu-mcp"
COMMAND = ["uvx", "--from", "all-abt-ntu[mcp,personal]@latest", "ntu", "mcp"]


def configure_codex_forwarding() -> None:
    """Forward the active Linux desktop session instead of storing its address."""
    import tomlkit

    path = Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex") / "config.toml"
    try:
        path = path.resolve(strict=True)
        document = tomlkit.parse(path.read_text(encoding="utf-8"))
        server = document["mcp_servers"][NAME]
        existing = server.get("env_vars", [])
        if not isinstance(existing, list):
            raise ValueError("Codex env_vars must be an array")
        variables = list(existing)
        for name in ("DBUS_SESSION_BUS_ADDRESS", "XDG_RUNTIME_DIR"):
            if name not in variables:
                variables.append(name)
        server["env_vars"] = variables
        server.setdefault("startup_timeout_sec", 120)
        server.setdefault("tool_timeout_sec", 240)
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", dir=path.parent, delete=False
            ) as output:
                temporary = Path(output.name)
                output.write(tomlkit.dumps(document))
            os.chmod(temporary, path.stat().st_mode & 0o777)
            os.replace(temporary, path)
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
    except (OSError, KeyError, TypeError, ValueError) as error:
        raise ConfigError(
            f"Codex was registered, but D-Bus forwarding could not be configured: {error}. "
            "See the Codex setup guide to add env_vars manually."
        ) from error
    if not os.environ.get("DBUS_SESSION_BUS_ADDRESS"):
        print(
            "DBUS_SESSION_BUS_ADDRESS is not set; start Codex from your desktop session "
            "or follow the Linux keyring guide.",
            file=sys.stderr,
        )


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
    command += [NAME, "--", *COMMAND]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=False)
    except OSError as error:
        raise ConfigError(f"Could not run {provider}: {error}") from error
    if result.returncode:
        detail = (result.stderr or result.stdout).strip()
        raise ConfigError(f"Could not configure {provider}: {detail}")
    if provider == "codex" and sys.platform.startswith("linux"):
        configure_codex_forwarding()
    print(f"Configured {NAME} in {provider}.")


def register_opencode() -> None:
    directory = (
        Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config") / "opencode"
    )
    json_path = directory / "opencode.json"
    jsonc_path = directory / "opencode.jsonc"
    if json_path.exists() and jsonc_path.exists():
        raise ConfigError(
            "Both opencode.json and opencode.jsonc exist; configure the server manually "
            "to avoid conflicting settings. See the OpenCode setup guide."
        )
    path = jsonc_path if jsonc_path.exists() else json_path
    try:
        source = path.read_text(encoding="utf-8") if path.exists() else "{}"
        if path == jsonc_path:
            from json5.loader import loads

            data = loads(source)
        else:
            data = json.loads(source)
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
        if path == jsonc_path:
            content = update_opencode_jsonc(source, entry)
        else:
            servers[NAME] = entry
            content = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
        directory.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=directory, delete=False
        ) as output:
            temporary = Path(output.name)
            output.write(content)
        try:
            if path.exists():
                os.chmod(temporary, path.stat().st_mode & 0o777)
            os.replace(temporary, path)
        finally:
            temporary.unlink(missing_ok=True)
    except (OSError, ValueError) as error:
        raise ConfigError(f"Could not configure OpenCode: {error}") from error
    print(f"Configured {NAME} in {path}.")


def update_opencode_jsonc(source: str, entry: dict) -> str:
    """Update the server entry without discarding unrelated JSONC comments."""
    from json5.dumper import ModelDumper, dumps
    from json5.loader import ModelLoader, loads
    from json5.model import JSONObject

    document = loads(source, loader=ModelLoader())
    root = document.value
    if not isinstance(root, JSONObject):
        raise ValueError("expected an object with an MCP object")

    def index_of(obj, name):
        matches = [
            i
            for i, key in enumerate(obj.keys)
            if getattr(key, "characters", getattr(key, "name", None)) == name
        ]
        if len(matches) > 1:
            raise ValueError(f"duplicate {name!r} keys")
        return matches[0] if matches else None

    index = index_of(root, "mcp")
    if index is None:
        node = loads('{"mcp":{}}', loader=ModelLoader()).value
        root.keys.extend(node.keys)
        root.values.extend(node.values)
        servers = node.values[0]
    else:
        servers = root.values[index]
    if not isinstance(servers, JSONObject):
        raise ValueError("expected an object with an MCP object")
    index = index_of(servers, NAME)
    node = loads(json.dumps({NAME: entry}), loader=ModelLoader()).value
    if index is None:
        servers.keys.extend(node.keys)
        servers.values.extend(node.values)
    else:
        value = node.values[0]
        value.wsc_before = servers.values[index].wsc_before
        value.wsc_after = servers.values[index].wsc_after
        servers.values[index] = value
    # json-five's ModelDumper implements the runtime protocol but not BaseDumper.
    return dumps(document, dumper=ModelDumper())  # type: ignore[arg-type]


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
