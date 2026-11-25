"""Opt-in, read-only probes for authenticated NTU services."""

import argparse
import asyncio
import logging
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from jsonschema import Draft202012Validator
from mcp import Client

from server import create_server
from tests.live import failure_kind


class SmokeFailure(Exception):
    """A diagnostic that contains no account data."""


def require(condition, message):
    if not condition:
        raise SmokeFailure(message)


def make_caller(client, tools):
    async def call(name, **arguments):
        tool = tools[name]
        require(tool.annotations.read_only_hint is True, name + " is not read-only.")
        result = await asyncio.wait_for(client.call_tool(name, arguments), timeout=90)
        if result.is_error:
            raise SmokeFailure(f"{name}: {failure_kind(result)}")
        data = result.structured_content
        if not Draft202012Validator(tool.output_schema).is_valid(data):
            raise SmokeFailure(name + ": output schema mismatch")
        print(name + ": OK", flush=True)
        return data

    return call


async def learn(call):
    result = await call("ntulearn_list_courses")
    courses = result["courses"]
    require(courses and all(course["id"] for course in courses), "No enrolled courses.")
    if (await call("ntulearn_auth_status"))["cache_ttl_seconds"]:
        cached = await call("ntulearn_list_courses")
        require(
            cached["from_cache"] and cached["retrieved_at"] == result["retrieved_at"],
            "Course cache missed.",
        )
    await call("ntulearn_get_calendar")
    course = next(
        (
            course
            for course in courses
            if course["available"] == "Yes" and not course["organization"]
        ),
        None,
    )
    require(course is not None, "No accessible course in sample.")
    for name in ("get_course_contents", "get_announcements", "get_gradebook"):
        await call("ntulearn_" + name, course_id=course["id"])


async def career(call):
    result = await call("careeraxis_search_opportunities", limit=2)
    require(result["opportunities"], "No opportunities in sample.")
    item = result["opportunities"][0]
    detail = await call("careeraxis_get_opportunity", url=item["url"])
    require(
        detail["url"] == item["url"] and detail["text"], "Opportunity detail mismatch."
    )
    failures = 0
    for section in (
        "events",
        "resources",
        "organisations",
        "appointment_topics",
        "internship_jobs",
    ):
        try:
            result = await call("careeraxis_search_" + section, limit=2)
            require(
                result["section"] == section, "CareerAxis returned another section."
            )
        except SmokeFailure as error:
            if "authentication" in str(error):
                raise
            print(error, flush=True)
            failures += 1
    require(not failures, "One or more CareerAxis sections failed.")


async def library(call):
    result = await call("library_list_facilities")
    room = next((room for room in result["facilities"] if room["space_id"]), None)
    require(room is not None, "No room with a space ID in the directory.")
    tomorrow = (
        datetime.now(ZoneInfo("Asia/Singapore")).date() + timedelta(days=1)
    ).isoformat()
    result = await call(
        "library_get_facility_schedule", date=tomorrow, space_id=room["space_id"]
    )
    require(
        result["spaces"] and all(space["name"] for space in result["spaces"]),
        "No named spaces in the schedule.",
    )


async def onestop(call):
    categories = await call("onestop_list_catalog_categories")
    require(categories["categories"], "No catalog categories.")
    await call("onestop_list_catalog_items", query="letter")
    result = await call("onestop_search_knowledge", query="VPN")
    require(result["articles"], "No knowledge articles in sample.")
    article = await call(
        "onestop_get_knowledge_article", article_id=result["articles"][0]["article_id"]
    )
    require(article["text"], "Knowledge article text is empty.")
    await call("onestop_get_dashboard")
    await call("onestop_list_my_requests")


async def main(service):
    # HTTP client and SDK debug logs can contain request URLs or external text.
    logging.disable(logging.CRITICAL)
    server = create_server("personal")
    try:
        async with Client(server) as client:
            tools = {tool.name: tool for tool in (await client.list_tools()).tools}
            call = make_caller(client, tools)
            await {
                "learn": learn,
                "library": library,
                "onestop": onestop,
                "career": career,
            }[service](call)
    finally:
        await server.ntu_application.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("service", choices=("learn", "career", "library", "onestop"))
    parser.add_argument(
        "--authenticated",
        action="store_true",
        help="Allow a real NTU sign-in using the local account.",
    )
    args = parser.parse_args()
    if not args.authenticated:
        parser.error("pass --authenticated to enable real sign-in")
    try:
        asyncio.run(main(args.service))
    except SmokeFailure as error:
        parser.exit(1, f"{error}\n")
    except Exception as error:
        parser.exit(1, f"Live probe stopped ({type(error).__name__}).\n")
