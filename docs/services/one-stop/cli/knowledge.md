# One Stop: Knowledge CLI commands

[One Stop overview](../index.md) · [All One Stop CLI topics](index.md) · [MCP reference](../mcp/index.md)

Search articles and inspect available feedback before adding a comment or changing a rating. Changes require confirmation.

```sh
ntu onestop knowledge search "transcript" --limit 10
```

Replace capitalized placeholders with values returned by the service. Use `--help` after a command for its current options. Choose a command to see its arguments, examples and result fields.

| Command | What it does |
| --- | --- |
| [`ntu onestop knowledge search`](knowledge.md#cmd-onestop-knowledge-search) | Search the signed-in student's One Stop knowledge base. |
| [`ntu onestop knowledge article`](knowledge.md#cmd-onestop-knowledge-article) | Read a knowledge article's text, text-template sections or wiki body by article_id from search_knowledge, with text pagination and source links. |
| [`ntu onestop knowledge feedback`](knowledge.md#cmd-onestop-knowledge-feedback) | Read native knowledge capabilities: ratings, helpfulness, comments, flags/reasons, subscription/inheritance, favourites and self-delivery channels. |
| [`ntu onestop knowledge rate`](knowledge.md#cmd-onestop-knowledge-rate) | Submit a 1–5 star knowledge rating when the native control is enabled. |
| [`ntu onestop knowledge helpful`](knowledge.md#cmd-onestop-knowledge-helpful) | Submit helpful/not-helpful feedback only when the article offers that native control. |
| [`ntu onestop knowledge flag`](knowledge.md#cmd-onestop-knowledge-flag) | Flag a knowledge article with the user's explanation when the native flag control is available. |
| [`ntu onestop knowledge subscribe`](knowledge.md#cmd-onestop-knowledge-subscribe) | Subscribe/unsubscribe to article updates. |
| [`ntu onestop knowledge favourite`](knowledge.md#cmd-onestop-knowledge-favourite) | Set an article's native favourite state when its Favourite control is enabled. |
| [`ntu onestop knowledge send-to-self`](knowledge.md#cmd-onestop-knowledge-send-to-self) | Send this article to your registered email/SMS channel using the native Send to myself action. |
| [`ntu onestop knowledge comments add`](knowledge.md#cmd-onestop-knowledge-comments-add) | Publish plain-text feedback to a knowledge article, or reply to a visible parent comment. |
| [`ntu onestop knowledge comments delete`](knowledge.md#cmd-onestop-knowledge-comments-delete) | Delete a visible article comment only when the native menu permits deletion by the current user. |
| [`ntu onestop knowledge comments like`](knowledge.md#cmd-onestop-knowledge-comments-like) | Like or unlike a visible knowledge comment using a desired state. |
| [`ntu onestop knowledge comments list`](knowledge.md#cmd-onestop-knowledge-comments-list) | Read visible knowledge comments/replies, author display names, text, dates, reactions, attachment IDs and delete permissions. |

## Command details

<a id="cmd-onestop-knowledge-search"></a>
### `ntu onestop knowledge search`

Search the signed-in student's One Stop knowledge base.

#### Usage

```sh
ntu onestop knowledge search example
```

Use `ntu onestop knowledge search --help` for the current interface.

#### Arguments and options

- `QUERY`: **Required.** The search terms. Quote multiword text so the shell passes it as one argument.
- `--limit`, `-l`: Maximum number of results to return in this page. Default: `20`.
- `--offset`: Number of results to skip before this page. Default: `0`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `offset`, `available_count`, `total_count`, `complete`, `next_offset`, `retrieved_at`, `source_url`, `cached`, `query`, `articles`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/knowledge.md#onestop_search_knowledge).

<a id="cmd-onestop-knowledge-article"></a>
### `ntu onestop knowledge article`

Read a knowledge article's text, text-template sections or wiki body by article_id from search_knowledge, with text pagination and source links.

#### Usage

```sh
ntu onestop knowledge article ARTICLE_ID
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu onestop knowledge article --help` for the current interface.

#### Arguments and options

- `ARTICLE_ID`: **Required.** The article ID returned by the relevant listing or details command.
- `--offset`: Number of results to skip before this page. Default: `0`.
- `--max-chars`: Maximum number of text characters to return. Default: `12000`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `article_id`, `number`, `title`, `updated_on`, `text`, `total_characters`, `offset`, `next_offset`, `links`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/knowledge.md#onestop_get_knowledge_article).

<a id="cmd-onestop-knowledge-feedback"></a>
### `ntu onestop knowledge feedback`

Read native knowledge capabilities: ratings, helpfulness, comments, flags/reasons, subscription/inheritance, favourites and self-delivery channels.

#### Usage

```sh
ntu onestop knowledge feedback ARTICLE_ID
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu onestop knowledge feedback --help` for the current interface.

#### Arguments and options

- `ARTICLE_ID`: **Required.** The article ID returned by the relevant listing or details command.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `article_id`, `can_rate`, `can_mark_helpful`, `can_comment`, `can_flag`, `can_subscribe`, `subscribed`, `inherited_subscription`, `can_favourite`, `favourite`, `send_channels`, `reasons`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/knowledge.md#onestop_get_article_feedback).

<a id="cmd-onestop-knowledge-rate"></a>
### `ntu onestop knowledge rate`

Submit a 1–5 star knowledge rating when the native control is enabled.

This operation requires local confirmation and is refused when confirmation cannot be obtained interactively.

#### Usage

```sh
ntu onestop knowledge rate ARTICLE_ID 5
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu onestop knowledge rate --help` for the current interface.

#### Arguments and options

- `ARTICLE_ID`: **Required.** The article ID returned by the relevant listing or details command.
- `RATING`: **Required.** The article rating.
- `--reason-id`: The reason ID returned by the relevant listing or details command.
- `--details`: Additional details for the selected feedback or action.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/knowledge.md#onestop_rate_article).

<a id="cmd-onestop-knowledge-helpful"></a>
### `ntu onestop knowledge helpful`

Submit helpful/not-helpful feedback only when the article offers that native control.

This operation requires local confirmation and is refused when confirmation cannot be obtained interactively.

#### Usage

```sh
ntu onestop knowledge helpful ARTICLE_ID yes
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu onestop knowledge helpful --help` for the current interface.

#### Arguments and options

- `ARTICLE_ID`: **Required.** The article ID returned by the relevant listing or details command.
- `HELPFUL`: **Required.** Choose whether the article was helpful. Choices: `yes`, `no`.
- `--reason-id`: The reason ID returned by the relevant listing or details command.
- `--details`: Additional details for the selected feedback or action.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/knowledge.md#onestop_set_article_helpful).

<a id="cmd-onestop-knowledge-flag"></a>
### `ntu onestop knowledge flag`

Flag a knowledge article with the user's explanation when the native flag control is available.

This operation requires local confirmation and is refused when confirmation cannot be obtained interactively.

#### Usage

```sh
ntu onestop knowledge flag ARTICLE_ID --text 'Example message'
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu onestop knowledge flag --help` for the current interface.

#### Arguments and options

- `ARTICLE_ID`: **Required.** The article ID returned by the relevant listing or details command.
- `--text`: **Required.** The text to send. Quote multiword text in the shell.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/knowledge.md#onestop_flag_article).

<a id="cmd-onestop-knowledge-subscribe"></a>
### `ntu onestop knowledge subscribe`

Subscribe/unsubscribe to article updates.

This operation requires local confirmation and is refused when confirmation cannot be obtained interactively.

#### Usage

```sh
ntu onestop knowledge subscribe ARTICLE_ID --state on
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu onestop knowledge subscribe --help` for the current interface.

#### Arguments and options

- `ARTICLE_ID`: **Required.** The article ID returned by the relevant listing or details command.
- `--state`: **Required.** The requested subscription state. Choices: `on`, `off`.
- `--include-knowledge-base`: Include the knowledge-base subscription where the native action supports it.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/knowledge.md#onestop_set_article_subscription).

<a id="cmd-onestop-knowledge-favourite"></a>
### `ntu onestop knowledge favourite`

Set an article's native favourite state when its Favourite control is enabled.

This operation requires local confirmation and is refused when confirmation cannot be obtained interactively.

#### Usage

```sh
ntu onestop knowledge favourite ARTICLE_ID --state on
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu onestop knowledge favourite --help` for the current interface.

#### Arguments and options

- `ARTICLE_ID`: **Required.** The article ID returned by the relevant listing or details command.
- `--state`: **Required.** The requested favourite state. Choices: `on`, `off`.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/knowledge.md#onestop_set_article_favourite).

<a id="cmd-onestop-knowledge-send-to-self"></a>
### `ntu onestop knowledge send-to-self`

Send this article to your registered email/SMS channel using the native Send to myself action.

This operation requires local confirmation and is refused when confirmation cannot be obtained interactively.

#### Usage

```sh
ntu onestop knowledge send-to-self ARTICLE_ID
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu onestop knowledge send-to-self --help` for the current interface.

#### Arguments and options

- `ARTICLE_ID`: **Required.** The article ID returned by the relevant listing or details command.
- `--channel`: The delivery channel offered by the service. Choices: `email`, `sms`. Default: `email`.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/knowledge.md#onestop_send_article_to_self).

<a id="cmd-onestop-knowledge-comments-add"></a>
### `ntu onestop knowledge comments add`

Publish plain-text feedback to a knowledge article, or reply to a visible parent comment.

This operation requires local confirmation and is refused when confirmation cannot be obtained interactively.

#### Usage

```sh
ntu onestop knowledge comments add ARTICLE_ID --text 'Example message'
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu onestop knowledge comments add --help` for the current interface.

#### Arguments and options

- `ARTICLE_ID`: **Required.** The article ID returned by the relevant listing or details command.
- `--text`: **Required.** The text to send. Quote multiword text in the shell.
- `--parent`: The ID of a parent folder. Omit it to browse the top level.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/knowledge.md#onestop_add_article_comment).

<a id="cmd-onestop-knowledge-comments-delete"></a>
### `ntu onestop knowledge comments delete`

Delete a visible article comment only when the native menu permits deletion by the current user.

This operation requires local confirmation and is refused when confirmation cannot be obtained interactively.

#### Usage

```sh
ntu onestop knowledge comments delete ARTICLE_ID COMMENT_ID
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu onestop knowledge comments delete --help` for the current interface.

#### Arguments and options

- `ARTICLE_ID`: **Required.** The article ID returned by the relevant listing or details command.
- `COMMENT_ID`: **Required.** The comment ID returned by the relevant listing or details command.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/knowledge.md#onestop_delete_article_comment).

<a id="cmd-onestop-knowledge-comments-like"></a>
### `ntu onestop knowledge comments like`

Like or unlike a visible knowledge comment using a desired state.

This operation requires local confirmation and is refused when confirmation cannot be obtained interactively.

#### Usage

```sh
ntu onestop knowledge comments like ARTICLE_ID COMMENT_ID --state on
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu onestop knowledge comments like --help` for the current interface.

#### Arguments and options

- `ARTICLE_ID`: **Required.** The article ID returned by the relevant listing or details command.
- `COMMENT_ID`: **Required.** The comment ID returned by the relevant listing or details command.
- `--state`: **Required.** Choose whether the comment should be liked. Choices: `on`, `off`.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/knowledge.md#onestop_set_article_comment_like).

<a id="cmd-onestop-knowledge-comments-list"></a>
### `ntu onestop knowledge comments list`

Read visible knowledge comments/replies, author display names, text, dates, reactions, attachment IDs and delete permissions.

#### Usage

```sh
ntu onestop knowledge comments list ARTICLE_ID
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu onestop knowledge comments list --help` for the current interface.

#### Arguments and options

- `ARTICLE_ID`: **Required.** The article ID returned by the relevant listing or details command.
- `--limit`, `-l`: Maximum number of results to return in this page. Default: `20`.
- `--offset`: Number of results to skip before this page. Default: `0`.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `offset`, `available_count`, `total_count`, `complete`, `next_offset`, `retrieved_at`, `source_url`, `cached`, `article_id`, `comments`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/knowledge.md#onestop_list_article_comments).
