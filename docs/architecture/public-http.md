# Public HTTP reads

Faculty, news, campus services, OneSearch, MazeMap, and DR-NTU use the top-level `public_http_client.py` for pooled public HTTPS reads. Each service keeps a five-minute response cache bounded to 64 entries and 16 MB, reuses connections, limits concurrent requests, and spaces request starts. The client follows only HTTPS redirects to that service's allowlisted hosts, rejects cookies, bounds responses to 8 MB, and makes at most one retry for transient network errors, HTTP 429, or selected 5xx responses. It honors short `Retry-After` delays and returns an error rather than retrying before a longer delay.

Set these variables before starting the server to tune the public-read scheduler:

| Variable | Default | Range | Effect |
| --- | --- | --- | --- |
| `NTU_PUBLIC_HTTP_CONCURRENCY` | `2` | 1–8 | Maximum in-flight requests per host across public service clients in this process |
| `NTU_PUBLIC_HTTP_INTERVAL_SECONDS` | `0.25` | 0–10 | Minimum spacing between request starts to the same host across public service clients in this process |
| `NTU_PUBLIC_HTTP_TIMEOUT_SECONDS` | `20` | 1–120 | Request timeout in seconds |
| `NTU_PUBLIC_HTTP_MAX_RETRY_DELAY_SECONDS` | `10` | 0–30 | Longest provider-requested wait the client will perform before retrying |

These limits are shared by all public clients in this process, grouped by host; hosted replicas keep independent limits. Omnibus and authenticated NTU endpoints use distinct request owners and are not merged into this public client.
