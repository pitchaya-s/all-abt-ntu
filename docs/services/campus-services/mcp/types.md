# Campus Services: MCP data types

[Service overview](../index.md) · [MCP reference](index.md)

## MCP data types

These named types describe nested fields in the [MCP tool reference](index.md). A required field may still be `null` when its type allows it.

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
