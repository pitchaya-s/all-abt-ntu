# DR-NTU: Search and browse CLI commands

[Back to DR-NTU CLI](index.md) · [MCP reference](../mcp/index.md)

- [`ntu research search`](#cmd-research-search)
- [`ntu research facets`](#cmd-research-facets)
- [`ntu research dataset`](#cmd-research-dataset)
- [`ntu research browse communities`](#cmd-research-browse-communities)
- [`ntu research browse collections`](#cmd-research-browse-collections)
- [`ntu research bundle files`](#cmd-research-bundle-files)
- [`ntu research item bundles`](#cmd-research-item-bundles)
- [`ntu research item show`](#cmd-research-item-show)

## Command details

<a id="cmd-research-search"></a>
### `ntu research search`

Search DR-NTU publications by keywords or Solr query.

#### Usage

```sh
ntu research search "machine learning" --page 0 --page-size 10
```

Use `ntu research search --help` for the current interface.

#### Arguments and options

- `QUERY`: **Required.** The search terms. Quote multiword text so the shell passes it as one argument.
- `--scope`: The scope ID returned by the relevant listing or details command.
- `--entity-type`: The kind of repository entity to search. Choices: `Publication`, `Person`, `all`. Default: `Publication`.
- `--filters`: Structured filters as a JSON value.
- `--page`, `-p`: Page number to request; page numbering depends on the service. Default: `0`.
- `--page-size`: Maximum number of results in a page. Default: `10`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `query`, `items`, `pagination`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/repository.md#drntu_search).

<a id="cmd-research-facets"></a>
### `ntu research facets`

Discover search facet names, or supply a facet name to list its values and counts for the query/scope/filters.

#### Usage

```sh
ntu research facets
```

Use `ntu research facets --help` for the current interface.

#### Arguments and options

- `--facet`: The facet name to inspect; omit it to discover available facets.
- `--query`: The search terms. Quote multiword text so the shell passes it as one argument.
- `--scope`: The scope ID returned by the relevant listing or details command.
- `--entity-type`: The kind of repository entity to search. Choices: `Publication`, `Person`, `all`. Default: `Publication`.
- `--filters`: Structured filters as a JSON value.
- `--page`, `-p`: Page number to request; page numbering depends on the service. Default: `0`.
- `--page-size`: Maximum number of results in a page. Default: `10`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `facet`, `definitions`, `values`, `pagination`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/repository.md#drntu_get_facets).

<a id="cmd-research-dataset"></a>
### `ntu research dataset`

Read a published DR-NTU Data dataset by doi: identifier: title, authors, descriptions, subjects, license and paginated file inventory.

#### Usage

```sh
ntu research dataset PERSISTENT_ID
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu research dataset --help` for the current interface.

#### Arguments and options

- `PERSISTENT_ID`: **Required.** The persistent identifier or DOI of the dataset.
- `--version`: The requested dataset version; omit it for the service default.
- `--limit`, `-l`: Maximum number of results to return in this page. Default: `50`.
- `--offset`: Number of results to skip before this page. Default: `0`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `persistent_id`, `dataset_id`, `version`, `version_state`, `title`, `authors`, `descriptions`, `subjects`, `publication_date`, `license_name`, `license_url`, `url`, `files`, `total_files`, `next_offset`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/repository.md#drntu_get_dataset).

<a id="cmd-research-browse-communities"></a>
### `ntu research browse communities`

Browse repository communities or collections.

#### Usage

```sh
ntu research browse communities
```

Use `ntu research browse communities --help` for the current interface.

#### Arguments and options

- `--community`: The community ID returned by the relevant listing or details command.
- `--page`, `-p`: Page number to request; page numbering depends on the service. Default: `0`.
- `--page-size`: Maximum number of results in a page. Default: `20`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `kind`, `containers`, `pagination`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/repository.md#drntu_browse).

<a id="cmd-research-browse-collections"></a>
### `ntu research browse collections`

Browse repository communities or collections.

#### Usage

```sh
ntu research browse collections
```

Use `ntu research browse collections --help` for the current interface.

#### Arguments and options

- `--community`: The community ID returned by the relevant listing or details command.
- `--page`, `-p`: Page number to request; page numbering depends on the service. Default: `0`.
- `--page-size`: Maximum number of results in a page. Default: `20`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `kind`, `containers`, `pagination`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/repository.md#drntu_browse).

<a id="cmd-research-bundle-files"></a>
### `ntu research bundle files`

List a bundle's file metadata: names, byte sizes, checksums, published rights and content URLs.

#### Usage

```sh
ntu research bundle files BUNDLE_ID
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu research bundle files --help` for the current interface.

#### Arguments and options

- `BUNDLE_ID`: **Required.** The bundle ID returned by the relevant listing or details command.
- `--page`, `-p`: Page number to request; page numbering depends on the service. Default: `0`.
- `--page-size`: Maximum number of results in a page. Default: `20`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `bundle_id`, `files`, `pagination`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/repository.md#drntu_list_files).

<a id="cmd-research-item-bundles"></a>
### `ntu research item bundles`

List an item's file groups.

#### Usage

```sh
ntu research item bundles ITEM_ID
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu research item bundles --help` for the current interface.

#### Arguments and options

- `ITEM_ID`: **Required.** The item ID returned by the relevant listing or details command.
- `--page`, `-p`: Page number to request; page numbering depends on the service. Default: `0`.
- `--page-size`: Maximum number of results in a page. Default: `20`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `item_id`, `bundles`, `pagination`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/repository.md#drntu_list_bundles).

<a id="cmd-research-item-show"></a>
### `ntu research item show`

Read a repository item's published metadata, including abstracts, citations, DOI, subjects and rights where supplied.

#### Usage

```sh
ntu research item show ITEM_ID
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu research item show --help` for the current interface.

#### Arguments and options

- `ITEM_ID`: **Required.** The item ID returned by the relevant listing or details command.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `item_id`, `title`, `entity_type`, `url`, `last_modified`, `withdrawn`, `metadata`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/repository.md#drntu_get_item).
