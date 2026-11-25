# DR-NTU

[Service overview](index.md) · [CLI reference](cli/index.md) · [MCP reference](mcp/index.md)

Search the public DR-NTU research repository, browse collections and inspect publication and dataset metadata. Try `ntu research search "machine learning"`.

## Service notes


Public publication, dataset, and OAI-PMH metadata lookups in the shared `all-abt-ntu-mcp` server. No credentials, keyring, Chromium, or extra dependencies are needed. See the [getting started guide](../../getting-started.md) for installation and MCP client configuration.

All results have `retrieved_at`, `source_url`, and `cached`. Responses are cached in memory for five minutes, with at most 64 entries and 16 MB per REST/OAI client. `refresh: true` refetches the requested response. Each client pools HTTPS connections, permits up to two in-flight reads with 250 ms default request pacing, limits responses to 8 MB, and uses a 20-second timeout. Requests to `researchdata.ntu.edu.sg` are spaced at least 60 seconds apart per process. It retries transient failures once and honors short `Retry-After` delays; longer server-requested delays return an error rather than retrying early. Public HTTP settings are documented in the [shared runtime guide](../../architecture/public-http.md#public-http-reads).

DSpace listings use zero-based `page` and `page_size` from 1–50. Follow `pagination.next_page` until `null`. Total counts remain `null` when the source omits them, as happens with individual search facets. Malformed records or inconsistent result pages fail rather than silently appearing complete.

### Sources

| Endpoint | Purpose |
| --- | --- |
| `https://dr.ntu.edu.sg/server/api/discover/search/objects` | Paginated publication/profile search, scopes, and facet filters |
| `https://dr.ntu.edu.sg/server/api/core/items/{uuid}` | Published item metadata, abstracts, and rights |
| `https://dr.ntu.edu.sg/server/api/core/communities` | Community browsing |
| `https://dr.ntu.edu.sg/server/api/core/collections` | Collection browsing |
| `https://dr.ntu.edu.sg/server/api/core/communities/{uuid}/subcommunities` | Community hierarchy |
| `https://dr.ntu.edu.sg/server/api/core/communities/{uuid}/collections` | Collections within a community |
| `https://dr.ntu.edu.sg/server/api/discover/facets` | Filter definitions |
| `https://dr.ntu.edu.sg/server/api/discover/facets/{name}` | Filter values, counts, and exact query filters |
| `https://dr.ntu.edu.sg/server/api/core/items/{uuid}/bundles` | Item file-group discovery |
| `https://dr.ntu.edu.sg/server/api/core/bundles/{uuid}/bitstreams` | File metadata and content links |
| `https://researchdata.ntu.edu.sg/api/datasets/:persistentId` | Latest dataset metadata with `persistentId=doi:...` |
| `https://researchdata.ntu.edu.sg/api/datasets/:persistentId/versions/{version}` | Explicit published dataset release |
| `https://dr.ntu.edu.sg/server/oai/request` | OAI-PMH Identify, ListMetadataFormats, ListSets, ListRecords, ListIdentifiers, and GetRecord |

### Tests

Offline parsers, pagination, filters, caching, network failures, CAPTCHA/error handling, and MCP schemas use synthetic records:

```sh
uv run python -m unittest discover -s tests/drntu -t . -v
```

Opt-in live stdio checks search pages, publication filtering, item abstracts, browsing, facets and their filters, file discovery, and both dataset version endpoints. Prints statuses and never downloads research file bodies:

```sh
uv run python -m tests.drntu.live_smoke
```

OAI-only live stdio checks exercise all six protocol verbs, provider continuation, date filters, alternate-format XML, empty results, and expired/invalid token errors. Prints statuses and counts without saving or printing research metadata:

```sh
uv run python -m tests.drntu.live_oai_smoke
```

### Limitation

The tools return public metadata and links. Metadata may describe restricted or embargoed content. OAI timestamps describe repository changes, and continuation tokens can expire. CAPTCHA may interrupt dataset lookups. The dataset tool is for individual lookups under the [DR-NTU (Data) terms](https://libguides.ntu.edu.sg/drntudataguidespolicies/TermsOfUse).
