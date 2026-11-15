# NTULearn tool guide

[CLI commands](#cli-commands) · [MCP tools](#mcp-tools) · [MCP data types](#mcp-data-types) · [Service notes](#service-notes)

For installation and shared authentication, see the [main README](../../README.md).

## CLI commands

The output column lists the JSON result fields; human-readable output is formatted for the terminal. Use `ntu learn --help` and append `--help` to a command for option details. `VALUE` denotes an option value; required arguments and options are marked. See the [complete CLI reference](../COMMANDS.md) for shared settings and all services.

| Command | Arguments and options | Purpose | Output |
| --- | --- | --- | --- |
| `ntu learn attachments` | `COURSE_ID (required)`, `CONTENT_ID (required)`, `--limit/-l VALUE (default: 50)`, `--offset VALUE`, `--refresh/-r`, `--json/-j` | List files attached to a course content item. | `retrieved_at`, `from_cache`, `cache_age_seconds`, `course_id`, `content_id`, `attachments`, `offset`, `next_offset` ([schema](#ntulearn_get_content_attachments)) |
| `ntu learn announcements` | `COURSE_ID (required)`, `--limit/-l VALUE (default: 50)`, `--offset VALUE`, `--refresh/-r`, `--json/-j` | Read published announcements for one enrolled course. | `retrieved_at`, `from_cache`, `cache_age_seconds`, `course_id`, `announcements`, `offset`, `next_offset` ([schema](#ntulearn_get_announcements)) |
| `ntu learn grades` | `COURSE_ID (required)`, `--limit/-l VALUE (default: 50)`, `--offset VALUE`, `--grades-offset VALUE`, `--refresh/-r`, `--json/-j` | Read visible gradebook columns and your own scores/status. | `retrieved_at`, `from_cache`, `cache_age_seconds`, `course_id`, `columns`, `grades`, `offset`, `next_offset`, `grades_next_offset`, `grades_offset` ([schema](#ntulearn_get_gradebook)) |
| `ntu learn calendar` | `--since VALUE`, `--until VALUE`, `--course VALUE`, `--limit/-l VALUE (default: 50)`, `--offset VALUE`, `--refresh/-r`, `--json/-j` | Read calendar entries and published deadlines, across your courses or for one course. | `retrieved_at`, `from_cache`, `cache_age_seconds`, `since`, `until`, `items`, `offset`, `next_offset` ([schema](#ntulearn_get_calendar)) |
| `ntu learn upcoming` | `--since VALUE`, `--until VALUE`, `--course-ids VALUE`, `--item-type VALUE`, `--max-requests VALUE (default: 100)`, `--refresh/-r`, `--json/-j` | Collect all calendar pages across your enrolled courses. | `retrieved_at`, `from_cache`, `cache_age_seconds`, `complete`, `requests_used`, `issues`, `since`, `until`, `items` ([schema](#ntulearn_get_upcoming)) |
| `ntu learn digest` | `--since VALUE`, `--until VALUE`, `--course-ids VALUE`, `--max-items VALUE (default: 200)`, `--max-requests VALUE (default: 100)`, `--refresh/-r`, `--json/-j` | Digest of recent announcements, upcoming calendar items and your gradebook across courses. | `retrieved_at`, `from_cache`, `cache_age_seconds`, `complete`, `requests_used`, `issues`, `since`, `until`, `announcements`, `upcoming`, `grades`, `grade_change_note` ([schema](#ntulearn_whats_new)) |
| `ntu learn users` | `COURSE_ID (required)`, `--limit/-l VALUE (default: 50)`, `--offset VALUE`, `--refresh/-r`, `--json/-j` | List course users visible to your account, with their published names and roles. | `retrieved_at`, `from_cache`, `cache_age_seconds`, `course_id`, `group_id`, `users`, `offset`, `next_offset` ([schema](#ntulearn_list_course_users)) |
| `ntu learn auth status` | `--json/-j` | Report credential configuration and this process's last verified login, without logging in. | `credentials_configured`, `credential_storage`, `credential_error`, `session_verified`, `authentication_method`, `last_verified_at`, `session_storage`, `cache_ttl_seconds` ([schema](#ntulearn_auth_status)) |
| `ntu learn content tree` | `COURSE_ID (required)`, `--max-depth VALUE (default: 5)`, `--max-nodes VALUE (default: 1000)`, `--max-requests VALUE (default: 100)`, `--refresh/-r`, `--json/-j` | Read a course's nested content tree. | `retrieved_at`, `from_cache`, `cache_age_seconds`, `complete`, `requests_used`, `issues`, `course_id`, `contents`, `max_depth` ([schema](#ntulearn_get_content_tree)) |
| `ntu learn content show` | `COURSE_ID (required)`, `--parent VALUE`, `--limit/-l VALUE (default: 50)`, `--offset VALUE`, `--refresh/-r`, `--json/-j` | Read one level of course content. | `retrieved_at`, `from_cache`, `cache_age_seconds`, `course_id`, `contents`, `offset`, `next_offset` ([schema](#ntulearn_get_course_contents)) |
| `ntu learn courses download` | `COURSE_ID (required)`, `--output/-o VALUE (required)`, `--max-depth VALUE (default: 5)`, `--max-nodes VALUE (default: 1000)`, `--max-files VALUE (default: 100)`, `--max-total-mb VALUE (default: 200)`, `--max-requests VALUE (default: 200)`, `--refresh/-r`, `--json/-j` | Recursively save readable Blackboard attachments under destination/course_id with content folder names and stable file IDs. | `retrieved_at`, `from_cache`, `cache_age_seconds`, `complete`, `requests_used`, `issues`, `course_id`, `destination`, `files`, `bytes_written` ([schema](#ntulearn_download_course)) |
| `ntu learn courses list` | `--limit/-l VALUE (default: 50)`, `--offset VALUE`, `--refresh/-r`, `--json/-j` | List your enrolled NTULearn courses and organizations, including published availability and course IDs. | `retrieved_at`, `from_cache`, `cache_age_seconds`, `courses`, `offset`, `next_offset` ([schema](#ntulearn_list_courses)) |
| `ntu learn files read` | `COURSE_ID (required)`, `CONTENT_ID (required)`, `ATTACHMENT_ID (required)`, `--max-chars VALUE (default: 20000)`, `--max-pages VALUE (default: 20)`, `--json/-j` | Read an attachment inline as text: PDF, DOCX, PPTX, XLSX and UTF text/code. | `course_id`, `content_id`, `attachment_id`, `file_name`, `text`, `truncated`, `pages_read`, `total_pages`, `retrieved_at` ([schema](#ntulearn_read_file_content)) |
| `ntu learn files download` | `COURSE_ID (required)`, `CONTENT_ID (required)`, `ATTACHMENT_ID (required)`, `--output/-o VALUE (required)`, `--max-bytes VALUE (default: 20000000)`, `--json/-j` | Download a Blackboard attachment to an explicit local file path, up to 20 MB. | `path`, `bytes_written`, `downloaded_at` ([schema](#ntulearn_download_file)) |
| `ntu learn groups members` | `COURSE_ID (required)`, `GROUP_ID (required)`, `--limit/-l VALUE (default: 50)`, `--offset VALUE`, `--refresh/-r`, `--json/-j` | List visible members of a course group through Blackboard's browser membership API. | `retrieved_at`, `from_cache`, `cache_age_seconds`, `course_id`, `group_id`, `users`, `offset`, `next_offset` ([schema](#ntulearn_get_group_members)) |
| `ntu learn groups list` | `COURSE_ID (required)`, `--limit/-l VALUE (default: 50)`, `--offset VALUE`, `--refresh/-r`, `--json/-j` | List groups and group sets defined in a course. | `retrieved_at`, `from_cache`, `cache_age_seconds`, `course_id`, `groups`, `offset`, `next_offset` ([schema](#ntulearn_list_course_groups)) |
| `ntu learn messages list` | `--folder VALUE [inbox, sent] (default: inbox)`, `--course VALUE`, `--since VALUE`, `--unread-only`, `--limit/-l VALUE (default: 50)`, `--offset VALUE`, `--max-requests VALUE (default: 100)`, `--refresh/-r`, `--json/-j` | List Blackboard inbox/sent messages through readable course conversations, without marking them read. | `retrieved_at`, `from_cache`, `cache_age_seconds`, `complete`, `requests_used`, `issues`, `folder`, `messages`, `offset`, `next_offset` ([schema](#ntulearn_list_messages)) |
| `ntu learn messages read` | `MESSAGE_ID (required)`, `--course VALUE`, `--conversation-id VALUE`, `--max-requests VALUE (default: 100)`, `--refresh/-r`, `--json/-j` | Read a message's full body and published conversation recipients. | `retrieved_at`, `from_cache`, `cache_age_seconds`, `complete`, `requests_used`, `issues`, `message`, `body`, `recipients`, `recipient_categories`, `includes_all_course_members`, `excluded_participant_ids`, `recipients_scope` ([schema](#ntulearn_read_message)) |
| `ntu learn search all` | `QUERY (required)`, `--course-ids VALUE`, `--max-depth VALUE (default: 5)`, `--max-nodes VALUE (default: 1000)`, `--max-results VALUE (default: 50)`, `--max-requests VALUE (default: 100)`, `--refresh/-r`, `--json/-j` | Recursively search content across available enrolled courses, or selected course_ids. | `retrieved_at`, `from_cache`, `cache_age_seconds`, `complete`, `requests_used`, `issues`, `query`, `courses_searched`, `matches` ([schema](#ntulearn_search_all_courses)) |
| `ntu learn search course` | `COURSE_ID (required)`, `QUERY (required)`, `--max-depth VALUE (default: 5)`, `--max-nodes VALUE (default: 1000)`, `--max-results VALUE (default: 50)`, `--max-requests VALUE (default: 100)`, `--refresh/-r`, `--json/-j` | Recursively search one course's content titles, body and description for a case-insensitive substring. | `retrieved_at`, `from_cache`, `cache_age_seconds`, `complete`, `requests_used`, `issues`, `query`, `courses_searched`, `matches` ([schema](#ntulearn_search_course_content)) |
| `ntu learn videos download` | `COURSE_ID (required)`, `CONTENT_ID (required)`, `--output/-o VALUE (required)`, `--max-mb VALUE (default: 1000)`, `--json/-j` | Download a Kaltura video embedded in an NTULearn content item to a new local file. | `path`, `bytes_written`, `downloaded_at` ([schema](#ntulearn_download_video)) |

## MCP tools

Inputs are required only where marked. Output fields marked required may still be `null` when their type allows it. See the nested data types below for object fields.

### `ntulearn_search_course_content`

Recursively search one course's content titles, body and description for a case-insensitive substring. Results include course_id and breadcrumbs. Does not search inside attachment bytes. Bounded or denied folders are reported in issues.

**Inputs:** `course_id`, a nonblank `query` of 1–200 characters; optional traversal limits, `max_results` of 1–200 with default 50, request budget, and refresh.

**Returns:** case-insensitive substring matches in titles, body, and description. Each match includes `course_id`, `content_id`, title, breadcrumb, and an excerpt. It does not search attachment bytes.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_id` | `string` | Yes | NTULearn ID returned by another tool; pattern: `^[A-Za-z0-9_-]{1,80}$` |
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
| `issues` | array of [`Issue`](#mcp-type-issue) | Yes | — |
| `query` | `string` | Yes | — |
| `courses_searched` | array of `string` | Yes | — |
| `matches` | array of [`ContentMatch`](#mcp-type-contentmatch) | Yes | — |

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
| `issues` | array of [`Issue`](#mcp-type-issue) | Yes | — |
| `query` | `string` | Yes | — |
| `courses_searched` | array of `string` | Yes | — |
| `matches` | array of [`ContentMatch`](#mcp-type-contentmatch) | Yes | — |

### `ntulearn_auth_status`

Report credential configuration and this process's last verified login, without logging in.

**Inputs:** none. Does not log in or require configured credentials.

**Returns:** `credentials_configured`, `credential_storage` of `os_keyring`, a sanitized `credential_error` when unavailable, `session_verified`, `authentication_method` (`browser_cookie` or `sso` when verified), `last_verified_at`, in-memory session storage mode, and cache TTL. A previously verified session is not a guarantee that NTU has not expired it since the last read. A browser-cookie session can be verified while `credentials_configured` is false.

`credentials_configured` is `true` when the stored account is readable, `false` when the keyring is readable but has no account, and `null` when storage cannot be read. See [Linux keyring troubleshooting](../shared/README.md#linux-keyring-access) if terminal `auth status` works but the MCP does not.

**Inputs**

None.

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `credentials_configured` | `boolean` or `null` | Yes | — |
| `credential_storage` | `"os_keyring"` | No | default: `"os_keyring"` |
| `credential_error` | `string` or `null` | No | default: `null` |
| `session_verified` | `boolean` | Yes | — |
| `authentication_method` | `"browser_cookie"`, `"sso"` or `null` | No | default: `null` |
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
| `courses` | array of [`Course`](#mcp-type-course) | Yes | — |
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
| `course_id` | `string` | Yes | NTULearn ID returned by another tool; pattern: `^[A-Za-z0-9_-]{1,80}$` |
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
| `contents` | array of [`Content`](#mcp-type-content) | Yes | — |
| `offset` | `integer` | Yes | — |
| `next_offset` | `integer` or `null` | Yes | — |

### `ntulearn_get_announcements`

Read published announcements for one enrolled course. An empty list is distinct from denied access.

**Inputs:** `course_id`; common pagination and refresh parameters.

**Returns:** published announcement IDs, titles, body text, and created/modified timestamps. A successful empty list is distinct from an access-denied error.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_id` | `string` | Yes | NTULearn ID returned by another tool; pattern: `^[A-Za-z0-9_-]{1,80}$` |
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
| `announcements` | array of [`Announcement`](#mcp-type-announcement) | Yes | — |
| `offset` | `integer` | Yes | — |
| `next_offset` | `integer` or `null` | Yes | — |

### `ntulearn_get_calendar`

Read calendar entries and published deadlines, across your courses or for one course. Defaults to the next 14 days. Supply timezone-aware timestamps and a window no longer than 112 days.

**Inputs:** optional `since`, `until`, `course_id`, pagination, and refresh. Defaults to the next 14 days. Explicit timestamps must include a timezone, with a positive window no longer than 112 days.

**Returns:** one page of calendar items with course attribution when provided, event type, dates, description, location, and cache metadata. Published deadlines can appear as type `GradebookColumn`.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `since` | `string` or `null` | No | default: `null`; format: `date-time` |
| `until` | `string` or `null` | No | default: `null`; format: `date-time` |
| `course_id` | `string` or `null` | No | default: `null`; NTULearn ID returned by another tool; pattern: `^[A-Za-z0-9_-]{1,80}$` |
| `limit` | `integer` | No | minimum: `1`; maximum: `100`; default: `50` |
| `offset` | `integer` | No | minimum: `0`; default: `0` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `from_cache` | `boolean` | Yes | — |
| `cache_age_seconds` | `integer` | Yes | — |
| `since` | `string` | Yes | format: `date-time` |
| `until` | `string` | Yes | format: `date-time` |
| `items` | array of [`CalendarItem`](#mcp-type-calendaritem) | Yes | — |
| `offset` | `integer` | Yes | — |
| `next_offset` | `integer` or `null` | Yes | — |

### `ntulearn_get_gradebook`

Read visible gradebook columns and your own scores/status. Missing scores remain null. Columns and grades paginate independently with offset and grades_offset.

**Inputs:** `course_id`; `limit`, `offset`, `refresh`; and `grades_offset`, default 0.

**Returns:** visible gradebook `columns` and your own `grades`. Columns include names, possible scores, due dates, availability, and content IDs when published. Grades include score/text, status, exemption, feedback, and modified time when published. Missing scores remain `null`; zero remains zero.

Columns and grades paginate independently. Follow `next_offset` for columns and `grades_next_offset` for grades, supplying `offset` and `grades_offset` respectively.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_id` | `string` | Yes | NTULearn ID returned by another tool; pattern: `^[A-Za-z0-9_-]{1,80}$` |
| `limit` | `integer` | No | minimum: `1`; maximum: `100`; default: `50` |
| `offset` | `integer` | No | minimum: `0`; default: `0` |
| `grades_offset` | `integer` | No | minimum: `0`; default: `0` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `from_cache` | `boolean` | Yes | — |
| `cache_age_seconds` | `integer` | Yes | — |
| `course_id` | `string` | Yes | — |
| `columns` | array of [`GradeColumn`](#mcp-type-gradecolumn) | Yes | — |
| `grades` | array of [`Grade`](#mcp-type-grade) | Yes | — |
| `offset` | `integer` | Yes | — |
| `next_offset` | `integer` or `null` | Yes | — |
| `grades_next_offset` | `integer` or `null` | Yes | — |
| `grades_offset` | `integer` | Yes | — |

### `ntulearn_get_content_attachments`

List files attached to a course content item. Use a leaf content ID rather than a folder. Some external/LTI content has no downloadable Blackboard attachment.

**Inputs:** `course_id`, `content_id`; common pagination and refresh parameters. Use a leaf content item rather than a folder.

**Returns:** attachment IDs, filenames, and MIME types when provided. Some external/LTI items do not expose Blackboard attachment files.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_id` | `string` | Yes | NTULearn ID returned by another tool; pattern: `^[A-Za-z0-9_-]{1,80}$` |
| `content_id` | `string` | Yes | NTULearn ID returned by another tool; pattern: `^[A-Za-z0-9_-]{1,80}$` |
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
| `content_id` | `string` | Yes | — |
| `attachments` | array of [`Attachment`](#mcp-type-attachment) | Yes | — |
| `offset` | `integer` | Yes | — |
| `next_offset` | `integer` or `null` | Yes | — |

### `ntulearn_get_content_tree`

Read a course's nested content tree. Root items are depth 1; max_depth is at most 10. Unopened, denied or cyclic branches are explicit; complete=false means the tree is partial.

**Inputs:** `course_id`; optional `max_depth`, `max_nodes`, `max_requests`, and `refresh`.

**Returns:** nested content nodes with `children` and `children_complete`. An unopened or denied branch is marked explicitly. `complete: false` means the full requested tree was not retrieved.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_id` | `string` | Yes | NTULearn ID returned by another tool; pattern: `^[A-Za-z0-9_-]{1,80}$` |
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
| `issues` | array of [`Issue`](#mcp-type-issue) | Yes | — |
| `course_id` | `string` | Yes | — |
| `contents` | array of [`ContentNode`](#mcp-type-contentnode) | Yes | — |
| `max_depth` | `integer` | Yes | — |

### `ntulearn_get_group_members`

List visible members of a course group through Blackboard's browser membership API. Use a group ID from ntulearn_list_course_groups; a group set may have no direct members.

**Inputs:** `course_id`, `group_id`; common pagination and refresh parameters.

**Returns:** members visible through the browser membership API, with IDs, names, and roles when published. A successful empty result is reported as returned; no hidden memberships or identities are inferred.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_id` | `string` | Yes | NTULearn ID returned by another tool; pattern: `^[A-Za-z0-9_-]{1,80}$` |
| `group_id` | `string` | Yes | NTULearn ID returned by another tool; pattern: `^[A-Za-z0-9_-]{1,80}$` |
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
| `group_id` | `string` or `null` | No | default: `null` |
| `users` | array of [`Person`](#mcp-type-person) | Yes | — |
| `offset` | `integer` | Yes | — |
| `next_offset` | `integer` or `null` | Yes | — |

### `ntulearn_get_upcoming`

Collect all calendar pages across your enrolled courses. Defaults to the next 14 days. Optionally select courses or item_type such as GradebookColumn. Partial failures are reported in issues.

**Inputs:** optional `since`, `until`, `course_ids`, `item_type`, `max_requests`, and `refresh`. Uses the same calendar window rules and default as `ntulearn_get_calendar`.

**Returns:** collected calendar pages sorted by start time. Use `course_ids` to select sites and `item_type: "GradebookColumn"` for assignment due-date entries. Unlike the paginated calendar tool, this tool collects pages within a single request budget and reports partial coverage.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `since` | `string` or `null` | No | default: `null`; format: `date-time` |
| `until` | `string` or `null` | No | default: `null`; format: `date-time` |
| `course_ids` | array of `string` or `null` | No | default: `null`; minimum items: `1`; maximum items: `100` |
| `item_type` | `string` or `null` | No | default: `null` |
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
| `issues` | array of [`Issue`](#mcp-type-issue) | Yes | — |
| `since` | `string` | Yes | format: `date-time` |
| `until` | `string` | Yes | format: `date-time` |
| `items` | array of [`CalendarItem`](#mcp-type-calendaritem) | Yes | — |

### `ntulearn_list_course_groups`

List groups and group sets defined in a course. Use a group's ID with ntulearn_get_group_members; availability remains unknown when NTU omits it.

**Inputs:** `course_id`; common pagination and refresh parameters.

**Returns:** group IDs, names, descriptions, availability, parent IDs, and group-set flags when published. Use a child group ID for its members; a group set may have no direct members.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_id` | `string` | Yes | NTULearn ID returned by another tool; pattern: `^[A-Za-z0-9_-]{1,80}$` |
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
| `groups` | array of [`Group`](#mcp-type-group) | Yes | — |
| `offset` | `integer` | Yes | — |
| `next_offset` | `integer` or `null` | Yes | — |

### `ntulearn_list_course_users`

List course users visible to your account, with their published names and roles. Includes instructors, TAs and students as NTU permits; does not expose raw profiles.

**Inputs:** `course_id`; common pagination and refresh parameters.

**Returns:** visible users with their IDs, published display names, and course roles. Instructors, TAs, and students appear only as NTU permits. Raw user profiles are not exposed.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_id` | `string` | Yes | NTULearn ID returned by another tool; pattern: `^[A-Za-z0-9_-]{1,80}$` |
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
| `group_id` | `string` or `null` | No | default: `null` |
| `users` | array of [`Person`](#mcp-type-person) | Yes | — |
| `offset` | `integer` | Yes | — |
| `next_offset` | `integer` or `null` | Yes | — |

### `ntulearn_list_messages`

List Blackboard inbox/sent messages through readable course conversations, without marking them read. Scope course_id to reduce requests. Use returned IDs for ntulearn_read_message. Inspect complete/issues before treating results as a full mailbox.

**Inputs:** `folder` of `"inbox"` or `"sent"`, default `"inbox"`; optional `course_id`, timezone-aware `since`, `unread_only` with default `false`, pagination, request budget, and refresh.

**Returns:** message IDs, course/conversation IDs, published subject, sender, timestamp, read status, and folder. Scope a course to reduce mailbox traversal. A missing read status remains unknown. Incomplete conversations and denied courses are reported in `issues`.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `folder` | `"inbox"`, `"sent"` | No | default: `"inbox"` |
| `course_id` | `string` or `null` | No | default: `null`; NTULearn ID returned by another tool; pattern: `^[A-Za-z0-9_-]{1,80}$` |
| `since` | `string` or `null` | No | default: `null`; format: `date-time` |
| `unread_only` | `boolean` | No | default: `false` |
| `limit` | `integer` | No | minimum: `1`; maximum: `100`; default: `50` |
| `offset` | `integer` | No | minimum: `0`; default: `0` |
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
| `issues` | array of [`Issue`](#mcp-type-issue) | Yes | — |
| `folder` | `"inbox"`, `"sent"` | Yes | — |
| `messages` | array of [`MessageSummary`](#mcp-type-messagesummary) | Yes | — |
| `offset` | `integer` | Yes | — |
| `next_offset` | `integer` or `null` | Yes | — |

### `ntulearn_read_file_content`

Read an attachment inline as text: PDF, DOCX, PPTX, XLSX and UTF text/code. Get attachment_id from ntulearn_get_content_attachments. Reports truncation; no OCR, image interpretation or external LTI downloads. Temporary files are removed.

**Inputs:** `course_id`, `content_id`, `attachment_id`; optional `max_chars` of 1–100000 with default 20000 and `max_pages` of 1–50 with default 20.

**Returns:** the filename, extracted `text`, `truncated`, retrieval time, and PDF page counts when applicable. Supports PDF, DOCX, PPTX including text notes, XLSX, and supported UTF-8/UTF-16 text/code files. PDFs are read from the beginning up to the page/character limit. Extraction is text-only: scanned images and diagrams are not interpreted, and OCR is not performed. Temporary files are removed after extraction.

Unsupported, encrypted, malformed, or oversized documents produce an actionable error; download them for local viewing instead. Extraction has a 30-second worker timeout. Attachments remain subject to the 20 MB download limit.

```json
{"course_id":"_100_1","content_id":"_200_1","attachment_id":"_300_1","max_pages":5,"max_chars":10000}
```

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_id` | `string` | Yes | NTULearn ID returned by another tool; pattern: `^[A-Za-z0-9_-]{1,80}$` |
| `content_id` | `string` | Yes | NTULearn ID returned by another tool; pattern: `^[A-Za-z0-9_-]{1,80}$` |
| `attachment_id` | `string` | Yes | NTULearn ID returned by another tool; pattern: `^[A-Za-z0-9_-]{1,80}$` |
| `max_chars` | `integer` | No | minimum: `1`; maximum: `100000`; default: `20000` |
| `max_pages` | `integer` | No | minimum: `1`; maximum: `50`; default: `20` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_id` | `string` | Yes | — |
| `content_id` | `string` | Yes | — |
| `attachment_id` | `string` | Yes | — |
| `file_name` | `string` | Yes | — |
| `text` | `string` | Yes | — |
| `truncated` | `boolean` | Yes | — |
| `pages_read` | `integer` or `null` | No | default: `null` |
| `total_pages` | `integer` or `null` | No | default: `null` |
| `retrieved_at` | `string` | Yes | format: `date-time` |

### `ntulearn_read_message`

Read a message's full body and published conversation recipients. Supply course_id and conversation_id from ntulearn_list_messages for direct lookup, or omit both for a bounded mailbox search. Conversation participants may differ from a message's exact To/Cc/Bcc recipients; this scope is explicit in the result. Does not mark messages read.

**Inputs:** `message_id`; optional `course_id` and `conversation_id` together, request budget, and refresh. Supplying the two IDs from `ntulearn_list_messages` allows direct lookup; omitting both searches the readable mailbox within the budget.

**Returns:** the message summary, full body as text, published participants/categories, excluded participant IDs, and whether all course members are included. `recipients_scope` is `conversation_participants`; these are not asserted to be an individual message's exact To/Cc/Bcc list. Participant names may be unknown. No mark-read request is sent.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `message_id` | `string` | Yes | NTULearn ID returned by another tool; pattern: `^[A-Za-z0-9_-]{1,80}$` |
| `course_id` | `string` or `null` | No | default: `null`; NTULearn ID returned by another tool; pattern: `^[A-Za-z0-9_-]{1,80}$` |
| `conversation_id` | `string` or `null` | No | default: `null`; NTULearn ID returned by another tool; pattern: `^[A-Za-z0-9_-]{1,80}$` |
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
| `issues` | array of [`Issue`](#mcp-type-issue) | Yes | — |
| `message` | [`MessageSummary`](#mcp-type-messagesummary) | Yes | — |
| `body` | `string` or `null` | No | default: `null` |
| `recipients` | array of [`Person`](#mcp-type-person) | Yes | — |
| `recipient_categories` | array of `string` | Yes | — |
| `includes_all_course_members` | `boolean` or `null` | No | default: `null` |
| `excluded_participant_ids` | array of `string` | Yes | — |
| `recipients_scope` | `"conversation_participants"` | No | default: `"conversation_participants"` |

### `ntulearn_whats_new`

Digest of recent announcements, upcoming calendar items and your gradebook across courses. Defaults to announcements from the last 7 days and events in the next 14 days. NTU often omits grade-change timestamps: those grades are labeled snapshots with changed_since=null. No persistent last-seen tracker. Check issues for partial coverage.

**Inputs:** optional timezone-aware `since`, default seven days ago; `until`, default 14 days ahead; `course_ids`; `max_items` of 1–500 with default 200; request budget; and refresh. `since` must be in the past, and `until` must be in the future within 112 days.

**Returns:** recent announcements, upcoming calendar entries, your gradebook snapshots, and collection issues. Change timestamps filter announcements/grades when available. Grades without a published change timestamp have `changed_since: null` and are explicitly current snapshots. `max_items` bounds each result category. No persistent last-seen tracker is stored.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `since` | `string` or `null` | No | default: `null`; format: `date-time` |
| `until` | `string` or `null` | No | default: `null`; format: `date-time` |
| `course_ids` | array of `string` or `null` | No | default: `null`; minimum items: `1`; maximum items: `100` |
| `max_items` | `integer` | No | minimum: `1`; maximum: `500`; default: `200` |
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
| `issues` | array of [`Issue`](#mcp-type-issue) | Yes | — |
| `since` | `string` | Yes | format: `date-time` |
| `until` | `string` | Yes | format: `date-time` |
| `announcements` | array of [`RecentAnnouncement`](#mcp-type-recentannouncement) | Yes | — |
| `upcoming` | array of [`CalendarItem`](#mcp-type-calendaritem) | Yes | — |
| `grades` | array of [`RecentGrade`](#mcp-type-recentgrade) | Yes | — |
| `grade_change_note` | `string` | No | default: `"Grades without a published change timestamp are current snapshots; changed_since is null."` |

### `ntulearn_download_file`

Download a Blackboard attachment to an explicit local file path, up to 20 MB. Never overwrites an existing file. Does not modify NTULearn or forward university cookies to file-delivery hosts.

**Inputs:** `course_id`, `content_id`, `attachment_id`, and an explicit local `destination` file path. Its parent directory must already exist.

**Returns:** saved path, bytes written, and download time. Saves at most 20 MB and never overwrites an existing file. It writes locally and does not modify NTULearn. Supported redirects stay on NTU or Blackboard delivery hosts; university cookies are not forwarded to delivery hosts. HTML/JSON attachments are unsupported.

MCP host confirmation is required before this action.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_id` | `string` | Yes | NTULearn ID returned by another tool; pattern: `^[A-Za-z0-9_-]{1,80}$` |
| `content_id` | `string` | Yes | NTULearn ID returned by another tool; pattern: `^[A-Za-z0-9_-]{1,80}$` |
| `attachment_id` | `string` | Yes | NTULearn ID returned by another tool; pattern: `^[A-Za-z0-9_-]{1,80}$` |
| `destination` | `string` | Yes | — |
| `max_bytes` | `integer` | No | minimum: `1`; maximum: `20000000`; default: `20000000` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `path` | `string` | Yes | — |
| `bytes_written` | `integer` | Yes | minimum: `0` |
| `downloaded_at` | `string` | Yes | format: `date-time` |

### `ntulearn_download_video`

Download a Kaltura video embedded in an NTULearn content item to a new local file. Uses your normal course access and a short-lived viewer session; max_mb is 1–2000, existing files are never overwritten, and NTULearn is not modified.

**Inputs:** `course_id`, `content_id`, an explicit local `destination` file path, and optional `max_mb` from 1–2000 (default 1000). The parent directory must already exist.

**Returns:** saved path, bytes written, and download time. Supports Kaltura players embedded in NTULearn content. It obtains the player’s short-lived viewer session in a temporary Chromium context, then streams the Kaltura download to disk. NTU cookies are used only for the NTULearn WebDAV wrapper and are never sent to Blackboard or Kaltura. Existing files and symbolic-link directories are rejected; failed partial downloads are removed. The item must be visible to your account and Kaltura must provide a downloadable source. This tool requires the optional `personal` dependencies and installed Chromium.

```json
{"course_id":"_100_1","content_id":"_200_1","destination":"/path/to/lecture.mp4","max_mb":1000}
```

MCP host confirmation is required before this action.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_id` | `string` | Yes | NTULearn ID returned by another tool; pattern: `^[A-Za-z0-9_-]{1,80}$` |
| `content_id` | `string` | Yes | NTULearn ID returned by another tool; pattern: `^[A-Za-z0-9_-]{1,80}$` |
| `destination` | `string` | Yes | — |
| `max_mb` | `integer` | No | minimum: `1`; maximum: `2000`; default: `1000` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `path` | `string` | Yes | — |
| `bytes_written` | `integer` | Yes | minimum: `0` |
| `downloaded_at` | `string` | Yes | format: `date-time` |

### `ntulearn_download_course`

Recursively save readable Blackboard attachments under destination/course_id with content folder names and stable file IDs. Creates local directories, skips existing regular files, rejects symlinks and never overwrites. Per-file limit 20 MB; batch limits and denied/external content are reported in issues. NTULearn is never modified.

**Inputs:** `course_id`, `destination` directory; optional traversal limits and refresh; `max_files` of 1–500 with default 100, `max_total_mb` of 1–500 with default 200, and `max_requests` with default 200.

**Returns:** destination, file statuses of `downloaded`, `skipped_existing`, or `failed`, bytes written, and coverage/issues. Files are saved beneath `destination/course_id` using content-folder names and stable IDs. Downloads run as the tree is traversed. Existing regular files are skipped, symbolic-link directories are rejected, and files are never overwritten. Each file is limited to 20 MB in addition to the total batch budget. External/LTI material may not be downloadable through these APIs.

MCP host confirmation is required before this action.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_id` | `string` | Yes | NTULearn ID returned by another tool; pattern: `^[A-Za-z0-9_-]{1,80}$` |
| `destination` | `string` | Yes | — |
| `max_depth` | `integer` | No | minimum: `1`; maximum: `10`; default: `5` |
| `max_nodes` | `integer` | No | minimum: `1`; maximum: `5000`; default: `1000` |
| `max_files` | `integer` | No | minimum: `1`; maximum: `500`; default: `100` |
| `max_total_mb` | `integer` | No | minimum: `1`; maximum: `500`; default: `200` |
| `max_requests` | `integer` | No | minimum: `1`; maximum: `200`; default: `200` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `from_cache` | `boolean` | Yes | — |
| `cache_age_seconds` | `integer` | Yes | — |
| `complete` | `boolean` | Yes | — |
| `requests_used` | `integer` | Yes | — |
| `issues` | array of [`Issue`](#mcp-type-issue) | Yes | — |
| `course_id` | `string` | Yes | — |
| `destination` | `string` | Yes | — |
| `files` | array of [`CourseDownloadFile`](#mcp-type-coursedownloadfile) | Yes | — |
| `bytes_written` | `integer` | Yes | — |

## MCP data types

These named types are used by the tool input and output fields above.

<a id="mcp-type-announcement"></a>
### `Announcement`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `id` | `string` | Yes | — |
| `title` | `string` | Yes | — |
| `body` | `string` or `null` | No | default: `null` |
| `created` | `string` or `null` | No | default: `null`; format: `date-time` |
| `modified` | `string` or `null` | No | default: `null`; format: `date-time` |

<a id="mcp-type-attachment"></a>
### `Attachment`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `id` | `string` | Yes | — |
| `file_name` | `string` | Yes | — |
| `mime_type` | `string` or `null` | No | default: `null` |

<a id="mcp-type-calendaritem"></a>
### `CalendarItem`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `id` | `string` | Yes | — |
| `title` | `string` | Yes | — |
| `type` | `string` or `null` | No | default: `null` |
| `calendar_name` | `string` or `null` | No | default: `null` |
| `course_id` | `string` or `null` | No | default: `null` |
| `start` | `string` or `null` | No | default: `null`; format: `date-time` |
| `end` | `string` or `null` | No | default: `null`; format: `date-time` |
| `description` | `string` or `null` | No | default: `null` |
| `location` | `string` or `null` | No | default: `null` |

<a id="mcp-type-content"></a>
### `Content`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `id` | `string` | Yes | — |
| `title` | `string` | Yes | — |
| `parent_id` | `string` or `null` | No | default: `null` |
| `has_children` | `boolean` or `null` | No | default: `null` |
| `type` | `string` or `null` | No | default: `null` |
| `body` | `string` or `null` | No | default: `null` |
| `description` | `string` or `null` | No | default: `null` |
| `modified` | `string` or `null` | No | default: `null`; format: `date-time` |

<a id="mcp-type-contentmatch"></a>
### `ContentMatch`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_id` | `string` | Yes | — |
| `content_id` | `string` | Yes | — |
| `title` | `string` | Yes | — |
| `breadcrumb` | array of `string` | Yes | — |
| `excerpt` | `string` | Yes | — |

<a id="mcp-type-contentnode"></a>
### `ContentNode`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `id` | `string` | Yes | — |
| `title` | `string` | Yes | — |
| `parent_id` | `string` or `null` | No | default: `null` |
| `has_children` | `boolean` or `null` | No | default: `null` |
| `type` | `string` or `null` | No | default: `null` |
| `body` | `string` or `null` | No | default: `null` |
| `description` | `string` or `null` | No | default: `null` |
| `modified` | `string` or `null` | No | default: `null`; format: `date-time` |
| `children` | array of [`ContentNode`](#mcp-type-contentnode) | No | — |
| `children_complete` | `boolean` or `null` | No | default: `null` |

<a id="mcp-type-course"></a>
### `Course`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `id` | `string` | Yes | — |
| `course_code` | `string` or `null` | No | default: `null` |
| `name` | `string` | Yes | — |
| `available` | `string` or `null` | No | default: `null` |
| `role` | `string` or `null` | No | default: `null` |
| `organization` | `boolean` or `null` | No | default: `null` |

<a id="mcp-type-coursedownloadfile"></a>
### `CourseDownloadFile`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `content_id` | `string` | Yes | — |
| `attachment_id` | `string` | Yes | — |
| `path` | `string` | Yes | — |
| `status` | `"downloaded"`, `"skipped_existing"`, `"failed"` | Yes | — |
| `bytes_written` | `integer` or `null` | No | default: `null` |

<a id="mcp-type-grade"></a>
### `Grade`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `column_id` | `string` | Yes | — |
| `score` | `number` or `null` | No | default: `null` |
| `text` | `string` or `null` | No | default: `null` |
| `status` | `string` or `null` | No | default: `null` |
| `exempt` | `boolean` or `null` | No | default: `null` |
| `feedback` | `string` or `null` | No | default: `null` |
| `modified` | `string` or `null` | No | default: `null`; format: `date-time` |

<a id="mcp-type-gradecolumn"></a>
### `GradeColumn`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `id` | `string` | Yes | — |
| `name` | `string` | Yes | — |
| `possible_score` | `number` or `null` | No | default: `null` |
| `due` | `string` or `null` | No | default: `null`; format: `date-time` |
| `available` | `string` or `null` | No | default: `null` |
| `content_id` | `string` or `null` | No | default: `null` |

<a id="mcp-type-group"></a>
### `Group`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `id` | `string` | Yes | — |
| `name` | `string` | Yes | — |
| `description` | `string` or `null` | No | default: `null` |
| `available` | `string` or `null` | No | default: `null` |
| `parent_id` | `string` or `null` | No | default: `null` |
| `is_group_set` | `boolean` or `null` | No | default: `null` |

<a id="mcp-type-issue"></a>
### `Issue`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `service` | `string` | Yes | — |
| `course_id` | `string` or `null` | No | default: `null` |
| `content_id` | `string` or `null` | No | default: `null` |
| `message` | `string` | Yes | — |

<a id="mcp-type-messagesummary"></a>
### `MessageSummary`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `id` | `string` | Yes | — |
| `course_id` | `string` | Yes | — |
| `conversation_id` | `string` | Yes | — |
| `subject` | `string` or `null` | No | default: `null` |
| `sender` | [`Person`](#mcp-type-person) | Yes | — |
| `created` | `string` or `null` | No | default: `null`; format: `date-time` |
| `read` | `boolean` or `null` | No | default: `null` |
| `folder` | `"inbox"`, `"sent"` | Yes | — |

<a id="mcp-type-person"></a>
### `Person`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `id` | `string` | Yes | — |
| `name` | `string` or `null` | No | default: `null` |
| `role` | `string` or `null` | No | default: `null` |

<a id="mcp-type-recentannouncement"></a>
### `RecentAnnouncement`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `id` | `string` | Yes | — |
| `title` | `string` | Yes | — |
| `body` | `string` or `null` | No | default: `null` |
| `created` | `string` or `null` | No | default: `null`; format: `date-time` |
| `modified` | `string` or `null` | No | default: `null`; format: `date-time` |
| `course_id` | `string` | Yes | — |
| `changed_since` | `boolean` or `null` | Yes | — |

<a id="mcp-type-recentgrade"></a>
### `RecentGrade`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_id` | `string` | Yes | — |
| `column` | [`GradeColumn`](#mcp-type-gradecolumn) or `null` | No | default: `null` |
| `grade` | [`Grade`](#mcp-type-grade) | Yes | — |
| `changed_since` | `boolean` or `null` | Yes | — |

## Service notes

These tools run in the shared `all-abt-ntu-mcp` server. See the [main README](../../README.md) for installation, Chromium, and MCP client configuration.

### Sessions

NTULearn authentication is lazy. It reuses the active validated session first, then tries browser cookies only when discovery is enabled, and finally reads credentials from the OS keyring for normal NTU/Microsoft sign-in in a temporary Chromium browser. An expired session is invalidated and recovered once; concurrent requests share the same login or refresh attempt. The server never retries a rejected password automatically.

#### Optional browser-cookie discovery

NTULearn can reuse an existing `BbRouter` session from Edge, Chrome, Firefox, Brave, or Safari. This is opt-in: set `NTULEARN_BROWSER_COOKIES=true` in the MCP server environment and enable the optional browser-cookie dependencies; see the [main installation guide](../../README.md#installation). If browser-cookie access is disabled (the default), unavailable, or cannot read a browser profile, NTULearn proceeds to SSO. Each browser profile is tried separately; cookies are never combined across profiles. Imported cookies are accepted only for NTU domains and are checked against `/users/me` before use. A failed or expired cookie set is discarded. Cookie values are held in memory only and are not written to the keyring or files. Cookie extraction depends on the browser, operating system, encryption support, and whether the profile can be unlocked; headless servers can leave this feature disabled and use SSO.

The browser-cookie strategy does not need a saved account when it succeeds. Automatic SSO requires credentials saved with `ntu auth save` and the optional `personal` dependencies with Chromium installed. If NTU requires MFA or CAPTCHA, headless login stops. To complete the normal challenge yourself, set `NTULEARN_HEADLESS=false` and run the MCP process in a local environment where the browser is visible. No MFA or CAPTCHA checks are bypassed.

Passwords are read from the [shared OS keyring](../shared/README.md#credential-storage), never retained on the session object, and checked once at the start of each data-tool operation. Replacing or revoking the credentials invalidates the SSO session and response cache on the next operation. Browser-cookie sessions do not use keyring credentials. Authentication state and cached academic responses stay in memory; cookies are not persisted. A validated session is not rechecked before every request: 401 responses, login redirects/pages, and credential revision changes trigger recovery.

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
- If SSO reports that Chromium is unavailable, install the `personal` extra and Chromium using the [main setup guide](../../README.md#chromium). In a headless environment, MFA or CAPTCHA requires a local visible browser; it is never bypassed.
- If `ntulearn_auth_status` reports a keyring error, follow [Linux keyring access](../shared/README.md#linux-keyring-access) or unlock the platform's native keyring. A verified browser-cookie session can work without a keyring account.
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
uv run --extra personal python tests/ntulearn/live_session_smoke.py
uv run --extra personal python tests/ntulearn/live_tools_smoke.py
```

Live checks require an account saved locally with `auth save` and Chromium when SSO is needed. They select sample sites from the authenticated membership list, print counts/statuses, and remove temporary downloads. The session smoke test invalidates its in-memory session to exercise recovery. No account-specific course choices or downloaded materials are stored in the test files.

### Code layout

`mcp.py` holds operation descriptions, input schemas, and registration. `client/` owns sessions and HTTP reads; `parser/` handles response normalization and document text; `services/` implements bounded workflows; `models/` holds typed results grouped by domain. The shared runtime registers these operations alongside STARS and closes both sessions on shutdown.
