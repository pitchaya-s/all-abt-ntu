# One Stop: Requests CLI commands

[One Stop overview](../index.md) · [All One Stop CLI topics](index.md) · [MCP reference](../mcp/index.md)

List your requests or apply for a catalog item. `apply` prepares, fills, reviews and submits a form in one interactive invocation.

```sh
ntu onestop requests list --status open
ntu onestop requests apply ITEM_ID
```

Replace capitalized placeholders with values returned by the service. Use `--help` after a command for its current options. Choose a command to see its arguments, examples and result fields.

| Command | What it does |
| --- | --- |
| [`ntu onestop requests list`](requests.md#cmd-onestop-requests-list) | Read your own open/closed One Stop cases and service requests, expanding native lists up to 500 records. |
| [`ntu onestop requests show`](requests.md#cmd-onestop-requests-show) | Read one of your requests after checking request_id against your retrieved personal lists. |
| [`ntu onestop requests activity`](requests.md#cmd-onestop-requests-activity) | Read visible comments and attachment events on a verified own request/item, plus current reply/upload/state-action permissions. |
| [`ntu onestop requests reply`](requests.md#cmd-onestop-requests-reply) | Post a real additional comment to a verified own ticket/item when its current native state permits replying. |
| [`ntu onestop requests action`](requests.md#cmd-onestop-requests-action) | Execute a state action currently offered by the native own-ticket page. |
| [`ntu onestop requests apply`](requests.md#cmd-onestop-requests-apply) | Prepare, fill, review and submit a native request in one session. |

## Command details

<a id="cmd-onestop-requests-list"></a>
### `ntu onestop requests list`

Read your own open/closed One Stop cases and service requests, expanding native lists up to 500 records.

#### Usage

```sh
ntu onestop requests list
```

Use `ntu onestop requests list --help` for the current interface.

#### Arguments and options

- `--status`: Restrict the listing to the selected status. Choices: `all`, `open`, `closed`. Default: `all`.
- `--kind`: Restrict the listing to the selected kind of request. Choices: `all`, `case`, `request`. Default: `all`.
- `--limit`, `-l`: Maximum number of results to return in this page. Default: `20`.
- `--offset`: Number of results to skip before this page. Default: `0`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `offset`, `available_count`, `total_count`, `complete`, `next_offset`, `retrieved_at`, `source_url`, `cached`, `requests`, `coverage`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/requests.md#onestop_list_my_requests).

<a id="cmd-onestop-requests-show"></a>
### `ntu onestop requests show`

Read one of your requests after checking request_id against your retrieved personal lists.

#### Usage

```sh
ntu onestop requests show REQUEST_ID
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu onestop requests show --help` for the current interface.

#### Arguments and options

- `REQUEST_ID`: **Required.** The request ID returned by the relevant listing or details command.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `request`, `records`, `requested_items`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/requests.md#onestop_get_my_request).

<a id="cmd-onestop-requests-activity"></a>
### `ntu onestop requests activity`

Read visible comments and attachment events on a verified own request/item, plus current reply/upload/state-action permissions.

#### Usage

```sh
ntu onestop requests activity REQUEST_ID
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu onestop requests activity --help` for the current interface.

#### Arguments and options

- `REQUEST_ID`: **Required.** The request ID returned by the relevant listing or details command.
- `--record-id`: A record ID for a request target when the request contains multiple records.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `request_id`, `record_id`, `entries`, `available_actions`, `can_reply`, `can_upload_attachment`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/requests.md#onestop_get_request_activity).

<a id="cmd-onestop-requests-reply"></a>
### `ntu onestop requests reply`

Post a real additional comment to a verified own ticket/item when its current native state permits replying.

This operation requires local confirmation and is refused when confirmation cannot be obtained interactively.

#### Usage

```sh
ntu onestop requests reply REQUEST_ID --text 'Example message'
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu onestop requests reply --help` for the current interface.

#### Arguments and options

- `REQUEST_ID`: **Required.** The request ID returned by the relevant listing or details command.
- `--text`: **Required.** The text to send. Quote multiword text in the shell.
- `--record-id`: A record ID for a request target when the request contains multiple records.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/requests.md#onestop_reply_to_request).

<a id="cmd-onestop-requests-action"></a>
### `ntu onestop requests action`

Execute a state action currently offered by the native own-ticket page.

This operation requires local confirmation and is refused when confirmation cannot be obtained interactively.

#### Usage

```sh
ntu onestop requests action REQUEST_ID close
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu onestop requests action --help` for the current interface.

#### Arguments and options

- `REQUEST_ID`: **Required.** The request ID returned by the relevant listing or details command.
- `ACTION`: **Required.** The native action to perform; inspect the record for the actions currently available. Choices: `close`, `reopen`, `accept-solution`, `reject-solution`.
- `--record-id`: A record ID for a request target when the request contains multiple records.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/requests.md#onestop_take_request_action).

<a id="cmd-onestop-requests-apply"></a>
### `ntu onestop requests apply`

Prepare, fill, review and submit a native request in one session.

This interactive workflow keeps its temporary state in one process and asks for confirmation before submitting.

#### Usage

```sh
ntu onestop requests apply ITEM_ID
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu onestop requests apply --help` for the current interface.

#### Arguments and options

- `ITEM_ID`: **Required.** The item ID returned by the relevant listing or details command.

#### Result

The result may include: `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/requests.md#onestop_submit_request).
