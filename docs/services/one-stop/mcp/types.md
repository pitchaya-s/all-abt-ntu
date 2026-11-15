# One Stop @ SAC: MCP data types

[Service overview](../index.md) · [MCP reference](index.md)

## MCP data types

These named types describe nested fields in the [MCP tool reference](index.md). A required field may still be `null` when its type allows it.

<a id="mcp-type-activityentry"></a>
### `ActivityEntry`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `entry_id` | `string` | Yes | — |
| `author` | `string` or `null` | Yes | — |
| `created_on` | `string` or `null` | Yes | — |
| `kind` | `"comment"`, `"attachment"` | Yes | — |
| `text` | `string` | Yes | — |
| `attachment_id` | `string` or `null` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-appointmentslot"></a>
### `AppointmentSlot`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `slot_id` | `string` | Yes | — |
| `start` | `string` | Yes | — |
| `end` | `string` | Yes | — |
| `start_utc` | `string` or `null` | Yes | — |
| `end_utc` | `string` or `null` | Yes | — |
| `label` | `string` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-articleattachmenttarget"></a>
### `ArticleAttachmentTarget`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `kind` | `"article"` | Yes | — |
| `article_id` | `string` | Yes | pattern: `^[0-9a-f]{32}$` |

Unknown fields are not accepted.

<a id="mcp-type-articlecomment"></a>
### `ArticleComment`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `comment_id` | `string` | Yes | — |
| `parent_id` | `string` or `null` | Yes | — |
| `author` | `string` or `null` | Yes | — |
| `created_on` | `string` or `null` | Yes | — |
| `text` | `string` | Yes | — |
| `liked` | `boolean` | Yes | — |
| `can_delete` | `boolean` | Yes | — |
| `attachment_ids` | array of `string` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-attachment"></a>
### `Attachment`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `attachment_id` | `string` | Yes | — |
| `file_name` | `string` | Yes | — |
| `size_bytes` | `integer` or `null` | Yes | — |
| `size_label` | `string` or `null` | Yes | — |
| `content_type` | `string` or `null` | Yes | — |
| `url` | `string` | Yes | — |
| `can_delete` | `boolean` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-cartitem"></a>
### `CartItem`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `cart_item_id` | `string` | Yes | — |
| `item_id` | `string` or `null` | Yes | — |
| `title` | `string` | Yes | — |
| `quantity` | `integer` | Yes | — |
| `quantity_editable` | `boolean` | Yes | — |
| `price_label` | `string` or `null` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-catalogitem"></a>
### `CatalogItem`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `item_id` | `string` | Yes | — |
| `title` | `string` | Yes | — |
| `summary` | `string` or `null` | Yes | — |
| `kind` | `"form"`, `"external"`, `"knowledge"`, `"content"` | Yes | — |
| `url` | `string` | Yes | — |
| `form_item_id` | `string` or `null` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-category"></a>
### `Category`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `category_id` | `string` | Yes | — |
| `title` | `string` | Yes | — |
| `parent_id` | `string` or `null` | Yes | — |
| `item_count` | `integer` | Yes | — |
| `total_item_count` | `integer` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-choice"></a>
### `Choice`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `value` | `string` | Yes | — |
| `label` | `string` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-commentattachmenttarget"></a>
### `CommentAttachmentTarget`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `kind` | `"article_comment"` | Yes | — |
| `article_id` | `string` | Yes | pattern: `^[0-9a-f]{32}$` |
| `comment_id` | `string` | Yes | pattern: `^[0-9a-f]{32}$` |

Unknown fields are not accepted.

<a id="mcp-type-draftattachmenttarget"></a>
### `DraftAttachmentTarget`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `kind` | `"draft"` | Yes | — |
| `draft_id` | `string` | Yes | minimum length: `16`; maximum length: `100` |

Unknown fields are not accepted.

