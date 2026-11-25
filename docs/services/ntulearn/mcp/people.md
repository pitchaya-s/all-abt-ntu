# NTULearn: Messages, users and groups MCP tools

[Service overview](../index.md) · [CLI reference](../cli/index.md) · [All MCP tools](index.md) · [Data types](types.md)

## Messages, users and groups

Inputs are required only where marked. A required output field may still be `null` if its type allows it. See [data types](types.md) for nested objects.

### `ntulearn_get_group_members`

List visible members of a course group through Blackboard's browser membership API. Use a group ID from ntulearn_list_course_groups; a group set may have no direct members.

**Inputs:** `course_id`, `group_id`; common pagination and refresh parameters.

**Returns:** members visible through the browser membership API, with IDs, names, and roles when published. A successful empty result is reported as returned; no hidden memberships or identities are inferred.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_id` | `string` | Yes | Blackboard course ID or enrolled course code; pattern: `^[A-Za-z0-9_-]{1,80}$` |
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
| `users` | array of [`Person`](types.md#mcp-type-person) | Yes | — |
| `offset` | `integer` | Yes | — |
| `next_offset` | `integer` or `null` | Yes | — |

### `ntulearn_list_course_groups`

List groups and group sets defined in a course. Use a group's ID with ntulearn_get_group_members; availability remains unknown when NTU omits it.

**Inputs:** `course_id`; common pagination and refresh parameters.

**Returns:** group IDs, names, descriptions, availability, parent IDs, and group-set flags when published. Use a child group ID for its members; a group set may have no direct members.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_id` | `string` | Yes | Blackboard course ID or enrolled course code; pattern: `^[A-Za-z0-9_-]{1,80}$` |
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
| `groups` | array of [`Group`](types.md#mcp-type-group) | Yes | — |
| `offset` | `integer` | Yes | — |
| `next_offset` | `integer` or `null` | Yes | — |

### `ntulearn_list_course_users`

List course users visible to your account, with their published names and roles. Includes instructors, TAs and students as NTU permits; does not expose raw profiles.

**Inputs:** `course_id`; common pagination and refresh parameters.

**Returns:** visible users with their IDs, published display names, and course roles. Instructors, TAs, and students appear only as NTU permits. Raw user profiles are not exposed.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_id` | `string` | Yes | Blackboard course ID or enrolled course code; pattern: `^[A-Za-z0-9_-]{1,80}$` |
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
| `users` | array of [`Person`](types.md#mcp-type-person) | Yes | — |
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
| `course_id` | `string` or `null` | No | default: `null`; Blackboard course ID or enrolled course code; pattern: `^[A-Za-z0-9_-]{1,80}$` |
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
| `issues` | array of [`Issue`](types.md#mcp-type-issue) | Yes | — |
| `folder` | `"inbox"`, `"sent"` | Yes | — |
| `messages` | array of [`MessageSummary`](types.md#mcp-type-messagesummary) | Yes | — |
| `offset` | `integer` | Yes | — |
| `next_offset` | `integer` or `null` | Yes | — |

### `ntulearn_read_message`

Read a message's full body and published conversation recipients. Supply course_id and conversation_id from ntulearn_list_messages for direct lookup, or omit both for a bounded mailbox search. Conversation participants may differ from a message's exact To/Cc/Bcc recipients; this scope is explicit in the result. Does not mark messages read.

**Inputs:** `message_id`; optional `course_id` and `conversation_id` together, request budget, and refresh. Supplying the two IDs from `ntulearn_list_messages` allows direct lookup; omitting both searches the readable mailbox within the budget.

**Returns:** the message summary, full body as text, published participants/categories, excluded participant IDs, and whether all course members are included. `recipients_scope` is `conversation_participants`; these are not asserted to be an individual message's exact To/Cc/Bcc list. Participant names may be unknown. No mark-read request is sent.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `message_id` | `string` | Yes | NTULearn ID returned by another tool; pattern: `^[A-Za-z0-9_-]{1,80}$` |
| `course_id` | `string` or `null` | No | default: `null`; Blackboard course ID or enrolled course code; pattern: `^[A-Za-z0-9_-]{1,80}$` |
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
| `issues` | array of [`Issue`](types.md#mcp-type-issue) | Yes | — |
| `message` | [`MessageSummary`](types.md#mcp-type-messagesummary) | Yes | — |
| `body` | `string` or `null` | No | default: `null` |
| `recipients` | array of [`Person`](types.md#mcp-type-person) | Yes | — |
| `recipient_categories` | array of `string` | Yes | — |
| `includes_all_course_members` | `boolean` or `null` | No | default: `null` |
| `excluded_participant_ids` | array of `string` | Yes | — |
| `recipients_scope` | `"conversation_participants"` | No | default: `"conversation_participants"` |
