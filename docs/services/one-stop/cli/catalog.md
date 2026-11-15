# One Stop: Catalog CLI commands

[One Stop overview](../index.md) · [All One Stop CLI topics](index.md) · [MCP reference](../mcp/index.md)

Browse categories and items; use an item ID to inspect a form before starting a request.

```sh
ntu onestop catalog categories
ntu onestop catalog search "transcript" --limit 10
```

Replace capitalized placeholders with values returned by the service. Use `--help` after a command for its current options. Choose a command to see its arguments, examples and result fields.

| Command | What it does |
| --- | --- |
| [`ntu onestop catalog categories`](catalog.md#cmd-onestop-catalog-categories) | List the signed-in student's visible One Stop catalog categories and subcategories, parent IDs and published item counts. |
| [`ntu onestop catalog search`](catalog.md#cmd-onestop-catalog-search) | Search the student's One Stop service catalog with query, or browse one category_id. |
| [`ntu onestop catalog item`](catalog.md#cmd-onestop-catalog-item) | Read a native One Stop form's description, current visible field labels/types, mandatory flags and choices. |
| [`ntu onestop catalog favourite`](catalog.md#cmd-onestop-catalog-favourite) | Set a catalog item's favourite state through its category's native control. |

## Command details

<a id="cmd-onestop-catalog-categories"></a>
### `ntu onestop catalog categories`

List the signed-in student's visible One Stop catalog categories and subcategories, parent IDs and published item counts.

#### Usage

```sh
ntu onestop catalog categories
```

Use `ntu onestop catalog categories --help` for the current interface.

#### Arguments and options

- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `categories`, `root_count`, `total_root_count`, `complete`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/catalog.md#onestop_list_catalog_categories).

<a id="cmd-onestop-catalog-search"></a>
### `ntu onestop catalog search`

Search the student's One Stop service catalog with query, or browse one category_id.

#### Usage

```sh
ntu onestop catalog search "transcript" --limit 10
```

Use `ntu onestop catalog search --help` for the current interface.

#### Arguments and options

- `QUERY`: The search terms. Quote multiword text so the shell passes it as one argument.
- `--category`: The category ID returned by the relevant listing or details command.
- `--limit`, `-l`: Maximum number of results to return in this page. Default: `20`.
- `--offset`: Number of results to skip before this page. Default: `0`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `offset`, `available_count`, `total_count`, `complete`, `next_offset`, `retrieved_at`, `source_url`, `cached`, `scope`, `query`, `category_id`, `items`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/catalog.md#onestop_list_catalog_items).

<a id="cmd-onestop-catalog-item"></a>
### `ntu onestop catalog item`

Read a native One Stop form's description, current visible field labels/types, mandatory flags and choices.

#### Usage

```sh
ntu onestop catalog item ITEM_ID
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu onestop catalog item --help` for the current interface.

#### Arguments and options

- `ITEM_ID`: **Required.** The item ID returned by the relevant listing or details command.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `item_id`, `title`, `summary`, `description`, `mandatory_attachment`, `fields`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/catalog.md#onestop_get_catalog_item).

<a id="cmd-onestop-catalog-favourite"></a>
### `ntu onestop catalog favourite`

Set a catalog item's favourite state through its category's native control.

This operation requires local confirmation and is refused when confirmation cannot be obtained interactively.

#### Usage

```sh
ntu onestop catalog favourite ITEM_ID --category CATEGORY_ID --state on
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu onestop catalog favourite --help` for the current interface.

#### Arguments and options

- `ITEM_ID`: **Required.** The item ID returned by the relevant listing or details command.
- `--category`: **Required.** The category ID returned by the relevant listing or details command.
- `--state`: **Required.** The requested favourite state. Choices: `on`, `off`.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/catalog.md#onestop_set_catalog_favourite).
