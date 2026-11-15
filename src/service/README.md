# Campus services

[CLI commands](#cli-commands) · [MCP tools](#mcp-tools) · [MCP data types](#mcp-data-types) · [Service notes](#service-notes)

For installation and shared authentication, see the [main README](../../README.md).

## CLI commands

The output column lists the JSON result fields; human-readable output is formatted for the terminal. Use `ntu services --help` and append `--help` to a command for option details. `VALUE` denotes an option value; required arguments and options are marked. See the [complete CLI reference](../COMMANDS.md) for shared settings and all services.

| Command | Arguments and options | Purpose | Output |
| --- | --- | --- | --- |
| `ntu services search` | `QUERY (optional)`, `--type VALUE`, `--category VALUE`, `--location VALUE (default: )`, `--limit/-l VALUE (default: 20)`, `--offset VALUE`, `--refresh/-r`, `--json/-j` | Find NTU food outlets, shops, clinics and campus services by name/address keyword and optional location substring. | `retrieved_at`, `source_url`, `cached`, `locations`, `total_count`, `directory_count`, `pages_checked`, `next_offset` ([schema](#service_search)) |
| `ntu services filters` | `--refresh/-r`, `--json/-j` | List official campus service type and category labels with filter IDs. | `retrieved_at`, `source_url`, `cached`, `types`, `categories` ([schema](#service_list_filters)) |

## MCP tools

Inputs are required only where marked. Output fields marked required may still be `null` when their type allows it. See the nested data types below for object fields.

### `service_search`

Find NTU food outlets, shops, clinics and campus services by name/address keyword and optional location substring. Optional type_id/category_id come from service_list_filters. Collects all source pages before local matching and result pagination; returns addresses, published hours, contact details and map links. Source taxonomy filters can omit relevant entries; use an unfiltered keyword search for broader coverage. Hours are not a live open-now check.

Optional inputs: `query`, `type_id`, `category_id`, `location_contains`, `limit`, `offset`, and `refresh`.

`query` matches a case-insensitive substring of a location's name or address. `location_contains` additionally filters its address. Each accepts up to 200 characters. Omit both to browse. `type_id` and `category_id` must be current IDs from `service_list_filters`.

```json
{"query": "clinic"}
```

```json
{"query": "coffee", "location_contains": "North Spine", "limit": 10}
```

The API ignores keyword parameters, so the client collects every page within the selected type/category before applying these substring filters locally. `limit` defaults to 20, maximum 100. Follow `next_offset` for remaining matches.

Each location includes its name, address, published operating hours, phone, fax, email, and map URL where supplied. Missing or blank values become `null`. Hours retain published wording, including holiday exceptions; they are not converted into an open-now guarantee.

Results include `total_count` after local matching, `directory_count` before local matching, and `pages_checked`. The latter covers all pages for the selected source filters. Collection stops with an error if pages are missing, inconsistent, duplicated, or exceed the 50-page safety limit; no partial directory is presented as complete.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `query` | `string` | No | maximum length: `200`; default: `""` |
| `type_id` | `string` or `null` | No | default: `null`; pattern: `^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$` |
| `category_id` | `string` or `null` | No | default: `null`; pattern: `^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$` |
| `location_contains` | `string` | No | maximum length: `200`; default: `""` |
| `limit` | `integer` | No | minimum: `1`; maximum: `100`; default: `20` |
| `offset` | `integer` | No | minimum: `0`; default: `0` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `locations` | array of [`Location`](#mcp-type-location) | Yes | — |
| `total_count` | `integer` | Yes | minimum: `0` |
| `directory_count` | `integer` | Yes | minimum: `0` |
| `pages_checked` | `integer` | Yes | minimum: `1` |
| `next_offset` | `integer` or `null` | Yes | minimum: `0` |

Unknown fields are not accepted.

### `service_list_filters`

List official campus service type and category labels with filter IDs. Pass a returned id as service_search.type_id or category_id. Taxonomy assignments may be incomplete; a filtered empty result does not establish no matching service exists.

Optional input: `refresh`.

Returns `types` and `categories`, each containing labels and IDs extracted from the official form. Types include food and beverages, retail, clinics, and services. Categories include the site's published dietary/general labels. Pass a returned `id` to the corresponding search argument.

**NTU's taxonomy assignments are incomplete.** During testing, the clinic and halal category filters returned no entries, even though the unfiltered directory contained a clinic and locations whose names mentioned halal certification. A zero-result source filter does not establish that no relevant services exist. Prefer an unfiltered keyword search when coverage matters. Published dietary labels are not independent verification of current certification.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `types` | array of [`FilterOption`](#mcp-type-filteroption) | Yes | — |
| `categories` | array of [`FilterOption`](#mcp-type-filteroption) | Yes | — |

Unknown fields are not accepted.

## MCP data types

These named types are used by the tool input and output fields above.

<a id="mcp-type-filteroption"></a>
### `FilterOption`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `id` | `string` | Yes | — |
| `name` | `string` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-location"></a>
### `Location`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `name` | `string` | Yes | minimum length: `1` |
| `address` | `string` or `null` | Yes | — |
| `phone` | `string` or `null` | Yes | — |
| `fax` | `string` or `null` | Yes | — |
| `email` | `string` or `null` | Yes | — |
| `operating_hours` | `string` or `null` | Yes | — |
| `map_url` | `string` or `null` | Yes | — |

Unknown fields are not accepted.

## Service notes

Read-only access to NTU's published food, retail, clinic, and service directory. No credentials or Chromium required.

### Requests and limitations

Results include `retrieved_at`, `source_url`, and `cached`. Pages are cached in memory for five minutes. For a collected directory, `retrieved_at` is the oldest page timestamp, `cached` is true only when every result page came from cache, and `source_url` identifies the first page. `refresh: true` fetches every page again.

The shared public HTTP client pools connections, bounds responses to 8 MB, uses a 20-second timeout, and permits up to two in-flight requests per client with 250 ms default pacing. Later directory pages are fetched with bounded concurrency, and results remain in source page order. Subsequent searches reuse cached pages. Public HTTP settings are documented in the [shared runtime guide](../shared/README.md#public-http-reads). Published hours, contact information, and map links can become outdated; the directory does not establish live opening, occupancy, accessibility, or booking availability.

### Sources

- [NTU general directory](https://www.ntu.edu.sg/life-at-ntu/leisure-and-dining/general-directory/) supplies filter labels and IDs.
- [GetLocations](https://www.ntu.edu.sg/life-at-ntu/leisure-and-dining/general-directory/GetLocations/) returns location cards, twelve per page. Verified parameters: `page`, `locationTypes`, and `locationCategories`. The tested `listingKeyword` parameter was ignored; keyword and address matching are therefore local.

### Tests

Run from the repository root:

```sh
uv run python -m unittest discover -s tests/service -t . -v
uv run python -m tests.service.live_smoke
```

Synthetic offline fixtures cover later-page keyword matches, source taxonomy gaps, address filtering, result pagination, missing contact fields, changing/malformed responses, and MCP schemas and errors. The opt-in live stdio smoke checks complete directory retrieval, keyword and location searches, a working source filter, pagination, and caching. It prints statuses without saving directory records.
