# STARS: CLI reference

[Service overview](../index.md) · [CLI reference](index.md) · [MCP reference](../mcp/index.md)

## Example

Search the published undergraduate schedule. The academic year is its first year; `2026` means AY2026/27.

```sh
ntu stars courses search "data structures" --year 2026 --semester 1 --limit 10
```

## Commands

Choose a command for its arguments, examples and result fields. Use `ntu stars --help` and append `--help` to a command for option details. Each command page identifies required arguments and any defaults. See the [complete CLI reference](../../../cli/commands.md) for shared settings and all services.

### Courses, prerequisites and exams

Search the published schedule or inspect a course, its prerequisites or exam. `--year` is the first year of the academic year.

| Command | What it does |
| --- | --- |
| [`ntu stars course`](courses.md#cmd-stars-course) | Get course name, AUs, prerequisites, description, and term metadata. |
| [`ntu stars prerequisites`](courses.md#cmd-stars-prerequisites) | Build before and after branches around a course, with separate depth limits.  The before branch follows the course's prerequisite rules; the after branch finds courses that depend on it in the selected term. |
| [`ntu stars exams`](courses.md#cmd-stars-exams) | Get public General Access exam dates and times for a course in the latest or specified published term. |
| [`ntu stars graduate`](courses.md#cmd-stars-graduate) | Get a graduate course's class groups for NTU's currently published academic term. |
| [`ntu stars courses search`](courses.md#cmd-stars-courses-search) | Search NTU's public undergraduate Class Schedule by partial code or title keywords. |

### Indexes and timetables

List indexes or compare their schedules. For `compare` and `match`, `--against` reads an existing timetable from a JSON file; `--constraints` also reads a JSON file.

| Command | What it does |
| --- | --- |
| [`ntu stars index`](indexes.md#cmd-stars-index) | Get one index's complete schedule, vacancies, and waitlist where matching-term counts are published. |
| [`ntu stars indexes compare`](indexes.md#cmd-stars-indexes-compare) | Compare shared and index-specific sessions; optionally check clashes with supplied time slots. |
| [`ntu stars indexes match`](indexes.md#cmd-stars-indexes-match) | Find indexes matching day/time/lesson/week rules and avoiding supplied timetable clashes. |
| [`ntu stars indexes list`](indexes.md#cmd-stars-indexes-list) | List a page of indexes with timetable details and matching-term vacancies/waitlists. |

### Rooms

Room searches use published teaching schedules. A teaching-free result does not establish that a room is unoccupied or bookable.

| Command | What it does |
| --- | --- |
| [`ntu stars rooms schedule`](rooms.md#cmd-stars-rooms-schedule) | Get all published undergraduate course/index lessons using one observed room, including full-time and part-time offerings. |
| [`ntu stars rooms available`](rooms.md#cmd-stars-rooms-available) | Find teaching-free rooms; this does not establish occupancy or bookability. |

### Personal planner and audit

These commands use your saved NTU account. `planner save` replaces the entire selected plan with the supplied JSON course list and requires confirmation.

| Command | What it does |
| --- | --- |
| [`ntu stars audit`](personal.md#cmd-stars-audit) | Get your degree requirements, examination results, and registered courses from Degree Audit. |
| [`ntu stars auth status`](personal.md#cmd-stars-auth-status) | Report whether WISH credentials are configured and whether this process has verified a session. |
| [`ntu stars planner show`](personal.md#cmd-stars-planner-show) | Get registered courses, the published term, and saved Plans 1–3 with indexes and timetables. |
| [`ntu stars planner save`](personal.md#cmd-stars-planner-save) | Replace saved Plan 1, 2, or 3 with the complete supplied course/index list for the current Planner term. |