<a id="mcp-type-draftfield"></a>
### `DraftField`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `name` | `string` | Yes | — |
| `label` | `string` | Yes | — |
| `type` | `string` | Yes | — |
| `mandatory` | `boolean` | Yes | — |
| `read_only` | `boolean` | Yes | — |
| `choices` | array of [`Choice`](#mcp-type-choice) | Yes | — |
| `value` | `string` or `null` | Yes | — |
| `display_value` | `string` or `null` | Yes | — |
| `reference` | `boolean` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-favourite"></a>
### `Favourite`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `favourite_id` | `string` | Yes | — |
| `item_id` | `string` | Yes | — |
| `title` | `string` | Yes | — |
| `pinned` | `boolean` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-formfield"></a>
### `FormField`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `name` | `string` | Yes | — |
| `label` | `string` | Yes | — |
| `type` | `string` | Yes | — |
| `mandatory` | `boolean` | Yes | — |
| `read_only` | `boolean` | Yes | — |
| `choices` | array of [`Choice`](#mcp-type-choice) | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-knowledgeresult"></a>
### `KnowledgeResult`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `article_id` | `string` | Yes | — |
| `number` | `string` | Yes | — |
| `title` | `string` | Yes | — |
| `summary` | `string` or `null` | Yes | — |
| `published` | `string` or `null` | Yes | — |
| `url` | `string` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-link"></a>
### `Link`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `label` | `string` | Yes | — |
| `url` | `string` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-listcoverage"></a>
### `ListCoverage`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `kind` | `"case"`, `"request"` | Yes | — |
| `state_group` | `"open"`, `"closed"` | Yes | — |
| `available_count` | `integer` | Yes | — |
| `source_count` | `integer` | Yes | — |
| `source_count_is_lower_bound` | `boolean` | Yes | — |
| `complete` | `boolean` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-namedvalue"></a>
### `NamedValue`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `name` | `string` | Yes | — |
| `label` | `string` | Yes | — |
| `value` | `string` or `null` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-portalrecord"></a>
### `PortalRecord`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `record_id` | `string` or `null` | Yes | — |
| `title` | `string` | Yes | — |
| `url` | `string` or `null` | Yes | — |
| `fields` | array of [`NamedValue`](#mcp-type-namedvalue) | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-preference"></a>
### `Preference`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `name` | `string` | Yes | — |
| `label` | `string` | Yes | — |
| `value` | `string` or `null` | Yes | — |
| `enabled` | `boolean` | Yes | — |
| `choices` | array of [`Choice`](#mcp-type-choice) | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-profilefield"></a>
### `ProfileField`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `name` | `string` | Yes | — |
| `label` | `string` | Yes | — |
| `value` | `string` or `null` | Yes | — |
| `type` | `string` | Yes | — |
| `read_only` | `boolean` | Yes | — |
| `choices` | array of [`Choice`](#mcp-type-choice) | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-referencechoice"></a>
### `ReferenceChoice`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `value` | `string` | Yes | — |
| `label` | `string` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-requestattachmenttarget"></a>
### `RequestAttachmentTarget`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `kind` | `"request"` | Yes | — |
| `request_id` | `string` | Yes | pattern: `^[0-9a-f]{32}$` |
| `record_id` | `string` or `null` | No | default: `null`; pattern: `^[0-9a-f]{32}$` |

Unknown fields are not accepted.

<a id="mcp-type-requestitemstage"></a>
### `RequestItemStage`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `item_id` | `string` | Yes | — |
| `stage` | `string` or `null` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-requestrecorddetails"></a>
### `RequestRecordDetails`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `record_id` | `string` | Yes | — |
| `record_type` | `string` | Yes | — |
| `fields` | array of [`NamedValue`](#mcp-type-namedvalue) | Yes | — |
| `variables` | array of [`NamedValue`](#mcp-type-namedvalue) | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-requestsummary"></a>
### `RequestSummary`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `request_id` | `string` | Yes | — |
| `kind` | `"case"`, `"request"` | Yes | — |
| `state_group` | `"open"`, `"closed"` | Yes | — |
| `title` | `string` | Yes | — |
| `number` | `string` or `null` | Yes | — |
| `state` | `string` or `null` | Yes | — |
| `created_on` | `string` or `null` | Yes | — |
| `record_type` | `string` | Yes | — |
| `url` | `string` | Yes | — |
| `detail_supported` | `boolean` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-savedcart"></a>
### `SavedCart`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `cart_id` | `string` | Yes | — |
| `name` | `string` | Yes | — |

Unknown fields are not accepted.
