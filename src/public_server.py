"""Public tool registration shared by local stdio and hosted HTTP servers."""

from mcp.server import MCPServer

from shared.catalog import PUBLIC_INSTRUCTIONS, register_public
from shared.mcp_adapter import MCPAdapter


INSTRUCTIONS = PUBLIC_INSTRUCTIONS


def register_tools(mcp: MCPServer, app=None) -> None:
    if app is None:
        from application import Application

        app = Application()
    setattr(mcp, "ntu_application", app)
    register_public(MCPAdapter(mcp, app, public_only=True))
