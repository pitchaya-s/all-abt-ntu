# CareerAxis: MCP data types

[Service overview](../index.md) · [MCP reference](index.md)

## MCP data types

These named types describe nested fields in the [MCP tool reference](index.md). A required field may still be `null` when its type allows it.

<a id="mcp-type-opportunity"></a>
### `Opportunity`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `title` | `string` | Yes | minimum length: `1`; maximum length: `500` |
| `url` | `string` | Yes | — |
| `details` | `string` | Yes | maximum length: `4000` |

Unknown fields are not accepted.

<a id="mcp-type-portalitem"></a>
### `PortalItem`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `title` | `string` | Yes | minimum length: `1`; maximum length: `500` |
| `url` | `string` | Yes | — |
| `summary` | `string` | Yes | maximum length: `4000` |

Unknown fields are not accepted.
