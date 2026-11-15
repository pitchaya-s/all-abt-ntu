# NTULearn: Announcements, calendar and grades MCP tools

[Service overview](../index.md) · [CLI reference](../cli/index.md) · [All MCP tools](index.md) · [Data types](types.md)

## Announcements, calendar and grades

Inputs are required only where marked. A required output field may still be `null` if its type allows it. See [data types](types.md) for nested objects.

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
| `announcements` | array of [`Announcement`](types.md#mcp-type-announcement) | Yes | — |
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
| `items` | array of [`CalendarItem`](types.md#mcp-type-calendaritem) | Yes | — |
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
| `columns` | array of [`GradeColumn`](types.md#mcp-type-gradecolumn) | Yes | — |
| `grades` | array of [`Grade`](types.md#mcp-type-grade) | Yes | — |
| `offset` | `integer` | Yes | — |
| `next_offset` | `integer` or `null` | Yes | — |
| `grades_next_offset` | `integer` or `null` | Yes | — |
| `grades_offset` | `integer` | Yes | — |

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
| `issues` | array of [`Issue`](types.md#mcp-type-issue) | Yes | — |
| `since` | `string` | Yes | format: `date-time` |
| `until` | `string` | Yes | format: `date-time` |
| `items` | array of [`CalendarItem`](types.md#mcp-type-calendaritem) | Yes | — |

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
| `issues` | array of [`Issue`](types.md#mcp-type-issue) | Yes | — |
| `since` | `string` | Yes | format: `date-time` |
| `until` | `string` | Yes | format: `date-time` |
| `announcements` | array of [`RecentAnnouncement`](types.md#mcp-type-recentannouncement) | Yes | — |
| `upcoming` | array of [`CalendarItem`](types.md#mcp-type-calendaritem) | Yes | — |
| `grades` | array of [`RecentGrade`](types.md#mcp-type-recentgrade) | Yes | — |
| `grade_change_note` | `string` | No | default: `"Grades without a published change timestamp are current snapshots; changed_since is null."` |
