"""Machine-local tool selection and service settings."""

import json
import math
import os
from contextlib import contextmanager
from pathlib import Path
import re
import tempfile
from typing import Any

from shared.paths import config_dir
from shared.settings import SETTINGS, resolved_settings, settings_scope

PROFILES = ("public", "personal")
_ENV_NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_]*\Z")
_SECRET_NAME = re.compile(
    r"(?:^|_)(?:password|passwd|secret|token|cookies?|credentials?|api_key|private_key)(?:_|$)",
    re.IGNORECASE,
)
_CONFIG_LOCATION_VARS = {"XDG_CONFIG_HOME", "APPDATA", "HOME", "USERPROFILE"}


class ConfigError(Exception):
    pass


def config_path() -> Path:
    return config_dir() / "tools.json"


def secret_setting(name: str) -> bool:
    return bool(_SECRET_NAME.search(name))


def visible_settings(settings: dict) -> dict:
    return {
        section: {
            name: "[hidden]" if section == "other" and secret_setting(name) else value
            for name, value in values.items()
        }
        for section, values in settings.items()
    }


def setting_entry(section: str, name: str, value, *, parse: bool = False):
    if section == "other":
        if parse and secret_setting(name):
            raise ConfigError(
                "This setting can contain a secret. Use the keyring or the documented process environment option."
            )
        if (
            not _ENV_NAME.fullmatch(name)
            or name in _CONFIG_LOCATION_VARS
            or not isinstance(value, str)
            or "\0" in value
        ):
            raise ConfigError(
                "Invalid environment name or value; configuration-location variables must be set outside this file."
            )
        return name, value
    setting = SETTINGS.get(section, {}).get(name)
    if setting is None:
        raise ConfigError(f"Unknown setting {section}.{name}.")
    variable, kind, minimum, maximum = setting
    if parse:
        try:
            if kind is bool:
                if value.lower() not in ("true", "false"):
                    raise ValueError
                value = value.lower() == "true"
            else:
                value = kind(value)
        except (ValueError, TypeError):
            raise ConfigError(f"Invalid value for {section}.{name}.") from None
    valid = type(value) is kind or (kind is float and type(value) is int)
    if valid and kind in (int, float):
        valid = (
            (kind is int or math.isfinite(value))
            and (minimum is None or value >= minimum)
            and (maximum is None or value <= maximum)
        )
    if valid and kind is str:
        valid = "\0" not in value
        if section == "onestop" and name == "upload_dir" and value:
            valid = Path(value).expanduser().is_absolute()
    if not valid:
        raise ConfigError(f"Invalid value for {section}.{name}.")
    return variable, str(value).lower() if kind is bool else str(value)


def validate_env_settings(env: dict) -> None:
    variables = set()
    for section, values in env.items():
        if section != "other" and section not in SETTINGS:
            raise ConfigError(f"Unknown settings group {section}.")
        for name, value in values.items():
            if not isinstance(name, str):
                raise ConfigError("Invalid setting name.")
            variable, _ = setting_entry(section, name, value)
            if variable in variables:
                raise ConfigError(
                    f"Environment variable {variable} is configured more than once."
                )
            variables.add(variable)


def load_config(*, validate_mcp: bool = True) -> dict:
    path = config_path()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        data = {}
    except (OSError, ValueError) as error:
        raise ConfigError(f"Cannot read configuration at {path}: {error}") from error
    if not isinstance(data, dict):
        raise ConfigError(f"Invalid configuration at {path}; fix or remove the file.")
    env = data.setdefault("env", {})
    if not isinstance(env, dict) or not all(
        isinstance(section, str) and isinstance(values, dict)
        for section, values in env.items()
    ):
        raise ConfigError(f"Invalid service settings at {path}; check the env section.")
    validate_env_settings(env)
    if not validate_mcp:
        return data

    data.setdefault("profile", "public")
    tools: Any = data.setdefault("tools", {})
    if isinstance(tools, dict):
        tools.setdefault("enabled", [])
        tools.setdefault("disabled", [])
        tools.setdefault("families", {})
    families = tools.get("families") if isinstance(tools, dict) else None
    if isinstance(families, dict):
        families.setdefault("enabled", [])
        families.setdefault("disabled", [])
    if (
        data.get("profile") not in PROFILES
        or not isinstance(tools, dict)
        or not all(isinstance(tools.get(key), list) for key in ("enabled", "disabled"))
        or not all(
            isinstance(name, str) and name
            for key in ("enabled", "disabled")
            for name in tools[key]
        )
        or set(tools["enabled"]) & set(tools["disabled"])
        or not isinstance(families, dict)
        or not all(
            isinstance(families.get(key), list) for key in ("enabled", "disabled")
        )
        or not all(
            isinstance(name, str) and name
            for key in ("enabled", "disabled")
            for name in families[key]
        )
        or set(families["enabled"]) & set(families["disabled"])
    ):
        raise ConfigError(f"Invalid configuration at {path}; fix or remove the file.")
    return data


def configured_environment(config: dict) -> dict[str, str]:
    values = {}
    for section, settings in config["env"].items():
        for name, value in settings.items():
            if section == "other" and secret_setting(name):
                continue
            variable, rendered = setting_entry(section, name, value)
            values[variable] = rendered
    return values


@contextmanager
def service_environment(config: dict | None = None):
    """Resolve once, forwarding environment-only settings to child processes."""
    if config is None:
        config = load_config(validate_mcp=False)
    defaults = configured_environment(config)
    settings = resolved_settings(defaults)
    forwarded = {
        name: value
        for name, value in defaults.items()
        if name not in os.environ
        and (name not in settings or name == "PLAYWRIGHT_BROWSERS_PATH")
    }
    os.environ.update(forwarded)
    try:
        with settings_scope(settings):
            yield settings
    finally:
        for variable in forwarded:
            os.environ.pop(variable, None)


def save_config(config: dict) -> Path:
    validate_env_settings(config["env"])
    path = config_path()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent, delete=False
        ) as file:
            temporary = Path(file.name)
            try:
                json.dump(config, file, indent=2, sort_keys=True)
                file.write("\n")
            except BaseException:
                temporary.unlink(missing_ok=True)
                raise
        try:
            os.replace(temporary, path)
        finally:
            temporary.unlink(missing_ok=True)
    except OSError as error:
        raise ConfigError(f"Cannot save configuration at {path}: {error}") from error
    return path
