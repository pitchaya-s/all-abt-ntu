"""Opt-in public exam lookup for a caller-selected course."""

import argparse
import asyncio

from mcp import Client

from tests.live import local_stdio


async def main(args):
    arguments = {"course_code": args.course_code}
    if args.academic_year is not None:
        arguments.update(academic_year=args.academic_year, semester=args.semester)
    async with Client(local_stdio()) as client:
        result = await client.call_tool(
            "stars_get_undergraduate_exam_schedule", arguments
        )
        if result.is_error:
            raise RuntimeError(
                "Live exam lookup failed; inspect the tool error locally."
            )
        data = result.structured_content
        assert data["course_code"] == args.course_code.upper()
        assert data["exam_count"] == len(data["exams"])
        if args.academic_year is not None:
            assert data["academic_year"] == args.academic_year
            assert str(data["semester"]) == str(args.semester)
        print(
            "Live public exam checks passed; status:",
            data["exam_status"],
            "; exams:",
            data["exam_count"],
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--course-code", required=True)
    parser.add_argument("--academic-year", type=int)
    parser.add_argument("--semester", type=int, choices=(1, 2))
    args = parser.parse_args()
    if (args.academic_year is None) != (args.semester is None):
        parser.error("pass --academic-year and --semester together")
    asyncio.run(main(args))
