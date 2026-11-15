# Campus Services: CLI reference

[Service overview](../index.md) · [CLI reference](index.md) · [MCP reference](../mcp/index.md)

## Example

Find outlets and services near a named location.

```sh
ntu services search "coffee" --location "North Spine" --limit 10
```

## Commands

Choose a command for its arguments, examples and result fields. Use `ntu services --help` and append `--help` to a command for option details. Each command page identifies required arguments and any defaults. See the [complete CLI reference](../../../cli/commands.md) for shared settings and all services.

| Command | What it does |
| --- | --- |
| [`ntu services search`](index.md#cmd-services-search) | Find NTU food outlets, shops, clinics and campus services by name/address keyword and optional location substring. |
| [`ntu services filters`](index.md#cmd-services-filters) | List official campus service type and category labels with filter IDs. |

## Command details

<a id="cmd-services-search"></a>
### `ntu services search`

Find NTU food outlets, shops, clinics and campus services by name/address keyword and optional location substring.

#### Usage

```sh
ntu services search "coffee" --location "North Spine" --limit 10
```

Use `ntu services search --help` for the current interface.

#### Arguments and options

- `QUERY`: The search terms. Quote multiword text so the shell passes it as one argument.
- `--type`: The type ID returned by the relevant listing or details command.
- `--category`: The category ID returned by the relevant listing or details command.
- `--location`: Match this text in the published location.
- `--limit`, `-l`: Maximum number of results to return in this page. Default: `20`.
- `--offset`: Number of results to skip before this page. Default: `0`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `locations`, `total_count`, `directory_count`, `pages_checked`, `next_offset`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/index.md#service_search).

<a id="cmd-services-filters"></a>
### `ntu services filters`

List official campus service type and category labels with filter IDs.

#### Usage

```sh
ntu services filters
```

Use `ntu services filters --help` for the current interface.

#### Arguments and options

- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `types`, `categories`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/index.md#service_list_filters).
