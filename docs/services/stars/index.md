# STARS

[Service overview](index.md) · [CLI reference](cli/index.md) · [MCP reference](mcp/index.md)

Search undergraduate courses, inspect schedules and indexes, and explore prerequisites. Public information does not need an NTU account; the planner and degree audit use your saved credentials.

## Service notes


These tools run in the shared `all-abt-ntu-mcp` server. See the [getting started guide](../../getting-started.md) for installation and client configuration.

Public academic and room operations are implemented in `tools/academic.py` and `tools/rooms.py`; `mcp.py` registers the MCP tools and their agent guidance. Authenticated operations live in `tools/personal.py` and are available only with the local personal profile; the hosted HTTP server exposes public tools only. Tool schemas are grouped in `schemas/`, with room-specific schemas in `schemas/rooms.py`.

### Inputs and results

Undergraduate schedule tools take a `course_code`, `academic_year`, and `semester`. The year is the first year of the academic year; semester is `1`, `2`, or `"S"` for Special Term. Course codes contain letters and digits, up to 10 characters. Keep index numbers as strings.

Examples below use fictional course codes, indexes, and years. Replace them with the course and published term you want to query.

Times use 24-hour `HH:MM` in Singapore time. Days use `MON` through `SUN`. Teaching-week numbers refer to the requested semester, rather than calendar weeks. Missing information remains unknown; it is not treated as zero or an empty requirement.

Every tool publishes an output schema. Index sessions inherit the course/index identifiers from their enclosing result. Unrecognized schedule values remain in raw fields, and uncertain matches are labeled explicitly.

### Vacancy and cache behavior

Vacancy lookup runs only from **09:00–22:00 Singapore time**. Counts are attached only when NTU's published vacancy term matches the requested schedule. Index status may be `available`, `not_listed`, `closed`, `term_mismatch`, or `unavailable`. Unknown vacancy/waitlist values are `null`; a reported zero is a known value. Schedules remain usable when vacancy data is unavailable.

Public responses are cached in memory for one hour by default. STARS public reads reuse pooled HTTPS connections and share the process-wide per-host request limit with other public clients. Public tools do not retain cookies; the multi-step General Access exam lookup keeps its form cookie only in a short-lived client for that lookup. Room tools share a separate term-wide full-time/part-time snapshot with the same lifetime and a four-term cache bound. `NTU_CACHE_TTL_SECONDS` changes that lifetime; `0` disables it. Vacancy snapshots are cached for at most 60 seconds. Personal WISH records use `NTU_PERSONAL_CACHE_TTL_SECONDS`, default 300 seconds. Sessions and personal records are not persisted to disk, and expired sessions trigger an authorized fresh login.

### Sources

Only NTU endpoints supply timetable and academic records. Forms are followed with their current request fields; this server does not use third-party course databases.

| Service | Official entry and response endpoints | Why used |
| --- | --- | --- |
| Class Schedule | [Current form](https://wish.wis.ntu.edu.sg/webexe/owa/AUS_schedule_NEW.class), [schedule response](https://wish.wis.ntu.edu.sg/webexe/owa/AUS_SCHEDULE_NEW.main_display1) | Search offerings and retrieve indexes, sessions, AUs, prerequisites, and remarks |
| Course descriptions | [Content of Courses form](https://wish.wis.ntu.edu.sg/webexe/owa/aus_subj_cont.main), [content response](https://wish.wis.ntu.edu.sg/webexe/owa/AUS_SUBJ_CONT.main_display1) | Course descriptions when published |
| Vacancies | [Public vacancy form](https://wish.wis.ntu.edu.sg/webexe/owa/aus_vacancy.check_vacancy), [vacancy response](https://wish.wis.ntu.edu.sg/webexe/owa/aus_vacancy.check_vacancy2) | Published vacancy term, per-index vacancies, and waitlist lengths |
| Graduate timetable | [GSLink/PGR entry](https://wish.wis.ntu.edu.sg/pls/webexe/pgr%24subrs_timetable.mmenu), [class timetable](https://wish.wis.ntu.edu.sg/pls/webexe/pgr%24subrs_timetable.examTimetable) | Currently published graduate groups and sessions |
| Undergraduate exams | [General Access entry](https://wis.ntu.edu.sg/webexe/owa/exam_timetable_und.main), [selection](https://wis.ntu.edu.sg/webexe/owa/exam_timetable_und.MainSubmit), [term page](https://wis.ntu.edu.sg/webexe/owa/exam_timetable_und.query_page), [exam response](https://wis.ntu.edu.sg/webexe/owa/exam_timetable_und.Get_detail) | Published exam dates/times through the public form workflow |
| STARS Planner | [Authenticated entry](https://wish.wis.ntu.edu.sg/pls/webexe/aus_stars_planner.main), [selection](https://wish.wis.ntu.edu.sg/pls/webexe/AUS_STARS_PLANNER.time_table), [Planner view](https://wish.wis.ntu.edu.sg/pls/webexe/AUS_STARS_PLANNER.planner), [load plan](https://wish.wis.ntu.edu.sg/pls/webexe/AUS_STARS_PLANNER.load_time_table), [save plan](https://wish.wis.ntu.edu.sg/pls/webexe/AUS_STARS_PLANNER.save_time_table) | Registered courses and saved plans; saving is limited to the chosen saved plan |

On 6 November 2026, the public Class Schedule form contained the hidden `staff_access=true` field. The client reproduces that public form value and sends no credentials to this endpoint; the field name alone does not establish that the caller is staff.
| Degree Audit | [Authenticated audit](https://wish.wis.ntu.edu.sg/pls/webexe/DARS_RESULT_RO.main_display) | The student's published degree requirements and academic tables |

WISH authentication follows NTU's [login workflow](https://wish.wis.ntu.edu.sg/pls/webexe/ldap_login.login). Credentials come from the [shared credential store](../../architecture/credentials.md#credential-storage), also used by NTULearn and LibFacilities; access restrictions and challenges are respected. Manage it locally with `ntu auth save`, `auth status`, and `auth delete`. Passwords are never accepted as MCP arguments or read from environment variables/config files.

### Tests

Run commands from the repository root. Offline fixtures use fictional course labels/indexes and synthetic personal records.

```sh
uv run python -m unittest discover -s tests -t . -v
uv run python tests/stars/live_smoke.py --course-code COURSE_CODE --academic-year YEAR --semester 1
uv run python tests/stars/live_search_smoke.py --query SEARCH_TEXT --academic-year YEAR --semester 1
uv run python tests/stars/live_rooms_smoke.py --academic-year YEAR --semester 1 --day WED --start-time 14:00 --end-time 16:00 --week WEEK
uv run python tests/stars/live_exam_smoke.py --course-code COURSE_CODE
uv run --extra personal python tests/stars/live_personal_smoke.py
```

Replace placeholders for opt-in live checks. Public smoke tests accept caller-selected courses and terms. The personal smoke test reads records without editing saved plans; output is limited to counts and statuses.
