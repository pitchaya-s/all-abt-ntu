# MazeMap: MCP data types

[Service overview](../index.md) · [MCP reference](index.md)

## MCP data types

These named types describe nested fields in the [MCP tool reference](index.md). A required field may still be `null` when its type allows it.

<a id="mcp-type-building"></a>
### `Building`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `building_id` | `integer` | Yes | greater than: `0` |
| `name` | `string` or `null` | Yes | — |
| `floors` | array of [`Floor`](#mcp-type-floor) | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-campus"></a>
### `Campus`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `campus_id` | `integer` | Yes | greater than: `0` |
| `name` | `string` | Yes | — |
| `center` | [`Point`](#mcp-type-point) | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-floor"></a>
### `Floor`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `floor_id` | `integer` | Yes | greater than: `0` |
| `name` | `string` or `null` | Yes | — |
| `level` | `number` or `null` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-place"></a>
### `Place`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `poi_id` | `integer` | Yes | greater than: `0` |
| `campus_id` | `integer` | Yes | greater than: `0` |
| `name` | `string` | Yes | — |
| `identifier` | `string` or `null` | Yes | — |
| `aliases` | array of `string` | Yes | — |
| `building_id` | `integer` or `null` | Yes | — |
| `building_name` | `string` or `null` | Yes | — |
| `floor_id` | `integer` or `null` | Yes | — |
| `floor_name` | `string` or `null` | Yes | — |
| `level` | `number` or `null` | Yes | — |
| `categories` | array of `string` | Yes | — |
| `point` | [`Point`](#mcp-type-point) or `null` | Yes | — |
| `description` | `string` or `null` | Yes | — |
| `capacity` | `integer` or `null` | Yes | minimum: `0` |
| `map_url` | `string` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-point"></a>
### `Point`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `longitude` | `number` | Yes | minimum: `-180`; maximum: `180` |
| `latitude` | `number` | Yes | minimum: `-90`; maximum: `90` |

Unknown fields are not accepted.

<a id="mcp-type-route"></a>
### `Route`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `distance_metres` | `number` or `null` | Yes | minimum: `0` |
| `duration_seconds` | `number` or `null` | Yes | minimum: `0` |
| `accessible` | `boolean` or `null` | Yes | — |
| `uncertain` | `boolean` or `null` | Yes | — |
| `instructions` | array of `string` or `null` | Yes | — |
| `issues` | array of `string` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-routebuilding"></a>
### `RouteBuilding`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `building_id` | `integer` | Yes | — |
| `name` | `string` or `null` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-routefloor"></a>
### `RouteFloor`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `floor_id` | `integer` | Yes | greater than: `0` |
| `name` | `string` or `null` | Yes | — |
| `level` | `number` or `null` | Yes | — |
| `building_id` | `integer` or `null` | Yes | — |

Unknown fields are not accepted.
