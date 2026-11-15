"""Opt-in bounded public Omnibus reads; no accounts or personal data."""

import asyncio

from jsonschema import Draft202012Validator
from mcp import Client

from server import create_server


async def main():
    server = create_server("public")
    try:
        async with Client(server) as client:
            tools = {tool.name: tool for tool in (await client.list_tools()).tools}
            for name, arguments in (
                ("omnibus_list_routes", {}),
                ("omnibus_get_service_status", {"route_code": "Blue"}),
            ):
                result = await client.call_tool(name, arguments)
                if result.is_error:
                    raise RuntimeError(
                        f"{name} failed; inspect the portal before retrying."
                    )
                Draft202012Validator(tools[name].output_schema).validate(
                    result.structured_content
                )
                assert result.structured_content["source_urls"]
                assert result.structured_content["retrieved_at"]
                print(name + ": OK", flush=True)
    finally:
        await server.ntu_application.close()


if __name__ == "__main__":
    asyncio.run(main())
