"""Offline tests for the hierarchical CLI and personal workflow boundaries."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import nullcontext
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import click
from typer.main import get_command
from typer.testing import CliRunner

from cli.cli import create_app
from cli.config import load_config, save_config
from omnibus.models import Stops


class UnifiedCLITests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        environment = patch.dict(
            os.environ, {"XDG_CONFIG_HOME": directory.name, "APPDATA": directory.name}
        )
        environment.start()
        self.addCleanup(environment.stop)
        self.directory = Path(directory.name)
        self.runner = CliRunner()
        self.app = create_app()

    def test_help_version_and_public_server_boundary(self):
        for args in ([], ["--help"]):
            result = self.runner.invoke(self.app, args)
            self.assertEqual(result.exit_code, 0, result.output)
            for family in (
                "stars",
                "learn",
                "career",
                "map",
                "research",
                "library",
                "faculty",
                "news",
                "services",
                "bus",
                "onestop",
            ):
                self.assertIn(family, result.output)
        self.assertEqual(self.runner.invoke(self.app, ["--version"]).exit_code, 0)
        program = (
            "import sys; from unittest.mock import patch; from cli.cli import main; "
            "sys.argv=['ntu','mcp','--profile','public']; p=patch('server.main'); p.start(); "
            "\ntry: main()\nexcept SystemExit as error: assert error.code == 0\n"
            "assert not any(n in sys.modules for n in "
            "('ntulearn', 'onestop', 'careeraxis', 'playwright', 'stars.tools.personal'))"
        )
        result = subprocess.run(
            [sys.executable, "-c", program], capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_help_describes_services_groups_and_important_arguments(self):
        root = self.runner.invoke(self.app, ["--help"])
        self.assertIn("Search courses, schedules, indexes", root.output)
        onestop = self.runner.invoke(self.app, ["onestop", "--help"])
        self.assertIn("Browse requests or apply", onestop.output)
        apply = self.runner.invoke(self.app, ["onestop", "requests", "apply", "--help"])
        self.assertIn("Catalog item ID", apply.output)
        stars = self.runner.invoke(self.app, ["stars", "courses", "search", "--help"])
        self.assertIn("Starting year", stars.output)
        self.assertIn("Semester 1, 2", stars.output)
        auth = self.runner.invoke(self.app, ["auth", "--help"])
        self.assertIn("Check the local keyring", auth.output)
        config = self.runner.invoke(self.app, ["config", "set", "--help"])
        self.assertIn("Setting name", config.output)

    def test_default_group_reports_unknown_commands_without_internal_names(self):
        result = self.runner.invoke(self.app, ["onestop", "cart", "apply"])
        self.assertEqual(result.exit_code, 2)
        self.assertIn("No such command 'apply'", result.output)
        self.assertNotIn("__default__", result.output)
        result = self.runner.invoke(self.app, ["onestop", "cart", "--unknown"])
        self.assertEqual(result.exit_code, 2)
        self.assertIn("No such option", result.output)
        self.assertNotIn("__default__", result.output)

    def test_default_group_accepts_resource_arguments(self):
        with patch("cli.commands.learn.invoke") as call:
            result = self.runner.invoke(self.app, ["learn", "content", "_100_1"])
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(call.call_args.args[1]["course_id"], "_100_1")

    def test_every_service_command_has_working_help(self):
        root = get_command(self.app)
        paths = []

        def collect(command, path):
            for parameter in command.params:
                with self.subTest(command=" ".join(path), parameter=parameter.name):
                    self.assertTrue(parameter.help, "Missing argument or option help")
            paths.append(path)
            for name, child in getattr(command, "commands", {}).items():
                if name == "__default__":
                    for parameter in child.params:
                        with self.subTest(
                            command=" ".join(path), parameter=parameter.name
                        ):
                            self.assertTrue(
                                parameter.help, "Missing default action help"
                            )
                elif not child.hidden:
                    collect(child, [*path, name])

        for service in (
            "stars",
            "learn",
            "career",
            "map",
            "research",
            "library",
            "faculty",
            "news",
            "services",
            "bus",
            "onestop",
        ):
            collect(root.commands[service], [service])
        self.assertGreater(len(paths), 140)
        for path in paths:
            with self.subTest(command=" ".join(path)):
                result = self.runner.invoke(self.app, [*path, "--help"])
                self.assertEqual(result.exit_code, 0, result.output)
                self.assertIn("Usage:", result.output)

    def test_service_auth_status_calls_live_verification(self):
        for service in ("stars", "learn", "career", "onestop"):
            with (
                self.subTest(service=service),
                patch(f"cli.commands.{service}.invoke") as invoke,
            ):
                result = self.runner.invoke(self.app, [service, "auth", "status"])
                self.assertEqual(result.exit_code, 0, result.output)
                self.assertEqual(invoke.call_args.args[0].__name__, "verify")

    def test_mcp_profile_launch(self):
        with (
            patch("server.main") as server,
            patch(
                "cli.tools.commands.effective_disabled", return_value={"news_search"}
            ),
        ):
            result = self.runner.invoke(self.app, ["mcp", "--profile", "personal"])
        self.assertEqual(result.exit_code, 0, result.output)
        server.assert_called_once_with("personal", disabled_tools=["news_search"])

    def test_direct_command_does_not_load_mcp_registration(self):
        program = (
            "import sys; from unittest.mock import patch; "
            "from typer.testing import CliRunner; from cli.cli import create_app; "
            "p=patch('cli.commands.map.invoke', return_value={}); p.start(); "
            "result=CliRunner().invoke(create_app(), ['map','search','LT1']); "
            "assert result.exit_code == 0, result.output; "
            "assert 'shared.catalog' not in sys.modules; "
            "assert 'mazemap.mcp' not in sys.modules"
        )
        result = subprocess.run(
            [sys.executable, "-c", program], capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_ntulearn_content_urls(self):
        document = "https://ntulearn.ntu.edu.sg/ultra/courses/_100_1/document/_200_1?view=content&state=view"
        video = "https://ntulearn.ntu.edu.sg/ultra/courses/_101_1/document/_201_1?view=content&state=view"
        launch = (
            "https://ntulearn.ntu.edu.sg/ultra/courses/_100_1/lti/launchFrame?"
            "toolHref=https:~2F~2Fntulearn.ntu.edu.sg~2Fwebapps~2Fblackboard~2Fexecute~2Fblti~2FlaunchPlacement"
            "%3Fblti_placement_id%3D_10_1%26content_id%3D_202_1%26course_id%3D_100_1%26wrapped%3Dtrue%26from_ultra%3Dtrue"
        )
        cases = (
            (["learn", "attachments", document], "_100_1", "_200_1"),
            (
                ["learn", "attachments", document.removeprefix("https://")],
                "_100_1",
                "_200_1",
            ),
            (
                ["learn", "attachments", "_100_1", document],
                "_100_1",
                "_200_1",
            ),
            (
                ["learn", "attachments", "_100_1", document.removeprefix("https://")],
                "_100_1",
                "_200_1",
            ),
            (
                ["learn", "files", "read", document, "_300_1"],
                "_100_1",
                "_200_1",
            ),
            (
                ["learn", "files", "download", document, "_300_1", "-o", "file.pdf"],
                "_100_1",
                "_200_1",
            ),
            (
                ["learn", "videos", "download", launch, "-o", "video.mp4"],
                "_100_1",
                "_202_1",
            ),
            (
                [
                    "learn",
                    "videos",
                    "download",
                    launch.removeprefix("https://"),
                    "-o",
                    "video.mp4",
                ],
                "_100_1",
                "_202_1",
            ),
            (
                ["learn", "videos", "download", video, "-o", "video.mp4"],
                "_101_1",
                "_201_1",
            ),
        )
        for arguments, course, content in cases:
            with (
                self.subTest(arguments=arguments),
                patch("cli.commands.learn.invoke") as call,
            ):
                result = self.runner.invoke(self.app, arguments)
                self.assertEqual(result.exit_code, 0, result.output)
                self.assertEqual(call.call_args.args[1]["course_id"], course)
                self.assertEqual(call.call_args.args[1]["content_id"], content)
                if "files" in arguments:
                    self.assertEqual(call.call_args.args[1]["attachment_id"], "_300_1")

        for url in (
            document.replace("ntulearn.ntu.edu.sg", "example.com"),
            document.replace("ntulearn.ntu.edu.sg", "ntulearn.ntu.edu.sg.example.com"),
            launch.replace("%26course_id%3D_100_1", "%26course_id%3D_other"),
        ):
            with self.subTest(url=url), patch("cli.commands.learn.invoke") as call:
                result = self.runner.invoke(self.app, ["learn", "attachments", url])
                self.assertNotEqual(result.exit_code, 0)
                call.assert_not_called()
        result = self.runner.invoke(
            self.app, ["learn", "attachments", "wrong", document]
        )
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("does not match", result.output)

        with patch("cli.commands.learn.invoke") as call:
            result = self.runner.invoke(
                self.app,
                [
                    "learn",
                    "content",
                    "_100_1",
                    "--parent",
                    document.removeprefix("https://"),
                ],
            )
            self.assertEqual(result.exit_code, 0, result.output)
            self.assertEqual(call.call_args.args[1]["parent_id"], "_200_1")

        result = self.runner.invoke(
            self.app, ["learn", "videos", "download", video, "-o", "video.mp4"]
        )
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Action was not confirmed", result.stderr)

    def test_completion_for_group_commands_and_fixed_choices(self):
        executable = str(Path(sys.executable).parent / "ntu")
        for words, index, expected in (
            ("ntu learn courses do", "3", "download"),
            ("ntu bus arrivals --route B", "4", "Blue"),
        ):
            environment = {
                **os.environ,
                "COMP_WORDS": words,
                "COMP_CWORD": index,
                "_NTU_COMPLETE": "complete_bash",
            }
            result = subprocess.run(
                [executable], env=environment, capture_output=True, text=True
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(expected, result.stdout.splitlines())

    def test_short_options_and_default_group_help(self):
        cases = (
            (
                "stars",
                [
                    "stars",
                    "indexes",
                    "SC2001",
                    "-y",
                    "2026",
                    "-s",
                    "1",
                    "-l",
                    "3",
                    "-j",
                ],
                {"academic_year": 2026, "semester": 1, "limit": 3},
            ),
            (
                "map",
                ["map", "search", "LT1", "-l", "2", "-r", "-j"],
                {"limit": 2, "refresh": True},
            ),
            (
                "news",
                ["news", "search", "AI", "-p", "2", "-j"],
                {"page": 2},
            ),
            (
                "learn",
                ["learn", "courses", "-l", "2", "-r", "-j"],
                {"limit": 2, "refresh": True},
            ),
        )
        for module, arguments, expected in cases:
            with (
                self.subTest(arguments=arguments),
                patch(f"cli.commands.{module}.invoke") as call,
            ):
                result = self.runner.invoke(self.app, arguments)
                self.assertEqual(result.exit_code, 0, result.output)
                for key, value in expected.items():
                    self.assertEqual(call.call_args.args[1][key], value)
                self.assertTrue(call.call_args.args[2])

        for arguments in (["learn", "courses", "-h"], ["stars", "indexes", "--help"]):
            result = self.runner.invoke(self.app, arguments)
            self.assertEqual(result.exit_code, 0, result.output)
            self.assertIn("Default action", result.output)
            self.assertIn("--limit", result.output)
        result = self.runner.invoke(self.app, ["map", "search", "-h"])
        help_text = click.unstyle(result.output)
        self.assertIn("--refresh", help_text)
        self.assertNotIn("--no-refresh", help_text)

    def test_representative_hierarchical_routes(self):
        cases = (
            (
                "stars",
                [
                    "stars",
                    "courses",
                    "search",
                    "data",
                    "--year",
                    "2026",
                    "--semester",
                    "1",
                ],
                "search_courses",
            ),
            (
                "stars",
                ["stars", "indexes", "SC2001", "--year", "2026", "--semester", "1"],
                "get_course_indexes",
            ),
            ("learn", ["learn", "courses"], "list_courses"),
            ("learn", ["learn", "content", "tree", "course1"], "get_content_tree"),
            ("career", ["career", "events", "search", "fair"], "search_events"),
            ("map", ["map", "directions", "1", "2", "--accessible"], "get_directions"),
            ("research", ["research", "browse", "collections"], "browse"),
            ("library", ["library", "facilities"], "list_facilities"),
            ("faculty", ["faculty", "interests", "computing"], "list_interests"),
            ("news", ["news", "search", "AI"], "search"),
            ("services", ["services", "filters"], "list_filters"),
            ("bus", ["bus", "stops", "--route", "Blue"], "list_stops"),
            ("onestop", ["onestop", "requests", "list"], "list_my_requests"),
        )
        for module, arguments, operation in cases:
            with (
                self.subTest(arguments=arguments),
                patch(f"cli.commands.{module}.invoke") as dispatch,
            ):
                if module == "bus":
                    dispatch.return_value = Stops(
                        stops=[],
                        total_count=0,
                        source_urls=[],
                        retrieved_at=datetime.now(timezone.utc),
                    )
                result = self.runner.invoke(self.app, arguments)
                self.assertEqual(result.exit_code, 0, result.output)
                target = dispatch.call_args.args[0]
                self.assertEqual(getattr(target, "func", target).__name__, operation)
                if module == "map":
                    self.assertEqual(
                        dispatch.call_args.args[1]["constraint"], "REQUIRE_ACCESSIBLE"
                    )
                if module == "research":
                    self.assertEqual(dispatch.call_args.args[1]["kind"], "collections")

    def test_direct_json_uses_service_without_transport(self):
        response = {
            "courses": [{"course_code": "SC2001", "course_name": "Example"}],
            "next_offset": None,
        }
        with (
            patch(
                "stars.tools.academic.fetch_course_search", return_value=response
            ) as search,
            patch("server.create_server", side_effect=AssertionError("transport used")),
        ):
            result = self.runner.invoke(
                self.app,
                [
                    "stars",
                    "courses",
                    "search",
                    "data",
                    "--year",
                    "2026",
                    "--semester",
                    "1",
                    "--json",
                ],
            )
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(json.loads(result.stdout), response)
        search.assert_called_once_with("data", 2026, 1, "full_time", 20, 0)

    def test_files_and_prerequisite_options(self):
        constraints = self.directory / "constraints.json"
        constraints.write_text('{"avoid_days":["MON"]}', encoding="utf-8")
        with patch("cli.commands.stars.invoke") as dispatch:
            result = self.runner.invoke(
                self.app,
                [
                    "stars",
                    "indexes",
                    "match",
                    "SC2001",
                    "--year",
                    "2026",
                    "--semester",
                    "1",
                    "--constraints",
                    str(constraints),
                ],
            )
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(
            dispatch.call_args.args[1]["constraints"], {"avoid_days": ["MON"]}
        )
        with patch("cli.commands.stars.invoke") as dispatch:
            result = self.runner.invoke(
                self.app,
                [
                    "stars",
                    "prerequisites",
                    "SC2001",
                    "--year",
                    "2026",
                    "--semester",
                    "1",
                    "--completed",
                    "SC1001",
                    "--eligible-only",
                ],
            )
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(dispatch.call_args.args[1]["completed_courses"], ["SC1001"])
        self.assertTrue(dispatch.call_args.args[1]["only_eligible"])

    def test_learn_dates_are_passed_as_singapore_time(self):
        from datetime import timedelta

        with patch("cli.commands.learn.invoke") as dispatch:
            result = self.runner.invoke(
                self.app,
                ["learn", "calendar", "--since", "2026-11-15", "--course", "course1"],
            )
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(
            dispatch.call_args.args[1]["since"].utcoffset(), timedelta(hours=8)
        )

    def test_room_filters_and_plan_replacement_warning(self):
        with patch("cli.commands.stars.invoke") as dispatch:
            result = self.runner.invoke(
                self.app,
                [
                    "stars",
                    "rooms",
                    "available",
                    "--year",
                    "2026",
                    "--semester",
                    "1",
                    "--day",
                    "MON",
                    "--from",
                    "14:00",
                    "--until",
                    "16:00",
                    "--week",
                    "3",
                    "--venue-prefix",
                    "LHN",
                ],
            )
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(dispatch.call_args.args[1]["window"]["teaching_weeks"], [3])
        self.assertEqual(
            dispatch.call_args.args[1]["filters"]["venue_prefixes"], ["LHN"]
        )
        plan = self.directory / "plan.json"
        plan.write_text('[{"course_code":"SC2001","index":"12345"}]', encoding="utf-8")
        with patch("cli.commands.stars.invoke") as dispatch:
            result = self.runner.invoke(
                self.app,
                [
                    "stars",
                    "planner",
                    "save",
                    "1",
                    "--year",
                    "2026",
                    "--semester",
                    "1",
                    "--courses",
                    str(plan),
                ],
            )
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertIn("replaces the complete saved plan", result.stderr)
        self.assertEqual(dispatch.call_args.args[1]["courses"][0]["index"], "12345")

    def test_typed_attachments_and_fixed_cart_actions(self):
        with patch("cli.commands.onestop.invoke") as dispatch:
            result = self.runner.invoke(
                self.app,
                ["onestop", "attachments", "list", "comment:article-id/comment-id"],
            )
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(
            dispatch.call_args.args[1]["target"],
            {
                "kind": "article_comment",
                "article_id": "article-id",
                "comment_id": "comment-id",
            },
        )
        with patch("cli.commands.onestop.invoke") as dispatch:
            result = self.runner.invoke(
                self.app, ["onestop", "cart", "quantity", "item-id", "3"]
            )
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(
            dispatch.call_args.args[1],
            {"item_id": "item-id", "quantity": 3, "action": "set_quantity"},
        )

    def test_cli_ignores_mcp_settings_and_refuses_noninteractive_actions(self):
        current = load_config()
        current["tools"]["families"]["disabled"] = ["news"]
        current["tools"]["enabled"] = ["ntulearn_download_file"]
        save_config(current)
        with patch("cli.services.run", return_value={}):
            result = self.runner.invoke(self.app, ["news", "search", "test", "--json"])
            self.assertEqual(result.exit_code, 0, result.output)
            result = self.runner.invoke(self.app, ["learn", "courses", "--json"])
            self.assertEqual(result.exit_code, 0, result.output)
        with patch(
            "ntulearn.client.session.Session.download", new=AsyncMock()
        ) as download:
            result = self.runner.invoke(
                self.app,
                [
                    "learn",
                    "files",
                    "download",
                    "course",
                    "content",
                    "file",
                    "-o",
                    "/tmp/example",
                ],
            )
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Action was not confirmed", result.stderr)
        self.assertNotIn("failed unexpectedly", result.stderr)
        download.assert_not_awaited()

    def test_video_confirmation_describes_action(self):
        import typer
        from functools import partial
        from cli.services import invoke
        from ntulearn.services.videos import download_video

        with (
            patch("sys.stdin.isatty", return_value=True),
            patch("sys.stderr.isatty", return_value=True),
            patch("typer.confirm", return_value=False) as confirm,
        ):
            with self.assertRaises(typer.Exit):
                invoke(partial(download_video, object()), {}, False, side_effect=True)
        self.assertIn("Download a Kaltura video", confirm.call_args.args[0])
        self.assertNotIn("partial(", confirm.call_args.args[0])

    def test_apply_reviews_before_submit(self):
        from cli.commands.onestop import cmd_requests_apply
        from onestop.services.forms import FormService

        field = SimpleNamespace(
            name="reason", label="Reason", read_only=False, choices=[]
        )
        initial = SimpleNamespace(
            draft_id="draft",
            missing_fields=["reason"],
            invalid_fields=[],
            fields=[field],
            ready=False,
        )
        updated = SimpleNamespace(
            draft_id="draft",
            missing_fields=[],
            invalid_fields=[],
            fields=[field],
            ready=True,
        )
        with (
            patch("cli.session.session_scope", return_value=nullcontext()),
            patch(
                "cli.commands.onestop.invoke",
                side_effect=[initial, updated, {"ok": True}],
            ) as invoke,
            patch("typer.prompt", return_value="Example"),
            patch("typer.confirm", return_value=False),
        ):
            self.assertEqual(cmd_requests_apply("item"), {"ok": True})
        self.assertEqual(
            [call.args[0].__func__ for call in invoke.call_args_list],
            [FormService.prepare, FormService.update, FormService.submit],
        )
        self.assertEqual(
            invoke.call_args_list[1].args[1]["values"], {"reason": "Example"}
        )

    def test_request_workflow_searches_references_and_selects_attachments(self):
        from cli.commands.onestop import _add_draft_attachments, _fill_draft
        from onestop.services.forms import FormService
        from onestop.attachments import AttachmentService

        field = SimpleNamespace(
            name="location",
            label="Location",
            read_only=False,
            choices=[],
            reference=True,
        )
        initial = SimpleNamespace(
            draft_id="draft",
            missing_fields=["location"],
            invalid_fields=[],
            fields=[field],
            ready=False,
        )
        updated = SimpleNamespace(
            draft_id="draft",
            missing_fields=[],
            invalid_fields=[],
            fields=[field],
            ready=True,
        )
        choices = SimpleNamespace(
            choices=[SimpleNamespace(value="choice", label="Example")]
        )
        with (
            patch(
                "cli.commands.onestop.invoke", side_effect=[choices, updated]
            ) as invoke,
            patch("typer.prompt", side_effect=["search", 1]),
            patch("typer.confirm", return_value=False),
        ):
            self.assertIs(_fill_draft(initial), updated)
        self.assertEqual(
            [call.args[0].__func__ for call in invoke.call_args_list],
            [FormService.search_references, FormService.update],
        )
        self.assertEqual(invoke.call_args.args[1]["values"], {"location": "choice"})
        with (
            patch(
                "cli.commands.onestop.invoke", side_effect=[{"ok": True}, updated]
            ) as invoke,
            patch("typer.prompt", return_value="/approved/file.pdf"),
            patch("typer.confirm", side_effect=[True, False]),
        ):
            self.assertIs(_add_draft_attachments(updated), updated)
        self.assertIs(
            invoke.call_args_list[0].args[0].__func__, AttachmentService.upload
        )
        self.assertEqual(
            invoke.call_args_list[0].args[1]["target"],
            {"kind": "draft", "draft_id": "draft"},
        )

    def test_workflow_previews_hide_temporary_identifiers(self):
        from contextlib import redirect_stdout
        from io import StringIO

        from pydantic import BaseModel

        from cli.commands.onestop import _show_workflow
        from cli.renderers.onestop import draft_preview

        class Preview(BaseModel):
            draft_id: str = "internal-draft"
            checkout_id: str = "internal-checkout"
            item_id: str = "internal-item"
            title: str = "Example"

        output = StringIO()
        with redirect_stdout(output):
            _show_workflow(Preview(), draft_preview)
        self.assertIn("Example", output.getvalue())
        self.assertNotIn("internal-", output.getvalue())

    def test_checkout_and_booking_workflows(self):
        from cli.commands.onestop import cmd_appointments_book, cmd_cart_checkout
        from onestop.services.cart import CartService
        from onestop.services.appointments import AppointmentService

        preview = SimpleNamespace(checkout_id="checkout")
        with (
            patch("cli.session.session_scope", return_value=nullcontext()),
            patch(
                "cli.commands.onestop.invoke", side_effect=[preview, {"ok": True}]
            ) as invoke,
        ):
            self.assertEqual(cmd_cart_checkout(), {"ok": True})
        self.assertEqual(
            [call.args[0].__func__ for call in invoke.call_args_list],
            [CartService.prepare_checkout, CartService.submit_checkout],
        )
        draft = SimpleNamespace(
            draft_id="draft",
            missing_fields=["appointment"],
            invalid_fields=[],
            fields=[],
            ready=False,
        )
        config = SimpleNamespace(enabled=True)
        slots = SimpleNamespace(slots=[SimpleNamespace(slot_id="slot", label="10:00")])
        with (
            patch("cli.session.session_scope", return_value=nullcontext()),
            patch(
                "cli.commands.onestop.invoke",
                side_effect=[draft, config, slots, {"ok": True}],
            ) as invoke,
            patch("typer.prompt", side_effect=["2026-11-15", 1]),
            patch("typer.confirm", return_value=False),
        ):
            self.assertEqual(cmd_appointments_book("item"), {"ok": True})
        self.assertIs(invoke.call_args.args[0].__func__, AppointmentService.book)
        self.assertEqual(invoke.call_args.args[1]["slot_id"], "slot")

    def test_apply_does_not_submit_when_confirmation_is_declined(self):
        import typer

        from cli.commands.onestop import cmd_requests_apply

        current = load_config()
        current["profile"] = "personal"
        current["tools"]["enabled"] = [
            "onestop_prepare_request",
            "onestop_submit_request",
        ]
        save_config(current)
        draft = SimpleNamespace(
            draft_id="draft",
            missing_fields=[],
            invalid_fields=[],
            fields=[],
            ready=True,
        )
        with (
            patch("cli.session.session_scope", return_value=nullcontext()),
            patch("sys.stdin.isatty", return_value=True),
            patch("sys.stderr.isatty", return_value=True),
            patch("typer.confirm", side_effect=[True, False, False]),
            patch("cli.services.run", return_value=draft) as run,
            patch("cli.services.render"),
        ):
            with self.assertRaises(typer.Exit):
                cmd_requests_apply("a" * 32)
            run.assert_called_once()

    def test_session_scope_reuses_one_loop_and_cleans_up(self):
        from cli.execution import SESSION_APPLICATION, SESSION_LOOP
        from cli.session import session_scope

        with (
            patch("sys.stdin.isatty", return_value=True),
            patch("sys.stderr.isatty", return_value=True),
            patch("application.Application.close", new=AsyncMock()) as close,
        ):
            with session_scope():
                loop = SESSION_LOOP.get()
                self.assertIsNotNone(loop)
                self.assertIsNotNone(SESSION_APPLICATION.get())
                self.assertIs(SESSION_LOOP.get(), loop)
            close.assert_awaited_once()
        self.assertIsNone(SESSION_LOOP.get())
        self.assertIsNone(SESSION_APPLICATION.get())


if __name__ == "__main__":
    unittest.main()
