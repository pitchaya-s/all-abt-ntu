# NTU Omnibus

[CLI commands](#cli-commands) · [MCP tools](#mcp-tools) · [MCP data types](#mcp-data-types) · [Service notes](#service-notes)

For installation and shared authentication, see the [main README](../../README.md).

## CLI commands

The output column lists the JSON result fields; human-readable output is formatted for the terminal. Use `ntu bus --help` and append `--help` to a command for option details. `VALUE` denotes an option value; required arguments and options are marked. See the [complete CLI reference](../COMMANDS.md) for shared settings and all services.

| Command | Arguments and options | Purpose | Output |
| --- | --- | --- | --- |
| `ntu bus routes` | `--json/-j` | List public NTU shuttle routes and their published display colors. | `retrieved_at`, `source_urls`, `cached`, `routes`, `colors` ([schema](#omnibus_list_routes)) |
| `ntu bus stops` | `QUERY (optional)`, `--route VALUE [Blue, Brown, Green, Grey, Red, 179, 179A, 199]`, `--limit/-l VALUE (default: 20)`, `--offset VALUE`, `--json/-j` | Search NTU shuttle and LTA bus stops by stop name or code, optionally limited to a route/service. | `retrieved_at`, `source_urls`, `cached`, `stops`, `total_count`, `next_offset` ([schema](#omnibus_list_stops)) |
| `ntu bus arrivals` | `--route VALUE [Blue, Brown, Green, Grey, Red, 179, 179A, 199]`, `--stop VALUE (default: )`, `--source VALUE [all, shuttle, lta] (default: all)`, `--json/-j` | Get arrival estimates for NTU shuttles and/or LTA services 179, 179A, and 199. | `retrieved_at`, `source_urls`, `cached`, `route_filter`, `stop_query`, `shuttle_arrivals`, `lta_arrivals` ([schema](#omnibus_get_arrivals)) |
| `ntu bus live` | `--route VALUE [Blue, Brown, Green, Grey, Red] (default: Blue)`, `--json/-j` | Get current live vehicle positions for one NTU campus shuttle route. | `retrieved_at`, `source_urls`, `cached`, `route_code`, `reported_bus_count`, `source_timestamp`, `buses` ([schema](#omnibus_get_live_buses)) |
| `ntu bus status` | `--route VALUE [Blue, Brown, Green, Grey, Red] (default: Blue)`, `--json/-j` | Get the published first/last bus schedule, public-holiday/special-day flags, and temporary notices for an NTU campus shuttle route. | `retrieved_at`, `source_urls`, `cached`, `route_code`, `schedules`, `schedule_from_local_db`, `is_public_holiday`, `is_special_day`, `special_day_notice`, `has_temporary_message`, `temporary_message`, `no_active_bus_message`, `no_operations_message` ([schema](#omnibus_get_service_status)) |

## MCP tools

Inputs are required only where marked. Output fields marked required may still be `null` when their type allows it. See the nested data types below for object fields.

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
| `buses` | array of [`BusPosition`](#mcp-type-busposition) | Yes | — |

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
| `routes` | array of [`Route`](#mcp-type-route) | Yes | — |
| `colors` | array of [`RouteColor`](#mcp-type-routecolor) | Yes | — |

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
| `stops` | array of [`Stop`](#mcp-type-stop) | Yes | — |
| `total_count` | `integer` | Yes | minimum: `0` |
| `next_offset` | `integer` or `null` | No | default: `null`; minimum: `0` |

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
| `shuttle_arrivals` | array of [`ShuttleArrival`](#mcp-type-shuttlearrival) | Yes | — |
| `lta_arrivals` | array of [`LtaArrival`](#mcp-type-ltaarrival) | Yes | — |

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
| `schedules` | array of [`RouteSchedule`](#mcp-type-routeschedule) | Yes | — |
| `schedule_from_local_db` | `boolean` | Yes | — |
| `is_public_holiday` | `boolean` | Yes | — |
| `is_special_day` | `boolean` | Yes | — |
| `special_day_notice` | `string` or `null` | No | default: `null` |
| `has_temporary_message` | `boolean` | Yes | — |
| `temporary_message` | `string` or `null` | No | default: `null` |
| `no_active_bus_message` | `string` or `null` | No | default: `null` |
| `no_operations_message` | `string` or `null` | No | default: `null` |

Unknown fields are not accepted.

## MCP data types

These named types are used by the tool input and output fields above.

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

## Service notes

Experimental read-only public access to NTU shuttle routes, stop associations, live vehicle positions, arrival estimates, schedules, and service notices. It depends on undocumented app internals that may change without notice. No NTU credentials or extra dependencies are needed. Responses include source URLs and retrieval times; freshness and availability depend on the upstream app.

The client reads NTU Omnibus' current module manifest and JavaScript bundles to discover screen-service paths and version hashes. It caches that endpoint metadata and route-stop associations for five minutes and uses a small cookie jar for the app's anonymous CSRF handshake. The stop cache holds at most eight routes per client and is shared by stop searches and arrival lookups. Live bus positions, arrival estimates, and status responses are not cached. Pooled HTTPS requests retain the anonymous cookie only for `apps.ntu.edu.sg`, share the process-wide per-host concurrency and pacing limit, and retry transient failures once while respecting short `Retry-After` delays. Omnibus operations remain serialized around their shared cookie and CSRF state. Requests also have a 20-second timeout and an 8 MB response limit.

### Sources and coverage

The app is hosted at [apps.ntu.edu.sg/NTUOmnibus](https://apps.ntu.edu.sg/NTUOmnibus/). Its current module manifest and public bundles are used to discover endpoint paths and API hashes at runtime. Reads use the same public map actions as the deployed Shuttle page; unused BusStop component endpoints reject requests and are not used. The client reads these screen services:

- `DataActionGetActiveBusServicesData` for live shuttle positions.
- `DataActionGetRoutesList` and `ActionGetRoutesCodejson` for route names and colors.
- `DataActionGetPickupCheckPoints` with the selected route and shuttle/LTA flag for route-stop associations.
- `ActionGetETAAndNextETA_FMS` and `ActionGetETAAndNextETA_LTA` for live estimates at each matching stop.
- `ActionGetRoutesMinMax`, `ActionCheckPHSpecialDay`, and `ActionGetTempMessages` for schedules and status.

Route path geometry is outside the current tool outputs. A missing vehicle or arrival in a snapshot does not establish that a route is not operating.

For public bus arrivals, [LTA DataMall's dynamic datasets](https://datamall.lta.gov.sg/content/datamall/en/dynamic-data.html) are an official alternative to evaluate if an API key and its terms are acceptable. They do not establish a replacement for NTU's campus shuttle data; this integration continues to use the NTU app.

### Checks

Synthetic tests cover native route IDs and input flags, stop-cache reuse and expiry, cache isolation and concurrent reads, fresh arrival estimates, per-source arrival lookups, missing estimates, result limits, endpoint discovery, CSRF recovery, bounded HTTP reads, schemas and public HTTP integration. On 6 November 2026, the bounded smoke check verified route listing and one service-status lookup; arrival tools were not reverified. Live results can change at any time.

To run a bounded live check of routes and one service status:

```sh
uv run python -m tests.omnibus.live_smoke
```
