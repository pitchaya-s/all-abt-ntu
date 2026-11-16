# STARS: Courses, prerequisites and exams CLI commands

[Back to STARS CLI](index.md) · [MCP reference](../mcp/index.md)

- [`ntu stars course`](#cmd-stars-course)
- [`ntu stars prerequisites`](#cmd-stars-prerequisites)
- [`ntu stars exams`](#cmd-stars-exams)
- [`ntu stars graduate`](#cmd-stars-graduate)
- [`ntu stars courses search`](#cmd-stars-courses-search)

## Command details

<a id="cmd-stars-course"></a>
### `ntu stars course`

Get course name, AUs, prerequisites, description, and term metadata.

#### Usage

```sh
ntu stars course ZZ0001 --year 2026 --semester 1
```

`ZZ0001` is a fictional course code. Use `ntu stars course --help` for the current interface.

#### Arguments and options

- `COURSE_CODE`: **Required.** The course code shown by STARS.
- `--year`, `-y`: **Required.** The first year of the academic year; `2026` means AY2026/27.
- `--semester`, `-s`: **Required.** Semester within the selected academic year. Choices: `1`, `2`, `S`.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `course_code`, `academic_year`, `semester`, `course_name`, `au`, `course_description`, `course_description_status`, `course_description_source`, `prerequisites`, `course_notes`, `retrieved_at`, `official_source`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/courses.md#stars_get_course_metadata).

<a id="cmd-stars-prerequisites"></a>
### `ntu stars prerequisites`

Build before and after branches around a course, with separate depth limits.  The before branch follows the course's prerequisite rules; the after branch finds courses that depend on it in the selected term.

#### Usage

```sh
ntu stars prerequisites ZZ0001 --year 2026 --semester 1
```

`ZZ0001` is a fictional course code. Use `ntu stars prerequisites --help` for the current interface.

#### Arguments and options

- `COURSE_CODE`: **Required.** The course code shown by STARS.
- `--year`, `-y`: **Required.** The first year of the academic year; `2026` means AY2026/27.
- `--semester`, `-s`: **Required.** Semester within the selected academic year. Choices: `1`, `2`, `S`.
- `--prerequisite-depth`: How many levels of prerequisites to follow. Default: `2`.
- `--dependent-depth`: How many levels of dependent courses to follow. Default: `2`.
- `--completed`: Completed course codes used when evaluating prerequisite eligibility.
- `--eligible-only`: Restrict results to courses eligible under the supplied completed courses.
- `--include-corequisites`: Include corequisites when building the prerequisite tree.
- `--max-nodes`: Maximum number of prerequisite and dependent nodes to examine. Default: `100`.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `course_code`, `academic_year`, `semester`, `prerequisite_depth`, `dependent_depth`, `include_corequisites`, `only_eligible`, `completed_courses`, `prerequisite_course_count`, `dependent_course_count`, `tree_node_count`, `prerequisites_truncated`, `dependents_truncated`, `truncated`, `coverage`, `root`, `source_urls`, `retrieved_at`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/courses.md#stars_get_prerequisite_tree).

<a id="cmd-stars-exams"></a>
### `ntu stars exams`

Get public General Access exam dates and times for a course in the latest or specified published term.

#### Usage

```sh
ntu stars exams ZZ0001
```

`ZZ0001` is a fictional course code. Use `ntu stars exams --help` for the current interface.

#### Arguments and options

- `COURSE_CODE`: **Required.** The course code shown by STARS.
- `--year`, `-y`: The first year of the academic year; `2026` means AY2026/27.
- `--semester`, `-s`: Semester within the selected academic year. Choices: `1`, `2`.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `course_code`, `course_name`, `academic_year`, `semester`, `exam_status`, `exam_count`, `exams`, `notice`, `source_url`, `retrieved_at`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/courses.md#stars_get_undergraduate_exam_schedule).

<a id="cmd-stars-graduate"></a>
### `ntu stars graduate`

Get a graduate course's class groups for NTU's currently published academic term.

#### Usage

```sh
ntu stars graduate ZZ0001
```

`ZZ0001` is a fictional course code. Use `ntu stars graduate --help` for the current interface.

#### Arguments and options

- `COURSE_CODE`: **Required.** The course code shown by STARS.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `course_code`, `course_name`, `au`, `academic_year`, `term`, `schedule_complete`, `class_groups`, `source_url`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/courses.md#stars_get_graduate_course_schedule).

<a id="cmd-stars-courses-search"></a>
### `ntu stars courses search`

Search NTU's public undergraduate Class Schedule by partial code or title keywords.

#### Usage

```sh
ntu stars courses search "data structures" --year 2026 --semester 1 --limit 10
```

Use `ntu stars courses search --help` for the current interface.

#### Arguments and options

- `QUERY`: **Required.** The search terms. Quote multiword text so the shell passes it as one argument.
- `--year`, `-y`: **Required.** The first year of the academic year; `2026` means AY2026/27.
- `--semester`, `-s`: **Required.** Semester within the selected academic year. Choices: `1`, `2`, `S`.
- `--study-mode`: The study mode for the published class schedule. Choices: `full_time`, `part_time`. Default: `full_time`.
- `--limit`, `-l`: Maximum number of results to return in this page. Default: `20`.
- `--offset`: Number of results to skip before this page. Default: `0`.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `query`, `academic_year`, `semester`, `study_mode`, `total_count`, `offset`, `has_more`, `courses`, `source_url`, `retrieved_at`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/courses.md#stars_search_courses).
