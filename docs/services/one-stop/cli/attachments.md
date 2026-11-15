# One Stop: Attachments CLI commands

[One Stop overview](../index.md) · [All One Stop CLI topics](index.md) · [MCP reference](../mcp/index.md)

List files on a verified target before downloading or changing them. Uploads use the configured One Stop upload directory. Uploading, downloading, renaming and deleting require confirmation.

```sh
ntu onestop attachments list request:REQUEST_ID
```

Replace capitalized placeholders with values returned by the service. Use `--help` after a command for its current options. Choose a command to see its arguments, examples and result fields.

`TARGET` identifies the parent record:

- `request:REQUEST_ID` for one of your requests; use `--record-id` when its details identify a particular record.
- `article:ARTICLE_ID` for a readable knowledge article.
- `comment:ARTICLE_ID/COMMENT_ID` for a visible article comment.

Draft attachments are managed inside the interactive request workflow rather than by a separate CLI command.

| Command | What it does |
| --- | --- |
| [`ntu onestop attachments list`](attachments.md#cmd-onestop-attachments-list) | List attachments on a verified own request/item or a readable knowledge article/comment. |
| [`ntu onestop attachments upload`](attachments.md#cmd-onestop-attachments-upload) | Upload an explicitly selected file from the configured One Stop upload directory to the verified target. |
| [`ntu onestop attachments download`](attachments.md#cmd-onestop-attachments-download) | Download a listed attachment of the verified target to a new explicit absolute file path, up to 20 MB. |
| [`ntu onestop attachments delete`](attachments.md#cmd-onestop-attachments-delete) | Delete an attachment only when it is listed on the verified target and native editing is allowed. |
| [`ntu onestop attachments rename`](attachments.md#cmd-onestop-attachments-rename) | Rename a listed editable attachment using the native attachment service. |

## Command details

<a id="cmd-onestop-attachments-list"></a>
### `ntu onestop attachments list`

List attachments on a verified own request/item or a readable knowledge article/comment.

#### Usage

```sh
ntu onestop attachments list request:REQUEST_ID
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu onestop attachments list --help` for the current interface.

#### Arguments and options

- `TARGET`: **Required.** A verified target such as `request:REQUEST_ID`, `article:ARTICLE_ID`, or `comment:ARTICLE_ID/COMMENT_ID`.
- `--record-id`: A record ID for a request target when the request contains multiple records.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `attachments`, `can_upload`, `max_upload_bytes`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/attachments.md#onestop_list_attachments).

<a id="cmd-onestop-attachments-upload"></a>
### `ntu onestop attachments upload`

Upload an explicitly selected file from the configured One Stop upload directory to the verified target.

This operation requires local confirmation and is refused when confirmation cannot be obtained interactively.

#### Usage

```sh
ntu onestop attachments upload request:REQUEST_ID /absolute/path/to/onestop-uploads/upload.pdf
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu onestop attachments upload --help` for the current interface.

#### Arguments and options

- `TARGET`: **Required.** A verified target such as `request:REQUEST_ID`, `article:ARTICLE_ID`, or `comment:ARTICLE_ID/COMMENT_ID`.
- `FILE_PATH`: **Required.** The path of the local file to upload.
- `--record-id`: A record ID for a request target when the request contains multiple records.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/attachments.md#onestop_upload_attachment).

<a id="cmd-onestop-attachments-download"></a>
### `ntu onestop attachments download`

Download a listed attachment of the verified target to a new explicit absolute file path, up to 20 MB.

This operation requires local confirmation and is refused when confirmation cannot be obtained interactively.

#### Usage

```sh
ntu onestop attachments download request:REQUEST_ID ATTACHMENT_ID --output /absolute/path/attachment.pdf
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu onestop attachments download --help` for the current interface.

#### Arguments and options

- `TARGET`: **Required.** A verified target such as `request:REQUEST_ID`, `article:ARTICLE_ID`, or `comment:ARTICLE_ID/COMMENT_ID`.
- `ATTACHMENT_ID`: **Required.** The attachment ID returned by the attachment listing.
- `--output`, `-o`: **Required.** The local destination path. Follow the command description for file or directory requirements.
- `--record-id`: A record ID for a request target when the request contains multiple records.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `attachment_id`, `path`, `bytes_written`, `sha256`, `downloaded_at`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/attachments.md#onestop_download_attachment).

<a id="cmd-onestop-attachments-delete"></a>
### `ntu onestop attachments delete`

Delete an attachment only when it is listed on the verified target and native editing is allowed.

This operation requires local confirmation and is refused when confirmation cannot be obtained interactively.

#### Usage

```sh
ntu onestop attachments delete request:REQUEST_ID ATTACHMENT_ID
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu onestop attachments delete --help` for the current interface.

#### Arguments and options

- `TARGET`: **Required.** A verified target such as `request:REQUEST_ID`, `article:ARTICLE_ID`, or `comment:ARTICLE_ID/COMMENT_ID`.
- `ATTACHMENT_ID`: **Required.** The attachment ID returned by the attachment listing.
- `--record-id`: A record ID for a request target when the request contains multiple records.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/attachments.md#onestop_delete_attachment).

<a id="cmd-onestop-attachments-rename"></a>
### `ntu onestop attachments rename`

Rename a listed editable attachment using the native attachment service.

This operation requires local confirmation and is refused when confirmation cannot be obtained interactively.

#### Usage

```sh
ntu onestop attachments rename request:REQUEST_ID ATTACHMENT_ID renamed.pdf
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu onestop attachments rename --help` for the current interface.

#### Arguments and options

- `TARGET`: **Required.** A verified target such as `request:REQUEST_ID`, `article:ARTICLE_ID`, or `comment:ARTICLE_ID/COMMENT_ID`.
- `ATTACHMENT_ID`: **Required.** The attachment ID returned by the attachment listing.
- `FILE_NAME`: **Required.** The new file name, without a directory path.
- `--record-id`: A record ID for a request target when the request contains multiple records.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/attachments.md#onestop_rename_attachment).
