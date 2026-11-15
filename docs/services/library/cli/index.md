# Library: CLI reference

[Service overview](../index.md) · [CLI reference](index.md) · [MCP reference](../mcp/index.md)

## Example

Search catalogue titles using OneSearch.

```sh
ntu library search "machine learning" --field title --match contains --limit 10
```

## Commands

Choose a command for its arguments, examples and result fields. Use `ntu library --help` and append `--help` to a command for option details. Each command page identifies required arguments and any defaults. See the [complete CLI reference](../../../cli/commands.md) for shared settings and all services.

| Command | What it does |
| --- | --- |
| [`ntu library search`](index.md#cmd-library-search) | Search NTU OneSearch for books, articles, journals and other catalogue resources. |
| [`ntu library record`](index.md#cmd-library-record) | Read a OneSearch record's bibliographic metadata, descriptions, subjects, identifiers and published access links. |
| [`ntu library availability`](index.md#cmd-library-availability) | Read published physical holdings with library, location, call number and status, plus institutional full-text service links and access notes. |
| [`ntu library facilities schedule`](index.md#cmd-library-facilities-schedule) | Read a day's LibFacilities room/seat time grid, room description and source status classes. |
| [`ntu library facilities list`](index.md#cmd-library-facilities-list) | List NTU Library facility categories, library/floor maps and closure notices. |
| [`ntu library map availability`](index.md#cmd-library-map-availability) | Read seat/room booking statuses for a library map at date YYYY-MM-DD and time HH:MM in Singapore. |

## Command details

<a id="cmd-library-search"></a>
### `ntu library search`

Search NTU OneSearch for books, articles, journals and other catalogue resources.

#### Usage

```sh
ntu library search "machine learning" --field title --match contains --limit 10
```

Use `ntu library search --help` for the current interface.

#### Arguments and options

- `QUERY`: **Required.** The search terms. Quote multiword text so the shell passes it as one argument.
- `--field`: The field to search or update, depending on the command. Choices: `any`, `title`, `creator`, `isbn`, `issn`, `sub`. Default: `any`.
- `--match`: How the search should match the selected field. Choices: `contains`, `exact`. Default: `contains`.
- `--resource-type`: The published resource-type facet token.
- `--limit`, `-l`: Maximum number of results to return in this page. Default: `10`.
- `--offset`: Number of results to skip before this page. Default: `0`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `query`, `records`, `offset`, `total_count`, `local_count`, `central_index_count`, `next_offset`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/index.md#library_search).

<a id="cmd-library-record"></a>
### `ntu library record`

Read a OneSearch record's bibliographic metadata, descriptions, subjects, identifiers and published access links.

#### Usage

```sh
ntu library record RECORD_ID
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu library record --help` for the current interface.

#### Arguments and options

- `RECORD_ID`: **Required.** A record ID for a request target when the request contains multiple records.
- `--context`: The library search context: local catalogue (`L`) or broader discovery (`PC`). Choices: `L`, `PC`. Default: `L`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `record`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/index.md#library_get_record).

<a id="cmd-library-availability"></a>
### `ntu library availability`

Read published physical holdings with library, location, call number and status, plus institutional full-text service links and access notes.

#### Usage

```sh
ntu library availability RECORD_ID
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu library availability --help` for the current interface.

#### Arguments and options

- `RECORD_ID`: **Required.** A record ID for a request target when the request contains multiple records.
- `--context`: The library search context: local catalogue (`L`) or broader discovery (`PC`). Choices: `L`, `PC`. Default: `L`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `record_id`, `context`, `holdings`, `electronic_services`, `availability_codes`, `services_source_url`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/index.md#library_get_availability).

<a id="cmd-library-facilities-schedule"></a>
### `ntu library facilities schedule`

Read a day's LibFacilities room/seat time grid, room description and source status classes.

#### Usage

```sh
ntu library facilities schedule --date 2026-11-14
```

Use `ntu library facilities schedule --help` for the current interface.

#### Arguments and options

- `--date`: **Required.** Date in `YYYY-MM-DD` format.
- `--space`: The space ID returned by the relevant listing or details command.
- `--location`: The location ID returned by the relevant listing or details command.
- `--group`: The group ID returned by the relevant listing or details command.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `date`, `timezone`, `title`, `description`, `spaces`, `window_end`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/index.md#library_get_facility_schedule).

<a id="cmd-library-facilities-list"></a>
### `ntu library facilities list`

List NTU Library facility categories, library/floor maps and closure notices.

#### Usage

```sh
ntu library facilities list
```

Use `ntu library facilities list --help` for the current interface.

#### Arguments and options

- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `facilities`, `notices`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/index.md#library_list_facilities).

<a id="cmd-library-map-availability"></a>
### `ntu library map availability`

Read seat/room booking statuses for a library map at date YYYY-MM-DD and time HH:MM in Singapore.

#### Usage

```sh
ntu library map availability MAP_SLUG --date 2026-11-14 --time 14:00
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu library map availability --help` for the current interface.

#### Arguments and options

- `MAP_SLUG`: **Required.** The library map slug returned by facility discovery.
- `--date`: **Required.** Date in `YYYY-MM-DD` format.
- `--time`: **Required.** Time in 24-hour `HH:MM` format.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `map_slug`, `at`, `spaces`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/index.md#library_get_map_availability).
