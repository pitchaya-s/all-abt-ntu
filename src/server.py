"""Static local stdio profiles for public and personal tools."""

import asyncio

from mcp.server import MCPServer

import public_server
from mcp_adapters.tools import NTUMCPServer
from shared.version import VERSION

PROFILES = ("public", "personal")
PERSONAL_INSTRUCTIONS = (
    "Personal tools use an opt-in native OS keyring entry; personal records are cached only in memory. "
    "Never request passwords through chat or tool arguments. Users manage credentials in their own terminal "
    "with ntu auth save/status/delete. Deleting credentials stops keyring-based sign-in. "
    "NTULearn can reuse a local browser session or a session cookie from the process environment. "
    "Never request session cookies through chat or tool arguments. "
    "When credential_error is present, credentials_configured is null: storage could not be read. "
    "Do not infer credentials were never saved or tell users to replace them without checking access. "
    "Personal tables omit rows only when headers and records reconstruct them exactly. "
)


def create_server(profile: str = "public", *, application=None) -> MCPServer:
    if profile not in PROFILES:
        raise ValueError(f"Unknown server profile: {profile!r}")
    instructions = public_server.INSTRUCTIONS
    if profile != "public":
        from services.careeraxis import mcp as careeraxis_mcp
        from services.library import personal_tools as library_personal_tools
        from services.ntulearn import mcp as ntulearn_mcp
        from services.onestop import mcp as onestop_mcp

        instructions += " " + PERSONAL_INSTRUCTIONS
        instructions += " " + " ".join(
            (
                ntulearn_mcp.INSTRUCTIONS,
                library_personal_tools.INSTRUCTIONS,
                onestop_mcp.INSTRUCTIONS,
                careeraxis_mcp.INSTRUCTIONS,
            )
        )
    server = NTUMCPServer(
        "all-abt-ntu-mcp",
        version=VERSION,
        instructions=instructions,
        log_level="WARNING",
    )
    public_server.register_tools(server, application)
    if profile != "public":
        from mcp_adapters.catalog import register_personal
        from mcp_adapters.tools import MCPAdapter

        register_personal(MCPAdapter(server, getattr(server, "ntu_application")))
    return server


def main(
    profile: str = "public",
    *,
    disabled_tools=(),
    select_disabled_tools=None,
    application=None,
) -> None:
    server = create_server(profile, application=application)

    async def serve() -> None:
        try:
            if disabled_tools or select_disabled_tools is not None:
                tools = await server.list_tools()
                disabled = set(disabled_tools)
                if select_disabled_tools is not None:
                    disabled.update(select_disabled_tools(tools))
                for tool in tools:
                    if tool.name in disabled:
                        server.remove_tool(tool.name)
            await server.run_stdio_async()
        finally:
            await getattr(server, "ntu_application").close()

    asyncio.run(serve())
