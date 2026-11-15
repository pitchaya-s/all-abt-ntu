# Faculty: MCP data types

[Service overview](../index.md) · [MCP reference](index.md)

## MCP data types

These named types describe nested fields in the [MCP tool reference](index.md). A required field may still be `null` when its type allows it.

<a id="mcp-type-interest"></a>
### `Interest`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `interest_id` | `string` | Yes | — |
| `name` | `string` | Yes | minimum length: `1` |

Unknown fields are not accepted.

<a id="mcp-type-profile"></a>
### `Profile`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `name` | `string` | Yes | minimum length: `1` |
| `school` | `string` or `null` | Yes | — |
| `email` | `string` or `null` | Yes | — |
| `appointments` | array of `string` or `null` | Yes | — |
| `interests` | array of `string` or `null` | Yes | — |
| `summary` | `string` or `null` | Yes | — |
| `profile_url` | `string` | Yes | — |

Unknown fields are not accepted.
