# NTULearn: Courses, content and search MCP tools

[Service overview](../index.md) · [CLI reference](../cli/index.md) · [All MCP tools](index.md) · [Data types](types.md)

## Courses, content and search

Inputs are required only where marked. A required output field may still be `null` if its type allows it. See [data types](types.md) for nested objects.

### `ntulearn_search_course_content`

Recursively search one course's content titles, body and description for a case-insensitive substring. Results include course_id and breadcrumbs. Does not search inside attachment bytes. Bounded or denied folders are reported in issues.

**Inputs:** `course_id`, a nonblank `query` of 1–200 characters; optional traversal limits, `max_results` of 1–200 with default 50, request budget, and refresh.

**Returns:** case-insensitive substring matches in titles, body, and description. Each match includes `course_id`, `content_id`, title, breadcrumb, and an excerpt. It does not search attachment bytes.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_id` | `string` | Yes | Blackboard course ID or enrolled course code; pattern: `^[A-Za-z0-9_-]{1,80}$` |
| `query` | `string` | Yes | minimum length: `1`; maximum length: `200` |
| `max_depth` | `integer` | No | minimum: `1`; maximum: `10`; default: `5` |
| `max_nodes` | `integer` | No | minimum: `1`; maximum: `5000`; default: `1000` |
| `max_results` | `integer` | No | minimum: `1`; maximum: `200`; default: `50` |
| `max_requests` | `integer` | No | minimum: `1`; maximum: `200`; default: `100` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `from_cache` | `boolean` | Yes | — |
| `cache_age_seconds` | `integer` | Yes | — |
| `complete` | `boolean` | Yes | — |
| `requests_used` | `integer` | Yes | — |
| `issues` | array of [`Issue`](types.md#mcp-type-issue) | Yes | — |
| `query` | `string` | Yes | — |
| `courses_searched` | array of `string` | Yes | — |
| `matches` | array of [`ContentMatch`](types.md#mcp-type-contentmatch) | Yes | — |

### `ntulearn_search_all_courses`

Recursively search content across available enrolled courses, or selected course_ids. Each result carries course_id and breadcrumb. max_nodes and max_requests apply to the whole search. Check complete/issues for coverage.

**Inputs:** `query`; optional `course_ids` of 1–100 IDs; the same search/traversal controls as `ntulearn_search_course_content`.

**Returns:** attributed matches across available enrolled course sites, excluding known organizations, or across the explicitly selected sites. Node and request budgets apply to the whole search. `courses_searched` records the sites visited.

```json
{"query":"assessment","course_ids":["_100_1","_101_1"],"max_depth":4,"max_results":20}
```

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `query` | `string` | Yes | minimum length: `1`; maximum length: `200` |
| `course_ids` | array of `string` or `null` | No | default: `null`; minimum items: `1`; maximum items: `100` |
| `max_depth` | `integer` | No | minimum: `1`; maximum: `10`; default: `5` |
| `max_nodes` | `integer` | No | minimum: `1`; maximum: `5000`; default: `1000` |
| `max_results` | `integer` | No | minimum: `1`; maximum: `200`; default: `50` |
| `max_requests` | `integer` | No | minimum: `1`; maximum: `200`; default: `100` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `from_cache` | `boolean` | Yes | — |
| `cache_age_seconds` | `integer` | Yes | — |
| `complete` | `boolean` | Yes | — |
| `requests_used` | `integer` | Yes | — |
| `issues` | array of [`Issue`](types.md#mcp-type-issue) | Yes | — |
| `query` | `string` | Yes | — |
| `courses_searched` | array of `string` | Yes | — |
| `matches` | array of [`ContentMatch`](types.md#mcp-type-contentmatch) | Yes | — |

### `ntulearn_auth_status`

Report the latest verified session. Cookie sessions skip the keyring check.

**Inputs:** none. Does not log in or require configured credentials.

**Returns:** `credentials_configured`, `credential_storage` of `os_keyring`, a sanitized `credential_error` when unavailable, `session_verified`, `authentication_method`, `last_verified_at`, in-memory session storage mode, and cache TTL. A verified session can still expire between reads.

`credentials_configured` is `true` when the stored account is readable, `false` when the keyring has no saved account, and `null` when the keyring was skipped or unavailable. Use `ntu auth status` to check the keyring directly. See [Linux keyring troubleshooting](../../../architecture/credentials.md#linux-keyring-access) if keyring access differs between the terminal and MCP.

**Inputs**

None.

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `credentials_configured` | `boolean` or `null` | Yes | — |
| `credential_storage` | `"os_keyring"` | No | default: `"os_keyring"` |
| `credential_error` | `string` or `null` | No | default: `null` |
| `session_verified` | `boolean` | Yes | — |
| `authentication_method` | `"browser_cookie"`, `"environment_cookie"`, `"sso"` or `null` | No | default: `null` |
| `last_verified_at` | `string` or `null` | Yes | format: `date-time` |
| `session_storage` | `"in_memory_only"` | No | default: `"in_memory_only"` |
| `cache_ttl_seconds` | `integer` | Yes | — |

### `ntulearn_list_courses`

List your enrolled NTULearn courses and organizations, including published availability and course IDs.

**Inputs:** common pagination and refresh parameters.

**Returns:** enrolled course and organization memberships with `id`, `course_code`, `name`, availability, role, and organization flag when NTU provides them. Available memberships may include older sites and training; availability does not establish current-semester registration.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `limit` | `integer` | No | minimum: `1`; maximum: `100`; default: `50` |
| `offset` | `integer` | No | minimum: `0`; default: `0` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `from_cache` | `boolean` | Yes | — |
| `cache_age_seconds` | `integer` | Yes | — |
| `courses` | array of [`Course`](types.md#mcp-type-course) | Yes | — |
| `offset` | `integer` | Yes | — |
| `next_offset` | `integer` or `null` | Yes | — |

### `ntulearn_get_course_contents`

Read one level of course content. Omit parent_id for the root; use an item's ID to open a folder. HTML body/description are returned as text.

**Inputs:** `course_id`; optional `parent_id`; common pagination and refresh parameters. Omit `parent_id` for the root, or use a returned folder ID to open it.

**Returns:** one level of content with IDs, titles, parent IDs, child flags, handler type, body/description as text, and modified timestamps when available.

```json
{"course_id":"_100_1","parent_id":"_200_1","limit":50}
```

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_id` | `string` | Yes | Blackboard course ID or enrolled course code; pattern: `^[A-Za-z0-9_-]{1,80}$` |
| `parent_id` | `string` or `null` | No | default: `null`; NTULearn ID returned by another tool; pattern: `^[A-Za-z0-9_-]{1,80}$` |
| `limit` | `integer` | No | minimum: `1`; maximum: `100`; default: `50` |
| `offset` | `integer` | No | minimum: `0`; default: `0` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `from_cache` | `boolean` | Yes | — |
| `cache_age_seconds` | `integer` | Yes | — |
| `course_id` | `string` | Yes | — |
| `contents` | array of [`Content`](types.md#mcp-type-content) | Yes | — |
| `offset` | `integer` | Yes | — |
| `next_offset` | `integer` or `null` | Yes | — |

### `ntulearn_get_content_tree`

Read a course's nested content tree. Root items are depth 1; max_depth is at most 10. Unopened, denied or cyclic branches are explicit; complete=false means the tree is partial.

**Inputs:** `course_id`; optional `max_depth`, `max_nodes`, `max_requests`, and `refresh`.

**Returns:** nested content nodes with `children` and `children_complete`. An unopened or denied branch is marked explicitly. `complete: false` means the full requested tree was not retrieved.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_id` | `string` | Yes | Blackboard course ID or enrolled course code; pattern: `^[A-Za-z0-9_-]{1,80}$` |
| `max_depth` | `integer` | No | minimum: `1`; maximum: `10`; default: `5` |
| `max_nodes` | `integer` | No | minimum: `1`; maximum: `5000`; default: `1000` |
| `max_requests` | `integer` | No | minimum: `1`; maximum: `200`; default: `100` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `from_cache` | `boolean` | Yes | — |
| `cache_age_seconds` | `integer` | Yes | — |
| `complete` | `boolean` | Yes | — |
| `requests_used` | `integer` | Yes | — |
| `issues` | array of [`Issue`](types.md#mcp-type-issue) | Yes | — |
| `course_id` | `string` | Yes | — |
| `contents` | array of [`ContentNode`](types.md#mcp-type-contentnode) | Yes | — |
| `max_depth` | `integer` | Yes | — |
