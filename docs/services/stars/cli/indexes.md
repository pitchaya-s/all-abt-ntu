# STARS: Indexes and timetables CLI commands

[Back to STARS CLI](index.md) · [MCP reference](../mcp/index.md)

- [`ntu stars index`](#cmd-stars-index)
- [`ntu stars indexes compare`](#cmd-stars-indexes-compare)
- [`ntu stars indexes match`](#cmd-stars-indexes-match)
- [`ntu stars indexes list`](#cmd-stars-indexes-list)

## Command details

<a id="cmd-stars-index"></a>
### `ntu stars index`

Get one index's complete schedule, vacancies, and waitlist where matching-term counts are published.

#### Usage

```sh
ntu stars index ZZ0001 00001 --year 2026 --semester 1
```

`ZZ0001` is a fictional course code. Use `ntu stars index --help` for the current interface.

#### Arguments and options

- `COURSE_CODE`: **Required.** The course code shown by STARS.
- `INDEX`: **Required.** The index number, kept as a string so leading zeroes are preserved.
- `--year`, `-y`: **Required.** The first year of the academic year; `2026` means AY2026/27.
- `--semester`, `-s`: **Required.** Semester within the selected academic year. Choices: `1`, `2`, `S`.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `course_code`, `academic_year`, `semester`, `vacancy_status`, `vacancies_available`, `waitlist_length`, `index`, `vacancy_metadata`, `schedule_complete`, `sessions`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/indexes.md#stars_get_index).

<a id="cmd-stars-indexes-compare"></a>
### `ntu stars indexes compare`

Compare shared and index-specific sessions; optionally check clashes with supplied time slots.

#### Usage

```sh
ntu stars indexes compare ZZ0001 00001 00002 --year 2026 --semester 1
```

`ZZ0001` is a fictional course code. Use `ntu stars indexes compare --help` for the current interface.

To check the indexes against an existing timetable, add `--against timetable.json`. For example, the file can contain:

```json
[
  {"day": "TUE", "start_time": "14:00", "end_time": "16:00", "teaching_weeks": [2, 4, 6]}
]
```

Use sessions from the same academic year and semester as the indexes being compared.

#### Arguments and options

- `COURSE_CODE`: **Required.** The course code shown by STARS.
- `INDEXES`: **Required.** Two or more index numbers to compare; keep leading zeroes.
- `--year`, `-y`: **Required.** The first year of the academic year; `2026` means AY2026/27.
- `--semester`, `-s`: **Required.** Semester within the selected academic year. Choices: `1`, `2`, `S`.
- `--against`: Path to a JSON file containing existing timetable sessions.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `course_code`, `academic_year`, `semester`, `retrieved_at`, `official_source`, `indexes_compared`, `common_sessions`, `unique_sessions_by_index`, `clash_check`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/indexes.md#stars_compare_indexes).

<a id="cmd-stars-indexes-match"></a>
### `ntu stars indexes match`

Find indexes matching day/time/lesson/week rules and avoiding supplied timetable clashes.

#### Usage

```sh
ntu stars indexes match ZZ0001 --year 2026 --semester 1
```

`ZZ0001` is a fictional course code. Use `ntu stars indexes match --help` for the current interface.

To apply constraints, create a JSON file such as `constraints.json`:

```json
{
  "avoid_days": ["FRI"],
  "latest_end": "17:00",
  "require_sessions": [{"lesson_type": "TUT", "day": "TUE"}]
}
```

Then add `--constraints constraints.json` to the command. Use `--against timetable.json` to check against existing sessions. The [MCP schema](../mcp/indexes.md#stars_find_matching_indexes) describes the supported fields and uncertainty in results.

#### Arguments and options

- `COURSE_CODE`: **Required.** The course code shown by STARS.
- `--year`, `-y`: **Required.** The first year of the academic year; `2026` means AY2026/27.
- `--semester`, `-s`: **Required.** Semester within the selected academic year. Choices: `1`, `2`, `S`.
- `--constraints`: Path to a JSON file containing matching constraints.
- `--against`: Path to a JSON file containing existing timetable sessions.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `course_code`, `academic_year`, `semester`, `retrieved_at`, `official_source`, `constraints`, `against_session_count`, `match_count`, `matches`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/indexes.md#stars_find_matching_indexes).

<a id="cmd-stars-indexes-list"></a>
### `ntu stars indexes list`

List a page of indexes with timetable details and matching-term vacancies/waitlists.

#### Usage

```sh
ntu stars indexes list ZZ0001 --year 2026 --semester 1
```

`ZZ0001` is a fictional course code. Use `ntu stars indexes list --help` for the current interface.

#### Arguments and options

- `COURSE_CODE`: **Required.** The course code shown by STARS.
- `--year`, `-y`: **Required.** The first year of the academic year; `2026` means AY2026/27.
- `--semester`, `-s`: **Required.** Semester within the selected academic year. Choices: `1`, `2`, `S`.
- `--limit`, `-l`: Maximum number of results to return in this page. Default: `10`.
- `--offset`: Number of results to skip before this page. Default: `0`.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `course_code`, `academic_year`, `semester`, `index_count`, `offset`, `next_offset`, `vacancy_metadata`, `indexes`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/indexes.md#stars_get_course_indexes).
