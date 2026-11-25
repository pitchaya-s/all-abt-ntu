# NTULearn: Courses, folders and search CLI commands

[Back to NTULearn CLI](index.md) · [MCP reference](../mcp/index.md)

- [`ntu learn auth status`](#cmd-learn-auth-status)
- [`ntu learn content tree`](#cmd-learn-content-tree)
- [`ntu learn content show`](#cmd-learn-content-show)
- [`ntu learn courses list`](#cmd-learn-courses-list)
- [`ntu learn search all`](#cmd-learn-search-all)
- [`ntu learn search course`](#cmd-learn-search-course)

## Command details

<a id="cmd-learn-auth-status"></a>
### `ntu learn auth status`

Sign in to NTULearn and report whether access is verified.

#### Usage

```sh
ntu learn auth status
```

Use `ntu learn auth status --help` for the current interface.

#### Arguments and options

- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `credentials_configured`, `credential_storage`, `credential_error`, `session_verified`, `authentication_method`, `last_verified_at`, `session_storage`, `cache_ttl_seconds`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/courses.md#ntulearn_auth_status).

<a id="cmd-learn-content-tree"></a>
### `ntu learn content tree`

Read a course's nested content tree.

#### Usage

```sh
ntu learn content tree ZZ0001
```

`ZZ0001` is a fictional course code. Use `ntu learn content tree --help` for the current interface.

#### Arguments and options

- `COURSE_ID`: **Required.** A course code or Blackboard course ID from `ntu learn courses`.
- `--max-depth`: Maximum nesting depth to traverse. Default: `5`.
- `--max-nodes`: Maximum number of content nodes to examine. Default: `1000`.
- `--max-requests`: Maximum number of upstream requests the operation may make. Default: `100`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `from_cache`, `cache_age_seconds`, `complete`, `requests_used`, `issues`, `course_id`, `contents`, `max_depth`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/courses.md#ntulearn_get_content_tree).

<a id="cmd-learn-content-show"></a>
### `ntu learn content show`

Read one level of course content.

#### Usage

```sh
ntu learn content show ZZ0001
```

`ZZ0001` is a fictional course code. Use `ntu learn content show --help` for the current interface.

#### Arguments and options

- `COURSE_ID`: **Required.** A course code or Blackboard course ID from `ntu learn courses`.
- `--parent`: The ID of a parent folder. Omit it to browse the top level.
- `--limit`, `-l`: Maximum number of results to return in this page. Default: `50`.
- `--offset`: Number of results to skip before this page. Default: `0`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `from_cache`, `cache_age_seconds`, `course_id`, `contents`, `offset`, `next_offset`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/courses.md#ntulearn_get_course_contents).

<a id="cmd-learn-courses-list"></a>
### `ntu learn courses list`

List your enrolled NTULearn courses and organizations, including published availability and course IDs.

#### Usage

```sh
ntu learn courses list --limit 20
```

Use `ntu learn courses list --help` for the current interface.

#### Arguments and options

- `--limit`, `-l`: Maximum number of results to return in this page. Default: `50`.
- `--offset`: Number of results to skip before this page. Default: `0`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `from_cache`, `cache_age_seconds`, `courses`, `offset`, `next_offset`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/courses.md#ntulearn_list_courses).

<a id="cmd-learn-search-all"></a>
### `ntu learn search all`

Recursively search content across available enrolled courses, or selected course_ids.

#### Usage

```sh
ntu learn search all example
```

Use `ntu learn search all --help` for the current interface.

#### Arguments and options

- `QUERY`: **Required.** The search terms. Quote multiword text so the shell passes it as one argument.
- `--course-ids`: A JSON array of course codes or Blackboard course IDs.
- `--max-depth`: Maximum nesting depth to traverse. Default: `5`.
- `--max-nodes`: Maximum number of content nodes to examine. Default: `1000`.
- `--max-results`: Maximum number of matching results to collect. Default: `50`.
- `--max-requests`: Maximum number of upstream requests the operation may make. Default: `100`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `from_cache`, `cache_age_seconds`, `complete`, `requests_used`, `issues`, `query`, `courses_searched`, `matches`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/courses.md#ntulearn_search_all_courses).

<a id="cmd-learn-search-course"></a>
### `ntu learn search course`

Recursively search one course's content titles, body and description for a case-insensitive substring.

#### Usage

```sh
ntu learn search course ZZ0001 example
```

`ZZ0001` is a fictional course code. Use `ntu learn search course --help` for the current interface.

#### Arguments and options

- `COURSE_ID`: **Required.** A course code or Blackboard course ID from `ntu learn courses`.
- `QUERY`: **Required.** The search terms. Quote multiword text so the shell passes it as one argument.
- `--max-depth`: Maximum nesting depth to traverse. Default: `5`.
- `--max-nodes`: Maximum number of content nodes to examine. Default: `1000`.
- `--max-results`: Maximum number of matching results to collect. Default: `50`.
- `--max-requests`: Maximum number of upstream requests the operation may make. Default: `100`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `from_cache`, `cache_age_seconds`, `complete`, `requests_used`, `issues`, `query`, `courses_searched`, `matches`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/courses.md#ntulearn_search_course_content).
