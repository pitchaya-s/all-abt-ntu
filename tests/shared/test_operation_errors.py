import unittest

from mcp.server.mcpserver.exceptions import ToolError
from pydantic import BaseModel

from cli.execution import execute
from mazemap.models import MapError
from shared.mcp import translate_errors
from shared.errors import OperationError


class OperationErrorTests(unittest.IsolatedAsyncioTestCase):
    async def test_cli_and_mcp_preserve_expected_service_errors(self):
        def failure():
            raise MapError("The place was not found.")

        with self.assertRaisesRegex(OperationError, "place was not found"):
            await execute(failure, {})
        with self.assertRaisesRegex(ToolError, "place was not found"):
            translate_errors(failure, "mazemap_get_place")()

    async def test_cli_and_mcp_hide_unexpected_exception_details(self):
        def failure():
            raise RuntimeError("private upstream response")

        message = "MazeMap returned an unexpected data format."
        with self.assertRaises(OperationError) as cli_error:
            await execute(failure, {})
        with self.assertRaises(ToolError) as mcp_error:
            translate_errors(failure, "mazemap_get_place", failure_message=message)()
        for error in (cli_error.exception, mcp_error.exception):
            self.assertNotIn("private upstream response", str(error))
        self.assertIn("MazeMap", str(mcp_error.exception))

    async def test_unexpected_onestop_write_error_warns_against_repeating(self):
        def failure():
            raise RuntimeError("private upstream response")

        name = "onestop_submit_request"
        message = "The action may have completed; check before retrying."
        with self.assertRaisesRegex(OperationError, "may have completed"):
            await execute(failure, {}, side_effect=True)
        with self.assertRaisesRegex(ToolError, "may have completed"):
            translate_errors(failure, name, failure_message=message)()

    async def test_cli_hides_invalid_private_upstream_data(self):
        class Response(BaseModel):
            count: int

        def failure():
            return Response(count="private upstream response")

        with self.assertRaises(OperationError) as error:
            await execute(failure, {})
        self.assertNotIn("private upstream response", str(error.exception))
