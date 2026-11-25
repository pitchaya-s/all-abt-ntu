"""Opt-in NTULearn capability checks; output is limited to counts and sanitized statuses."""

import argparse
import asyncio
import tempfile
from pathlib import Path

from jsonschema import Draft202012Validator
from mcp import Client
from mcp.types import ElicitResult

from server import create_server

from tests.live import failure_kind


def flatten(nodes):
    for node in nodes:
        yield node
        yield from flatten(node["children"])


async def check_community(call, courses):
    # Sample several available courses since many have no groups. Bound roster reads separately.
    member_reads = 0
    group_verified = False
    for course in courses[:12]:
        cid = course["id"]
        groups = await call("ntulearn_list_course_groups", course_id=cid, limit=100)
        assert groups["course_id"] == cid
        for group in groups["groups"]:
            if group["is_group_set"] is True or member_reads >= 6:
                continue
            member_reads += 1
            members = await call(
                "ntulearn_get_group_members",
                course_id=cid,
                group_id=group["id"],
                limit=2,
            )
            assert members["course_id"] == cid and members["group_id"] == group["id"]
            if members["users"]:
                assert all(member["id"] for member in members["users"])
                print(
                    "Live course group and populated member list verified.", flush=True
                )
                group_verified = True
                break
        if group_verified or member_reads >= 6:
            break
    if not group_verified:
        print(
            "Live group members unverified within the bounded course sample.",
            flush=True,
        )

    detail_verified = False
    for folder in ("inbox", "sent"):
        mailbox = await call(
            "ntulearn_list_messages", folder=folder, limit=2, max_requests=35
        )
        assert mailbox["folder"] == folder
        print(
            f"Live {folder}: {len(mailbox['messages'])} sampled messages; "
            f"complete: {mailbox['complete']}; issues: {len(mailbox['issues'])}.",
            flush=True,
        )
        for message in mailbox["messages"]:
            if detail_verified:
                break
            assert message["folder"] == folder
            detail = await call(
                "ntulearn_read_message",
                message_id=message["id"],
                course_id=message["course_id"],
                conversation_id=message["conversation_id"],
            )
            assert all(
                detail["message"][key] == message[key]
                for key in ("id", "course_id", "conversation_id")
            )
            assert detail["recipients_scope"] == "conversation_participants"
            if detail["body"] and detail["body"].strip():
                print(
                    "Live message body and conversation recipient scope verified.",
                    flush=True,
                )
                detail_verified = True
    if not detail_verified:
        print(
            "Live message detail unverified within the bounded mailbox sample.",
            flush=True,
        )


async def main(community_only=False):
    mcp = create_server("personal")

    async def approve_temp_download(context, params):
        if "ntulearn_download_course" not in params.message:
            return ElicitResult(action="decline")
        return ElicitResult(action="accept", content={"confirm": True})

    try:
        async with Client(mcp, elicitation_callback=approve_temp_download) as client:
            tools = {
                tool.name: tool
                for tool in (await client.list_tools()).tools
                if tool.name.startswith("ntulearn_")
            }
            assert len(tools) == 21

            async def call(name, **arguments):
                tool = tools[name]
                if community_only:
                    assert tool.annotations.read_only_hint is True
                result = await asyncio.wait_for(
                    client.call_tool(name, arguments), timeout=90
                )
                if result.is_error:
                    raise RuntimeError(f"{name}: {failure_kind(result)}")
                if not Draft202012Validator(tool.output_schema).is_valid(
                    result.structured_content
                ):
                    raise RuntimeError(f"{name}: output schema mismatch")
                return result.structured_content

            courses = (await call("ntulearn_list_courses", limit=100))["courses"]
            selected = [
                course
                for course in courses
                if course.get("available") == "Yes"
                and course.get("organization") is not True
            ]
            assert selected, "No available enrolled course to sample."
            if community_only:
                await check_community(call, selected)
                return
            course = selected[-1]
            cid = course["id"]
            tree = await call(
                "ntulearn_get_content_tree", course_id=cid, max_depth=5, max_requests=50
            )
            nodes = list(flatten(tree["contents"]))
            assert nodes
            print(
                "Live content tree:",
                len(nodes),
                "nodes; complete:",
                tree["complete"],
                flush=True,
            )
            query = nodes[0]["title"][:40]
            for name, args in [
                ("ntulearn_search_course_content", {"course_id": cid}),
                ("ntulearn_search_all_courses", {"course_ids": [cid]}),
            ]:
                result = await call(name, query=query, max_requests=50, **args)
                assert result["matches"] and all(
                    item["course_id"] == cid and item["breadcrumb"]
                    for item in result["matches"]
                )
                print("Live", name, "matches:", len(result["matches"]), flush=True)
            for name, args, field in [
                ("ntulearn_get_upcoming", {"course_ids": [cid]}, "items"),
                ("ntulearn_list_course_users", {"course_id": cid, "limit": 2}, "users"),
                (
                    "ntulearn_whats_new",
                    {"course_ids": [cid], "max_requests": 30},
                    "grades",
                ),
            ]:
                result = await call(name, **args)
                print(
                    "Live",
                    name,
                    "items:",
                    len(result[field]),
                    "issues:",
                    len(result.get("issues", [])),
                    flush=True,
                )
            await check_community(call, selected)
            for node in nodes:
                if (
                    node["has_children"]
                    or "file" not in (node.get("type") or "").lower()
                ):
                    continue
                attachments = await call(
                    "ntulearn_get_content_attachments",
                    course_id=cid,
                    content_id=node["id"],
                )
                attachment = next(
                    (
                        item
                        for item in attachments["attachments"]
                        if Path(item["file_name"]).suffix.lower()
                        in {".pdf", ".docx", ".pptx", ".xlsx", ".txt"}
                    ),
                    None,
                )
                if attachment:
                    result = await call(
                        "ntulearn_read_file_content",
                        course_id=cid,
                        content_id=node["id"],
                        attachment_id=attachment["id"],
                        max_pages=2,
                        max_chars=2000,
                    )
                    assert result["text"]
                    print(
                        "Live inline document characters:",
                        len(result["text"]),
                        "truncated:",
                        result["truncated"],
                        flush=True,
                    )
                    break
            else:
                print(
                    "Live inline reading not verified: no supported attachment in the bounded tree.",
                    flush=True,
                )
            with tempfile.TemporaryDirectory() as directory:
                downloaded = await call(
                    "ntulearn_download_course",
                    course_id=cid,
                    destination=directory,
                    max_files=1,
                    max_requests=50,
                    max_total_mb=20,
                )
                assert len(downloaded["files"]) <= 1
                for item in downloaded["files"]:
                    if item["status"] == "downloaded":
                        assert (
                            Path(item["path"]).is_relative_to(directory)
                            and Path(item["path"]).stat().st_size
                            == item["bytes_written"]
                        )
                print(
                    "Live bounded course download: files:",
                    len(downloaded["files"]),
                    "bytes:",
                    downloaded["bytes_written"],
                    "issues:",
                    len(downloaded["issues"]),
                    flush=True,
                )
    finally:
        await mcp.ntu_application.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--community-only",
        action="store_true",
        help="Sample course groups, group members and mailbox details without downloading files.",
    )
    asyncio.run(main(community_only=parser.parse_args().community_only))
