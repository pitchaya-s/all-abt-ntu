# STARS: Personal planner and audit CLI commands

[Back to STARS CLI](index.md) · [MCP reference](../mcp/index.md)

- [`ntu stars audit`](#cmd-stars-audit)
- [`ntu stars auth status`](#cmd-stars-auth-status)
- [`ntu stars planner show`](#cmd-stars-planner-show)
- [`ntu stars planner save`](#cmd-stars-planner-save)

## Command details

<a id="cmd-stars-audit"></a>
### `ntu stars audit`

Get your degree requirements, examination results, and registered courses from Degree Audit.

#### Usage

```sh
ntu stars audit
```

Use `ntu stars audit --help` for the current interface.

#### Arguments and options

- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `service`, `page_title`, `requirements`, `requirements_status`, `examination_results`, `examination_results_status`, `courses_registered`, `courses_registered_status`, `source_url`, `retrieved_at`, `from_cache`, `cache_age_seconds`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/personal.md#stars_get_degree_audit).

<a id="cmd-stars-auth-status"></a>
### `ntu stars auth status`

Report whether WISH credentials are configured and whether this process has verified a session.

#### Usage

```sh
ntu stars auth status
```

Use `ntu stars auth status --help` for the current interface.

#### Arguments and options

- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `credentials_configured`, `credential_storage`, `credential_error`, `session_verified`, `last_verified_at`, `session_storage`, `personal_cache_ttl_seconds`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/personal.md#stars_auth_status).

<a id="cmd-stars-planner-show"></a>
### `ntu stars planner show`

Get registered courses, the published term, and saved Plans 1–3 with indexes and timetables.

#### Usage

```sh
ntu stars planner show
```

Use `ntu stars planner show --help` for the current interface.

#### Arguments and options

- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `service`, `page_title`, `academic_year`, `semester`, `registration_notice`, `registered_courses`, `registered_courses_status`, `planner_tables`, `timetable_tables`, `timetable_status`, `saved_plans`, `source_url`, `retrieved_at`, `from_cache`, `cache_age_seconds`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/personal.md#stars_get_stars_planner).

<a id="cmd-stars-planner-save"></a>
### `ntu stars planner save`

Replace saved Plan 1, 2, or 3 with the complete supplied course/index list for the current Planner term.

This operation requires local confirmation and is refused when confirmation cannot be obtained interactively.

#### Usage

```sh
ntu stars planner save 1 --courses courses.json --year 2026 --semester 1
```

Use `ntu stars planner save --help` for the current interface.

For example, `courses.json` can contain:

```json
[
  {"course_code": "ZZ0001", "index": "00001"},
  {"course_code": "ZZ0002", "index": "00002"}
]
```

This is the **complete replacement plan**: courses omitted from the file are removed from the saved plan. The selected term must match the current Planner term. This action does not register or drop courses.

#### Arguments and options

- `PLAN_NUMBER`: **Required.** The saved plan number, from 1 to 3. Choices: `1`, `2`, `3`.
- `--courses`: **Required.** Path to a JSON file containing the complete replacement plan.
- `--year`, `-y`: **Required.** The first year of the academic year; `2026` means AY2026/27.
- `--semester`, `-s`: **Required.** Semester within the selected academic year. Choices: `1`, `2`.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `status`, `academic_year`, `semester`, `saved_plan`, `verified_at`, `source_url`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/personal.md#stars_save_stars_plan).
