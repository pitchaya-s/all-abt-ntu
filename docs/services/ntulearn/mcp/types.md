# NTULearn: MCP data types

[Service overview](../index.md) · [MCP reference](index.md)

## MCP data types

These named types describe nested fields in the [MCP tool reference](index.md). A required field may still be `null` when its type allows it.

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
