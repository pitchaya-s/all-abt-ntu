"""Presentations for course registration and schedules."""

from rich.table import Table
from rich.tree import Tree

from .common import auth_status as auth_status
from .common import detail, details, listing, notices, pagination, table, text

courses_search = listing("Courses", "courses", ("course_code", "course_name", "au"))
course = detail(
    "Course",
    (
        "course_code",
        "course_name",
        "au",
        "course_description",
        "course_description_status",
        "prerequisites",
        "course_notes",
    ),
)
rooms_schedule = listing(
    "Room teaching schedule",
    "sessions",
    (
        "course_code",
        "indexes",
        "lesson_type",
        "group",
        "day",
        "start_time",
        "end_time",
        "teaching_weeks",
        "remarks",
    ),
)
SESSION_FIELDS = (
    "lesson_type",
    "group",
    "day",
    "start_time",
    "end_time",
    "venue",
    "teaching_weeks",
    "remarks",
    "raw_time",
)


def audit(console, data):
    for key, title in (
        ("requirements", "Requirements"),
        ("examination_results", "Examination results"),
        ("courses_registered", "Registered courses"),
    ):
        tables = data.get(key) or []
        if not tables:
            console.print(f"{title}: No results.")
        for item in tables:
            heading = title
            if item.get("section"):
                heading += f" — {item['section']}"
            headers = item.get("headers") or []
            rows = item.get("rows")
            if rows is not None and headers:
                view = Table(title=heading)
                for header in headers:
                    view.add_column(str(header), overflow="fold")
                for row in rows:
                    view.add_row(
                        *(
                            text(row[i]) if i < len(row) else ""
                            for i in range(len(headers))
                        )
                    )
                console.print(view)
            else:
                records = item.get("records") or []
                fields = headers or (list(records[0]) if records else [])
                table(console, heading, records, fields)
        status = data.get(key + "_status")
        if status and status not in ("parsed", "empty"):
            console.print(f"{title} status: {status}")


def exams(console, data):
    table(
        console,
        "Exams",
        data.get("exams"),
        (
            "date",
            "day",
            "start_time",
            "end_time",
            "duration_minutes",
            "duration_text",
            "venue",
            "raw_date",
            "raw_time",
        ),
    )
    if data.get("notice"):
        console.print(data["notice"])
    if data.get("exam_status") == "not_listed":
        console.print("No exam is listed for this course.")
    notices(console, data)


def prerequisites(console, data):
    def node(parent, item):
        name = " — ".join(
            str(item[k]) for k in ("course_code", "course_name") if item.get(k)
        )
        branch = parent.add(name or "Course")
        for field in ("prerequisite_text", "eligibility_status", "match_status"):
            if item.get(field) and item[field] not in ("root", "not_evaluated"):
                branch.add(f"{field.replace('_', ' ').capitalize()}: {item[field]}")
        for field in ("prerequisites", "dependents"):
            if item.get(field):
                group = branch.add(field.capitalize())
                for child in item[field]:
                    node(group, child)

    tree = Tree("Course relationships")
    node(tree, data.get("root") or {})
    console.print(tree)
    notices(console, data)


def indexes_default(console, data):
    for item in data.get("indexes") or []:
        title = f"Index {item.get('index', '')}"
        details(
            console,
            title,
            item,
            (
                "vacancy_status",
                "vacancies_available",
                "waitlist_length",
                "schedule_complete",
            ),
        )
        table(console, "Schedule", item.get("sessions"), SESSION_FIELDS)
    if not data.get("indexes"):
        console.print("Indexes: No results.")
    pagination(console, data)


def index(console, data):
    details(
        console,
        "Index",
        data,
        (
            "course_code",
            "index",
            "vacancy_status",
            "vacancies_available",
            "waitlist_length",
            "schedule_complete",
        ),
    )
    table(console, "Schedule", data.get("sessions"), SESSION_FIELDS)
    notices(console, data)


def indexes_compare(console, data):
    table(console, "Common sessions", data.get("common_sessions"), SESSION_FIELDS)
    for name, sessions in (data.get("unique_sessions_by_index") or {}).items():
        table(console, f"Index {name}", sessions, SESSION_FIELDS)
    if data.get("clash_check"):
        details(console, "Clash check", data, ("clash_check",))
    notices(console, data)


def indexes_match(console, data):
    for item in data.get("matches") or []:
        details(
            console,
            f"Index {item.get('index', '')}",
            item,
            ("status", "uncertainties", "schedule_complete"),
        )
        table(console, "Schedule", item.get("sessions"), SESSION_FIELDS)
    if not data.get("matches"):
        console.print("Matching indexes: No results.")
    notices(console, data)


def graduate(console, data):
    details(
        console,
        "Graduate course",
        data,
        (
            "course_code",
            "course_name",
            "au",
            "academic_year",
            "term",
            "schedule_complete",
        ),
    )
    for group in data.get("class_groups") or []:
        details(
            console,
            group.get("class_group") or "Class group",
            group,
            ("coordinator", "schedule_remarks", "schedule_text"),
        )
        table(
            console,
            "Schedule",
            group.get("sessions"),
            SESSION_FIELDS + ("commence_date",),
        )


def rooms_available(console, data):
    console.print(
        "Rooms have no known scheduled teaching; availability or booking is not guaranteed."
    )
    table(
        console,
        "Teaching-free rooms",
        data.get("rooms"),
        ("venue", "room_type", "free_from", "free_until"),
    )
    pagination(console, data)
    details(console, "Coverage", data, ("coverage", "excluded_uncertain_count"))


def planner_show(console, data):
    if data.get("registration_notice"):
        console.print(data["registration_notice"])
    registered = [
        {
            "course_code": row.get("course_code") or row.get("Course"),
            "course_name": row.get("Course Title") or row.get("Course Name"),
            "index": row.get("index") or row.get("Index No"),
            "au": row.get("Course AU") or row.get("AU"),
            "course_type": row.get("course_type") or row.get("Type"),
        }
        for row in data.get("registered_courses") or []
    ]
    table(
        console,
        "Registered courses",
        registered,
        ("course_code", "course_name", "index", "au", "course_type"),
    )
    status = data.get("registered_courses_status")
    if status and status not in ("parsed", "empty"):
        console.print(f"Registered courses status: {status}")
    for plan in data.get("saved_plans") or []:
        details(
            console,
            f"Plan {plan.get('plan_number')}",
            plan,
            ("status", "timetable_status"),
        )
        table(
            console,
            "Courses",
            plan.get("courses"),
            ("course_code", "index", "course_type"),
        )
        table(
            console,
            "Schedule",
            plan.get("sessions"),
            ("course_code", "index") + SESSION_FIELDS,
        )
        if plan.get("unparsed_sessions"):
            details(console, "Unparsed sessions", plan, ("unparsed_sessions",))


def planner_save(console, data):
    details(
        console,
        "Saved plan",
        data,
        ("status", "academic_year", "semester", "saved_plan"),
    )
