# NTU Omnibus: MCP reference

[Service overview](../index.md) · [CLI reference](../cli/index.md) · [MCP reference](index.md)

## Tools

Inputs are required only where marked. Output fields marked required may still be `null` when their type allows it. See the [data types](types.md) for object fields.

### `omnibus_get_live_buses`

Get current live vehicle positions for one NTU campus shuttle route. An empty list means no positions were reported in this snapshot; source timestamps may be unavailable.

Input: `route_code` (`Blue`, `Brown`, `Green`, `Grey`, or `Red`), default `Blue`.

Returns bus positions, speed/direction and available crowd data for one selected route. `reported_bus_count` and `buses` can be empty. `source_timestamp` may be `null` when NTU publishes its placeholder timestamp; `retrieved_at` is when this MCP fetched the snapshot.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `route_code` | `"Blue"`, `"Brown"`, `"Green"`, `"Grey"`, `"Red"` | No | default: `"Blue"` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_urls` | array of `string` | Yes | — |
| `cached` | `boolean` | No | default: `false` |
| `route_code` | `string` | Yes | — |
| `reported_bus_count` | `integer` | Yes | minimum: `0` |
| `source_timestamp` | `string` or `null` | No | default: `null`; format: `date-time` |
| `buses` | array of [`BusPosition`](types.md#mcp-type-busposition) | Yes | — |

Unknown fields are not accepted.

### `omnibus_list_routes`

List public NTU shuttle routes and their published display colors. This does not include route path geometry.

Returns the app's campus shuttle routes and published route colors. The route-list action currently lists Blue, Brown, Green, Grey, and Red. It does not supply route path geometry.

**Inputs**

None.

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_urls` | array of `string` | Yes | — |
| `cached` | `boolean` | No | default: `false` |
| `routes` | array of [`Route`](types.md#mcp-type-route) | Yes | — |
| `colors` | array of [`RouteColor`](types.md#mcp-type-routecolor) | Yes | — |

Unknown fields are not accepted.

### `omnibus_list_stops`

Search NTU shuttle and LTA bus stops by stop name or code, optionally limited to a route/service. Follow next_offset for more results.

Inputs: optional `query` (stop name or code), `route_code` (campus route or `179`, `179A`, `199`), `limit` (1–100, default 20), and `offset` (default 0).

Returns matching route-stop associations, with `total_count` and `next_offset`. A stop associated with more than one route can appear more than once. `cached` is true when every requested route came from the stop cache; `retrieved_at` is the oldest contributing route snapshot, including when fresh and cached routes are combined.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `query` | `string` | No | maximum length: `120`; default: `""` |
| `route_code` | `"Blue"`, `"Brown"`, `"Green"`, `"Grey"`, `"Red"`, `"179"`, `"179A"`, `"199"` or `null` | No | default: `null` |
| `limit` | `integer` | No | minimum: `1`; maximum: `100`; default: `20` |
| `offset` | `integer` | No | minimum: `0`; default: `0` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_urls` | array of `string` | Yes | — |
| `cached` | `boolean` | No | default: `false` |
| `stops` | array of [`Stop`](types.md#mcp-type-stop) | Yes | — |
| `total_count` | `integer` | Yes | minimum: `0` |
| `next_offset` | `integer` or `null` | No | default: `null`; minimum: `0` |
| `routes_without_stop_data` | array of `string` | No | Queried routes with no stop associations in the upstream response. |

Unknown fields are not accepted.

### `omnibus_get_arrivals`

Get arrival estimates for NTU shuttles and/or LTA services 179, 179A, and 199. Filter by route and stop name/code; at most 20 matching route-stop pairs can be fetched per call. Broader matches require a narrower filter. LTA estimates use minutes; unavailable estimates and unpublished seconds are null.

Inputs: optional `route_filter` (campus route or `179`, `179A`, `199`), `stop_query`, and `source` (`all`, `shuttle`, or `lta`; default `all`).

Returns `shuttle_arrivals` and `lta_arrivals` separately. LTA minute estimates are retained; seconds/load are null when the public per-stop action does not publish them. `IsETA_NotFound` becomes null estimates rather than a zero-minute arrival. A call fetches at most 20 matching route-stop pairs; broader matches return an explicit error asking for a narrower stop/route filter. Services 179, 179A and 199 are exposed by the arrival and stop tools, not the campus shuttle vehicle-position endpoint. Estimates may be unavailable.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `route_filter` | `"Blue"`, `"Brown"`, `"Green"`, `"Grey"`, `"Red"`, `"179"`, `"179A"`, `"199"` or `null` | No | default: `null` |
| `stop_query` | `string` | No | maximum length: `120`; default: `""` |
| `source` | `"all"`, `"shuttle"`, `"lta"` | No | default: `"all"` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_urls` | array of `string` | Yes | — |
| `cached` | `boolean` | No | default: `false` |
| `route_filter` | `string` or `null` | Yes | — |
| `stop_query` | `string` | Yes | — |
| `shuttle_arrivals` | array of [`ShuttleArrival`](types.md#mcp-type-shuttlearrival) | Yes | — |
| `lta_arrivals` | array of [`LtaArrival`](types.md#mcp-type-ltaarrival) | Yes | — |
| `routes_without_stop_data` | array of `string` | No | Queried routes with no stop associations in the upstream response. |

Unknown fields are not accepted.

### `omnibus_get_service_status`

Get the published first/last bus schedule, public-holiday/special-day flags, and temporary notices for an NTU campus shuttle route.

Input: `route_code` (campus route), default `Blue`.

Returns published first/last bus schedule rows, whether the app used its local schedule table, public-holiday and special-day flags, and temporary service messages. Schedules and notices are source data, not a live guarantee of operation.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `route_code` | `"Blue"`, `"Brown"`, `"Green"`, `"Grey"`, `"Red"` | No | default: `"Blue"` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_urls` | array of `string` | Yes | — |
| `cached` | `boolean` | No | default: `false` |
| `route_code` | `string` | Yes | — |
| `schedules` | array of [`RouteSchedule`](types.md#mcp-type-routeschedule) | Yes | — |
| `schedule_from_local_db` | `boolean` | Yes | — |
| `is_public_holiday` | `boolean` | Yes | — |
| `is_special_day` | `boolean` | Yes | — |
| `special_day_notice` | `string` or `null` | No | default: `null` |
| `has_temporary_message` | `boolean` | Yes | — |
| `temporary_message` | `string` or `null` | No | default: `null` |
| `no_active_bus_message` | `string` or `null` | No | default: `null` |
| `no_operations_message` | `string` or `null` | No | default: `null` |

Unknown fields are not accepted.

See the [MCP data types](types.md) for nested object fields.
