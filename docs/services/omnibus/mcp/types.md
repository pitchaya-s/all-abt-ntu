# NTU Omnibus: MCP data types

[Service overview](../index.md) · [MCP reference](index.md)

## MCP data types

These named types describe nested fields in the [MCP tool reference](index.md). A required field may still be `null` when its type allows it.

<a id="mcp-type-busposition"></a>
### `BusPosition`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `vehicle_plate` | `string` | Yes | — |
| `latitude` | `number` | Yes | minimum: `-90`; maximum: `90` |
| `longitude` | `number` | Yes | minimum: `-180`; maximum: `180` |
| `speed` | `number` or `null` | No | default: `null` |
| `direction_degrees` | `number` or `null` | No | default: `null` |
| `crowd_level` | `string` or `null` | No | default: `null` |
| `occupancy` | `string` or `null` | No | default: `null` |
| `capacity` | `integer` or `null` | No | default: `null` |
| `ridership` | `integer` or `null` | No | default: `null` |

Unknown fields are not accepted.

<a id="mcp-type-ltaarrival"></a>
### `LtaArrival`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `service_no` | `string` | Yes | minimum length: `1` |
| `stop_code` | `string` | Yes | minimum length: `1` |
| `stop_name` | `string` or `null` | No | default: `null` |
| `eta_minutes` | `string` or `null` | No | default: `null` |
| `eta_seconds` | `integer` or `null` | No | default: `null` |
| `next_eta_minutes` | `string` or `null` | No | default: `null` |
| `next_eta_seconds` | `integer` or `null` | No | default: `null` |
| `load` | `string` or `null` | No | default: `null` |

Unknown fields are not accepted.

<a id="mcp-type-route"></a>
### `Route`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `route_code` | `string` | Yes | minimum length: `1` |
| `description` | `string` or `null` | No | default: `null` |
| `long_name` | `string` or `null` | No | default: `null` |
| `is_lta_service` | `boolean` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-routecolor"></a>
### `RouteColor`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `route_code` | `string` | Yes | minimum length: `1` |
| `color_code` | `string` | Yes | minimum length: `1` |
| `display_order` | `integer` or `null` | No | default: `null` |

Unknown fields are not accepted.

<a id="mcp-type-routeschedule"></a>
### `RouteSchedule`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `route_code` | `string` | Yes | minimum length: `1` |
| `first_bus` | `string` or `null` | No | default: `null` |
| `last_bus` | `string` or `null` | No | default: `null` |
| `schedule_type` | `string` or `null` | No | default: `null` |
| `day_type` | `string` or `null` | No | default: `null` |
| `display_order` | `integer` or `null` | No | default: `null` |

Unknown fields are not accepted.

<a id="mcp-type-shuttlearrival"></a>
### `ShuttleArrival`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `route_code` | `string` | Yes | minimum length: `1` |
| `stop_name` | `string` | Yes | minimum length: `1` |
| `stop_code` | `string` | Yes | minimum length: `1` |
| `eta` | `string` or `null` | No | default: `null` |
| `next_eta` | `string` or `null` | No | default: `null` |
| `color_code` | `string` or `null` | No | default: `null` |

Unknown fields are not accepted.

<a id="mcp-type-stop"></a>
### `Stop`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `name` | `string` | Yes | minimum length: `1` |
| `stop_code` | `string` | Yes | minimum length: `1` |
| `route_code` | `string` | Yes | minimum length: `1` |
| `service_id` | `string` or `null` | No | default: `null` |
| `is_lta_service` | `boolean` | Yes | — |
| `route_long_name` | `string` or `null` | No | default: `null` |
| `color_code` | `string` or `null` | No | default: `null` |

Unknown fields are not accepted.
