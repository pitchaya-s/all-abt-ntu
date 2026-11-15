# NTULearn: Announcements, calendar and grades CLI commands

[Back to NTULearn CLI](index.md) · [MCP reference](../mcp/index.md)

- [`ntu learn announcements`](#cmd-learn-announcements)
- [`ntu learn grades`](#cmd-learn-grades)
- [`ntu learn calendar`](#cmd-learn-calendar)
- [`ntu learn upcoming`](#cmd-learn-upcoming)
- [`ntu learn digest`](#cmd-learn-digest)

## Command details

<a id="cmd-learn-announcements"></a>
### `ntu learn announcements`

Read published announcements for one enrolled course.

#### Usage

```sh
ntu learn announcements ZZ0001
```

`ZZ0001` is a fictional course code. Use `ntu learn announcements --help` for the current interface.

#### Arguments and options

- `COURSE_ID`: **Required.** The NTULearn course ID returned by `ntu learn courses`.
- `--limit`, `-l`: Maximum number of results to return in this page. Default: `50`.
- `--offset`: Number of results to skip before this page. Default: `0`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `from_cache`, `cache_age_seconds`, `course_id`, `announcements`, `offset`, `next_offset`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/activity.md#ntulearn_get_announcements).

<a id="cmd-learn-grades"></a>
### `ntu learn grades`

Read visible gradebook columns and your own scores/status.

#### Usage

```sh
ntu learn grades ZZ0001
```

`ZZ0001` is a fictional course code. Use `ntu learn grades --help` for the current interface.

#### Arguments and options

- `COURSE_ID`: **Required.** The NTULearn course ID returned by `ntu learn courses`.
- `--limit`, `-l`: Maximum number of results to return in this page. Default: `50`.
- `--offset`: Number of results to skip before this page. Default: `0`.
- `--grades-offset`: Offset into the grade entries, independent of the column offset. Default: `0`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `from_cache`, `cache_age_seconds`, `course_id`, `columns`, `grades`, `offset`, `next_offset`, `grades_next_offset`, `grades_offset`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/activity.md#ntulearn_get_gradebook).

<a id="cmd-learn-calendar"></a>
### `ntu learn calendar`

Read calendar entries and published deadlines, across your courses or for one course.

#### Usage

```sh
ntu learn calendar
```

Use `ntu learn calendar --help` for the current interface.

#### Arguments and options

- `--since`: Start of the date or time range in ISO format.
- `--until`: End of the date or time range in ISO format.
- `--course`: The NTULearn course ID returned by `ntu learn courses`.
- `--limit`, `-l`: Maximum number of results to return in this page. Default: `50`.
- `--offset`: Number of results to skip before this page. Default: `0`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `from_cache`, `cache_age_seconds`, `since`, `until`, `items`, `offset`, `next_offset`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/activity.md#ntulearn_get_calendar).

<a id="cmd-learn-upcoming"></a>
### `ntu learn upcoming`

Collect all calendar pages across your enrolled courses.

#### Usage

```sh
ntu learn upcoming
```

Use `ntu learn upcoming --help` for the current interface.

#### Arguments and options

- `--since`: Start of the date or time range in ISO format.
- `--until`: End of the date or time range in ISO format.
- `--course-ids`: A JSON array of course IDs.
- `--item-type`: Restrict calendar results to the selected item type.
- `--max-requests`: Maximum number of upstream requests the operation may make. Default: `100`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `from_cache`, `cache_age_seconds`, `complete`, `requests_used`, `issues`, `since`, `until`, `items`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/activity.md#ntulearn_get_upcoming).

<a id="cmd-learn-digest"></a>
### `ntu learn digest`

Digest of recent announcements, upcoming calendar items and your gradebook across courses.

#### Usage

```sh
ntu learn digest
```

Use `ntu learn digest --help` for the current interface.

#### Arguments and options

- `--since`: Start of the date or time range in ISO format.
- `--until`: End of the date or time range in ISO format.
- `--course-ids`: A JSON array of course IDs.
- `--max-items`: Maximum number of items to include. Default: `200`.
- `--max-requests`: Maximum number of upstream requests the operation may make. Default: `100`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `from_cache`, `cache_age_seconds`, `complete`, `requests_used`, `issues`, `since`, `until`, `announcements`, `upcoming`, `grades`, `grade_change_note`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/activity.md#ntulearn_whats_new).
