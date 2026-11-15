# News: MCP data types

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

<a id="mcp-type-story"></a>
### `Story`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `title` | `string` | Yes | minimum length: `1` |
| `url` | `string` | Yes | — |
| `published_date` | `string` or `null` | Yes | — |
| `summary` | `string` or `null` | Yes | — |

Unknown fields are not accepted.
