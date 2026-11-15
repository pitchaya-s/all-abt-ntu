# Faculty: CLI reference

[Service overview](../index.md) · [CLI reference](index.md) · [MCP reference](../mcp/index.md)

## Example

Search by name, or list the available research-interest filters.

```sh
ntu faculty search "Tan" --page 1
ntu faculty interests --limit 10
```

## Commands

Choose a command for its arguments, examples and result fields. Use `ntu faculty --help` and append `--help` to a command for option details. Each command page identifies required arguments and any defaults. See the [complete CLI reference](../../../cli/commands.md) for shared settings and all services.

| Command | What it does |
| --- | --- |
| [`ntu faculty search`](index.md#cmd-faculty-search) | Search NTU's public faculty directory by name, optionally filtered by one research interest. |
| [`ntu faculty interests`](index.md#cmd-faculty-interests) | List current faculty research-interest labels and filter IDs from NTU's directory form. |

## Command details

<a id="cmd-faculty-search"></a>
### `ntu faculty search`

Search NTU's public faculty directory by name, optionally filtered by one research interest.

#### Usage

```sh
ntu faculty search "Tan" --page 1
```

Use `ntu faculty search --help` for the current interface.

#### Arguments and options

- `QUERY`: The search terms. Quote multiword text so the shell passes it as one argument.
- `--interest`: The interest ID returned by the relevant listing or details command.
- `--page`, `-p`: Page number to request; page numbering depends on the service. Default: `1`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `profiles`, `page`, `total_pages`, `total_count`, `next_page`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/index.md#faculty_search).

<a id="cmd-faculty-interests"></a>
### `ntu faculty interests`

List current faculty research-interest labels and filter IDs from NTU's directory form.

#### Usage

```sh
ntu faculty interests example
```

Use `ntu faculty interests --help` for the current interface.

#### Arguments and options

- `QUERY`: The search terms. Quote multiword text so the shell passes it as one argument.
- `--limit`, `-l`: Maximum number of results to return in this page. Default: `50`.
- `--offset`: Number of results to skip before this page. Default: `0`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `interests`, `total_count`, `next_offset`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/index.md#faculty_list_interests).
