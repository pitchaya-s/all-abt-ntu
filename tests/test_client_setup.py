import json
import os
from pathlib import Path
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from typer.testing import CliRunner

from cli.cli import create_app
from cli.config import ConfigError
from cli.tools import clients


class ClientSetupTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        environment = patch.dict(os.environ, {"XDG_CONFIG_HOME": self.directory.name})
        environment.start()
        self.addCleanup(environment.stop)

    def test_codex_linux_receives_dbus(self):
        missing = SimpleNamespace(returncode=1, stdout="", stderr="not found")
        success = SimpleNamespace(returncode=0, stdout="", stderr="")
        with (
            patch("cli.tools.clients.sys.platform", "linux"),
            patch.dict(
                os.environ, {"DBUS_SESSION_BUS_ADDRESS": "unix:path=/example/bus"}
            ),
            patch(
                "cli.tools.clients.subprocess.run", side_effect=[missing, success]
            ) as run,
        ):
            clients.register_command("codex")
        command = run.call_args.args[0]
        self.assertIn("DBUS_SESSION_BUS_ADDRESS=unix:path=/example/bus", command)
        self.assertEqual(command[-5:], clients.COMMAND)

    def test_claude_does_not_receive_dbus(self):
        missing = SimpleNamespace(returncode=1, stdout="", stderr="not found")
        success = SimpleNamespace(returncode=0, stdout="", stderr="")
        with patch(
            "cli.tools.clients.subprocess.run", side_effect=[missing, success]
        ) as run:
            clients.register_command("claude")
        command = run.call_args.args[0]
        self.assertIn("--scope", command)
        self.assertNotIn("--env", command)

    def test_codex_uses_runtime_bus_when_address_is_unset(self):
        missing = SimpleNamespace(returncode=1, stdout="", stderr="not found")
        success = SimpleNamespace(returncode=0, stdout="", stderr="")
        with (
            patch("cli.tools.clients.sys.platform", "linux"),
            patch.dict(os.environ, {"XDG_RUNTIME_DIR": "/run/user/123"}),
            patch(
                "cli.tools.clients.subprocess.run", side_effect=[missing, success]
            ) as run,
        ):
            os.environ.pop("DBUS_SESSION_BUS_ADDRESS", None)
            clients.register_command("codex")
        self.assertIn(
            "DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/123/bus",
            run.call_args.args[0],
        )

    def test_existing_codex_requires_confirmation(self):
        existing = SimpleNamespace(returncode=0, stdout="", stderr="")
        dialog = Mock()
        dialog.return_value.unsafe_ask.return_value = False
        with (
            patch("cli.tools.clients.subprocess.run", return_value=existing) as run,
            patch("questionary.confirm", dialog),
        ):
            clients.register_command("codex")
        self.assertEqual(run.call_count, 1)

    def test_opencode_preserves_other_settings_and_is_repeatable(self):
        path = Path(self.directory.name) / "opencode" / "opencode.json"
        path.parent.mkdir()
        path.write_text(
            json.dumps({"model": "example", "mcp": {"other": {"type": "local"}}})
        )
        clients.register_opencode()
        data = json.loads(path.read_text())
        self.assertEqual(data["model"], "example")
        self.assertIn("other", data["mcp"])
        self.assertEqual(data["mcp"][clients.NAME]["command"], clients.COMMAND)
        clients.register_opencode()

    def test_opencode_jsonc_and_invalid_config_are_not_overwritten(self):
        directory = Path(self.directory.name) / "opencode"
        directory.mkdir()
        jsonc = directory / "opencode.jsonc"
        jsonc.write_text('{ /* keep */ "mcp": {} }')
        with self.assertRaises(ConfigError):
            clients.register_opencode()
        self.assertIn("/* keep */", jsonc.read_text())
        jsonc.unlink()
        path = directory / "opencode.json"
        path.write_text("{broken")
        with self.assertRaises(ConfigError):
            clients.register_opencode()
        self.assertEqual(path.read_text(), "{broken")

    def test_selection_configures_requested_clients(self):
        dialog = Mock()
        dialog.return_value.unsafe_ask.return_value = ["codex", "opencode"]
        with (
            patch("questionary.checkbox", dialog),
            patch("cli.tools.clients.register_command") as command,
            patch("cli.tools.clients.register_opencode") as opencode,
        ):
            clients.configure_clients()
        command.assert_called_once_with("codex")
        opencode.assert_called_once_with()

    def test_mcp_setup_opens_client_selection(self):
        with (
            patch("cli.tools.commands.setup", return_value=False),
            patch("cli.tools.clients.configure_clients") as configure,
        ):
            result = CliRunner().invoke(create_app(), ["mcp", "setup"])
        self.assertEqual(result.exit_code, 0, result.output)
        configure.assert_called_once_with()

    def test_partial_failure_reports_error_after_other_clients(self):
        dialog = Mock()
        dialog.return_value.unsafe_ask.return_value = ["codex", "opencode"]
        with (
            patch("questionary.checkbox", dialog),
            patch(
                "cli.tools.clients.register_command",
                side_effect=ConfigError("missing client"),
            ),
            patch("cli.tools.clients.register_opencode") as opencode,
            self.assertRaisesRegex(ConfigError, "missing client"),
        ):
            clients.configure_clients()
        opencode.assert_called_once_with()
