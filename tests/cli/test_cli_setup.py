import unittest
import sys
from unittest.mock import Mock, patch

from typer.testing import CliRunner

from cli.cli import create_app


class CLISetupTests(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        self.app = create_app()

    def invoke(self):
        terminal = Mock(executable=sys.executable)
        with patch("cli.manage.sys", terminal):
            return self.runner.invoke(self.app, ["cli", "setup"])

    def test_setup_can_save_credentials_and_install_chromium(self):
        prompt = Mock()
        prompt.return_value.unsafe_ask.side_effect = [True, True]
        with (
            patch("questionary.confirm", prompt),
            patch("cli.manage.save_auth") as save,
            patch("cli.manage.find_spec", return_value=object()),
            patch("cli.manage.subprocess.run", return_value=Mock(returncode=0)) as run,
        ):
            result = self.invoke()
        self.assertEqual(result.exit_code, 0, result.output)
        save.assert_called_once_with()
        self.assertEqual(
            run.call_args.args[0][1:], ["-m", "playwright", "install", "chromium"]
        )

    def test_declining_both_steps_has_no_side_effects(self):
        prompt = Mock()
        prompt.return_value.unsafe_ask.return_value = False
        with (
            patch("questionary.confirm", prompt),
            patch("cli.manage.save_auth") as save,
            patch("cli.manage.subprocess.run") as run,
        ):
            result = self.invoke()
        self.assertEqual(result.exit_code, 0, result.output)
        save.assert_not_called()
        run.assert_not_called()

    def test_noninteractive_setup_is_refused(self):
        with patch("questionary.confirm") as prompt:
            result = self.runner.invoke(self.app, ["cli", "setup"])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("interactive terminal", result.output)
        prompt.assert_not_called()

    def test_missing_personal_extra_reports_how_to_install_it(self):
        prompt = Mock()
        prompt.return_value.unsafe_ask.side_effect = [False, True]
        with (
            patch("questionary.confirm", prompt),
            patch("cli.manage.find_spec", return_value=None),
            patch("cli.manage.subprocess.run") as run,
        ):
            result = self.invoke()
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("all-abt-ntu[cli,personal]", result.output)
        run.assert_not_called()

    def test_install_failure_is_reported(self):
        prompt = Mock()
        prompt.return_value.unsafe_ask.side_effect = [False, True]
        with (
            patch("questionary.confirm", prompt),
            patch("cli.manage.find_spec", return_value=object()),
            patch("cli.manage.subprocess.run", return_value=Mock(returncode=1)),
        ):
            result = self.invoke()
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Chromium installation failed", result.output)
