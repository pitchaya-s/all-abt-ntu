# NTULearn: Messages, participants and groups CLI commands

[Back to NTULearn CLI](index.md) · [MCP reference](../mcp/index.md)

- [`ntu learn users`](#cmd-learn-users)
- [`ntu learn groups members`](#cmd-learn-groups-members)
- [`ntu learn groups list`](#cmd-learn-groups-list)
- [`ntu learn messages list`](#cmd-learn-messages-list)
- [`ntu learn messages read`](#cmd-learn-messages-read)

## Command details

<a id="cmd-learn-users"></a>
### `ntu learn users`

List course users visible to your account, with their published names and roles.

#### Usage

```sh
ntu learn users ZZ0001
```

`ZZ0001` is a fictional course code. Use `ntu learn users --help` for the current interface.

#### Arguments and options

- `COURSE_ID`: **Required.** The NTULearn course ID returned by `ntu learn courses`.
- `--limit`, `-l`: Maximum number of results to return in this page. Default: `50`.
- `--offset`: Number of results to skip before this page. Default: `0`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `from_cache`, `cache_age_seconds`, `course_id`, `group_id`, `users`, `offset`, `next_offset`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/people.md#ntulearn_list_course_users).

<a id="cmd-learn-groups-members"></a>
### `ntu learn groups members`

List visible members of a course group through Blackboard's browser membership API.

#### Usage

```sh
ntu learn groups members ZZ0001 GROUP_ID
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. `ZZ0001` is a fictional course code. Use `ntu learn groups members --help` for the current interface.

#### Arguments and options

- `COURSE_ID`: **Required.** The NTULearn course ID returned by `ntu learn courses`.
- `GROUP_ID`: **Required.** The group ID returned by the relevant listing or details command.
- `--limit`, `-l`: Maximum number of results to return in this page. Default: `50`.
- `--offset`: Number of results to skip before this page. Default: `0`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `from_cache`, `cache_age_seconds`, `course_id`, `group_id`, `users`, `offset`, `next_offset`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/people.md#ntulearn_get_group_members).

<a id="cmd-learn-groups-list"></a>
### `ntu learn groups list`

List groups and group sets defined in a course.

#### Usage

```sh
ntu learn groups list ZZ0001
```

`ZZ0001` is a fictional course code. Use `ntu learn groups list --help` for the current interface.

#### Arguments and options

- `COURSE_ID`: **Required.** The NTULearn course ID returned by `ntu learn courses`.
- `--limit`, `-l`: Maximum number of results to return in this page. Default: `50`.
- `--offset`: Number of results to skip before this page. Default: `0`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `from_cache`, `cache_age_seconds`, `course_id`, `groups`, `offset`, `next_offset`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/people.md#ntulearn_list_course_groups).

<a id="cmd-learn-messages-list"></a>
### `ntu learn messages list`

List Blackboard inbox/sent messages through readable course conversations, without marking them read.

#### Usage

```sh
ntu learn messages list
```

Use `ntu learn messages list --help` for the current interface.

#### Arguments and options

- `--folder`: Choose the inbox or sent message folder. Choices: `inbox`, `sent`. Default: `inbox`.
- `--course`: The NTULearn course ID returned by `ntu learn courses`.
- `--since`: Start of the date or time range in ISO format.
- `--unread-only`: Restrict messages to unread items.
- `--limit`, `-l`: Maximum number of results to return in this page. Default: `50`.
- `--offset`: Number of results to skip before this page. Default: `0`.
- `--max-requests`: Maximum number of upstream requests the operation may make. Default: `100`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `from_cache`, `cache_age_seconds`, `complete`, `requests_used`, `issues`, `folder`, `messages`, `offset`, `next_offset`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/people.md#ntulearn_list_messages).

<a id="cmd-learn-messages-read"></a>
### `ntu learn messages read`

Read a message's full body and published conversation recipients.

#### Usage

```sh
ntu learn messages read MESSAGE_ID
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu learn messages read --help` for the current interface.

#### Arguments and options

- `MESSAGE_ID`: **Required.** The message ID returned by the relevant listing or details command.
- `--course`: The NTULearn course ID returned by `ntu learn courses`.
- `--conversation-id`: The conversation ID returned by the relevant listing or details command.
- `--max-requests`: Maximum number of upstream requests the operation may make. Default: `100`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `from_cache`, `cache_age_seconds`, `complete`, `requests_used`, `issues`, `message`, `body`, `recipients`, `recipient_categories`, `includes_all_course_members`, `excluded_participant_ids`, `recipients_scope`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/people.md#ntulearn_read_message).
