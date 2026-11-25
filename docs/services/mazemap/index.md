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
