# MazeMap: MCP reference

[Service overview](../index.md) · [CLI reference](../cli/index.md) · [MCP reference](index.md)

## Tools

Inputs are required only where marked. Output fields marked required may still be `null` when their type allows it. See the [data types](types.md) for object fields.

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
| `campuses` | array of [`Campus`](types.md#mcp-type-campus) | Yes | — |

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
| `buildings` | array of [`Building`](types.md#mcp-type-building) | Yes | — |

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
| `places` | array of [`Place`](types.md#mcp-type-place) | Yes | — |
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
| `place` | [`Place`](types.md#mcp-type-place) | Yes | — |

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
| `routes` | array of [`Route`](types.md#mcp-type-route) | Yes | — |
| `buildings` | array of [`RouteBuilding`](types.md#mcp-type-routebuilding) | Yes | — |
| `floors` | array of [`RouteFloor`](types.md#mcp-type-routefloor) | Yes | — |

Unknown fields are not accepted.

See the [MCP data types](types.md) for nested object fields.
