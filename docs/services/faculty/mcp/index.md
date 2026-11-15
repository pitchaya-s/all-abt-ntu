# Faculty: MCP reference

[Service overview](../index.md) · [CLI reference](../cli/index.md) · [MCP reference](index.md)

## Tools

Inputs are required only where marked. Output fields marked required may still be `null` when their type allows it. See the [data types](types.md) for object fields.

### `faculty_search`

Search NTU's public faculty directory by name, optionally filtered by one research interest. Omit query to browse. Copy interest_id from faculty_list_interests. Returns names, schools, public emails, appointments, interests, abbreviated biographies and profile links. Pages start at 1, with up to ten profiles; follow next_page.

Optional inputs: `query`, `interest_id`, `page`, and `refresh`.

`query` searches faculty names, up to 200 characters. Omit it to browse. `interest_id` selects one research interest; obtain its ID with `faculty_list_interests`. Search pages start at 1 and contain up to ten profiles. Follow `next_page` until it is `null`.

```json
{"query": "faculty member name", "page": 1}
```

Returns `profiles`, `page`, `total_pages`, `total_count`, and `next_page`. Each profile contains its published name, school, email, appointments, research interests, biography summary, and profile URL. Missing information stays `null`; summaries may be abbreviated by NTU. Profile URLs often point to DR-NTU person pages; their readable slugs are not item UUIDs accepted by `drntu_get_item`.

For pages after the first, the client checks the first page's totals, using the cache when available, and rejects pages beyond the reported range. It also rejects inconsistent totals between the two pages rather than presenting a changed result set as complete.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `query` | `string` | No | maximum length: `200`; default: `""` |
| `interest_id` | `string` or `null` | No | default: `null`; pattern: `^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$` |
| `page` | `integer` | No | minimum: `1`; maximum: `10000`; default: `1` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `profiles` | array of [`Profile`](types.md#mcp-type-profile) | Yes | — |
| `page` | `integer` | Yes | minimum: `1` |
| `total_pages` | `integer` | Yes | minimum: `0` |
| `total_count` | `integer` | Yes | minimum: `0` |
| `next_page` | `integer` or `null` | Yes | minimum: `1` |

Unknown fields are not accepted.

### `faculty_list_interests`

List current faculty research-interest labels and filter IDs from NTU's directory form. Optional query matches labels by case-insensitive substring. Follow next_offset for remaining labels, then pass one interest_id to faculty_search.

Optional inputs: `query`, `limit`, `offset`, and `refresh`.

Lists research-interest labels and IDs from the official directory form. `query` filters labels by case-insensitive substring. `limit` defaults to 50, maximum 100. Follow `next_offset` for additional results, then pass a returned `interest_id` to `faculty_search`.

```json
{"query": "intelligence"}
```

Labels are not API filter values. Unknown IDs are rejected rather than silently returning an unfiltered directory.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `query` | `string` | No | maximum length: `200`; default: `""` |
| `limit` | `integer` | No | minimum: `1`; maximum: `100`; default: `50` |
| `offset` | `integer` | No | minimum: `0`; default: `0` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `interests` | array of [`Interest`](types.md#mcp-type-interest) | Yes | — |
| `total_count` | `integer` | Yes | minimum: `0` |
| `next_offset` | `integer` or `null` | Yes | minimum: `0` |

Unknown fields are not accepted.

See the [MCP data types](types.md) for nested object fields.
