"""Opt-in bounded public Omnibus reads; no accounts or personal data."""

import asyncio

from jsonschema import Draft202012Validator
from mcp import Client

from services.omnibus.contracts import LTA_SERVICES
from server import create_server


async def main():
    server = create_server("public")
    try:
        async with Client(server) as client:
            tools = {tool.name: tool for tool in (await client.list_tools()).tools}

            async def call(name, **arguments):
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
                return result.structured_content

            assert any(
                route["route_code"] == "Blue"
                for route in (await call("omnibus_list_routes"))["routes"]
            )
            assert (await call("omnibus_get_service_status", route_code="Blue"))[
                "schedules"
            ]
            await call("omnibus_get_live_buses", route_code="Blue")
            stops = await call("omnibus_list_stops", route_code="Blue", limit=1)
            stop = stops["stops"][0]
            arrivals = await call(
                "omnibus_get_arrivals",
                route_filter="Blue",
                stop_query=stop["stop_code"],
                source="shuttle",
            )
            assert any(
                row["stop_code"] == stop["stop_code"]
                for row in arrivals["shuttle_arrivals"]
            )
            for route in LTA_SERVICES:
                stops = await call("omnibus_list_stops", route_code=route, limit=1)
                assert stops["stops"] and not stops["routes_without_stop_data"]
                assert any("data.busrouter.sg/" in url for url in stops["source_urls"])
                stop = stops["stops"][0]
                arrivals = await call(
                    "omnibus_get_arrivals",
                    route_filter=route,
                    stop_query=stop["stop_code"],
                    source="lta",
                )
                assert any(
                    row["stop_code"] == stop["stop_code"] and row["service_no"] == route
                    for row in arrivals["lta_arrivals"]
                )
                assert any(
                    "arrivelah2.busrouter.sg/" in url for url in arrivals["source_urls"]
                )
    finally:
        await server.ntu_application.close()


if __name__ == "__main__":
    asyncio.run(main())
