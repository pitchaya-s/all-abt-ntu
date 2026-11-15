import contextlib
import io
import sys
import unittest
from unittest.mock import patch

from cli import entrypoint


class EntrypointTests(unittest.TestCase):
    def test_mcp_server_does_not_require_cli_dependencies(self):
        with (
            patch.object(sys, "argv", ["ntu", "mcp", "--profile", "public"]),
            patch(
                "cli.entrypoint.find_spec",
                side_effect=lambda name: (
                    None if name in {"typer", "rich"} else object()
                ),
            ),
            patch("cli.mcp.run_server") as run_server,
            contextlib.redirect_stdout(io.StringIO()) as stdout,
        ):
            entrypoint.main()
        run_server.assert_called_once_with("public")
        self.assertEqual(stdout.getvalue(), "")

    def test_mcp_server_reports_missing_extra(self):
        with (
            patch.object(sys, "argv", ["ntu", "mcp"]),
            patch("cli.entrypoint.find_spec", return_value=None),
            contextlib.redirect_stderr(io.StringIO()) as stderr,
            self.assertRaises(SystemExit) as exit_error,
        ):
            entrypoint.main()
        self.assertEqual(exit_error.exception.code, 1)
        self.assertIn("all-abt-ntu[mcp]", stderr.getvalue())

    def test_management_requires_cli_and_mcp(self):
        with (
            patch.object(sys, "argv", ["ntu", "mcp", "tools", "list"]),
            patch("cli.entrypoint.find_spec", return_value=None),
            contextlib.redirect_stderr(io.StringIO()) as stderr,
            self.assertRaises(SystemExit),
        ):
            entrypoint.main()
        self.assertIn("all-abt-ntu[cli,mcp]", stderr.getvalue())

    def test_management_delegates_to_cli(self):
        with (
            patch.object(
                sys, "argv", ["ntu", "mcp", "--profile", "personal", "tools", "list"]
            ),
            patch("cli.entrypoint._run_cli") as run_cli,
        ):
            entrypoint.main()
        run_cli.assert_called_once_with(mcp_management=True)

    def test_help_without_optional_interfaces(self):
        with (
            patch.object(sys, "argv", ["ntu", "--help"]),
            patch("cli.entrypoint.find_spec", return_value=None),
            contextlib.redirect_stdout(io.StringIO()) as stdout,
        ):
            entrypoint.main()
        self.assertIn("Usage: ntu", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
