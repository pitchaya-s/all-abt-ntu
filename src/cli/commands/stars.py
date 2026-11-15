"""Stars service commands."""

from typing import Literal, Optional

from functools import partial

import typer

from ..helpers import group, parse_json, read_json_file
from ..execution import application_scope
from ..services import invoke

app = typer.Typer(no_args_is_help=True)
g_auth = group(default=False)
app.add_typer(g_auth, name="auth")
g_courses = group(default=False)
app.add_typer(g_courses, name="courses")
g_indexes = group(default=True)
app.add_typer(g_indexes, name="indexes")
g_planner = group(default=False)
app.add_typer(g_planner, name="planner")
g_rooms = group(default=False)
app.add_typer(g_rooms, name="rooms")


@g_courses.command("search")
def cmd_courses_search(
    query: str,
    academic_year: int = typer.Option(..., "--year", "-y"),
    semester: Literal[1, 2, "S"] = typer.Option(..., "--semester", "-s"),
    study_mode: Literal["full_time", "part_time"] = "full_time",
    limit: int = typer.Option(20, "--limit", "-l"),
    offset: int = 0,
    json_output: bool = typer.Option(False, "--json", "-j"),
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
    course_code: str,
    academic_year: int = typer.Option(..., "--year", "-y"),
    semester: Literal[1, 2, "S"] = typer.Option(..., "--semester", "-s"),
    json_output: bool = typer.Option(False, "--json", "-j"),
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
    course_code: str,
    academic_year: int = typer.Option(..., "--year", "-y"),
    semester: Literal[1, 2, "S"] = typer.Option(..., "--semester", "-s"),
    prerequisite_depth: int = 2,
    dependent_depth: int = 2,
    completed_courses: Optional[list[str]] = typer.Option(None, "--completed"),
    only_eligible: bool = typer.Option(False, "--eligible-only"),
    include_corequisites: bool = typer.Option(False, "--include-corequisites"),
    max_nodes: int = 100,
    json_output: bool = typer.Option(False, "--json", "-j"),
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
    course_code: str,
    academic_year: int = typer.Option(..., "--year", "-y"),
    semester: Literal[1, 2, "S"] = typer.Option(..., "--semester", "-s"),
    limit: int = typer.Option(10, "--limit", "-l"),
    offset: int = 0,
    json_output: bool = typer.Option(False, "--json", "-j"),
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
    course_code: str,
    index: str,
    academic_year: int = typer.Option(..., "--year", "-y"),
    semester: Literal[1, 2, "S"] = typer.Option(..., "--semester", "-s"),
    json_output: bool = typer.Option(False, "--json", "-j"),
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
    course_code: str,
    indexes: list[str] = typer.Argument(...),
    academic_year: int = typer.Option(..., "--year", "-y"),
    semester: Literal[1, 2, "S"] = typer.Option(..., "--semester", "-s"),
    against_sessions: Optional[str] = typer.Option(
        None, "--against", help="Read JSON from a file."
    ),
    json_output: bool = typer.Option(False, "--json", "-j"),
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
    course_code: str,
    academic_year: int = typer.Option(..., "--year", "-y"),
    semester: Literal[1, 2, "S"] = typer.Option(..., "--semester", "-s"),
    constraints: Optional[str] = typer.Option(
        None, "--constraints", help="Read JSON from a file."
    ),
    against_sessions: Optional[str] = typer.Option(
        None, "--against", help="Read JSON from a file."
    ),
    json_output: bool = typer.Option(False, "--json", "-j"),
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
    course_code: str,
    academic_year: Optional[int] = typer.Option(None, "--year", "-y"),
    semester: Optional[Literal[1, 2]] = typer.Option(None, "--semester", "-s"),
    json_output: bool = typer.Option(False, "--json", "-j"),
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
    course_code: str,
    json_output: bool = typer.Option(False, "--json", "-j"),
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
    venue: str,
    academic_year: int = typer.Option(..., "--year", "-y"),
    semester: Literal[1, 2, "S"] = typer.Option(..., "--semester", "-s"),
    day: Optional[Literal["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]] = None,
    teaching_weeks: Optional[list[int]] = typer.Option(None, "--week"),
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    limit: int = typer.Option(50, "--limit", "-l"),
    offset: int = 0,
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
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
def cmd_auth_status(json_output: bool = typer.Option(False, "--json", "-j")):
    """Report whether WISH credentials are configured and whether this process has verified a session."""
    with application_scope() as application:
        return invoke(application.stars_personal.status, {}, json_output)


@g_planner.command("show")
def cmd_planner_show(
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
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
    plan_number: Literal[1, 2, 3],
    courses: str = typer.Option(..., "--courses", help="Read JSON from a file."),
    academic_year: int = typer.Option(..., "--year", "-y"),
    semester: Literal[1, 2] = typer.Option(..., "--semester", "-s"),
    json_output: bool = typer.Option(False, "--json", "-j"),
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
def cmd_audit(json_output: bool = typer.Option(False, "--json", "-j")):
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
    academic_year: int = typer.Option(..., "--year", "-y"),
    semester: Literal[1, 2, "S"] = typer.Option(..., "--semester", "-s"),
    day: Literal["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"] = typer.Option(
        ..., "--day"
    ),
    start_time: str = typer.Option(..., "--from"),
    end_time: str = typer.Option(..., "--until"),
    teaching_weeks: Optional[list[int]] = typer.Option(None, "--week"),
    buffer_minutes: int = 0,
    room_type: Optional[list[str]] = typer.Option(
        None, "--room-type", autocompletion=complete_room_type
    ),
    venue_contains: Optional[str] = None,
    venue_prefix: Optional[list[str]] = typer.Option(None, "--venue-prefix"),
    exclude_venue: Optional[list[str]] = typer.Option(None, "--exclude-venue"),
    filters: Optional[str] = typer.Option(None, "--filters", help="JSON room filters."),
    limit: int = typer.Option(20, "--limit", "-l"),
    offset: int = 0,
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
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
