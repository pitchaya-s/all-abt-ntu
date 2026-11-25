# Campus Services: MCP reference

[Service overview](../index.md) · [CLI reference](../cli/index.md) · [MCP reference](index.md)

## Tools

Inputs are required only where marked. Output fields marked required may still be `null` when their type allows it. See the [data types](types.md) for object fields.

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
| `locations` | array of [`Location`](types.md#mcp-type-location) | Yes | — |
| `total_count` | `integer` | Yes | minimum: `0` |
| `directory_count` | `integer` | Yes | minimum: `0` |
| `pages_checked` | `integer` | Yes | minimum: `1` |
| `next_offset` | `integer` or `null` | Yes | minimum: `0` |

Unknown fields are not accepted.

### `service_list_filters`

List official campus service type and category labels with filter IDs. Pass a returned id as service_search.type_id or category_id. Taxonomy assignments may be incomplete; a filtered empty result does not establish no matching service exists.

Optional input: `refresh`.

Returns `types` and `categories`, each containing labels and IDs extracted from the official form. Types include food and beverages, retail, clinics, and services. Categories include the site's published dietary/general labels. Pass a returned `id` to the corresponding search argument.

NTU's category labels can omit relevant entries. If a category search finds nothing, try a keyword search with no category filter. Check current dietary certification with the outlet.

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
| `types` | array of [`FilterOption`](types.md#mcp-type-filteroption) | Yes | — |
| `categories` | array of [`FilterOption`](types.md#mcp-type-filteroption) | Yes | — |

Unknown fields are not accepted.

See the [MCP data types](types.md) for nested object fields.
