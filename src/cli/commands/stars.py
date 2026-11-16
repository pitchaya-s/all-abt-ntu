"""Stars service commands."""

from typing import Annotated, Literal, Optional

from functools import partial

import typer

from ..helpers import group, parse_json, read_json_file
from ..execution import application_scope
from ..services import invoke

app = typer.Typer(
    no_args_is_help=True, help="Search courses, schedules, indexes, and prerequisites."
)
g_auth = group(default=False)
app.add_typer(g_auth, name="auth", help="Check STARS authentication.")
g_courses = group(default=False)
app.add_typer(g_courses, name="courses", help="Search undergraduate courses.")
g_indexes = group(default=True)
app.add_typer(g_indexes, name="indexes", help="List, compare, or match course indexes.")
g_planner = group(default=False)
app.add_typer(g_planner, name="planner", help="View or replace a saved STARS plan.")
g_rooms = group(default=False)
app.add_typer(
    g_rooms, name="rooms", help="Find teaching-free rooms and published schedules."
)


@g_courses.command("search")
def cmd_courses_search(
    query: str = typer.Argument(..., help="Search text or keywords."),
    academic_year: int = typer.Option(
        ..., "--year", "-y", help="Starting year of the academic year, such as 2026."
    ),
    semester: Literal[1, 2, "S"] = typer.Option(
        ..., "--semester", "-s", help="Semester 1, 2, or special term S."
    ),
    study_mode: Annotated[
        Literal["full_time", "part_time"],
        typer.Option(
            help="The study mode for the published class schedule. Choices: full_time, part_time. Default: full_time."
        ),
    ] = "full_time",
    limit: int = typer.Option(20, "--limit", "-l", help="Maximum number of results."),
    offset: int = typer.Option(0, "--offset", help="Number of results to skip."),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Search NTU's public undergraduate Class Schedule by partial code or title keywords."""
    with application_scope():
        from stars.tools import academic

        return invoke(
            academic.search_courses,
            {
                "query": query,
                "academic_year": academic_year,
                "semester": semester,
                "study_mode": study_mode,
                "limit": limit,
                "offset": offset,
            },
            json_output,
        )


@app.command("course")
def cmd_course(
    course_code: Annotated[str, typer.Argument(help="The course code shown by STARS.")],
    academic_year: int = typer.Option(
        ..., "--year", "-y", help="Starting year of the academic year, such as 2026."
    ),
    semester: Literal[1, 2, "S"] = typer.Option(
        ..., "--semester", "-s", help="Semester 1, 2, or special term S."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Get course name, AUs, prerequisites, description, and term metadata."""
    with application_scope():
        from stars.tools import academic

        return invoke(
            academic.get_course_metadata,
            {
                "course_code": course_code,
                "academic_year": academic_year,
                "semester": semester,
            },
            json_output,
        )


@app.command("prerequisites")
def cmd_prerequisites(
    course_code: Annotated[str, typer.Argument(help="The course code shown by STARS.")],
    academic_year: int = typer.Option(
        ..., "--year", "-y", help="Starting year of the academic year, such as 2026."
    ),
    semester: Literal[1, 2, "S"] = typer.Option(
        ..., "--semester", "-s", help="Semester 1, 2, or special term S."
    ),
    prerequisite_depth: Annotated[
        int,
        typer.Option(help="How many levels of prerequisites to follow. Default: 2."),
    ] = 2,
    dependent_depth: Annotated[
        int,
        typer.Option(
            help="How many levels of dependent courses to follow. Default: 2."
        ),
    ] = 2,
    completed_courses: Optional[list[str]] = typer.Option(
        None,
        "--completed",
        help="Completed course codes used when evaluating prerequisite eligibility.",
    ),
    only_eligible: bool = typer.Option(
        False,
        "--eligible-only",
        help="Restrict results to courses eligible under the supplied completed courses.",
    ),
    include_corequisites: bool = typer.Option(
        False,
        "--include-corequisites",
        help="Include corequisites when building the prerequisite tree.",
    ),
    max_nodes: Annotated[
        int,
        typer.Option(
            help="Maximum number of prerequisite and dependent nodes to examine. Default: 100."
        ),
    ] = 100,
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Build before and after branches around a course, with separate depth limits.

    The before branch follows the course's prerequisite rules; the after branch finds courses
    that depend on it in the selected term."""
    with application_scope():
        from stars.tools import academic

        return invoke(
            academic.get_prerequisite_tree,
            {
                "course_code": course_code,
                "academic_year": academic_year,
                "semester": semester,
                "prerequisite_depth": prerequisite_depth,
                "dependent_depth": dependent_depth,
                "completed_courses": completed_courses,
                "only_eligible": only_eligible,
                "include_corequisites": include_corequisites,
                "max_nodes": max_nodes,
            },
            json_output,
        )


@g_indexes.command("__default__", hidden=True)
def cmd_indexes_default(
    course_code: Annotated[str, typer.Argument(help="The course code shown by STARS.")],
    academic_year: int = typer.Option(
        ..., "--year", "-y", help="Starting year of the academic year, such as 2026."
    ),
    semester: Literal[1, 2, "S"] = typer.Option(
        ..., "--semester", "-s", help="Semester 1, 2, or special term S."
    ),
    limit: int = typer.Option(10, "--limit", "-l", help="Maximum number of results."),
    offset: int = typer.Option(0, "--offset", help="Number of results to skip."),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """List a page of indexes with timetable details and matching-term vacancies/waitlists."""
    with application_scope():
        from stars.tools import academic

        return invoke(
            academic.get_course_indexes,
            {
                "course_code": course_code,
                "academic_year": academic_year,
                "semester": semester,
                "limit": limit,
                "offset": offset,
            },
            json_output,
        )


@app.command("index")
def cmd_index(
    course_code: Annotated[str, typer.Argument(help="The course code shown by STARS.")],
    index: Annotated[
        str,
        typer.Argument(
            help="The index number, kept as a string so leading zeroes are preserved."
        ),
    ],
    academic_year: int = typer.Option(
        ..., "--year", "-y", help="Starting year of the academic year, such as 2026."
    ),
    semester: Literal[1, 2, "S"] = typer.Option(
        ..., "--semester", "-s", help="Semester 1, 2, or special term S."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Get one index's complete schedule, vacancies, and waitlist where matching-term counts are published."""
    with application_scope():
        from stars.tools import academic

        return invoke(
            academic.get_index,
            {
                "course_code": course_code,
                "index": index,
                "academic_year": academic_year,
                "semester": semester,
            },
            json_output,
        )


@g_indexes.command("compare")
def cmd_indexes_compare(
    course_code: Annotated[str, typer.Argument(help="The course code shown by STARS.")],
    indexes: list[str] = typer.Argument(
        ..., help="Two or more index numbers to compare; keep leading zeroes."
    ),
    academic_year: int = typer.Option(
        ..., "--year", "-y", help="Starting year of the academic year, such as 2026."
    ),
    semester: Literal[1, 2, "S"] = typer.Option(
        ..., "--semester", "-s", help="Semester 1, 2, or special term S."
    ),
    against_sessions: Optional[str] = typer.Option(
        None, "--against", help="Read JSON from a file."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Compare shared and index-specific sessions; optionally check clashes with supplied time slots."""
    with application_scope():
        from stars.tools import academic

        against_sessions = (
            read_json_file(against_sessions) if against_sessions is not None else None
        )
        return invoke(
            academic.compare_indexes,
            {
                "course_code": course_code,
                "indexes": indexes,
                "academic_year": academic_year,
                "semester": semester,
                "against_sessions": against_sessions,
            },
            json_output,
        )


@g_indexes.command("match")
def cmd_indexes_match(
    course_code: Annotated[str, typer.Argument(help="The course code shown by STARS.")],
    academic_year: int = typer.Option(
        ..., "--year", "-y", help="Starting year of the academic year, such as 2026."
    ),
    semester: Literal[1, 2, "S"] = typer.Option(
        ..., "--semester", "-s", help="Semester 1, 2, or special term S."
    ),
    constraints: Optional[str] = typer.Option(
        None, "--constraints", help="Read JSON from a file."
    ),
    against_sessions: Optional[str] = typer.Option(
        None, "--against", help="Read JSON from a file."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Find indexes matching day/time/lesson/week rules and avoiding supplied timetable clashes."""
    with application_scope():
        from stars.tools import academic

        constraints = read_json_file(constraints) if constraints is not None else None
        against_sessions = (
            read_json_file(against_sessions) if against_sessions is not None else None
        )
        return invoke(
            academic.find_matching_indexes,
            {
                "course_code": course_code,
                "academic_year": academic_year,
                "semester": semester,
                "constraints": constraints,
                "against_sessions": against_sessions,
            },
            json_output,
        )


@app.command("exams")
def cmd_exams(
    course_code: Annotated[str, typer.Argument(help="The course code shown by STARS.")],
    academic_year: Optional[int] = typer.Option(
        None,
        "--year",
        "-y",
        help="The first year of the academic year; 2026 means AY2026/27.",
    ),
    semester: Optional[Literal[1, 2]] = typer.Option(
        None,
        "--semester",
        "-s",
        help="Semester within the selected academic year. Choices: 1, 2.",
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Get public General Access exam dates and times for a course in the latest or specified published term."""
    with application_scope():
        from stars.tools import academic

        return invoke(
            academic.get_undergraduate_exam_schedule,
            {
                "course_code": course_code,
                "academic_year": academic_year,
                "semester": semester,
            },
            json_output,
        )


@app.command("graduate")
def cmd_graduate(
    course_code: Annotated[str, typer.Argument(help="The course code shown by STARS.")],
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Get a graduate course's class groups for NTU's currently published academic term."""
    with application_scope():
        from stars.tools import academic

        return invoke(
            academic.get_graduate_course_schedule,
            {"course_code": course_code},
            json_output,
        )


@g_rooms.command("schedule")
def cmd_rooms_schedule(
    venue: Annotated[str, typer.Argument(help="The published room or venue name.")],
    academic_year: int = typer.Option(
        ..., "--year", "-y", help="Starting year of the academic year, such as 2026."
    ),
    semester: Literal[1, 2, "S"] = typer.Option(
        ..., "--semester", "-s", help="Semester 1, 2, or special term S."
    ),
    day: Annotated[
        Optional[Literal["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]],
        typer.Option(
            help="Day of the week for the requested schedule. Choices: MON, TUE, WED, THU, FRI, SAT, SUN."
        ),
    ] = None,
    teaching_weeks: Optional[list[int]] = typer.Option(
        None,
        "--week",
        help="A teaching week to include; repeat --week for multiple weeks.",
    ),
    start_time: Annotated[
        Optional[str], typer.Option(help="Start time in 24-hour HH:MM format.")
    ] = None,
    end_time: Annotated[
        Optional[str], typer.Option(help="End time in 24-hour HH:MM format.")
    ] = None,
    limit: int = typer.Option(50, "--limit", "-l", help="Maximum number of results."),
    offset: int = typer.Option(0, "--offset", help="Number of results to skip."),
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Get all published undergraduate course/index lessons using one observed room, including full-time and part-time offerings."""
    with application_scope():
        from stars.tools import rooms

        return invoke(
            rooms.get_room_schedule,
            {
                "venue": venue,
                "academic_year": academic_year,
                "semester": semester,
                "day": day,
                "teaching_weeks": teaching_weeks,
                "start_time": start_time,
                "end_time": end_time,
                "limit": limit,
                "offset": offset,
                "refresh": refresh,
            },
            json_output,
        )


@g_auth.command("status")
def cmd_auth_status(
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Sign in to STARS and report whether access is verified."""
    with application_scope() as application:
        return invoke(application.stars_personal.verify, {}, json_output)


@g_planner.command("show")
def cmd_planner_show(
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Get registered courses, the published term, and saved Plans 1–3 with indexes and timetables."""
    with application_scope() as application:
        from stars.tools import personal

        return invoke(
            partial(personal.get_stars_planner, application),
            {"refresh": refresh},
            json_output,
        )


@g_planner.command("save")
def cmd_planner_save(
    plan_number: Annotated[
        Literal[1, 2, 3],
        typer.Argument(help="The saved plan number, from 1 to 3. Choices: 1, 2, 3."),
    ],
    courses: str = typer.Option(..., "--courses", help="Read JSON from a file."),
    academic_year: int = typer.Option(
        ..., "--year", "-y", help="Starting year of the academic year, such as 2026."
    ),
    semester: Literal[1, 2] = typer.Option(
        ...,
        "--semester",
        "-s",
        help="Semester within the selected academic year. Choices: 1, 2.",
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Replace saved Plan 1, 2, or 3 with the complete supplied course/index list for the current Planner term."""
    with application_scope() as application:
        from stars.tools import personal

        courses = read_json_file(courses)
        typer.echo("Warning: this replaces the complete saved plan.", err=True)
        return invoke(
            partial(personal.save_stars_plan, application),
            {
                "plan_number": plan_number,
                "courses": courses,
                "academic_year": academic_year,
                "semester": semester,
            },
            json_output,
            side_effect=True,
        )


@app.command("audit")
def cmd_audit(
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Get your degree requirements, examination results, and registered courses from Degree Audit."""
    with application_scope() as application:
        from stars.tools import personal

        return invoke(partial(personal.get_degree_audit, application), {}, json_output)


def complete_room_type(incomplete: str):
    return [
        value
        for value in (
            "tutorial_room",
            "seminar_room",
            "lecture_theatre",
            "laboratory",
            "other",
        )
        if value.startswith(incomplete)
    ]


@g_rooms.command("available")
def cmd_rooms_available(
    academic_year: int = typer.Option(
        ..., "--year", "-y", help="Starting year of the academic year, such as 2026."
    ),
    semester: Literal[1, 2, "S"] = typer.Option(
        ..., "--semester", "-s", help="Semester 1, 2, or special term S."
    ),
    day: Literal["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"] = typer.Option(
        ...,
        "--day",
        help="Day of the week for the requested schedule. Choices: MON, TUE, WED, THU, FRI, SAT, SUN.",
    ),
    start_time: str = typer.Option(
        ..., "--from", help="Start time in 24-hour HH:MM format."
    ),
    end_time: str = typer.Option(
        ..., "--until", help="End time in 24-hour HH:MM format."
    ),
    teaching_weeks: Optional[list[int]] = typer.Option(
        None,
        "--week",
        help="A teaching week to include; repeat --week for multiple weeks.",
    ),
    buffer_minutes: Annotated[
        int,
        typer.Option(
            help="Extra minutes to keep clear around the requested room window. Default: 0."
        ),
    ] = 0,
    room_type: Optional[list[str]] = typer.Option(
        None,
        "--room-type",
        autocompletion=complete_room_type,
        help="A room type to include; repeat the option for multiple types. Values are tutorial_room, seminar_room, lecture_theatre, laboratory and other.",
    ),
    venue_contains: Annotated[
        Optional[str], typer.Option(help="Require the venue name to contain this text.")
    ] = None,
    venue_prefix: Optional[list[str]] = typer.Option(
        None,
        "--venue-prefix",
        help="A venue-name prefix to include; repeat the option for multiple prefixes.",
    ),
    exclude_venue: Optional[list[str]] = typer.Option(
        None,
        "--exclude-venue",
        help="A venue to exclude; repeat the option for multiple venues.",
    ),
    filters: Optional[str] = typer.Option(None, "--filters", help="JSON room filters."),
    limit: int = typer.Option(20, "--limit", "-l", help="Maximum number of results."),
    offset: int = typer.Option(0, "--offset", help="Number of results to skip."),
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Find teaching-free rooms; this does not establish occupancy or bookability."""
    with application_scope():
        from stars.tools import rooms

        window = {
            "day": day,
            "start_time": start_time,
            "end_time": end_time,
            "teaching_weeks": teaching_weeks,
            "buffer_minutes": buffer_minutes,
        }
        room_filters = parse_json(filters) if filters else {}
        if not isinstance(room_filters, dict):
            raise typer.BadParameter("--filters must be a JSON object.")
        for key, value in (
            ("room_types", room_type),
            ("venue_contains", venue_contains),
            ("venue_prefixes", venue_prefix),
            ("exclude_venues", exclude_venue),
        ):
            if value is not None:
                if key in room_filters:
                    raise typer.BadParameter(
                        f"Specify {key} through either --filters or its option, not both."
                    )
                room_filters[key] = value
        return invoke(
            rooms.find_available_rooms,
            {
                "academic_year": academic_year,
                "semester": semester,
                "window": window,
                "filters": room_filters or None,
                "limit": limit,
                "offset": offset,
                "refresh": refresh,
            },
            json_output,
        )


g_indexes.command("list")(cmd_indexes_default)
