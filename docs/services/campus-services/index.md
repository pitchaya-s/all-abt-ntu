# Campus Services

[Service overview](index.md) · [CLI reference](cli/index.md) · [MCP reference](mcp/index.md)

Find campus food outlets, shops, clinics and other services. Run `ntu services filters` for the published type and category IDs.

## Service notes


Read-only access to NTU's published food, retail, clinic, and service directory. No credentials or Chromium required.

### Requests and limitations

Results include `retrieved_at`, `source_url`, and `cached`. Pages are cached in memory for five minutes. For a collected directory, `retrieved_at` is the oldest page timestamp, `cached` is true only when every result page came from cache, and `source_url` identifies the first page. `refresh: true` fetches every page again.

The shared public HTTP client pools connections, bounds responses to 8 MB, uses a 20-second timeout, and permits up to two in-flight requests per client with 250 ms default pacing. Later directory pages are fetched with bounded concurrency, and results remain in source page order. Subsequent searches reuse cached pages. Public HTTP settings are documented in the [shared runtime guide](../../architecture/public-http.md#public-http-reads). Published hours, contact information, and map links can become outdated; the directory does not establish live opening, occupancy, accessibility, or booking availability.

### Sources

- [NTU general directory](https://www.ntu.edu.sg/life-at-ntu/leisure-and-dining/general-directory/) supplies filter labels and IDs.
- [GetLocations](https://www.ntu.edu.sg/life-at-ntu/leisure-and-dining/general-directory/GetLocations/) returns location cards, twelve per page. Verified parameters: `page`, `locationTypes`, and `locationCategories`. The tested `listingKeyword` parameter was ignored; keyword and address matching are therefore local.

### Tests

Run from the repository root:

```sh
uv run python -m unittest discover -s tests/service -t . -v
uv run python -m tests.service.live_smoke
```

Synthetic offline fixtures cover later-page keyword matches, source taxonomy gaps, address filtering, result pagination, missing contact fields, changing/malformed responses, and MCP schemas and errors. The opt-in live stdio smoke checks complete directory retrieval, keyword and location searches, a working source filter, pagination, and caching. It prints statuses without saving directory records.
