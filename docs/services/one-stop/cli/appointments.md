# One Stop: Appointments CLI commands

[One Stop overview](../index.md) · [All One Stop CLI topics](index.md) · [MCP reference](../mcp/index.md)

List appointments or book one using a catalog item ID. Booking prepares the form and asks you to choose a slot before confirming. Cancellation and rescheduling are not available.

```sh
ntu onestop appointments list
ntu onestop appointments book ITEM_ID
```

Replace capitalized placeholders with values returned by the service. Use `--help` after a command for its current options. Choose a command to see its arguments, examples and result fields.

| Command | What it does |
| --- | --- |
| [`ntu onestop appointments book`](appointments.md#cmd-onestop-appointments-book) | Prepare an appointment form, choose a slot and book it in one session. |
| [`ntu onestop appointments list`](appointments.md#cmd-onestop-appointments-list) | Read your native upcoming appointment list with appointment numbers, published dates/times and locations. |

## Command details

<a id="cmd-onestop-appointments-book"></a>
### `ntu onestop appointments book`

Prepare an appointment form, choose a slot and book it in one session.

This interactive workflow keeps its temporary state in one process and asks for confirmation before submitting.

#### Usage

```sh
ntu onestop appointments book ITEM_ID
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu onestop appointments book --help` for the current interface.

#### Arguments and options

- `ITEM_ID`: **Required.** The item ID returned by the relevant listing or details command.

#### Result

The result may include: `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/appointments.md#onestop_book_appointment).

<a id="cmd-onestop-appointments-list"></a>
### `ntu onestop appointments list`

Read your native upcoming appointment list with appointment numbers, published dates/times and locations.

#### Usage

```sh
ntu onestop appointments list
```

Use `ntu onestop appointments list --help` for the current interface.

#### Arguments and options

- `--limit`, `-l`: Maximum number of results to return in this page. Default: `20`.
- `--offset`: Number of results to skip before this page. Default: `0`.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `offset`, `available_count`, `total_count`, `complete`, `next_offset`, `retrieved_at`, `source_url`, `cached`, `records`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/appointments.md#onestop_list_my_appointments).
