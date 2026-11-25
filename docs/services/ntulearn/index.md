# NTULearn

[Service overview](index.md) · [CLI reference](cli/index.md) · [MCP reference](mcp/index.md)

Access your enrolled courses, content, attachments, videos, announcements, calendar and grades. Start with `ntu learn courses`; the returned course IDs can be used to browse content. An NTU account and access to the course are required.

## Service notes


These tools run in the shared `all-abt-ntu-mcp` server. See the [getting started guide](../../getting-started.md) for installation, Chromium, and MCP client configuration.

### Sessions

NTULearn reuses a validated session for as long as it can. When it needs a session, it tries these sources in order:

1. **Browser cookies.** By default, NTULearn looks for an existing `BbRouter` cookie in Edge, Chrome, Firefox, Brave, or Safari. Each browser's cookie set is tried separately. To disable discovery for MCP, run `ntu config set ntulearn.browser_cookies false` and restart the server. For direct CLI use, set `NTULEARN_BROWSER_COOKIES=false` in the process environment.
2. **Environment cookie.** Set `NTULEARN_SESSION_COOKIE` in the process environment to a current NTULearn `BbRouter` value. Both the raw value and `BbRouter=<value>` are accepted. Treat it like a password and keep it out of chat, shell command arguments, and configuration files.
3. **Playwright sign-in.** Save an account with `ntu auth save` and install Chromium. If NTU requires an interactive challenge, set `NTULEARN_HEADLESS=false` and run the process where you can use the browser. A rejected password is never retried automatically.

Both cookie sources are validated with NTULearn before use and can work without a saved keyring account. NTULearn uses the account that owns the first valid session. Browser discovery depends on the operating system and access to the local browser profile. The environment cookie is sent only to `ntulearn.ntu.edu.sg`.

For sessions established by Playwright, NTULearn checks the [shared OS keyring](../../architecture/credentials.md#credential-storage) once per data operation. Replacing or revoking the saved account invalidates its session and cache on the next operation. NTULearn keeps authentication state and academic responses in memory. When a session expires, concurrent requests share one recovery attempt.

#### HTTP, cache, and performance settings

NTULearn uses a pooled asynchronous HTTP client for read requests. Multi-course tools run up to four courses at a time, while a shared scheduler limits request concurrency and spaces request starts. 429 and transient 5xx responses are retried with bounded backoff and `Retry-After` when provided. Blackboard and Kaltura file delivery use a separate cookie-free client; NTU cookies are not sent to delivery hosts.

| Environment variable | Default | Allowed range / behavior |
| --- | ---: | --- |
| `NTULEARN_BROWSER_COOKIES` | `true` | `false` skips local browser discovery |
| `NTULEARN_SESSION_COOKIE` | Unset | Optional current `BbRouter` cookie, tried after browser discovery |
| `NTULEARN_HEADLESS` | `true` | `false` shows Chromium for interactive SSO challenges |
| `NTULEARN_CACHE_TTL_SECONDS` | `300` | 0–86400; `0` disables the in-memory response cache |
| `NTULEARN_REQUEST_CONCURRENCY` | `4` | 1–8 shared HTTP requests |
| `NTULEARN_REQUEST_INTERVAL_SECONDS` | `0.1` | 0–5 minimum seconds between request starts |
| `NTULEARN_TIMEOUT_SECONDS` | `30` | 1–120 seconds per HTTP request |

The response cache is separate from authentication, bounded to 128 entries, and scoped to this process. `refresh: true` skips cached data and replaces it with a fresh response. Authentication changes clear the cache. Shutdown closes both HTTP clients and discards in-memory cookies and cached responses.

#### Troubleshooting

- If browser discovery finds no session, confirm you are signed in to NTULearn in a supported browser and that the local profile is accessible. A missing, expired, or rejected cookie advances to the next method.
- If SSO reports that Chromium is unavailable, install the `personal` extra and Chromium using the [main setup guide](../../mcp/index.md#chromium). In a headless environment, MFA or CAPTCHA requires a local visible browser; it is never bypassed.
- If Playwright sign-in needs the keyring, follow [Linux keyring access](../../architecture/credentials.md#linux-keyring-access) or unlock the platform's native keyring.
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

Use `--community-only` on `tests.ntulearn.live_tools_smoke` to check course groups, group members, and mailbox details without downloading files. The probe samples multiple courses because group and messaging availability varies by course.

Live checks use the standard authentication order. They select sample sites from the authenticated membership list, print counts and statuses, and remove temporary downloads. The session smoke test invalidates its in-memory session to exercise recovery.

### Code layout

`mcp.py` holds operation descriptions, input schemas, and registration. `client/` owns sessions and HTTP reads; `parser/` handles response normalization and document text; `services/` implements bounded workflows; `models/` holds typed results grouped by domain. The shared runtime registers these operations alongside STARS and closes both sessions on shutdown.
