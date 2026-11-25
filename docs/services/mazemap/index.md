# MazeMap

[Service overview](index.md) · [CLI reference](cli/index.md) · [MCP reference](mcp/index.md)

Find campus buildings, rooms and amenities, or get walking directions between place IDs. Try `ntu map search "LT1"`; map data does not establish that a room is available or accessible at a particular time.

## Service notes


Public campus lookups in the shared `all-abt-ntu-mcp` server. No credentials, keyring, Chromium, or additional dependencies are needed. See the [getting started guide](../../getting-started.md) for installation and MCP client configuration.

All tools return typed structured results with `retrieved_at`, `source_url`, and `cached`. Responses use the shared in-memory cache, bounded to 64 entries for five minutes. Set `refresh: true` to refetch the requested data. Pooled HTTPS connections support up to two in-flight reads per client, with request starts paced at 250 ms by default and one retry for transient failures. Public HTTP settings are documented in the [shared runtime guide](../../architecture/public-http.md#public-http-reads). There is no background map download.

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

Provider documentation: [search](https://mazemap.atlassian.net/wiki/spaces/MCSH/pages/3761668097/Developers+Guide+Search+-+JS+SDK), [v2 routing](https://mazemap.atlassian.net/wiki/spaces/MCSH/pages/3304685834/Supplementary+Guide+for+Version+2+Routing+in+MazeMap+JS+API). The [older Data API reference](https://github.com/MazeMap/Data-API) is deprecated.

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
