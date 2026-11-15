# NTU MazeMap tools

[CLI commands](#cli-commands) · [MCP tools](#mcp-tools) · [MCP data types](#mcp-data-types) · [Service notes](#service-notes)

For installation and shared authentication, see the [main README](../../README.md).

## CLI commands

The output column lists the JSON result fields; human-readable output is formatted for the terminal. Use `ntu map --help` and append `--help` to a command for option details. `VALUE` denotes an option value; required arguments and options are marked. See the [complete CLI reference](../COMMANDS.md) for shared settings and all services.

| Command | Arguments and options | Purpose | Output |
| --- | --- | --- | --- |
| `ntu map campuses` | `--refresh/-r`, `--json/-j` | List campuses in NTU's MazeMap collection with IDs and center coordinates. | `retrieved_at`, `source_url`, `cached`, `campuses` ([schema](#mazemap_list_campuses)) |
| `ntu map buildings` | `--campus VALUE (default: 2123)`, `--query VALUE`, `--refresh/-r`, `--json/-j` | List campus buildings and their floor IDs/names/levels. | `retrieved_at`, `source_url`, `cached`, `campus_id`, `buildings` ([schema](#mazemap_list_buildings)) |
| `ntu map search` | `QUERY (required)`, `--campus VALUE`, `--limit/-l VALUE (default: 10)`, `--offset VALUE`, `--refresh/-r`, `--json/-j` | Search NTU rooms, venues and amenities by code, name or category, including aliases such as TR+7. | `retrieved_at`, `source_url`, `cached`, `query`, `places`, `next_offset` ([schema](#mazemap_search_places)) |
| `ntu map place` | `POI_ID (required)`, `--refresh/-r`, `--json/-j` | Read one NTU place's location, aliases, building, floor, categories and published description/capacity. | `retrieved_at`, `source_url`, `cached`, `place` ([schema](#mazemap_get_place)) |
| `ntu map directions` | `FROM_POI_ID (required)`, `TO_POI_ID (required)`, `--constraint VALUE [NO_CONSTRAINT, PREFER_ACCESSIBLE, REQUIRE_ACCESSIBLE] (default: NO_CONSTRAINT)`, `--refresh/-r`, `--accessible`, `--json/-j` | Get walking routes between two NTU POIs, estimated metres/seconds and English instructions where available. | `retrieved_at`, `source_url`, `cached`, `from_poi_id`, `to_poi_id`, `constraint`, `routes`, `buildings`, `floors` ([schema](#mazemap_get_directions)) |

## MCP tools

Inputs are required only where marked. Output fields marked required may still be `null` when their type allows it. See the nested data types below for object fields.

### `mazemap_list_campuses`

List campuses in NTU's MazeMap collection with IDs and center coordinates.

List NTU collection campuses with `campus_id`, name, and center coordinates. Accepts optional `refresh`. Main Campus is `2123`; other campus IDs are discovered from the collection rather than hardcoded.

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
| `campuses` | array of [`Campus`](#mcp-type-campus) | Yes | — |

Unknown fields are not accepted.

### `mazemap_list_buildings`

List campus buildings and their floor IDs/names/levels. Defaults to NTU Main Campus. Optionally filter by building-name substring.

Inputs: optional `campus_id`, default `2123`; optional `query` to filter building names by a case-insensitive substring; optional `refresh`.

Returns buildings with their floor IDs, printed names, and numeric levels. Floor names and levels can differ. A building with no published floors returns an empty floor list. Large polygon coordinates are omitted.

```json
{"campus_id": 2123, "query": "North Spine"}
```

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `campus_id` | `integer` | No | Numeric ID returned by a MazeMap tool; greater than: `0`; default: `2123` |
| `query` | `string` or `null` | No | default: `null`; minimum length: `1`; maximum length: `200` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `campus_id` | `integer` | Yes | — |
| `buildings` | array of [`Building`](#mcp-type-building) | Yes | — |

Unknown fields are not accepted.

### `mazemap_search_places`

Search NTU rooms, venues and amenities by code, name or category, including aliases such as TR+7. Defaults to all NTU campuses; use campus_id to narrow. Follow next_offset for more matches. This is place search, not room availability.

Inputs: `query`, optional `campus_id`, `limit` from 1–50, default 10; `offset` from 0–10000, default 0; optional `refresh`.

Searches rooms, venues, and amenities using MazeMap's ranked search, including room aliases. Without a campus ID it searches the `ntu-sg` collection. Results include POI and campus IDs, name, identifier, aliases, building, floor, categories, coordinates, and a map link. Missing descriptions or capacities remain `null`.

Follow `next_offset` until it is `null`. The client requests one extra match to determine whether another page exists. Results are search matches, not a complete campus room inventory. Multiple buildings may use the same tutorial-room number; select the appropriate result before routing.

```json
{"query": "TR+7", "campus_id": 2123, "limit": 5}
```

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `query` | `string` | Yes | minimum length: `1`; maximum length: `200` |
| `campus_id` | `integer` or `null` | No | default: `null`; Numeric ID returned by a MazeMap tool; greater than: `0` |
| `limit` | `integer` | No | minimum: `1`; maximum: `50`; default: `10` |
| `offset` | `integer` | No | minimum: `0`; maximum: `10000`; default: `0` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `query` | `string` | Yes | — |
| `places` | array of [`Place`](#mcp-type-place) | Yes | — |
| `next_offset` | `integer` or `null` | Yes | — |

Unknown fields are not accepted.

### `mazemap_get_place`

Read one NTU place's location, aliases, building, floor, categories and published description/capacity. Missing fields remain null.

Inputs: `poi_id`, optional `refresh`.

Returns one place's published details, including description and capacity where supplied. Deleted places, mismatched IDs, and places outside NTU are rejected.

```json
{"poi_id": 1002362545}
```

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `poi_id` | `integer` | Yes | Numeric ID returned by a MazeMap tool; greater than: `0` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `place` | [`Place`](#mcp-type-place) | Yes | — |

Unknown fields are not accepted.

### `mazemap_get_directions`

Get walking routes between two NTU POIs, estimated metres/seconds and English instructions where available. Choose REQUIRE_ACCESSIBLE to request only accessible paths. Accessibility and travel times do not guarantee current physical access.

Inputs: `from_poi_id`, `to_poi_id`; optional `constraint`, one of `NO_CONSTRAINT`, `PREFER_ACCESSIBLE`, or `REQUIRE_ACCESSIBLE`; optional `refresh`.

Both POIs must belong to NTU. Returns route alternatives, distance in metres, estimated duration in seconds, English directions when available, and referenced building/floor information. Distance is summed from the published basic path steps; duration comes from MazeMap's route estimate. Accessibility and uncertain-segment flags remain unknown when the source omits them. Missing directions for any leg are reported in `issues`, and `instructions` is `null` rather than presenting an incomplete instruction list as the whole route.

```json
{"from_poi_id": 1002362545, "to_poi_id": 1002362569, "constraint": "REQUIRE_ACCESSIBLE"}
```

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `from_poi_id` | `integer` | Yes | Numeric ID returned by a MazeMap tool; greater than: `0` |
| `to_poi_id` | `integer` | Yes | Numeric ID returned by a MazeMap tool; greater than: `0` |
| `constraint` | `"NO_CONSTRAINT"`, `"PREFER_ACCESSIBLE"`, `"REQUIRE_ACCESSIBLE"` | No | default: `"NO_CONSTRAINT"` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `from_poi_id` | `integer` | Yes | — |
| `to_poi_id` | `integer` | Yes | — |
| `constraint` | `string` | Yes | — |
| `routes` | array of [`Route`](#mcp-type-route) | Yes | — |
| `buildings` | array of [`RouteBuilding`](#mcp-type-routebuilding) | Yes | — |
| `floors` | array of [`RouteFloor`](#mcp-type-routefloor) | Yes | — |

Unknown fields are not accepted.

## MCP data types

These named types are used by the tool input and output fields above.

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

## Service notes

Public campus lookups in the shared `all-abt-ntu-mcp` server. No credentials, keyring, Chromium, or additional dependencies are needed. See the [main README](../../README.md) for installation and MCP client configuration.

All tools return typed structured results with `retrieved_at`, `source_url`, and `cached`. Responses use the shared in-memory cache, bounded to 64 entries for five minutes. Set `refresh: true` to refetch the requested data. Pooled HTTPS connections support up to two in-flight reads per client, with request starts paced at 250 ms by default and one retry for transient failures. Public HTTP settings are documented in the [shared runtime guide](../shared/README.md#public-http-reads). There is no background map download.

### Sources

| Endpoint | Used for |
| --- | --- |
| `https://api.mazemap.com/api/campuscollection/ntu-sg/?withcampuses=true` | NTU campus discovery and scope validation |
| `https://api.mazemap.com/api/buildings/?campusid=2123&srid=4326` | Building names and floor metadata |
| `https://search.mazemap.com/search/equery/` | Ranked, paginated place search scoped with `campuscollectiontag=ntu-sg` |
| `https://api.mazemap.com/api/pois/{poi_id}/?srid=4326` | Place details and routing endpoint validation |
| `https://routing.mazemap.com/routing/v2/a-to-b/` | Walking routes with `campusCollectionTag=ntu-sg`, English text, and metric units |

The supplied campus information, single-building, POI-type, floor-outline, and web configuration endpoints were also inspected. Their useful metadata is already supplied by collection/building/place responses, while polygon data and web application settings are unnecessary for these tools.

The bulk campus POI endpoint returned 2,000 entries and a limit of 2,000. Its `zlevel=1` response included rooms on other levels. The integration uses the dedicated search service instead of treating that bulk response as complete or correctly floor-filtered.

Provider documentation: [search](https://mazemap.atlassian.net/wiki/spaces/MCSH/pages/3761668097/Developers+Guide+Search+-+JS+SDK), [v2 routing](https://mazemap.atlassian.net/wiki/spaces/MCSH/pages/3304685834/Supplementary+Guide+for+Version+2+Routing+in+MazeMap+JS+API). The [older Data API reference](https://github.com/MazeMap/Data-API) is marked deprecated; current response shapes were checked directly over HTTPS.

### Tests

Offline parser, request, cache, failure, and stdio schema tests use synthetic map fixtures:

```sh
uv run python -m unittest discover -s tests/mazemap -t . -v
```

Opt-in live smoke test makes public HTTP requests through the stdio MCP server and prints only statuses:

```sh
uv run python -m tests.mazemap.live_smoke
```

### Limitation

Search is ranked and bounded; no exhaustive room inventory or free-room search is provided. Directions and accessibility depend on published map data and may differ from current access, closures, or lift operation. Maps do not indicate actual occupancy. These tools do not join maps with STARS class schedules.
