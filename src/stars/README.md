# STARS tool guide

[CLI commands](#cli-commands) · [MCP tools](#mcp-tools) · [MCP data types](#mcp-data-types) · [Service notes](#service-notes)

For installation and shared authentication, see the [main README](../../README.md).

## CLI commands

The output column lists the JSON result fields; human-readable output is formatted for the terminal. Use `ntu stars --help` and append `--help` to a command for option details. `VALUE` denotes an option value; required arguments and options are marked. See the [complete CLI reference](../COMMANDS.md) for shared settings and all services.

| Command | Arguments and options | Purpose | Output |
| --- | --- | --- | --- |
| `ntu stars course` | `COURSE_CODE (required)`, `--year/-y VALUE (required)`, `--semester/-s VALUE [1, 2, S] (required)`, `--json/-j` | Get course name, AUs, prerequisites, description, and term metadata. | `course_code`, `academic_year`, `semester`, `course_name`, `au`, `course_description`, `course_description_status`, `course_description_source`, `prerequisites`, `course_notes`, `retrieved_at`, `official_source` ([schema](#stars_get_course_metadata)) |
| `ntu stars prerequisites` | `COURSE_CODE (required)`, `--year/-y VALUE (required)`, `--semester/-s VALUE [1, 2, S] (required)`, `--prerequisite-depth VALUE (default: 2)`, `--dependent-depth VALUE (default: 2)`, `--completed VALUE`, `--eligible-only`, `--include-corequisites`, `--max-nodes VALUE (default: 100)`, `--json/-j` | Build before and after branches around a course, with separate depth limits.  The before branch follows the course's prerequisite rules; the after branch finds courses that depend on it in the selected term. | `course_code`, `academic_year`, `semester`, `prerequisite_depth`, `dependent_depth`, `include_corequisites`, `only_eligible`, `completed_courses`, `prerequisite_course_count`, `dependent_course_count`, `tree_node_count`, `prerequisites_truncated`, `dependents_truncated`, `truncated`, `coverage`, `root`, `source_urls`, `retrieved_at` ([schema](#stars_get_prerequisite_tree)) |
| `ntu stars index` | `COURSE_CODE (required)`, `INDEX (required)`, `--year/-y VALUE (required)`, `--semester/-s VALUE [1, 2, S] (required)`, `--json/-j` | Get one index's complete schedule, vacancies, and waitlist where matching-term counts are published. | `course_code`, `academic_year`, `semester`, `vacancy_status`, `vacancies_available`, `waitlist_length`, `index`, `vacancy_metadata`, `schedule_complete`, `sessions` ([schema](#stars_get_index)) |
| `ntu stars exams` | `COURSE_CODE (required)`, `--year/-y VALUE`, `--semester/-s VALUE [1, 2]`, `--json/-j` | Get public General Access exam dates and times for a course in the latest or specified published term. | `course_code`, `course_name`, `academic_year`, `semester`, `exam_status`, `exam_count`, `exams`, `notice`, `source_url`, `retrieved_at` ([schema](#stars_get_undergraduate_exam_schedule)) |
| `ntu stars graduate` | `COURSE_CODE (required)`, `--json/-j` | Get a graduate course's class groups for NTU's currently published academic term. | `course_code`, `course_name`, `au`, `academic_year`, `term`, `schedule_complete`, `class_groups`, `source_url` ([schema](#stars_get_graduate_course_schedule)) |
| `ntu stars audit` | `--json/-j` | Get your degree requirements, examination results, and registered courses from Degree Audit. | `service`, `page_title`, `requirements`, `requirements_status`, `examination_results`, `examination_results_status`, `courses_registered`, `courses_registered_status`, `source_url`, `retrieved_at`, `from_cache`, `cache_age_seconds` ([schema](#stars_get_degree_audit)) |
| `ntu stars auth status` | `--json/-j` | Report whether WISH credentials are configured and whether this process has verified a session. | `credentials_configured`, `credential_storage`, `credential_error`, `session_verified`, `last_verified_at`, `session_storage`, `personal_cache_ttl_seconds` ([schema](#stars_auth_status)) |
| `ntu stars courses search` | `QUERY (required)`, `--year/-y VALUE (required)`, `--semester/-s VALUE [1, 2, S] (required)`, `--study-mode VALUE [full_time, part_time] (default: full_time)`, `--limit/-l VALUE (default: 20)`, `--offset VALUE`, `--json/-j` | Search NTU's public undergraduate Class Schedule by partial code or title keywords. | `query`, `academic_year`, `semester`, `study_mode`, `total_count`, `offset`, `has_more`, `courses`, `source_url`, `retrieved_at` ([schema](#stars_search_courses)) |
| `ntu stars indexes compare` | `COURSE_CODE (required)`, `INDEXES... (required)`, `--year/-y VALUE (required)`, `--semester/-s VALUE [1, 2, S] (required)`, `--against VALUE`, `--json/-j` | Compare shared and index-specific sessions; optionally check clashes with supplied time slots. | `course_code`, `academic_year`, `semester`, `retrieved_at`, `official_source`, `indexes_compared`, `common_sessions`, `unique_sessions_by_index`, `clash_check` ([schema](#stars_compare_indexes)) |
| `ntu stars indexes match` | `COURSE_CODE (required)`, `--year/-y VALUE (required)`, `--semester/-s VALUE [1, 2, S] (required)`, `--constraints VALUE`, `--against VALUE`, `--json/-j` | Find indexes matching day/time/lesson/week rules and avoiding supplied timetable clashes. | `course_code`, `academic_year`, `semester`, `retrieved_at`, `official_source`, `constraints`, `against_session_count`, `match_count`, `matches` ([schema](#stars_find_matching_indexes)) |
| `ntu stars indexes list` | `COURSE_CODE (required)`, `--year/-y VALUE (required)`, `--semester/-s VALUE [1, 2, S] (required)`, `--limit/-l VALUE (default: 10)`, `--offset VALUE`, `--json/-j` | List a page of indexes with timetable details and matching-term vacancies/waitlists. | `course_code`, `academic_year`, `semester`, `index_count`, `offset`, `next_offset`, `vacancy_metadata`, `indexes` ([schema](#stars_get_course_indexes)) |
| `ntu stars planner show` | `--refresh/-r`, `--json/-j` | Get registered courses, the published term, and saved Plans 1–3 with indexes and timetables. | `service`, `page_title`, `academic_year`, `semester`, `registration_notice`, `registered_courses`, `registered_courses_status`, `planner_tables`, `timetable_tables`, `timetable_status`, `saved_plans`, `source_url`, `retrieved_at`, `from_cache`, `cache_age_seconds` ([schema](#stars_get_stars_planner)) |
| `ntu stars planner save` | `PLAN_NUMBER (required)`, `--courses VALUE (required)`, `--year/-y VALUE (required)`, `--semester/-s VALUE [1, 2] (required)`, `--json/-j` | Replace saved Plan 1, 2, or 3 with the complete supplied course/index list for the current Planner term. | `status`, `academic_year`, `semester`, `saved_plan`, `verified_at`, `source_url` ([schema](#stars_save_stars_plan)) |
| `ntu stars rooms schedule` | `VENUE (required)`, `--year/-y VALUE (required)`, `--semester/-s VALUE [1, 2, S] (required)`, `--day VALUE [MON, TUE, WED, THU, FRI, SAT, SUN]`, `--week VALUE`, `--start-time VALUE`, `--end-time VALUE`, `--limit/-l VALUE (default: 50)`, `--offset VALUE`, `--refresh/-r`, `--json/-j` | Get all published undergraduate course/index lessons using one observed room, including full-time and part-time offerings. | `academic_year`, `semester`, `source_url`, `retrieved_at`, `cached`, `coverage`, `room`, `session_count`, `offset`, `has_more`, `sessions` ([schema](#stars_get_room_schedule)) |
| `ntu stars rooms available` | `--year/-y VALUE (required)`, `--semester/-s VALUE [1, 2, S] (required)`, `--day VALUE [MON, TUE, WED, THU, FRI, SAT, SUN] (required)`, `--from VALUE (required)`, `--until VALUE (required)`, `--week VALUE`, `--buffer-minutes VALUE`, `--room-type VALUE`, `--venue-contains VALUE`, `--venue-prefix VALUE`, `--exclude-venue VALUE`, `--filters VALUE`, `--limit/-l VALUE (default: 20)`, `--offset VALUE`, `--refresh/-r`, `--json/-j` | Find teaching-free rooms; this does not establish occupancy or bookability. | `academic_year`, `semester`, `source_url`, `retrieved_at`, `cached`, `coverage`, `availability_basis`, `window`, `match_count`, `offset`, `has_more`, `rooms`, `excluded_busy_count`, `excluded_uncertain_count` ([schema](#stars_find_available_rooms)) |

## MCP tools

Inputs are required only where marked. Output fields marked required may still be `null` when their type allows it. See the nested data types below for object fields.

### `stars_search_courses`

Search NTU's public undergraduate Class Schedule by partial code or title keywords. Returns course codes, names and AUs for the requested term and study mode. Use offset/limit to page through matches, then stars_get_course_metadata or stars_get_course_indexes for details. This is not a graduate or all-catalogue search.

Find scheduled undergraduate offerings by partial code or title words.

**Inputs:** `query` of 2–80 characters, `academic_year`, `semester`; optional `study_mode` of `"full_time"` or `"part_time"`, `limit` of 1–100 with default 20, and nonnegative `offset` with default 0. Wildcards are not accepted.

**Returns:** course codes, names, AUs, `total_count`, `has_more`, and source/retrieval metadata. Continue with a larger offset to read another page. Results cover scheduled offerings for that term and study mode, rather than the entire historical catalogue or graduate courses.

```json
{"query":"ZZ00","academic_year":2030,"semester":1,"limit":20}
```

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `query` | `string` | Yes | Partial course code or title words, such as SC20 or DATA STRUCTURES; no wildcards; minimum length: `2`; maximum length: `80` |
| `academic_year` | `integer` | Yes | — |
| `semester` | `1`, `2`, `"S"` | Yes | — |
| `study_mode` | `"full_time"`, `"part_time"` | No | default: `"full_time"` |
| `limit` | `integer` | No | minimum: `1`; maximum: `100`; default: `20` |
| `offset` | `integer` | No | minimum: `0`; default: `0` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `query` | `string` | Yes | — |
| `academic_year` | `integer` | Yes | — |
| `semester` | `string` | Yes | — |
| `study_mode` | `"full_time"`, `"part_time"` | Yes | — |
| `total_count` | `integer` | Yes | — |
| `offset` | `integer` | Yes | — |
| `has_more` | `boolean` | Yes | — |
| `courses` | array of [`CourseSearchMatch`](#mcp-type-coursesearchmatch) | Yes | — |
| `source_url` | `string` | Yes | — |
| `retrieved_at` | `string` | Yes | — |

### `stars_get_course_metadata`

Get course name, AUs, prerequisites, description, and term metadata.

**Inputs:** `course_code`, `academic_year`, `semester`, optional `limit` (1–50, default 10) and non-negative `offset`.

**Returns:** course name, AU, prerequisites when published, course description, course notes, term, and source metadata. `course_description_status` distinguishes `available`, `not_listed`, and `unavailable`. This tool returns metadata rather than index timetables.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_code` | `string` | Yes | — |
| `academic_year` | `integer` | Yes | — |
| `semester` | `1`, `2`, `"S"` | Yes | — |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_code` | `string` | Yes | — |
| `academic_year` | `integer` or `null` | Yes | — |
| `semester` | `string` or `null` | Yes | — |
| `course_name` | `string` | Yes | — |
| `au` | `number` or `null` | Yes | — |
| `course_description` | `string` or `null` | Yes | — |
| `course_description_status` | `"available"`, `"not_listed"`, `"unavailable"` | Yes | — |
| `course_description_source` | `string` or `null` | Yes | — |
| `prerequisites` | `string` or `null` | Yes | — |
| `course_notes` | array of [`CourseNote`](#mcp-type-coursenote) | Yes | — |
| `retrieved_at` | `string` or `null` | Yes | — |
| `official_source` | `string` or `null` | Yes | — |

### `stars_get_prerequisite_tree`

Build before and after branches around a course, with separate depth limits.      The before branch follows the course's prerequisite rules; the after branch finds courses     that depend on it in the selected term. The center course is treated as completed for eligibility.

Build a tree around one course, with a **before** branch for its prerequisites and an **after** branch for courses that depend on it.

**Inputs:** `course_code`, `academic_year`, `semester`; optional `prerequisite_depth` and `dependent_depth`, each 0–5 with default 2; `completed_courses` (up to 100 course codes); `only_eligible` (default false); `include_corequisites` (default false); and `max_nodes` per branch, 1–100 with default 100. The center course is treated as completed for eligibility evaluation. `only_eligible` requires `completed_courses` and filters the **after** branch.

**Returns:** a nested tree with published prerequisite expressions on each course. Recognized `AND`/`OR` rules preserve their alternative paths; `completed_courses` marks which paths are satisfied. The **before** branch uses NTU course-content metadata for prerequisite courses that are not offered in the selected term. The **after** branch searches scheduled undergraduate offerings in that term across full-time and part-time study modes. `source_urls` lists the official endpoints used, and each expanded course includes its source when available.

Unrecognized expressions, conflicting full-time/part-time records, and unavailable off-term course metadata remain labeled uncertain. Possible text matches are not treated as confirmed prerequisite rules. The tree is bounded by both depth inputs and `max_nodes`; `prerequisites_truncated` and `dependents_truncated` identify a branch cut short. This is not a historical or complete course-catalogue search.

```json
{"course_code":"ZZ0001","academic_year":2030,"semester":1,"prerequisite_depth":2,"dependent_depth":2,"completed_courses":["MH1812"]}
```

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_code` | `string` | Yes | Course at the center of the prerequisite tree; minimum length: `2`; maximum length: `10` |
| `academic_year` | `integer` | Yes | — |
| `semester` | `1`, `2`, `"S"` | Yes | — |
| `prerequisite_depth` | `integer` | No | How many prerequisite levels to expand before the center course; minimum: `0`; maximum: `5`; default: `2` |
| `dependent_depth` | `integer` | No | How many dependent-course levels to expand after the center course; minimum: `0`; maximum: `5`; default: `2` |
| `completed_courses` | array of `string` or `null` | No | Courses already completed; the center course is added automatically for eligibility evaluation; default: `null`; maximum items: `100` |
| `only_eligible` | `boolean` | No | Keep only dependent courses whose parsed prerequisite rules are satisfied by completed_courses; default: `false` |
| `include_corequisites` | `boolean` | No | Also follow co-requisite links in both directions; default: `false` |
| `max_nodes` | `integer` | No | Maximum nodes per before/after branch; minimum: `1`; maximum: `100`; default: `100` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_code` | `string` | Yes | — |
| `academic_year` | `integer` | Yes | — |
| `semester` | `string` | Yes | — |
| `prerequisite_depth` | `integer` | Yes | — |
| `dependent_depth` | `integer` | Yes | — |
| `include_corequisites` | `boolean` | Yes | — |
| `only_eligible` | `boolean` | Yes | — |
| `completed_courses` | array of `string` or `null` | Yes | — |
| `prerequisite_course_count` | `integer` | Yes | — |
| `dependent_course_count` | `integer` | Yes | — |
| `tree_node_count` | `integer` | Yes | — |
| `prerequisites_truncated` | `boolean` | Yes | — |
| `dependents_truncated` | `boolean` | Yes | — |
| `truncated` | `boolean` | Yes | — |
| `coverage` | object of `integer` | Yes | — |
| `root` | [`PrerequisiteTreeNode`](#mcp-type-prerequisitetreenode) | Yes | — |
| `source_urls` | array of `string` | Yes | — |
| `retrieved_at` | `string` | Yes | — |

### `stars_get_course_indexes`

List a page of indexes with timetable details and matching-term vacancies/waitlists. Follow next_offset to see the rest. Sessions inherit course_code and index from their enclosing result; null raw_day/raw_time are omitted.

**Inputs:** `course_code`, `academic_year`, `semester`.

**Returns:** one page of indexes, their associated sessions, schedule completeness, vacancies, waitlist length, and vacancy metadata. `index_count` is the total; follow `next_offset` until it is null. Shared lectures remain attached to each applicable index. Sessions include lesson type, group, day, times, venue, teaching weeks, and remarks.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_code` | `string` | Yes | — |
| `academic_year` | `integer` | Yes | — |
| `semester` | `1`, `2`, `"S"` | Yes | — |
| `limit` | `integer` | No | minimum: `1`; maximum: `50`; default: `10` |
| `offset` | `integer` | No | minimum: `0`; default: `0` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_code` | `string` | Yes | — |
| `academic_year` | `integer` or `null` | Yes | — |
| `semester` | `string` or `null` | Yes | — |
| `index_count` | `integer` | Yes | — |
| `offset` | `integer` | Yes | — |
| `next_offset` | `integer` or `null` | Yes | — |
| `vacancy_metadata` | [`VacancyMetadata`](#mcp-type-vacancymetadata) | Yes | — |
| `indexes` | array of [`CourseIndex`](#mcp-type-courseindex) | Yes | — |

### `stars_get_index`

Get one index's complete schedule, vacancies, and waitlist where matching-term counts are published.

**Inputs:** `course_code`, `index`, `academic_year`, `semester`.

**Returns:** one index's sessions and matching-term vacancy snapshot. Use an index returned by `stars_get_course_indexes`; an unknown index produces an error rather than an empty timetable.

```json
{"course_code":"ZZ0001","index":"00001","academic_year":2030,"semester":1}
```

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_code` | `string` | Yes | — |
| `index` | `string` | Yes | — |
| `academic_year` | `integer` | Yes | — |
| `semester` | `1`, `2`, `"S"` | Yes | — |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_code` | `string` | Yes | — |
| `academic_year` | `integer` or `null` | Yes | — |
| `semester` | `string` or `null` | Yes | — |
| `vacancy_status` | `"available"`, `"not_listed"`, `"closed"`, `"term_mismatch"`, `"unavailable"` | Yes | — |
| `vacancies_available` | `integer` or `null` | Yes | — |
| `waitlist_length` | `integer` or `null` | Yes | — |
| `index` | `string` | Yes | — |
| `vacancy_metadata` | [`VacancyMetadata`](#mcp-type-vacancymetadata) | Yes | — |
| `schedule_complete` | `boolean` | Yes | — |
| `sessions` | array of [`CompactSession`](#mcp-type-compactsession) | Yes | — |

### `stars_compare_indexes`

Compare shared and index-specific sessions; optionally check clashes with supplied time slots.

**Inputs:** `course_code`, `academic_year`, `semester`, at least two unique `indexes`; optional `against_sessions`.

**Returns:** `common_sessions`, `unique_sessions_by_index`, and an optional `clash_check`. Common sessions apply to every entry in `indexes_compared`. Clash checks distinguish definite overlaps from comparisons with unknown week/day/time information.

```json
{"course_code":"ZZ0001","academic_year":2030,"semester":1,"indexes":["00001","00002"],"against_sessions":[{"day":"TUE","start_time":"14:00","end_time":"16:00","teaching_weeks":[2,4,6]}]}
```

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_code` | `string` | Yes | — |
| `indexes` | array of `string` | Yes | — |
| `academic_year` | `integer` | Yes | — |
| `semester` | `1`, `2`, `"S"` | Yes | — |
| `against_sessions` | array of [`TimeSlot`](#mcp-type-timeslot) or `null` | No | default: `null` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_code` | `string` | Yes | — |
| `academic_year` | `integer` or `null` | Yes | — |
| `semester` | `string` or `null` | Yes | — |
| `retrieved_at` | `string` or `null` | Yes | — |
| `official_source` | `string` or `null` | Yes | — |
| `indexes_compared` | array of `string` | Yes | — |
| `common_sessions` | array of [`CompactSession`](#mcp-type-compactsession) | Yes | — |
| `unique_sessions_by_index` | object of array of [`CompactSession`](#mcp-type-compactsession) | Yes | — |
| `clash_check` | [`ClashCheck`](#mcp-type-clashcheck) or `null` | Yes | — |

### `stars_find_matching_indexes`

Find indexes matching day/time/lesson/week rules and avoiding supplied timetable clashes.

**Inputs:** `course_code`, `academic_year`, `semester`; optional `constraints` and `against_sessions`.

Supported constraints:

| Field | Meaning |
| --- | --- |
| `avoid_days` | Reject sessions on the listed days |
| `earliest_start` | Every session must start at or after this time |
| `latest_end` | Every session must end by this time |
| `avoid_windows` | Reject overlaps with listed day/start/end windows |
| `require_sessions` | Each rule must match a session by lesson type, day, or start-time bounds |
| `teaching_weeks` | Evaluate sessions in the specified weeks, from 1–20 |

Required-session rules accept `lesson_type`, `day`, `starts_at_or_after`, and `starts_at_or_before`. Supply at least one condition per rule. Use lesson types as returned by NTU.

**Returns:** matching indexes with schedules, `status` of `confirmed` or `uncertain`, and reasons for uncertainty. Against-schedule slots accept `day`, `start_time`, `end_time`, and optional `teaching_weeks`. Use slots from the same academic year and semester. Overlaps in disjoint known teaching weeks do not clash.

```json
{"course_code":"ZZ0001","academic_year":2030,"semester":1,"constraints":{"avoid_days":["FRI"],"latest_end":"17:00","require_sessions":[{"lesson_type":"TUT","day":"TUE","starts_at_or_after":"13:00"}]}}
```

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_code` | `string` | Yes | — |
| `academic_year` | `integer` | Yes | — |
| `semester` | `1`, `2`, `"S"` | Yes | — |
| `constraints` | [`SearchConstraints`](#mcp-type-searchconstraints) or `null` | No | default: `null` |
| `against_sessions` | array of [`TimeSlot`](#mcp-type-timeslot) or `null` | No | default: `null` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_code` | `string` | Yes | — |
| `academic_year` | `integer` or `null` | Yes | — |
| `semester` | `string` or `null` | Yes | — |
| `retrieved_at` | `string` or `null` | Yes | — |
| `official_source` | `string` or `null` | Yes | — |
| `constraints` | [`ConstraintsResult`](#mcp-type-constraintsresult) | Yes | — |
| `against_session_count` | `integer` | Yes | — |
| `match_count` | `integer` | Yes | — |
| `matches` | array of [`MatchingIndex`](#mcp-type-matchingindex) | Yes | — |

### `stars_get_graduate_course_schedule`

Get a graduate course's class groups for NTU's currently published academic term.

**Input:** `course_code`.

**Returns:** the latest published graduate term, class groups, coordinators when provided, sessions, commencement dates, and schedule remarks. Graduate results use class groups rather than undergraduate indexes. GSLink/PGR does not publish teaching-week rules through this lookup.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_code` | `string` | Yes | — |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_code` | `string` | Yes | — |
| `course_name` | `string` | Yes | — |
| `au` | `number` or `null` | Yes | — |
| `academic_year` | `integer` | Yes | — |
| `term` | `string` | Yes | — |
| `schedule_complete` | `boolean` | Yes | — |
| `class_groups` | array of [`GraduateClassGroup`](#mcp-type-graduateclassgroup) | Yes | — |
| `source_url` | `string` | Yes | — |

### `stars_get_undergraduate_exam_schedule`

Get public General Access exam dates and times for a course in the latest or specified published term.

**Inputs:** `course_code`; optionally both `academic_year` and `semester` of `1` or `2`. Omitting both selects NTU's latest published exam term.

**Returns:** exam date, day, start/end time, duration, publication notice, source, and retrieval time. `exam_status` distinguishes `available` from `not_listed`. General Access does not provide personal exam-seat assignments.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_code` | `string` | Yes | — |
| `academic_year` | `integer` or `null` | No | default: `null` |
| `semester` | `1`, `2` or `null` | No | default: `null` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_code` | `string` | Yes | — |
| `course_name` | `string` or `null` | Yes | — |
| `academic_year` | `integer` | Yes | — |
| `semester` | `string` | Yes | — |
| `exam_status` | `"available"`, `"not_listed"` | Yes | — |
| `exam_count` | `integer` | Yes | — |
| `exams` | array of [`ExamResult`](#mcp-type-examresult) | Yes | — |
| `notice` | `string` or `null` | Yes | — |
| `source_url` | `string` | Yes | — |
| `retrieved_at` | `string` | Yes | — |

### `stars_find_available_rooms`

Find rooms with no known published undergraduate teaching throughout a day/time interval and every requested teaching week. Covers all indexes from both full-time and part-time schedules, including all lesson types. Filters select room type inferred from venue code, venue text/prefix, excluded rooms or observed lesson types. Unknown conflicting schedules are excluded. Only teaching-observed rooms are returned; this does not establish occupancy, access, capacity or availability against graduate classes, exams or other bookings. Times are Singapore time and weeks are semester teaching weeks. Omit weeks for a conservative whole-term check. Follow has_more with offset.

Find a teaching-observed room with no known scheduled undergraduate classes throughout a requested interval.

**Inputs:** `academic_year`, `semester`, and `window` with `day`, `start_time`, and `end_time`. Optional `window.teaching_weeks` selects semester teaching weeks, from 1–20; the room must be free in **every** selected week. Omitting weeks checks every published meeting conservatively across the term. `window.buffer_minutes`, default 0 and maximum 120, requires additional teaching-free time before and after the interval. The interval plus buffer must fit in one day.

Optional `filters`:

| Field | Meaning |
| --- | --- |
| `room_types` | `tutorial_room`, `seminar_room`, `lecture_theatre`, `laboratory`, or `other`, inferred from venue labels |
| `venue_contains` | Case-insensitive literal text within a normalized venue code |
| `venue_prefixes` | Any matching code prefix, such as `LHN`, `LHS`, `SPMS`, or `S4` |
| `exclude_venues` | Exact venue codes or equivalent normalized aliases to omit |
| `used_for_lesson_types` | Require observed use for any listed lesson type, such as `TUT` or `LAB` |

All lesson types still block availability, regardless of filters. `limit` is 1–100, default 20; `offset` defaults to 0. `refresh: true` reloads the complete shared teaching snapshot.

**Returns:** room codes, inferred types, observed aliases/lesson types, `free_from`/`free_until` teaching-free bounds on that day, total `match_count`, and pagination. A `free_until` of `24:00` is the end of the day, not a building opening-hours statement. Conflicting unknown days, times or teaching weeks exclude a room and contribute to `excluded_uncertain_count`; known clashes contribute to `excluded_busy_count`.

The first lookup fetches two public schedule pages concurrently: a blank-course search for full-time offerings and another for part-time offerings. Every published index/session is checked; no course-by-course crawl, course-description lookup or vacancy request is needed. Both pages must parse successfully before results are returned. The normalized snapshot is shared with room timetable lookups, cached for `NTU_CACHE_TTL_SECONDS`, and bounded to four terms.

Only recognizable room labels actually observed in teaching are candidates. Online, placeholder, date-like, course-reference and unrecognized venue labels are excluded. Common punctuation, quotation and tutorial-number variants are merged conservatively; multi-room cells block each independently observed component. Unknown raw venue text is retained in room timetable results. Coverage reports course/index/lesson counts, courses without published indexes, observed room count, excluded venue-label count and unplaced lesson count. Empty official index tables remain missing data; they do not establish that a course has no classes.

```json
{"academic_year":2030,"semester":1,"window":{"day":"WED","start_time":"14:00","end_time":"16:00","teaching_weeks":[7],"buffer_minutes":10},"filters":{"room_types":["tutorial_room","seminar_room"],"venue_prefixes":["LHN","LHS"]}}
```

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `academic_year` | `integer` | Yes | minimum: `2000`; maximum: `2100` |
| `semester` | `1`, `2`, `"S"` | Yes | — |
| `window` | [`RoomWindow`](#mcp-type-roomwindow) | Yes | — |
| `filters` | [`RoomFilters`](#mcp-type-roomfilters) or `null` | No | default: `null` |
| `limit` | `integer` | No | minimum: `1`; maximum: `100`; default: `20` |
| `offset` | `integer` | No | minimum: `0`; default: `0` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `academic_year` | `integer` | Yes | — |
| `semester` | `string` | Yes | — |
| `source_url` | `string` | Yes | — |
| `retrieved_at` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `coverage` | [`RoomCoverage`](#mcp-type-roomcoverage) | Yes | — |
| `availability_basis` | `"no_known_scheduled_teaching"` | No | default: `"no_known_scheduled_teaching"` |
| `window` | [`RoomWindow`](#mcp-type-roomwindow) | Yes | — |
| `match_count` | `integer` | Yes | — |
| `offset` | `integer` | Yes | — |
| `has_more` | `boolean` | Yes | — |
| `rooms` | array of [`AvailableRoom`](#mcp-type-availableroom) | Yes | — |
| `excluded_busy_count` | `integer` | Yes | — |
| `excluded_uncertain_count` | `integer` | Yes | — |

Unknown fields are not accepted.

### `stars_get_room_schedule`

Get all published undergraduate course/index lessons using one observed room, including full-time and part-time offerings. Accepts a venue code or returned alias. Shared lessons carry all associated index numbers. Optional day, teaching weeks and overlapping time interval filter the result; uncertain lessons remain included. Missing weeks/times are unknown. Paginate with offset/limit and has_more. This is teaching data, not room bookings or actual occupancy.

Retrieve the courses and indexes using a room, from the same complete full-time/part-time undergraduate teaching snapshot.

**Inputs:** `venue`, `academic_year`, `semester`. Optional `day`, `teaching_weeks`, and both `start_time`/`end_time` restrict the result to potentially overlapping lessons. Unknown timing/week data remains included rather than being silently discarded. `limit` is 1–100, default 50; `offset` defaults to 0. `refresh` reloads the shared snapshot.

**Returns:** the canonical venue and aliases, inferred room type, observed lesson types, and paginated sessions. Shared sessions are grouped with every associated index in `indexes`. Course codes and indexes remain strings. Sessions retain teaching weeks, unusual remarks, raw day/time values and original venue labels when they differ from the enclosing room. An unidentified venue returns an error rather than an empty or apparently free timetable.

```json
{"venue":"TR+7","academic_year":2030,"semester":1,"day":"TUE","teaching_weeks":[7]}
```

These tools report **no known scheduled undergraduate teaching**, not guaranteed room availability or occupancy. Graduate classes, exams, private bookings, closures and access restrictions are outside coverage. Room types are inferred from names; capacities, equipment, accessibility and opening hours are not supplied by this source. Bare `TR`/`LT` codes do not establish North/South Spine or a building location; use MazeMap for verified location information.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `venue` | `string` | Yes | minimum length: `1`; maximum length: `80` |
| `academic_year` | `integer` | Yes | minimum: `2000`; maximum: `2100` |
| `semester` | `1`, `2`, `"S"` | Yes | — |
| `day` | `"MON"`, `"TUE"`, `"WED"`, `"THU"`, `"FRI"`, `"SAT"`, `"SUN"` or `null` | No | default: `null` |
| `teaching_weeks` | array of `integer` or `null` | No | default: `null`; minimum items: `1`; maximum items: `20` |
| `start_time` | `string` or `null` | No | default: `null`; pattern: `^(?:[01]\d\|2[0-3]):[0-5]\d$` |
| `end_time` | `string` or `null` | No | default: `null`; pattern: `^(?:[01]\d\|2[0-3]):[0-5]\d$` |
| `limit` | `integer` | No | minimum: `1`; maximum: `100`; default: `50` |
| `offset` | `integer` | No | minimum: `0`; default: `0` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `academic_year` | `integer` | Yes | — |
| `semester` | `string` | Yes | — |
| `source_url` | `string` | Yes | — |
| `retrieved_at` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `coverage` | [`RoomCoverage`](#mcp-type-roomcoverage) | Yes | — |
| `room` | [`RoomIdentity`](#mcp-type-roomidentity) | Yes | — |
| `session_count` | `integer` | Yes | — |
| `offset` | `integer` | Yes | — |
| `has_more` | `boolean` | Yes | — |
| `sessions` | array of [`RoomLesson`](#mcp-type-roomlesson) | Yes | — |

Unknown fields are not accepted.

### `stars_auth_status`

Report whether WISH credentials are configured and whether this process has verified a session.

**Inputs:** none. Does not log in.

**Returns:** whether a shared keyring account is stored, `credential_storage` of `os_keyring`, a sanitized `credential_error` when unavailable, whether this process has verified a WISH session, its last verification time, and personal-cache settings. No credential or cookie values are returned.

`credentials_configured: null` means the store could not be read; it does not mean the account was never saved. `false` means a readable store has no account.

**Inputs**

None.

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `credentials_configured` | `boolean` or `null` | Yes | — |
| `credential_storage` | `"os_keyring"` | Yes | — |
| `credential_error` | `string` or `null` | Yes | — |
| `session_verified` | `boolean` | Yes | — |
| `last_verified_at` | `string` or `null` | Yes | — |
| `session_storage` | `string` | Yes | — |
| `personal_cache_ttl_seconds` | `integer` | Yes | — |

### `stars_get_stars_planner`

Get registered courses, the published term, and saved Plans 1–3 with indexes and timetables. Use refresh after editing a plan.

**Input:** optional `refresh`, default `false`. Requires credentials.

**Returns:** the published Planner term, registered courses and timetable information, and saved Plans 1–3 with their course/index lists and sessions. Registered courses and saved plans are separate sections. Status fields distinguish empty, parsed, and unavailable data. Use `refresh: true` after editing a plan.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `service` | `string` | Yes | — |
| `page_title` | `string` or `null` | Yes | — |
| `academic_year` | `integer` or `null` | Yes | — |
| `semester` | `integer` or `null` | Yes | — |
| `registration_notice` | `string` or `null` | Yes | — |
| `registered_courses` | array of object of `string` | Yes | — |
| `registered_courses_status` | `string` | Yes | — |
| `planner_tables` | array of [`PersonalTable`](#mcp-type-personaltable) | Yes | — |
| `timetable_tables` | array of [`PersonalTable`](#mcp-type-personaltable) | Yes | — |
| `timetable_status` | `string` | Yes | — |
| `saved_plans` | array of [`SavedPlan`](#mcp-type-savedplan) | Yes | — |
| `source_url` | `string` | Yes | — |
| `retrieved_at` | `string` | Yes | — |
| `from_cache` | `boolean` | Yes | — |
| `cache_age_seconds` | `integer` | Yes | — |

### `stars_get_degree_audit`

Get your degree requirements, examination results, and registered courses from Degree Audit.

**Inputs:** none. Requires credentials.

**Returns:** published degree/AU requirements, examination results, registered courses, and status/source/cache metadata. Academic tables retain their published headers and records. Identity/contact tables are excluded; unknown or missing academic information is not inferred.

**Inputs**

None.

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `service` | `string` | Yes | — |
| `page_title` | `string` or `null` | Yes | — |
| `requirements` | array of [`PersonalTable`](#mcp-type-personaltable) | Yes | — |
| `requirements_status` | `string` | Yes | — |
| `examination_results` | array of [`PersonalTable`](#mcp-type-personaltable) | Yes | — |
| `examination_results_status` | `string` | Yes | — |
| `courses_registered` | array of [`PersonalTable`](#mcp-type-personaltable) | Yes | — |
| `courses_registered_status` | `string` | Yes | — |
| `source_url` | `string` | Yes | — |
| `retrieved_at` | `string` | Yes | — |
| `from_cache` | `boolean` | Yes | — |
| `cache_age_seconds` | `integer` | Yes | — |

### `stars_save_stars_plan`

Replace saved Plan 1, 2, or 3 with the complete supplied course/index list for the current Planner term. Omitted courses are removed from that plan. Verifies persistence by loading the saved plan. Does not perform course registration, dropping, or index swapping.

**Inputs:** `plan_number` of 1–3, the complete `courses` list of 1–13 course/index pairs, `academic_year`, and `semester` of `1` or `2`. Requires credentials, and the term must match the Planner's current term.

**Returns:** the saved plan and verification time after reloading it. This replaces the plan's entire course/index list; omitted courses are removed. It does not register, drop, or swap registered courses. If persistence is uncertain, refresh the Planner before retrying; an uncertain save is not automatically repeated.

```json
{"plan_number":1,"academic_year":2030,"semester":1,"courses":[{"course_code":"ZZ0001","index":"00001"}]}
```

MCP host confirmation is required before this action.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `plan_number` | `1`, `2`, `3` | Yes | — |
| `courses` | array of [`PlannedIndex`](#mcp-type-plannedindex) | Yes | minimum items: `1`; maximum items: `13` |
| `academic_year` | `integer` | Yes | — |
| `semester` | `1`, `2` | Yes | — |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `status` | `string` | Yes | — |
| `academic_year` | `integer` | Yes | — |
| `semester` | `integer` | Yes | — |
| `saved_plan` | [`SavedPlan`](#mcp-type-savedplan) | Yes | — |
| `verified_at` | `string` | Yes | — |
| `source_url` | `string` | Yes | — |

## MCP data types

These named types are used by the tool input and output fields above.

<a id="mcp-type-availableroom"></a>
### `AvailableRoom`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `venue` | `string` | Yes | — |
| `room_type` | `"tutorial_room"`, `"seminar_room"`, `"lecture_theatre"`, `"laboratory"`, `"other"` | Yes | — |
| `aliases` | array of `string` | Yes | — |
| `observed_lesson_types` | array of `string` | Yes | — |
| `free_from` | `string` | Yes | — |
| `free_until` | `string` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-clashcheck"></a>
### `ClashCheck`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `against_session_count` | `integer` | Yes | — |
| `clashes_by_index` | object of array of [`ClashPair`](#mcp-type-clashpair) | Yes | — |
| `uncertain_comparisons_by_index` | object of `integer` | Yes | — |

<a id="mcp-type-clashpair"></a>
### `ClashPair`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_session` | [`CompactSession`](#mcp-type-compactsession) | Yes | — |
| `existing_session` | [`ExistingSession`](#mcp-type-existingsession) | Yes | — |

<a id="mcp-type-compactsession"></a>
### `CompactSession`

Course/index are inherited from the result; unfamiliar day/time text stays explicit.

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `lesson_type` | `string` or `null` | Yes | — |
| `group` | `string` or `null` | Yes | — |
| `day` | `string` or `null` | Yes | — |
| `start_time` | `string` or `null` | Yes | — |
| `end_time` | `string` or `null` | Yes | — |
| `venue` | `string` or `null` | Yes | — |
| `teaching_weeks` | array of `integer` or `null` | Yes | — |
| `remarks` | `string` or `null` | Yes | — |
| `raw_time` | `string` | No | — |
| `raw_day` | `string` | No | — |

<a id="mcp-type-constraintsresult"></a>
### `ConstraintsResult`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `avoid_days` | array of `string` | No | — |
| `earliest_start` | `string` | No | — |
| `latest_end` | `string` | No | — |
| `avoid_windows` | array of [`TimeWindowResult`](#mcp-type-timewindowresult) | No | — |
| `require_sessions` | array of [`SessionRule`](#mcp-type-sessionrule) | No | — |
| `teaching_weeks` | array of `integer` | No | — |

<a id="mcp-type-courseindex"></a>
### `CourseIndex`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `vacancy_status` | `"available"`, `"not_listed"`, `"closed"`, `"term_mismatch"`, `"unavailable"` | Yes | — |
| `vacancies_available` | `integer` or `null` | Yes | — |
| `waitlist_length` | `integer` or `null` | Yes | — |
| `index` | `string` | Yes | — |
| `schedule_complete` | `boolean` | Yes | — |
| `sessions` | array of [`CompactSession`](#mcp-type-compactsession) | Yes | — |

<a id="mcp-type-coursenote"></a>
### `CourseNote`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `label` | `string` | Yes | — |
| `text` | `string` | Yes | — |

<a id="mcp-type-coursesearchmatch"></a>
### `CourseSearchMatch`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_code` | `string` | Yes | — |
| `course_name` | `string` | Yes | — |
| `au` | `number` or `null` | Yes | — |

<a id="mcp-type-examresult"></a>
### `ExamResult`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `date` | `string` or `null` | Yes | — |
| `day` | `string` or `null` | Yes | — |
| `start_time` | `string` or `null` | Yes | — |
| `end_time` | `string` or `null` | Yes | — |
| `duration_minutes` | `integer` or `null` | Yes | — |
| `duration_text` | `string` | No | — |
| `raw_date` | `string` | No | — |
| `raw_day` | `string` or `null` | No | — |
| `raw_time` | `string` or `null` | No | — |

<a id="mcp-type-existingsession"></a>
### `ExistingSession`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `day` | `string` | No | — |
| `start_time` | `string` | No | — |
| `end_time` | `string` | No | — |
| `teaching_weeks` | array of `integer` | No | — |

<a id="mcp-type-graduateclassgroup"></a>
### `GraduateClassGroup`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `class_group` | `string` or `null` | Yes | — |
| `coordinator` | `string` or `null` | Yes | — |
| `sessions` | array of [`GraduateSession`](#mcp-type-graduatesession) | Yes | — |
| `schedule_remarks` | array of `string` | Yes | — |
| `schedule_text` | `string` or `null` | No | — |

<a id="mcp-type-graduatesession"></a>
### `GraduateSession`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `day` | `string` or `null` | Yes | — |
| `start_time` | `string` or `null` | Yes | — |
| `end_time` | `string` or `null` | Yes | — |
| `venue` | `string` or `null` | Yes | — |
| `commence_date` | `string` or `null` | Yes | — |
| `teaching_weeks` | array of `integer` or `null` | Yes | — |

<a id="mcp-type-matchingindex"></a>
### `MatchingIndex`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `index` | `string` | Yes | — |
| `status` | `"confirmed"`, `"uncertain"` | Yes | — |
| `uncertainties` | array of `string` | Yes | — |
| `schedule_complete` | `boolean` | Yes | — |
| `sessions` | array of [`CompactSession`](#mcp-type-compactsession) | Yes | — |

<a id="mcp-type-personaltable"></a>
### `PersonalTable`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `section` | `string` or `null` | Yes | — |
| `headers` | array of `string` | Yes | — |
| `rows` | array of array of `string` | No | — |
| `records` | array of object of `string` | Yes | — |

<a id="mcp-type-plannedcourse"></a>
### `PlannedCourse`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_code` | `string` | Yes | — |
| `index` | `string` or `null` | Yes | — |
| `course_type` | `string` or `null` | Yes | — |

<a id="mcp-type-plannedindex"></a>
### `PlannedIndex`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_code` | `string` | Yes | NTU undergraduate course code |
| `index` | `string` | Yes | Index number as a string; pattern: `^[0-9]{1,12}$` |

<a id="mcp-type-plannersession"></a>
### `PlannerSession`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_code` | `string` | Yes | — |
| `index` | `string` or `null` | No | — |
| `lesson_type` | `string` | Yes | — |
| `group` | `string` | Yes | — |
| `day` | `string` | Yes | — |
| `start_time` | `string` or `null` | Yes | — |
| `end_time` | `string` or `null` | Yes | — |
| `venue` | `string` | Yes | — |
| `teaching_weeks` | array of `integer` or `null` | Yes | — |
| `remarks` | `string` or `null` | Yes | — |
| `raw_time` | `string` or `null` | No | — |

<a id="mcp-type-prerequisitetreenode"></a>
### `PrerequisiteTreeNode`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_code` | `string` | Yes | — |
| `course_name` | `string` or `null` | Yes | — |
| `au` | `number` or `null` | Yes | — |
| `offered_this_term` | `boolean` | Yes | — |
| `course_data_status` | `"available"`, `"unavailable"`, `"not_loaded"` | Yes | — |
| `official_source` | `string` or `null` | Yes | — |
| `retrieved_at` | `string` or `null` | Yes | — |
| `depth` | `integer` | Yes | — |
| `match_status` | `"root"`, `"confirmed"`, `"possible"` | Yes | — |
| `path_status` | `"root"`, `"confirmed"`, `"possible"` | Yes | — |
| `matched_relations` | array of `string` | Yes | — |
| `prerequisite_status` | `"parsed"`, `"unparsed"`, `"not_listed"`, `"conflicting_records"`, `"unavailable"`, `"not_loaded"` | Yes | — |
| `prerequisite_text` | `string` or `null` | Yes | — |
| `prerequisite_texts` | array of `string` or `null` | Yes | — |
| `prerequisite_expression` | `object` or `null` | Yes | — |
| `eligibility_status` | `"eligible"`, `"not_eligible"`, `"unknown"`, `"not_evaluated"`, `"not_listed"` | Yes | — |
| `prerequisites` | array of `object` | Yes | — |
| `dependents` | array of `object` | Yes | — |
| `cycle_detected` | `boolean` | No | — |
| `prerequisites_truncated` | `boolean` | No | — |
| `dependents_truncated` | `boolean` | No | — |

<a id="mcp-type-roomcoverage"></a>
### `RoomCoverage`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `scope` | `"published_undergraduate_full_time_and_part_time_teaching"` | No | default: `"published_undergraduate_full_time_and_part_time_teaching"` |
| `course_count` | `integer` | Yes | — |
| `courses_without_published_indexes` | `integer` | Yes | — |
| `index_count` | `integer` | Yes | — |
| `lesson_count` | `integer` | Yes | — |
| `observed_room_count` | `integer` | Yes | — |
| `excluded_venue_label_count` | `integer` | Yes | — |
| `unplaced_lesson_count` | `integer` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-roomfilters"></a>
### `RoomFilters`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `room_types` | array of `"tutorial_room"`, `"seminar_room"`, `"lecture_theatre"`, `"laboratory"`, `"other"` or `null` | No | Inferred from venue codes, not lesson types or an official room inventory.; default: `null`; minimum items: `1`; maximum items: `5` |
| `venue_contains` | `string` or `null` | No | default: `null`; minimum length: `1`; maximum length: `80` |
| `venue_prefixes` | array of `string` or `null` | No | Venue-code prefixes such as LHN, LHS, SPMS or S4. No geographic location is inferred for bare TR/LT labels.; default: `null`; minimum items: `1`; maximum items: `20` |
| `exclude_venues` | array of `string` | No | maximum items: `100` |
| `used_for_lesson_types` | array of `string` or `null` | No | Candidate rooms must have at least one published lesson of these types. All lesson types still block availability.; default: `null`; minimum items: `1`; maximum items: `20` |

Unknown fields are not accepted.

<a id="mcp-type-roomidentity"></a>
### `RoomIdentity`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `venue` | `string` | Yes | — |
| `room_type` | `"tutorial_room"`, `"seminar_room"`, `"lecture_theatre"`, `"laboratory"`, `"other"` | Yes | — |
| `aliases` | array of `string` | Yes | — |
| `observed_lesson_types` | array of `string` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-roomlesson"></a>
### `RoomLesson`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_code` | `string` | Yes | — |
| `indexes` | array of `string` | Yes | — |
| `lesson_type` | `string` or `null` | Yes | — |
| `group` | `string` or `null` | Yes | — |
| `day` | `string` or `null` | Yes | — |
| `start_time` | `string` or `null` | Yes | — |
| `end_time` | `string` or `null` | Yes | — |
| `teaching_weeks` | array of `integer` or `null` | Yes | — |
| `remarks` | `string` or `null` | Yes | — |
| `raw_day` | `string` or `null` | Yes | — |
| `raw_time` | `string` or `null` | Yes | — |
| `source_venue_labels` | array of `string` | No | Original venue text when it differs from the enclosing canonical room, including multi-room cells. |

Unknown fields are not accepted.

<a id="mcp-type-roomwindow"></a>
### `RoomWindow`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `day` | `"MON"`, `"TUE"`, `"WED"`, `"THU"`, `"FRI"`, `"SAT"`, `"SUN"` | Yes | — |
| `start_time` | `string` | Yes | pattern: `^(?:[01]\d\|2[0-3]):[0-5]\d$` |
| `end_time` | `string` | Yes | pattern: `^(?:[01]\d\|2[0-3]):[0-5]\d$` |
| `teaching_weeks` | array of `integer` or `null` | No | Free in every requested teaching week. Omit to consider every published meeting, conservatively across the whole term.; default: `null`; minimum items: `1`; maximum items: `20` |
| `buffer_minutes` | `integer` | No | Additional teaching-free minutes required before and after the requested interval.; minimum: `0`; maximum: `120`; default: `0` |

Unknown fields are not accepted.

<a id="mcp-type-savedplan"></a>
### `SavedPlan`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `plan_number` | `integer` | Yes | — |
| `status` | `string` | Yes | — |
| `courses` | array of [`PlannedCourse`](#mcp-type-plannedcourse) | Yes | — |
| `sessions` | array of [`PlannerSession`](#mcp-type-plannersession) | Yes | — |
| `unparsed_sessions` | array of object of `string` | Yes | — |
| `timetable_status` | `string` | Yes | — |

<a id="mcp-type-searchconstraints"></a>
### `SearchConstraints`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `avoid_days` | array of `"MON"`, `"TUE"`, `"WED"`, `"THU"`, `"FRI"`, `"SAT"`, `"SUN"` | No | Reject indexes with a known class on these days |
| `earliest_start` | `string` or `null` | No | Every class must start at or after this time; default: `null`; 24-hour time in HH:MM format; pattern: `^(?:[01]\d\|2[0-3]):[0-5]\d$` |
| `latest_end` | `string` or `null` | No | Every class must end by this time; default: `null`; 24-hour time in HH:MM format; pattern: `^(?:[01]\d\|2[0-3]):[0-5]\d$` |
| `avoid_windows` | array of [`TimeWindow`](#mcp-type-timewindow) | No | Reject classes overlapping these day/time windows |
| `require_sessions` | array of [`SessionRequirement`](#mcp-type-sessionrequirement) | No | Each requirement must match at least one session |
| `teaching_weeks` | array of `integer` or `null` | No | Evaluate only sessions meeting in these teaching weeks; unspecified week rules remain uncertain; default: `null`; minimum items: `1`; maximum items: `20` |

<a id="mcp-type-sessionrequirement"></a>
### `SessionRequirement`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `lesson_type` | `string` or `null` | No | Exact NTU lesson type, such as TUT or LAB; default: `null` |
| `day` | `"MON"`, `"TUE"`, `"WED"`, `"THU"`, `"FRI"`, `"SAT"`, `"SUN"` or `null` | No | default: `null` |
| `starts_at_or_after` | `string` or `null` | No | default: `null`; 24-hour time in HH:MM format; pattern: `^(?:[01]\d\|2[0-3]):[0-5]\d$` |
| `starts_at_or_before` | `string` or `null` | No | default: `null`; 24-hour time in HH:MM format; pattern: `^(?:[01]\d\|2[0-3]):[0-5]\d$` |

<a id="mcp-type-sessionrule"></a>
### `SessionRule`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `lesson_type` | `string` | No | — |
| `day` | `string` | No | — |
| `starts_at_or_after` | `string` | No | — |
| `starts_at_or_before` | `string` | No | — |

<a id="mcp-type-timeslot"></a>
### `TimeSlot`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `day` | `"MON"`, `"TUE"`, `"WED"`, `"THU"`, `"FRI"`, `"SAT"`, `"SUN"` or `null` | No | default: `null` |
| `start_time` | `string` or `null` | No | default: `null`; 24-hour time in HH:MM format; pattern: `^(?:[01]\d\|2[0-3]):[0-5]\d$` |
| `end_time` | `string` or `null` | No | default: `null`; 24-hour time in HH:MM format; pattern: `^(?:[01]\d\|2[0-3]):[0-5]\d$` |
| `teaching_weeks` | array of `integer` or `null` | No | Known teaching weeks; omit if unknown. Overlapping times with unknown weeks remain uncertain.; default: `null`; minimum items: `1`; maximum items: `20` |

<a id="mcp-type-timewindow"></a>
### `TimeWindow`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `day` | `"MON"`, `"TUE"`, `"WED"`, `"THU"`, `"FRI"`, `"SAT"`, `"SUN"` | Yes | — |
| `start_time` | `string` | Yes | 24-hour time in HH:MM format; pattern: `^(?:[01]\d\|2[0-3]):[0-5]\d$` |
| `end_time` | `string` | Yes | 24-hour time in HH:MM format; pattern: `^(?:[01]\d\|2[0-3]):[0-5]\d$` |

<a id="mcp-type-timewindowresult"></a>
### `TimeWindowResult`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `day` | `string` | Yes | — |
| `start_time` | `string` | Yes | — |
| `end_time` | `string` | Yes | — |

<a id="mcp-type-vacancymetadata"></a>
### `VacancyMetadata`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `status` | `"available"`, `"closed"`, `"term_mismatch"`, `"unavailable"` | Yes | — |
| `retrieved_at` | `string` or `null` | Yes | — |
| `academic_year` | `integer` or `null` | No | — |
| `semester` | `string` or `null` | No | — |
| `source_url` | `string` | No | — |
| `from_cache` | `boolean` | No | — |
| `cache_age_seconds` | `number` or `null` | No | — |
| `message` | `string` | No | — |

## Service notes

These tools run in the shared `all-abt-ntu-mcp` server. See the [main README](../../README.md) for installation and client configuration.

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

WISH authentication follows NTU's [login workflow](https://wish.wis.ntu.edu.sg/pls/webexe/ldap_login.login). Credentials come from the [shared credential store](../shared/README.md#credential-storage), also used by NTULearn and LibFacilities; access restrictions and challenges are respected. Manage it locally with `ntu auth save`, `auth status`, and `auth delete`. Passwords are never accepted as MCP arguments or read from environment variables/config files.

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
