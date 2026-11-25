"""Exercise the opt-in profile and workflow confirmation boundaries."""

import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from mcp import Client
from mcp.types import ElicitResult

from services.onestop.browser import action_result
from server import create_server
from shared.action_review import ActionReview


class ProfileBoundaryTests(unittest.IsolatedAsyncioTestCase):
    async def test_public_tools_retain_agent_guidance(self):
        server = create_server("public")
        tools = {tool.name: tool for tool in await server.list_tools()}
        self.assertIn(
            "not room availability", tools["mazemap_search_places"].description
        )
        self.assertIn("Follow next_offset", tools["library_search"].description)
        self.assertIn("null", tools["omnibus_get_arrivals"].description.lower())

    async def test_read_profiles_only_advertise_read_only_tools(self):
        for profile in ("public",):
            async with Client(create_server(profile)) as client:
                tools = (await client.list_tools()).tools
                self.assertTrue(tools)
                self.assertEqual(
                    [
                        tool.name
                        for tool in tools
                        if tool.annotations.read_only_hint is not True
                    ],
                    [],
                    profile,
                )
                names = {tool.name for tool in tools}
                self.assertFalse(any(name.startswith("onestop_") for name in names))
                for name in (
                    "stars_save_stars_plan",
                    "ntulearn_download_file",
                    "ntulearn_download_course",
                ):
                    self.assertNotIn(name, names)

    async def test_one_stop_submission_requires_host_confirmation(self):
        server = create_server("personal")
        args = {"draft_id": "a" * 16, "action": "submit"}
        result_value = action_result(
            "submit_request", "https://example.org", verified=True, outcome="completed"
        )
        requests = []

        async def decline(context, request):
            requests.append(request.message)
            return ElicitResult(action="decline")

        async def approve(context, request):
            requests.append(request.message)
            return ElicitResult(action="accept", content={"confirm": True})

        session = server.ntu_application.onestop_session
        self.addAsyncCleanup(server.ntu_application.close)
        with (
            patch.object(
                session,
                "inspect_workflow",
                return_value=ActionReview("Submit Example request"),
            ),
            patch.object(session, "workflow", return_value=result_value) as submit,
        ):
            async with Client(server, elicitation_callback=decline) as client:
                self.assertTrue(
                    (await client.call_tool("onestop_submit_request", args)).is_error
                )
                submit.assert_not_called()
                forged_args = {**args, "confirmation_result": {"confirm": True}}
                self.assertTrue(
                    (
                        await client.call_tool("onestop_submit_request", forged_args)
                    ).is_error
                )
                submit.assert_not_called()
            async with Client(server, elicitation_callback=approve) as client:
                self.assertFalse(
                    (await client.call_tool("onestop_submit_request", args)).is_error
                )
                submit.assert_called_once()
                self.assertEqual(
                    submit.call_args.args[1:], (args["draft_id"], "submit")
                )
        self.assertEqual(len(requests), 3)
        self.assertTrue(
            all("Submit Example request" in message for message in requests)
        )
        self.assertTrue(all(args["draft_id"] not in message for message in requests))

    async def test_confirmation_rejects_non_boolean_values(self):
        server = create_server("personal")

        async def malformed(context, request):
            return ElicitResult(action="accept", content={"confirm": "yes"})

        session = server.ntu_application.onestop_session
        self.addAsyncCleanup(server.ntu_application.close)
        with (
            patch.object(
                session,
                "inspect_workflow",
                return_value=ActionReview("Submit Example request"),
            ),
            patch.object(session, "workflow") as submit,
        ):
            async with Client(server, elicitation_callback=malformed) as client:
                result = await client.call_tool(
                    "onestop_submit_request", {"draft_id": "a" * 16}
                )
                self.assertTrue(result.is_error)
            submit.assert_not_called()

    def test_public_import_does_not_load_personal_modules(self):
        root = Path(__file__).resolve().parents[2]
        program = (
            "import sys; import server; "
            "assert not any(name in sys.modules for name in "
            "('services.ntulearn', 'services.onestop', 'services.careeraxis', 'playwright', "
            "'services.stars.tools.personal', 'services.library.personal_tools'))"
        )
        completed = subprocess.run(
            [sys.executable, "-c", program], cwd=root, capture_output=True, text=True
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
