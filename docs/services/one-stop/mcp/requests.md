# One Stop: Requests and drafts MCP tools

[Service overview](../index.md) · [CLI reference](../cli/index.md) · [All MCP tools](index.md) · [Data types](types.md)

## Requests and drafts

Draft IDs are temporary state in the running MCP server. Prepare and review a draft before submission, and keep the same server process alive for subsequent draft calls. A draft normally expires after 15 minutes. If a submission outcome is uncertain, inspect the request before attempting another action.

### `onestop_list_my_requests`

Read your own open/closed One Stop cases and service requests, expanding native lists up to 500 records. Inspect per-list coverage and complete. next_offset only pages retrieved records, not older portal history. Returns IDs, status labels, creation dates and links without changing requests.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `status` | `"all"`, `"open"`, `"closed"` | No | default: `"all"` |
| `kind` | `"all"`, `"case"`, `"request"` | No | default: `"all"` |
| `limit` | `integer` | No | minimum: `1`; maximum: `100`; default: `20` |
| `offset` | `integer` | No | minimum: `0`; default: `0` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `offset` | `integer` | Yes | minimum: `0` |
| `available_count` | `integer` | Yes | minimum: `0` |
| `total_count` | `integer` or `null` | Yes | minimum: `0` |
| `complete` | `boolean` | Yes | — |
| `next_offset` | `integer` or `null` | Yes | minimum: `0` |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `requests` | array of [`RequestSummary`](types.md#mcp-type-requestsummary) | Yes | — |
| `coverage` | array of [`ListCoverage`](types.md#mcp-type-listcoverage) | Yes | — |

Unknown fields are not accepted.

### `onestop_get_my_request`

Read one of your requests after checking request_id against your retrieved personal lists. Returns visible fields/answers as separate records for the request or its verified child items, and item stages (up to 20 children). Older records outside those lists and unsupported detail pages need the portal. Does not return conversations, work notes or attachments, or change the request.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `request_id` | `string` | Yes | pattern: `^[0-9a-f]{32}$` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `request` | [`RequestSummary`](types.md#mcp-type-requestsummary) | Yes | — |
| `records` | array of [`RequestRecordDetails`](types.md#mcp-type-requestrecorddetails) | Yes | — |
| `requested_items` | array of [`RequestItemStage`](types.md#mcp-type-requestitemstage) | Yes | — |

Unknown fields are not accepted.

### `onestop_get_request_activity`

Read visible comments and attachment events on a verified own request/item, plus current reply/upload/state-action permissions. Work notes are excluded. Select record_id from get_my_request when it has multiple records.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `request_id` | `string` | Yes | pattern: `^[0-9a-f]{32}$` |
| `record_id` | `string` or `null` | No | default: `null`; pattern: `^[0-9a-f]{32}$` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `request_id` | `string` | Yes | — |
| `record_id` | `string` | Yes | — |
| `entries` | array of [`ActivityEntry`](types.md#mcp-type-activityentry) | Yes | — |
| `available_actions` | array of `string` | Yes | — |
| `can_reply` | `boolean` | Yes | — |
| `can_upload_attachment` | `boolean` | Yes | — |

Unknown fields are not accepted.

### `onestop_get_request_draft`

Inspect a local catalog draft's current visible fields, caller-supplied values, choices, missing requirements, native actions and any submission receipt. Personal defaults are omitted. Does not submit.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `draft_id` | `string` | Yes | minimum length: `16`; maximum length: `100` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `draft_id` | `string` | Yes | — |
| `item_id` | `string` | Yes | — |
| `title` | `string` | Yes | — |
| `source_url` | `string` | Yes | — |
| `expires_at` | `string` | Yes | format: `date-time` |
| `state` | `"prepared"`, `"submitting"`, `"submitted"`, `"uncertain"` | Yes | — |
| `ready` | `boolean` | Yes | — |
| `missing_fields` | array of `string` | Yes | — |
| `invalid_fields` | array of `string` | Yes | — |
| `fields` | array of [`DraftField`](types.md#mcp-type-draftfield) | Yes | — |
| `available_actions` | array of `string` | Yes | — |
| `receipt_id` | `string` or `null` | No | default: `null` |

Unknown fields are not accepted.

### `onestop_search_form_references`

Search a visible reference question using its native picker and original reference qualifier. Use returned value IDs in update_request_draft. Supports the portal's leading * wildcard. Encoded-query operators and arbitrary tables/filters are refused.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `draft_id` | `string` | Yes | minimum length: `16`; maximum length: `100` |
| `field_name` | `string` | Yes | — |
| `query` | `string` | Yes | minimum length: `1`; maximum length: `100` |
| `limit` | `integer` | No | minimum: `1`; maximum: `100`; default: `20` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `draft_id` | `string` | Yes | — |
| `field_name` | `string` | Yes | — |
| `query` | `string` | Yes | — |
| `choices` | array of [`ReferenceChoice`](types.md#mcp-type-referencechoice) | Yes | — |
| `complete` | `boolean` | Yes | — |

Unknown fields are not accepted.

### `onestop_prepare_request`

Prepare a native catalog form in a private in-memory browser tab. Use form_item_id from catalog results. values maps visible editable question names to strings. Runs native change scripts and reports missing/invalid questions without submitting. Password fields, hidden/read-only values and scripts are refused. Drafts expire after 15 minutes; at most four are open.

This tool changes local workflow state.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `item_id` | `string` | Yes | pattern: `^[0-9a-f]{32}$` |
| `values` | object of `string` or `null` | No | default: `null` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `draft_id` | `string` | Yes | — |
| `item_id` | `string` | Yes | — |
| `title` | `string` | Yes | — |
| `source_url` | `string` | Yes | — |
| `expires_at` | `string` | Yes | format: `date-time` |
| `state` | `"prepared"`, `"submitting"`, `"submitted"`, `"uncertain"` | Yes | — |
| `ready` | `boolean` | Yes | — |
| `missing_fields` | array of `string` | Yes | — |
| `invalid_fields` | array of `string` | Yes | — |
| `fields` | array of [`DraftField`](types.md#mcp-type-draftfield) | Yes | — |
| `available_actions` | array of `string` | Yes | — |
| `receipt_id` | `string` or `null` | No | default: `null` |

Unknown fields are not accepted.

### `onestop_update_request_draft`

Change editable questions on an in-memory draft and rerun native change scripts. Set controlling questions first when conditional questions are hidden. Updating answers invalidates the latest appointment slots; select a slot again before booking.

This tool changes local workflow state.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `draft_id` | `string` | Yes | minimum length: `16`; maximum length: `100` |
| `values` | object of `string` | Yes | — |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `draft_id` | `string` | Yes | — |
| `item_id` | `string` | Yes | — |
| `title` | `string` | Yes | — |
| `source_url` | `string` | Yes | — |
| `expires_at` | `string` | Yes | format: `date-time` |
| `state` | `"prepared"`, `"submitting"`, `"submitted"`, `"uncertain"` | Yes | — |
| `ready` | `boolean` | Yes | — |
| `missing_fields` | array of `string` | Yes | — |
| `invalid_fields` | array of `string` | Yes | — |
| `fields` | array of [`DraftField`](types.md#mcp-type-draftfield) | Yes | — |
| `available_actions` | array of `string` | Yes | — |
| `receipt_id` | `string` or `null` | No | default: `null` |

Unknown fields are not accepted.

### `onestop_discard_request_draft`

Close and discard a local draft. This does not withdraw submitted requests. Previously uploaded server attachments follow ServiceNow retention; use delete_attachment first to remove editable temporary attachments.

This tool changes local workflow state.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `draft_id` | `string` | Yes | minimum length: `16`; maximum length: `100` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `operation` | `string` | Yes | — |
| `completed_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `resource_id` | `string` or `null` | Yes | — |
| `outcome` | `"completed"`, `"unchanged"`, `"uncertain"`, `"requires_user_action"` | Yes | — |
| `verified` | `boolean` | Yes | — |
| `message` | `string` or `null` | Yes | — |
| `references` | array of [`NamedValue`](types.md#mcp-type-namedvalue) | Yes | — |

Unknown fields are not accepted.

### `onestop_submit_request`

Execute a native action on a reviewed local draft: submit a real request, add it to your cart, or save it to favourites when that button is offered. Uses native form validation and one submission attempt. Reusing a completed draft returns its receipt. An uncertain result must be checked in the portal before another submission.

MCP host confirmation is required before this action.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `draft_id` | `string` | Yes | minimum length: `16`; maximum length: `100` |
| `action` | `"submit"`, `"add_to_cart"`, `"save_favourite"` | No | default: `"submit"` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `operation` | `string` | Yes | — |
| `completed_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `resource_id` | `string` or `null` | Yes | — |
| `outcome` | `"completed"`, `"unchanged"`, `"uncertain"`, `"requires_user_action"` | Yes | — |
| `verified` | `boolean` | Yes | — |
| `message` | `string` or `null` | Yes | — |
| `references` | array of [`NamedValue`](types.md#mcp-type-namedvalue) | Yes | — |

Unknown fields are not accepted.

### `onestop_reply_to_request`

Post a real additional comment to a verified own ticket/item when its current native state permits replying. Sends only to the comments journal, never work notes. Do not repeat an uncertain reply; inspect activity first.

MCP host confirmation is required before this action.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `request_id` | `string` | Yes | pattern: `^[0-9a-f]{32}$` |
| `text` | `string` | Yes | minimum length: `1`; maximum length: `20000` |
| `record_id` | `string` or `null` | No | default: `null`; pattern: `^[0-9a-f]{32}$` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `operation` | `string` | Yes | — |
| `completed_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `resource_id` | `string` or `null` | Yes | — |
| `outcome` | `"completed"`, `"unchanged"`, `"uncertain"`, `"requires_user_action"` | Yes | — |
| `verified` | `boolean` | Yes | — |
| `message` | `string` or `null` | Yes | — |
| `references` | array of [`NamedValue`](types.md#mcp-type-namedvalue) | Yes | — |

Unknown fields are not accepted.

### `onestop_take_request_action`

Execute a state action currently offered by the native own-ticket page. Read get_request_activity.available_actions first. Does not invent unavailable close/reopen/solution actions or accept arbitrary state/table values.

MCP host confirmation is required before this action.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `request_id` | `string` | Yes | pattern: `^[0-9a-f]{32}$` |
| `action` | `"close"`, `"reopen"`, `"accept_solution"`, `"reject_solution"` | Yes | — |
| `record_id` | `string` or `null` | No | default: `null`; pattern: `^[0-9a-f]{32}$` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `operation` | `string` | Yes | — |
| `completed_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `resource_id` | `string` or `null` | Yes | — |
| `outcome` | `"completed"`, `"unchanged"`, `"uncertain"`, `"requires_user_action"` | Yes | — |
| `verified` | `boolean` | Yes | — |
| `message` | `string` or `null` | Yes | — |
| `references` | array of [`NamedValue`](types.md#mcp-type-namedvalue) | Yes | — |

Unknown fields are not accepted.
