"""Static local stdio profiles for public and personal tools."""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from importlib.util import find_spec
from pathlib import Path

from mcp.server import MCPServer

import public_server
from shared.version import VERSION

PROFILES = ("public", "personal")
PERSONAL_INSTRUCTIONS = (
    "Personal tools use an opt-in native OS keyring entry; personal records are cached only in memory. "
    "Never request passwords through chat or tool arguments. Users manage credentials in their own terminal "
    "with ntu auth save/status/delete. Deleting credentials blocks personal calls. "
    "When credential_error is present, credentials_configured is null: storage could not be read. "
    "Do not infer credentials were never saved or tell users to replace them without checking access. "
    "Personal tables omit rows only when headers and records reconstruct them exactly. "
)


def _chromium_installed() -> bool:
    # Playwright's synchronous API cannot start in a running asyncio loop.
    def inspect_browser():
        from playwright.sync_api import sync_playwright

        with sync_playwright() as playwright:
            return Path(playwright.chromium.executable_path).is_file()

    try:
        with ThreadPoolExecutor(max_workers=1) as executor:
            return executor.submit(inspect_browser).result()
    except Exception:
        return False


def create_server(
    profile: str = "public", *, check_dependencies: bool = True, application=None
) -> MCPServer:
    if profile not in PROFILES:
        raise ValueError(f"Unknown server profile: {profile!r}")
    if profile != "public" and check_dependencies and find_spec("playwright") is None:
        raise RuntimeError(
            "Personal profiles require Playwright. Install all-abt-ntu[mcp,personal] and Chromium; see the setup guide."
        )
    if profile != "public" and check_dependencies and not _chromium_installed():
        raise RuntimeError(
            "Personal profiles require Playwright Chromium. Install it using the setup guide before starting this profile."
        )

    instructions = public_server.INSTRUCTIONS
    if profile != "public":
        import careeraxis.mcp
        import library.personal_tools
        import ntulearn.mcp
        import onestop.mcp

        instructions += " " + PERSONAL_INSTRUCTIONS
        instructions += " " + " ".join(
            (
                ntulearn.mcp.INSTRUCTIONS,
                library.personal_tools.INSTRUCTIONS,
                onestop.mcp.INSTRUCTIONS,
                careeraxis.mcp.INSTRUCTIONS,
            )
        )
    server = MCPServer("all-abt-ntu-mcp", version=VERSION, instructions=instructions)
    public_server.register_tools(server, application)
    if profile != "public":
        from shared.catalog import register_personal
        from shared.mcp import MCPAdapter

        register_personal(MCPAdapter(server, getattr(server, "ntu_application")))
    return server


def main(
    profile: str = "public",
    *,
    check_dependencies: bool = True,
    disabled_tools=(),
    application=None,
) -> None:
    server = create_server(
        profile, check_dependencies=check_dependencies, application=application
    )
    if disabled_tools:
        available = {tool.name for tool in asyncio.run(server.list_tools())}
        for name in available.intersection(disabled_tools):
            server.remove_tool(name)

    async def serve() -> None:
        try:
            await server.run_stdio_async()
        finally:
            await getattr(server, "ntu_application").close()

    asyncio.run(serve())
