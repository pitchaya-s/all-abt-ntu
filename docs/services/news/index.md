# News

[Service overview](index.md) · [CLI reference](cli/index.md) · [MCP reference](mcp/index.md)

Browse NTU news, filter by category or search published articles. Try `ntu news search "artificial intelligence"`.

## Service notes


Read-only tools for NTU's public news listing and article pages. No credentials or Chromium required.

### Requests and limitations

All results include `retrieved_at`, `source_url`, and `cached`. Responses are cached in memory for five minutes; `refresh: true` fetches them again. The shared public HTTP client pools connections, bounds responses to 8 MB, uses a 20-second timeout, and permits up to two in-flight requests per client with 250 ms default pacing. Public HTTP settings are documented in the [shared runtime guide](../../architecture/public-http.md#public-http-reads). Published news may be corrected or removed; cached results are snapshots.

### Sources

- [NTU news page](https://www.ntu.edu.sg/news/) supplies category labels and IDs, plus the supported sort values.
- [GetStories](https://www.ntu.edu.sg/news/GetStories/?categories=all&page=1&listingKeyword=&sort=latest) returns story cards and pagination. Verified parameters: `categories`, `page`, `listingKeyword`, and `sort`.
- Article URLs returned by the API supply the full published HTML text.

### Tests

Run from the repository root:

```sh
uv run python -m unittest discover -s tests/news -t . -v
uv run python -m tests.news.live_smoke
```

Offline tests use synthetic stories, category forms, and article markup. The opt-in live stdio smoke checks keyword search, categories, pagination, oldest-first ordering, empty results, current and older article text, chunking, and caching. It prints statuses without saving article bodies.
