import unittest
from unittest.mock import Mock

from mcp import Client
from mcp.server import MCPServer
from mcp.types import ElicitResult
from mcp.shared.exceptions import MCPError

from mcp_adapters.confirmation import confirmed_tool
from mcp_adapters.tools import MCPAdapter, ToolPolicy
from shared.action_review import ActionReview


class ConfirmationTests(unittest.IsolatedAsyncioTestCase):
    async def test_changed_review_cannot_execute_write(self):
        server = MCPServer("review-test")
        write = Mock()
        state = {"item": "Original request"}

        def review(draft_id):
            return ActionReview(state["item"], state.copy())

        @MCPAdapter(server).tool(
            name="submit",
            annotations=ToolPolicy(
                confirmation="submit",
                review=review,
                serialize_reviewed=lambda execute: execute(),
            ),
        )
        def submit(draft_id: str) -> dict[str, bool]:
            write(draft_id)
            return {"submitted": True}

        async def accept(context, params):
            self.assertIn("Original request", params.message)
            self.assertNotIn("synthetic-draft-id", params.message)
            state["item"] = "Changed request"
            return ElicitResult(action="accept", content={"confirm": True})

        async with Client(server, mode="legacy", elicitation_callback=accept) as client:
            tool = (await client.list_tools()).tools[0]
            self.assertNotIn("confirmation_result", tool.input_schema["properties"])
            result = await client.call_tool(
                "submit", {"draft_id": "synthetic-draft-id"}
            )
            self.assertTrue(result.is_error)
            self.assertIn("reviewed action changed", result.content[0].text)
        write.assert_not_called()

    async def test_host_must_confirm_before_side_effect(self):
        server = MCPServer("confirmation-test")
        action = Mock()

        def write(value: str) -> dict[str, str]:
            action(value)
            return {"value": value}

        server.tool(name="write")(confirmed_tool(write, "write"))
        async with Client(server) as client:
            tool = (await client.list_tools()).tools[0]
            self.assertNotIn("confirmation_result", tool.input_schema["properties"])
            with self.assertRaises(MCPError):
                await client.call_tool("write", {"value": "example"})
            with self.assertRaises(MCPError):
                await client.call_tool(
                    "write",
                    {"value": "example", "confirmation_result": {"confirm": True}},
                )
            action.assert_not_called()

        async def decline(context, params):
            return ElicitResult(action="decline")

        async with Client(server, elicitation_callback=decline) as client:
            result = await client.call_tool("write", {"value": "example"})
            self.assertTrue(result.is_error)
            action.assert_not_called()

        async def approve(context, params):
            self.assertNotIn("example", params.message)
            self.assertIn("Confirm this action: write", params.message)
            return ElicitResult(action="accept", content={"confirm": True})

        async with Client(server, elicitation_callback=approve) as client:
            result = await client.call_tool("write", {"value": "example"})
            self.assertFalse(result.is_error)
            action.assert_called_once_with("example")
