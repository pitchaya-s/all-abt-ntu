# NTULearn: Attachments and downloads MCP tools

[Service overview](../index.md) · [CLI reference](../cli/index.md) · [All MCP tools](index.md) · [Data types](types.md)

## Attachments and downloads

Inputs are required only where marked. A required output field may still be `null` if its type allows it. See [data types](types.md) for nested objects.

### `ntulearn_get_content_attachments`

List files attached to a course content item. Use a leaf content ID rather than a folder. Some external/LTI content has no downloadable Blackboard attachment.

**Inputs:** `course_id`, `content_id`; common pagination and refresh parameters. Use a leaf content item rather than a folder.

**Returns:** attachment IDs, filenames, and MIME types when provided. Some external/LTI items do not expose Blackboard attachment files.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_id` | `string` | Yes | Blackboard course ID or enrolled course code; pattern: `^[A-Za-z0-9_-]{1,80}$` |
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
| `attachments` | array of [`Attachment`](types.md#mcp-type-attachment) | Yes | — |
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
| `course_id` | `string` | Yes | Blackboard course ID or enrolled course code; pattern: `^[A-Za-z0-9_-]{1,80}$` |
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

### `ntulearn_download_file`

Download a Blackboard attachment to an explicit local file path, up to 20 MB. Never overwrites an existing file. Does not modify NTULearn or forward university cookies to file-delivery hosts.

**Inputs:** `course_id`, `content_id`, `attachment_id`, and an explicit local `destination` file path. Its parent directory must already exist.

**Returns:** saved path, bytes written, and download time. Saves at most 20 MB and never overwrites an existing file. It writes locally and does not modify NTULearn. Supported redirects stay on NTU or Blackboard delivery hosts; university cookies are not forwarded to delivery hosts. HTML/JSON attachments are unsupported.

MCP host confirmation is required before this action.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_id` | `string` | Yes | Blackboard course ID or enrolled course code; pattern: `^[A-Za-z0-9_-]{1,80}$` |
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
| `course_id` | `string` | Yes | Blackboard course ID or enrolled course code; pattern: `^[A-Za-z0-9_-]{1,80}$` |
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
| `course_id` | `string` | Yes | Blackboard course ID or enrolled course code; pattern: `^[A-Za-z0-9_-]{1,80}$` |
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
| `issues` | array of [`Issue`](types.md#mcp-type-issue) | Yes | — |
| `course_id` | `string` | Yes | — |
| `destination` | `string` | Yes | — |
| `files` | array of [`CourseDownloadFile`](types.md#mcp-type-coursedownloadfile) | Yes | — |
| `bytes_written` | `integer` | Yes | — |

See the [MCP data types](types.md) for nested object fields.
