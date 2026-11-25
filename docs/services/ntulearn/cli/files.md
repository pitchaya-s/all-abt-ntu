# NTULearn: Attachments and downloads CLI commands

[Back to NTULearn CLI](index.md) · [MCP reference](../mcp/index.md)

- [`ntu learn attachments`](#cmd-learn-attachments)
- [`ntu learn courses download`](#cmd-learn-courses-download)
- [`ntu learn files read`](#cmd-learn-files-read)
- [`ntu learn files download`](#cmd-learn-files-download)
- [`ntu learn videos download`](#cmd-learn-videos-download)

## Command details

<a id="cmd-learn-attachments"></a>
### `ntu learn attachments`

List files attached to a course content item.

A supported NTULearn content URL can replace the course and content IDs.

#### Usage

```sh
ntu learn attachments ZZ0001 CONTENT_ID
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. `ZZ0001` is a fictional course code. Use `ntu learn attachments --help` for the current interface.

#### Arguments and options

- `COURSE_ID`: **Required.** A course code or Blackboard course ID from `ntu learn courses`.
- `CONTENT_ID`: The content ID returned when you browse the course. Where supported, a content URL can supply the course and content IDs.
- `--limit`, `-l`: Maximum number of results to return in this page. Default: `50`.
- `--offset`: Number of results to skip before this page. Default: `0`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `from_cache`, `cache_age_seconds`, `course_id`, `content_id`, `attachments`, `offset`, `next_offset`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/files.md#ntulearn_get_content_attachments).

<a id="cmd-learn-courses-download"></a>
### `ntu learn courses download`

Recursively save readable Blackboard attachments under destination/course_id with content folder names and stable file IDs.

This operation requires local confirmation and is refused when confirmation cannot be obtained interactively.

#### Usage

```sh
ntu learn courses download ZZ0001 --output ./course-materials
```

`ZZ0001` is a fictional course code. Use `ntu learn courses download --help` for the current interface.

#### Arguments and options

- `COURSE_ID`: **Required.** A course code or Blackboard course ID from `ntu learn courses`.
- `--output`, `-o`: **Required.** The local destination path. Follow the command description for file or directory requirements.
- `--max-depth`: Maximum nesting depth to traverse. Default: `5`.
- `--max-nodes`: Maximum number of content nodes to examine. Default: `1000`.
- `--max-files`: Maximum number of files to download. Default: `100`.
- `--max-total-mb`: Maximum total download size in megabytes. Default: `200`.
- `--max-requests`: Maximum number of upstream requests the operation may make. Default: `200`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `from_cache`, `cache_age_seconds`, `complete`, `requests_used`, `issues`, `course_id`, `destination`, `files`, `bytes_written`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/files.md#ntulearn_download_course).

<a id="cmd-learn-files-read"></a>
### `ntu learn files read`

Read an attachment inline as text: PDF, DOCX, PPTX, XLSX and UTF text/code.

When using a supported content URL as the first argument, provide the attachment ID as the second argument; a separate content ID is not needed.

#### Usage

```sh
ntu learn files read ZZ0001 CONTENT_ID ATTACHMENT_ID
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. `ZZ0001` is a fictional course code. Use `ntu learn files read --help` for the current interface.

#### Arguments and options

- `COURSE_ID`: **Required.** A course code or Blackboard course ID from `ntu learn courses`.
- `CONTENT_ID`: **Required.** The content ID returned when you browse the course. Where supported, a content URL can supply the course and content IDs.
- `ATTACHMENT_ID`: The attachment ID returned by the attachment listing.
- `--max-chars`: Maximum number of text characters to return. Default: `20000`.
- `--max-pages`: Maximum number of document pages to read. Default: `20`.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `course_id`, `content_id`, `attachment_id`, `file_name`, `text`, `truncated`, `pages_read`, `total_pages`, `retrieved_at`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/files.md#ntulearn_read_file_content).

<a id="cmd-learn-files-download"></a>
### `ntu learn files download`

Download a Blackboard attachment to an explicit local file path, up to 20 MB.

When using a supported content URL as the first argument, provide the attachment ID as the second argument; a separate content ID is not needed.

This operation requires local confirmation and is refused when confirmation cannot be obtained interactively.

#### Usage

```sh
ntu learn files download ZZ0001 CONTENT_ID ATTACHMENT_ID --output ./download.pdf
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. `ZZ0001` is a fictional course code. Use `ntu learn files download --help` for the current interface.

#### Arguments and options

- `COURSE_ID`: **Required.** A course code or Blackboard course ID from `ntu learn courses`.
- `CONTENT_ID`: **Required.** The content ID returned when you browse the course. Where supported, a content URL can supply the course and content IDs.
- `ATTACHMENT_ID`: The attachment ID returned by the attachment listing.
- `--output`, `-o`: **Required.** The local destination path. Follow the command description for file or directory requirements.
- `--max-bytes`: Maximum file size in bytes. Default: `20000000`.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `path`, `bytes_written`, `downloaded_at`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/files.md#ntulearn_download_file).

<a id="cmd-learn-videos-download"></a>
### `ntu learn videos download`

Download a Kaltura video embedded in an NTULearn content item to a new local file.

A supported NTULearn content URL can replace the course and content IDs.

This operation requires local confirmation and is refused when confirmation cannot be obtained interactively.

#### Usage

```sh
ntu learn videos download ZZ0001 CONTENT_ID --output ./lecture.mp4
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. `ZZ0001` is a fictional course code. Use `ntu learn videos download --help` for the current interface.

#### Arguments and options

- `COURSE_ID`: **Required.** A course code or Blackboard course ID from `ntu learn courses`.
- `CONTENT_ID`: The content ID returned when you browse the course. Where supported, a content URL can supply the course and content IDs.
- `--output`, `-o`: **Required.** The local destination path. Follow the command description for file or directory requirements.
- `--max-mb`: Maximum video size in megabytes. Default: `1000`.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `path`, `bytes_written`, `downloaded_at`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/files.md#ntulearn_download_video).
