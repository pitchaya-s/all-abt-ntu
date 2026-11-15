# One Stop: Attachments MCP tools

[Service overview](../index.md) · [CLI reference](../cli/index.md) · [All MCP tools](index.md) · [Data types](types.md)

## Attachments

Attachment operations use a verified target, such as a request, draft, or knowledge article. Uploads are limited to the configured One Stop upload directory and require confirmation; downloads also require confirmation and an explicit destination.

### `onestop_list_attachments`

List attachments on a verified own request/item, a readable knowledge article/comment, or an active local draft. Returns IDs, names, sizes, URLs and upload/delete permissions. Article assets are read-only; comments are editable only when the native menu permits it.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `target` | [`RequestAttachmentTarget`](types.md#mcp-type-requestattachmenttarget) or [`ArticleAttachmentTarget`](types.md#mcp-type-articleattachmenttarget) or [`CommentAttachmentTarget`](types.md#mcp-type-commentattachmenttarget) or [`DraftAttachmentTarget`](types.md#mcp-type-draftattachmenttarget) | Yes | — |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `attachments` | array of [`Attachment`](types.md#mcp-type-attachment) | Yes | — |
| `can_upload` | `boolean` | Yes | — |
| `max_upload_bytes` | `integer` | Yes | — |

Unknown fields are not accepted.

### `onestop_upload_attachment`

Upload an explicitly selected file from the configured One Stop upload directory to the verified target. The default is the dedicated onestop-uploads folder in the app configuration directory; NTU_ONESTOP_UPLOAD_DIR can override it. Requires an absolute path and obeys the smaller of the source limit and 20 MB. Article-comment uploads are visible to the article audience. Never chooses files automatically.

MCP host confirmation is required before this action.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `target` | [`RequestAttachmentTarget`](types.md#mcp-type-requestattachmenttarget) or [`ArticleAttachmentTarget`](types.md#mcp-type-articleattachmenttarget) or [`CommentAttachmentTarget`](types.md#mcp-type-commentattachmenttarget) or [`DraftAttachmentTarget`](types.md#mcp-type-draftattachmenttarget) | Yes | — |
| `file_path` | `string` | Yes | — |

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

### `onestop_download_attachment`

Download a listed attachment of the verified target to a new explicit absolute file path, up to 20 MB. Existing files and symbolic-link destinations are refused. Returns file size and SHA-256; does not execute or automatically open files.

MCP host confirmation is required before this action.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `target` | [`RequestAttachmentTarget`](types.md#mcp-type-requestattachmenttarget) or [`ArticleAttachmentTarget`](types.md#mcp-type-articleattachmenttarget) or [`CommentAttachmentTarget`](types.md#mcp-type-commentattachmenttarget) or [`DraftAttachmentTarget`](types.md#mcp-type-draftattachmenttarget) | Yes | — |
| `attachment_id` | `string` | Yes | pattern: `^[0-9a-f]{32}$` |
| `destination` | `string` | Yes | — |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `attachment_id` | `string` | Yes | — |
| `path` | `string` | Yes | — |
| `bytes_written` | `integer` | Yes | — |
| `sha256` | `string` | Yes | — |
| `downloaded_at` | `string` | Yes | format: `date-time` |

Unknown fields are not accepted.

### `onestop_delete_attachment`

Delete an attachment only when it is listed on the verified target and native editing is allowed. Knowledge article assets and closed/read-only ticket attachments cannot be deleted.

MCP host confirmation is required before this action.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `target` | [`RequestAttachmentTarget`](types.md#mcp-type-requestattachmenttarget) or [`ArticleAttachmentTarget`](types.md#mcp-type-articleattachmenttarget) or [`CommentAttachmentTarget`](types.md#mcp-type-commentattachmenttarget) or [`DraftAttachmentTarget`](types.md#mcp-type-draftattachmenttarget) | Yes | — |
| `attachment_id` | `string` | Yes | pattern: `^[0-9a-f]{32}$` |

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

### `onestop_rename_attachment`

Rename a listed editable attachment using the native attachment service. The new name cannot contain path separators or control characters.

MCP host confirmation is required before this action.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `target` | [`RequestAttachmentTarget`](types.md#mcp-type-requestattachmenttarget) or [`ArticleAttachmentTarget`](types.md#mcp-type-articleattachmenttarget) or [`CommentAttachmentTarget`](types.md#mcp-type-commentattachmenttarget) or [`DraftAttachmentTarget`](types.md#mcp-type-draftattachmenttarget) | Yes | — |
| `attachment_id` | `string` | Yes | pattern: `^[0-9a-f]{32}$` |
| `file_name` | `string` | Yes | minimum length: `1`; maximum length: `200` |

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
