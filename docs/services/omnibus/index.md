# NTU Omnibus

[Service overview](index.md) · [CLI reference](cli/index.md) · [MCP reference](mcp/index.md)

Check NTU shuttle routes, stops, arrivals, live vehicles and published schedules. Arrival and vehicle positions are snapshots and may be unavailable or stale.

## Service notes


Data comes from the public [NTU Omnibus app](https://apps.ntu.edu.sg/NTUOmnibus/). No NTU account is needed. Responses include the source and retrieval time. Stop data can be cached for five minutes. Positions, arrival estimates, and service status are fetched on request.

Route path geometry is outside the current tool outputs. A missing vehicle or arrival in a snapshot does not establish that a route is not operating.

Stop and arrival results list any queried routes for which Omnibus supplied no stops. In JSON and MCP, this is `routes_without_stop_data`.

### Checks

Synthetic tests cover native route IDs and input flags, stop-cache reuse and expiry, cache isolation and concurrent reads, fresh arrival estimates, per-source arrival lookups, missing estimates, result limits, endpoint discovery, CSRF recovery, bounded HTTP reads, schemas and public HTTP integration. Live results can change at any time.

To run a bounded live check of routes, service status, and sample stops and arrivals:

```sh
uv run python -m tests.omnibus.live_smoke
```
