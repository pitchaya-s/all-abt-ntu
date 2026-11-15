# Faculty

[Service overview](index.md) · [CLI reference](cli/index.md) · [MCP reference](mcp/index.md)

Search the public faculty directory by name or research interest. Run `ntu faculty interests` to discover the available interest filters.

## Service notes


Public, read-only access to NTU's faculty directory. No credentials or Chromium are needed.

### Requests and caching

Both tools include `retrieved_at`, `source_url`, and `cached`. Responses stay in memory for five minutes; `refresh: true` fetches them again. Requests use the shared pooled HTTP client with an 8 MB response bound, a 20-second timeout, up to two in-flight reads per client, and 250 ms default pacing. Public HTTP settings are documented in the [shared runtime guide](../../architecture/public-http.md#public-http-reads). Unexpected JSON, changed form structure, inconsistent pagination, and access denials return errors.

The directory covers profiles NTU publishes here; it does not establish a complete employee list, current employment, supervision availability, or contact responsiveness. No full profile pages are fetched.

### Sources

- [Faculty directory](https://www.ntu.edu.sg/research/faculty-directory/) supplies current research-interest IDs and labels.
- [GetAcademicProfiles](https://www.ntu.edu.sg/research/faculty-directory/GetAcademicProfiles/?interests=all&page=1&searchFaculty=) supplies JSON profile cards and pagination. Parameters: `searchFaculty`, `interests` set to `all` or one returned interest ID, and `page` starting at 1.

### Tests

Run from the repository root:

```sh
uv run python -m unittest discover -s tests/faculty -t . -v
uv run python -m tests.faculty.live_smoke
```

Offline tests use synthetic profiles and form options. The opt-in live stdio smoke checks name search, pagination, no matches, interest filtering, and cache reuse. It prints statuses and saves no profiles.
