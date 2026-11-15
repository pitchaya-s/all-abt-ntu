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

    def test_codex_linux_forwards_dbus_dynamically(self):
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
            patch("cli.tools.clients.configure_codex_forwarding") as forwarding,
        ):
            clients.register_command("codex")
        command = run.call_args.args[0]
        self.assertNotIn("--env", command)
        self.assertEqual(command[-5:], clients.COMMAND)
        forwarding.assert_called_once_with()

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

    def test_codex_forwarding_preserves_config_and_does_not_freeze_bus_address(self):
        import tomlkit

        path = Path(self.directory.name) / "config.toml"
        path.write_text(
            '# keep this comment\nmodel = "example"\n'
            '[mcp_servers.all-abt-ntu-mcp]\ncommand = "uvx"\n'
            'env_vars = ["EXISTING"]\n',
            encoding="utf-8",
        )
        with (
            patch.dict(
                os.environ,
                {
                    "CODEX_HOME": self.directory.name,
                    "DBUS_SESSION_BUS_ADDRESS": "unix:path=/example/session-a",
                },
            ),
        ):
            clients.configure_codex_forwarding()
        written = path.read_text(encoding="utf-8")
        config = tomlkit.parse(written)
        server = config["mcp_servers"][clients.NAME]
        self.assertIn("# keep this comment", written)
        self.assertEqual(config["model"], "example")
        self.assertNotIn("/example/session-a", written)
        self.assertEqual(
            list(server["env_vars"]),
            ["EXISTING", "DBUS_SESSION_BUS_ADDRESS", "XDG_RUNTIME_DIR"],
        )
        self.assertEqual(server["startup_timeout_sec"], 120)
        self.assertEqual(server["tool_timeout_sec"], 240)

    def test_codex_forwarding_rejects_invalid_config_without_overwriting(self):
        path = Path(self.directory.name) / "config.toml"
        path.write_text("invalid = [", encoding="utf-8")
        with (
            patch.dict(os.environ, {"CODEX_HOME": self.directory.name}),
            self.assertRaises(ConfigError),
        ):
            clients.configure_codex_forwarding()
        self.assertEqual(path.read_text(encoding="utf-8"), "invalid = [")

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

    def test_opencode_jsonc_preserves_comments_and_other_servers(self):
        directory = Path(self.directory.name) / "opencode"
        directory.mkdir()
        jsonc = directory / "opencode.jsonc"
        jsonc.write_text("""{
  // model comment
  "model": "https://example.test/model",
  "mcp": {
    "other": {"type": "local"}, // server comment
  },
}
""")
        clients.register_opencode()
        from json5.loader import loads

        content = jsonc.read_text()
        self.assertIn("// model comment", content)
        self.assertIn("// server comment", content)
        data = loads(content)
        self.assertEqual(data["model"], "https://example.test/model")
        self.assertIn("other", data["mcp"])
        self.assertEqual(data["mcp"][clients.NAME]["command"], clients.COMMAND)
        clients.register_opencode()
        self.assertEqual(jsonc.read_text(), content)

    def test_opencode_jsonc_replace_requires_confirmation(self):
        directory = Path(self.directory.name) / "opencode"
        directory.mkdir()
        path = directory / "opencode.jsonc"
        original = '{ /* keep */ "mcp": {"all-abt-ntu-mcp": {"type":"local"}} }'
        path.write_text(original)
        dialog = Mock()
        dialog.return_value.unsafe_ask.return_value = False
        with patch("questionary.confirm", dialog):
            clients.register_opencode()
        self.assertEqual(path.read_text(), original)
        dialog.return_value.unsafe_ask.return_value = True
        with patch("questionary.confirm", dialog):
            clients.register_opencode()
        self.assertIn("/* keep */", path.read_text())
        from json5.loader import loads

        self.assertEqual(
            loads(path.read_text())["mcp"][clients.NAME]["command"], clients.COMMAND
        )

    def test_opencode_jsonc_without_mcp_preserves_comments(self):
        directory = Path(self.directory.name) / "opencode"
        directory.mkdir()
        path = directory / "opencode.jsonc"
        path.write_text('{ // keep\n model: "example",\n}')
        clients.register_opencode()
        from json5.loader import loads

        content = path.read_text()
        self.assertIn("// keep", content)
        self.assertEqual(
            loads(content)["mcp"][clients.NAME]["command"], clients.COMMAND
        )

    def test_opencode_invalid_and_conflicting_configs_are_not_overwritten(self):
        directory = Path(self.directory.name) / "opencode"
        directory.mkdir()
        jsonc = directory / "opencode.jsonc"
        jsonc.write_text('{ /* keep */ "mcp": {} }')
        path = directory / "opencode.json"
        path.write_text("{broken")
        with self.assertRaises(ConfigError):
            clients.register_opencode()
        self.assertIn("/* keep */", jsonc.read_text())
        self.assertEqual(path.read_text(), "{broken")
        jsonc.unlink()
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
