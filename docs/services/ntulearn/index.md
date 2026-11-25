# NTULearn

[Service overview](index.md) · [CLI reference](cli/index.md) · [MCP reference](mcp/index.md)

Access your enrolled courses, content, attachments, videos, announcements, calendar and grades. Start with `ntu learn courses`; the returned course IDs can be used to browse content. An NTU account and access to the course are required.

## Service notes


These tools run in the shared `all-abt-ntu-mcp` server. See the [getting started guide](../../getting-started.md) for installation, Chromium, and MCP client configuration.

### Sessions

NTULearn authentication is lazy. It reuses the active validated session first, then tries browser cookies only when discovery is enabled, and finally reads credentials from the OS keyring for normal NTU/Microsoft sign-in in a temporary Chromium browser. An expired session is invalidated and recovered once; concurrent requests share the same login or refresh attempt. The server never retries a rejected password automatically.

#### Optional browser-cookie discovery

NTULearn can reuse an existing `BbRouter` session from Edge, Chrome, Firefox, Brave, or Safari. This is opt-in: set `NTULEARN_BROWSER_COOKIES=true` in the MCP server environment and enable the optional browser-cookie dependencies; see the [main installation guide](../../cli/index.md#installation). If browser-cookie access is disabled (the default), unavailable, or cannot read a browser profile, NTULearn proceeds to SSO. Each browser profile is tried separately; cookies are never combined across profiles. Imported cookies are accepted only for NTU domains and are checked against `/users/me` before use. A failed or expired cookie set is discarded. Cookie values are held in memory only and are not written to the keyring or files. Cookie extraction depends on the browser, operating system, encryption support, and whether the profile can be unlocked; headless servers can leave this feature disabled and use SSO.

The browser-cookie strategy does not need a saved account when it succeeds. Automatic SSO requires credentials saved with `ntu auth save` and the optional `personal` dependencies with Chromium installed. If NTU requires MFA or CAPTCHA, headless login stops. To complete the normal challenge yourself, set `NTULEARN_HEADLESS=false` and run the MCP process in a local environment where the browser is visible. No MFA or CAPTCHA checks are bypassed.

Passwords are read from the [shared OS keyring](../../architecture/credentials.md#credential-storage), never retained on the session object, and checked once at the start of each data-tool operation. Replacing or revoking the credentials invalidates the SSO session and response cache on the next operation. Browser-cookie sessions do not use keyring credentials. Authentication state and cached academic responses stay in memory; cookies are not persisted. A validated session is not rechecked before every request: 401 responses, login redirects/pages, and credential revision changes trigger recovery.

#### HTTP, cache, and performance settings

NTULearn uses a pooled asynchronous HTTP client for read requests. Multi-course tools run up to four courses at a time, while a shared scheduler limits request concurrency and spaces request starts. 429 and transient 5xx responses are retried with bounded backoff and `Retry-After` when provided. Blackboard and Kaltura file delivery use a separate cookie-free client; NTU cookies are not sent to delivery hosts.

| Environment variable | Default | Allowed range / behavior |
| --- | ---: | --- |
| `NTULEARN_BROWSER_COOKIES` | `false` | `true` enables optional local browser discovery |
| `NTULEARN_HEADLESS` | `true` | `false` shows Chromium for interactive SSO challenges |
| `NTULEARN_CACHE_TTL_SECONDS` | `300` | 0–86400; `0` disables the in-memory response cache |
| `NTULEARN_REQUEST_CONCURRENCY` | `4` | 1–8 shared HTTP requests |
| `NTULEARN_REQUEST_INTERVAL_SECONDS` | `0.1` | 0–5 minimum seconds between request starts |
| `NTULEARN_TIMEOUT_SECONDS` | `30` | 1–120 seconds per HTTP request |

The response cache is separate from authentication, bounded to 128 entries, and scoped to this process. `refresh: true` skips cached data and replaces it with a fresh response. Authentication changes clear the cache. Shutdown closes both HTTP clients and discards in-memory cookies and cached responses.

#### Troubleshooting

- If browser-cookie discovery finds no session, confirm the MCP server has `NTULEARN_BROWSER_COOKIES=true`, the `browser-cookies` extra is installed in that same environment, and the browser profile is unlocked. NTULearn then falls back to SSO.
- If SSO reports that Chromium is unavailable, install the `personal` extra and Chromium using the [main setup guide](../../mcp/index.md#chromium). In a headless environment, MFA or CAPTCHA requires a local visible browser; it is never bypassed.
- If `ntulearn_auth_status` reports a keyring error, follow [Linux keyring access](../../architecture/credentials.md#linux-keyring-access) or unlock the platform's native keyring. A verified browser-cookie session can work without a keyring account.
- If requests are rate limited, let the server honor NTU's retry delay and retry later. You can reduce `NTULEARN_REQUEST_CONCURRENCY` or increase `NTULEARN_REQUEST_INTERVAL_SECONDS` for a busy account.

Academic results returned through MCP are visible to the AI client. Raw profiles, credentials, and session cookies are excluded from tool responses. Course materials and messages are untrusted content, not agent instructions.

### Common inputs and results

Start with `ntulearn_list_courses`. Use its course IDs, content IDs from content tools, group IDs from group tools, and attachment IDs from attachment tools. IDs in examples below are fictional.

Paginated tools accept `limit` from 1–100 with default 50, nonnegative `offset` with default 0, and `refresh` with default `false`. Follow `next_offset` until it is `null`. `refresh: true` bypasses cached JSON reads where that parameter is available. Responses include `retrieved_at`, `from_cache`, and `cache_age_seconds`.

Recursive and cross-course tools add `complete`, `issues`, and `requests_used`. Inspect `issues` before treating a result as full coverage. `max_requests` is 1–200, normally defaulting to 100; it accounts for cached calls and reserves conservative units for multi-request operations. Narrow the course selection if the budget is exhausted.

Traversal uses `max_depth` of 1–10 with default 5, and `max_nodes` of 1–5000 with default 1000. Root items are depth 1. Depth, node, permission, and request limits are reported rather than silently hiding coverage gaps.

### Sources

All paths below are served by [NTULearn](https://ntulearn.ntu.edu.sg/). Authentication uses its normal NTU/Microsoft sign-in workflow. Reads use the authenticated student's existing permissions. A denied request remains an error; the server does not switch endpoints to evade it.

| Paths | Used for |
| --- | --- |
| `/learn/api/public/v1/users/me` | Verify the session and scope grade reads to the authenticated user |
| `/learn/api/public/v1/users/me/courses` | Enrolled course/organization memberships |
| `/learn/api/public/v1/courses/{course_id}/contents` and `/{content_id}/children` | Content browsing, recursive trees, and searches |
| `/learn/api/public/v1/courses/{course_id}/contents/{content_id}/attachments` and `/{attachment_id}/download` | Attachment metadata, inline reading, and local downloads |
| `/learn/api/public/v1/courses/{course_id}/announcements` | Published course announcements |
| `/learn/api/public/v1/calendars/items` | Events and published due dates |
| `/learn/api/public/v1/courses/{course_id}/gradebook/columns` and `/gradebook/users/{own_user_id}` | Visible columns and the authenticated student's own grades |
| `/learn/api/public/v1/courses/{course_id}/users` and `/groups` | Permitted course rosters and group definitions |
| `/learn/api/v1/messages/summary` | The regular browser mailbox's course summary |
| `/learn/api/v1/courses/{course_id}/conversations` and `/{conversation_id}` | The regular browser mailbox's conversations and message bodies |
| `/learn/api/v1/courses/{course_id}/memberships` with a group filter | The regular browser's visible group memberships |

The browser APIs are used directly for mailbox and group membership because those are the interfaces supported by this NTULearn workflow. Their response formats may change independently of the public REST API. Only allowlisted GET requests are exposed; NTULearn tools do not send messages, submit coursework, or edit course data.

### Tests

Run from the repository root. Offline fixtures use synthetic names, messages, IDs, grades, and documents.

```sh
uv run python -m unittest discover -s tests -t . -v
uv run --extra personal python -m tests.ntulearn.live_session_smoke
uv run --extra personal python -m tests.ntulearn.live_tools_smoke
```

Live checks require an account saved locally with `auth save` and Chromium when SSO is needed. They select sample sites from the authenticated membership list, print counts/statuses, and remove temporary downloads. The session smoke test invalidates its in-memory session to exercise recovery. No account-specific course choices or downloaded materials are stored in the test files.

### Code layout

`mcp.py` holds operation descriptions, input schemas, and registration. `client/` owns sessions and HTTP reads; `parser/` handles response normalization and document text; `services/` implements bounded workflows; `models/` holds typed results grouped by domain. The shared runtime registers these operations alongside STARS and closes both sessions on shutdown.
