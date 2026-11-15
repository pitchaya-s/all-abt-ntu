# NTU Omnibus

[Service overview](index.md) · [CLI reference](cli/index.md) · [MCP reference](mcp/index.md)

Check NTU shuttle routes, stops, arrivals, live vehicles and published schedules. Arrival and vehicle positions are snapshots and may be unavailable or stale.

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
