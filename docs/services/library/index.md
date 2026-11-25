# Library

[Service overview](index.md) · [CLI reference](cli/index.md) · [MCP reference](mcp/index.md)

Search OneSearch, inspect catalogue records and holdings, or discover library facilities. Public access labels do not guarantee a subscription, a loanable copy or current seat availability.

## Service notes


Catalogue discovery and library facility information in the shared `all-abt-ntu-mcp` server. Public tools need no credentials or API key. Detailed facility schedules use the [shared credential store](../../architecture/credentials.md#credential-storage), also used by STARS and NTULearn, and the optional Chromium installation. See the [getting started guide](../../getting-started.md) for installation and client configuration.

`mcp.py` defines public operations. `personal_tools.py` defines the authenticated facility schedule operation only for the local personal profile; it is unavailable on the hosted public HTTP server. LibFacilities directory parsing, browser sessions, and schedule parsing are grouped under `facilities/`.

Results are typed and include `retrieved_at`, `source_url`, and `cached`. The shared public HTTP client caches responses for five minutes, bounds the cache to 64 entries, pools connections, permits up to two in-flight reads per client with 250 ms default pacing, applies a 20-second timeout, retries transient failures once, and limits each response to 8 MB. Public tools do not access account cookies, the keyring or a browser. Public HTTP settings are documented in the [shared runtime guide](../../architecture/public-http.md#public-http-reads).

### Sources and endpoint choice

The deployment is linked from [NTU Library](https://www.ntu.edu.sg/education/libraries/); see also the [NTU OneSearch guide](https://libguides.ntu.edu.sg/OneSearch).

| Endpoint | Purpose |
| --- | --- |
| `https://ntu-sp.primo.exlibrisgroup.com/primaws/rest/pub/pnxs` | Catalogue search |
| `https://ntu-sp.primo.exlibrisgroup.com/primaws/rest/pub/pnxs/{context}/{record_id}` | Local or central-index record details |
| `https://ntu-sp.primo.exlibrisgroup.com/primaws/rest/pub/edelivery/{record_id}` | Published institutional full-text services and access notes |
| `https://libcalendar.ntu.edu.sg/` | Facility directory and notices |
| `https://libcalendar.ntu.edu.sg/map/{slug}` | Public floor-map configuration |
| `https://libcalendar.ntu.edu.sg/maps/search/spaces` | Public date/time map availability |
| `https://libcalendar.ntu.edu.sg/space/{id}` and `/spaces?lid=…&gid=…` | Authenticated facility descriptions and resource configuration |
| `https://libcalendar.ntu.edu.sg/spaces/availability/grid` | Read-only daily time-grid query |

LibFacilities redirects through `au.libauth.com` to NTU's `loginfs.ntu.edu.sg/adfs/ls/` login. The implementation submits the saved password only to that NTU host using the verified student network-account format, and reuses the resulting session. The time-grid POST is a read query matching the page's request; booking endpoints are not called. OneSearch's separate Microsoft login required MFA during testing, so authenticated OneSearch account access and licensed full-text retrieval are not implemented.

Search parameters include `vid=65NTU_INST:65NTU_INST`, `tab=Everything`, `scope=MyInst_and_CI`, `q={field},{match},{query}`, `limit`, and `offset`. Resource filtering uses `qInclude=facet_rtype,exact,{resource_type}`.

The supplied `/rest/pub/pnxs` and `/rest/external/pnxs` endpoints were compared with an algorithms search, exact ISBN, and an article-filtered machine-learning search. Ordered canonical record IDs and total counts matched in those samples. The first two samples also had identical record payloads; the article comparison differed in some source, facet, ranking, and delivery metadata. This does not prove universal equivalence.

The implementation uses `/pub/pnxs` for search and for both local and central record details.

The [Ex Libris PNX API documentation](https://developers.exlibrisgroup.com/primo/apis/webservices/rest/pnxs/) and [search documentation](https://developers.exlibrisgroup.com/primo/apis/docs/primoSearch/R0VUIC9wcmltby92MS9zZWFyY2g%3D/) explain the general PNX and search conventions.

### Tests

Offline tests use synthetic catalogue and facility responses and cover normalization, query encoding, pagination, canonical IDs, the central adaptor, missing data, conflicting access signals, input rejection, source-status preservation, compact time grids, credential-cache checks, error redaction, and MCP schemas:

```sh
uv run python -m unittest discover -s tests/library -t . -v
```

Opt-in live stdio checks search pages, local and central record details, resource filtering, and ISBN search. Only statuses are printed:

```sh
uv run python -m tests.library.live_smoke
```

To also query a facility schedule using saved local credentials and Chromium:

```sh
uv run --extra personal python -m tests.library.live_smoke --personal
```

Live tests print statuses and counts only; they do not save credentials, bookings or account records.

### Limitation

These deployment-specific endpoints and HTML structures may change. No authenticated OneSearch account, loans, reservations, renewals, licensed file downloads or live copy-level loan checks are implemented. Catalogue and facility statuses are snapshots and may be incomplete or inconsistent. Personal facility reads stop at MFA/CAPTCHA; no bypass is attempted.
