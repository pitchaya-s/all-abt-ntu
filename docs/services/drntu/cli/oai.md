# DR-NTU: OAI-PMH CLI commands

[Back to DR-NTU CLI](index.md) · [MCP reference](../mcp/index.md)

- [`ntu research oai info`](#cmd-research-oai-info)
- [`ntu research oai formats`](#cmd-research-oai-formats)
- [`ntu research oai sets`](#cmd-research-oai-sets)
- [`ntu research oai records`](#cmd-research-oai-records)
- [`ntu research oai record`](#cmd-research-oai-record)

## Command details

<a id="cmd-research-oai-info"></a>
### `ntu research oai info`

Describe DR-NTU's OAI-PMH repository, modification-date precision, deletion policy and earliest datestamp.

#### Usage

```sh
ntu research oai info
```

Use `ntu research oai info --help` for the current interface.

#### Arguments and options

- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `response_date`, `repository_name`, `base_url`, `protocol_version`, `admin_emails`, `earliest_datestamp`, `deleted_record`, `granularity`, `descriptions_xml`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/oai.md#drntu_oai_identify).

<a id="cmd-research-oai-formats"></a>
### `ntu research oai formats`

List OAI metadata prefixes, namespaces and schemas.

#### Usage

```sh
ntu research oai formats
```

Use `ntu research oai formats --help` for the current interface.

#### Arguments and options

- `IDENTIFIER`: The OAI identifier for the requested record.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `response_date`, `formats`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/oai.md#drntu_oai_list_metadata_formats).

<a id="cmd-research-oai-sets"></a>
### `ntu research oai sets`

List OAI collection/community sets.

#### Usage

```sh
ntu research oai sets
```

Use `ntu research oai sets --help` for the current interface.

#### Arguments and options

- `--token`: The continuation token returned by the OAI server.
- `--limit`, `-l`: Maximum number of results to return in this page. Default: `20`.
- `--offset`: Number of results to skip before this page. Default: `0`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `response_date`, `sets`, `pagination`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/oai.md#drntu_oai_list_sets).

<a id="cmd-research-oai-records"></a>
### `ntu research oai records`

Read one bounded OAI records page, defaulting to oai_dc.

#### Usage

```sh
ntu research oai records
```

Use `ntu research oai records --help` for the current interface.

#### Arguments and options

- `--prefix`: The OAI metadata format prefix, such as `oai_dc`.
- `--set`: The OAI set identifier returned by the sets listing.
- `--from-date`: Start of the date range in ISO format.
- `--until-date`: End of the date range in ISO format.
- `--token`: The continuation token returned by the OAI server.
- `--headers-only`: List record headers instead of full OAI metadata.
- `--limit`, `-l`: Maximum number of results to return in this page. Default: `10`.
- `--offset`: Number of results to skip before this page. Default: `0`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `response_date`, `headers_only`, `records`, `pagination`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/oai.md#drntu_oai_list_records).

<a id="cmd-research-oai-record"></a>
### `ntu research oai record`

Get one record by its OAI identifier, not a REST UUID.

#### Usage

```sh
ntu research oai record IDENTIFIER
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu research oai record --help` for the current interface.

#### Arguments and options

- `IDENTIFIER`: **Required.** The OAI identifier for the requested record.
- `--prefix`: The OAI metadata format prefix, such as `oai_dc`. Default: `oai_dc`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `response_date`, `metadata_prefix`, `record`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/oai.md#drntu_oai_get_record).
