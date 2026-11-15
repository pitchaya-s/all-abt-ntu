# News: CLI reference

[Service overview](../index.md) · [CLI reference](index.md) · [MCP reference](../mcp/index.md)

## Example

Find news stories by keyword.

```sh
ntu news search "artificial intelligence" --sort latest --page 1
```

## Commands

Choose a command for its arguments, examples and result fields. Use `ntu news --help` and append `--help` to a command for option details. Each command page identifies required arguments and any defaults. See the [complete CLI reference](../../../cli/commands.md) for shared settings and all services.

| Command | What it does |
| --- | --- |
| [`ntu news search`](index.md#cmd-news-search) | Search public NTU news by keyword and optional category, sorted latest or oldest. |
| [`ntu news categories`](index.md#cmd-news-categories) | List current news category labels and filter IDs from NTU's official news form. |
| [`ntu news article`](index.md#cmd-news-article) | Read the published text of an NTU /news/detail/ article URL returned by news_search. |

## Command details

<a id="cmd-news-search"></a>
### `ntu news search`

Search public NTU news by keyword and optional category, sorted latest or oldest.

#### Usage

```sh
ntu news search "artificial intelligence" --sort latest --page 1
```

Use `ntu news search --help` for the current interface.

#### Arguments and options

- `QUERY`: The search terms. Quote multiword text so the shell passes it as one argument.
- `--category`: The category ID returned by the relevant listing or details command.
- `--sort`: The order in which results should be returned. Choices: `latest`, `oldest`. Default: `latest`.
- `--page`, `-p`: Page number to request; page numbering depends on the service. Default: `1`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `stories`, `page`, `total_count`, `total_pages`, `next_page`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/index.md#news_search).

<a id="cmd-news-categories"></a>
### `ntu news categories`

List current news category labels and filter IDs from NTU's official news form.

#### Usage

```sh
ntu news categories
```

Use `ntu news categories --help` for the current interface.

#### Arguments and options

- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `categories`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/index.md#news_list_categories).

<a id="cmd-news-article"></a>
### `ntu news article`

Read the published text of an NTU /news/detail/ article URL returned by news_search.

#### Usage

```sh
ntu news article URL
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu news article --help` for the current interface.

#### Arguments and options

- `URL`: **Required.** The URL of the record or article returned by a search.
- `--offset`: Number of results to skip before this page. Default: `0`.
- `--max-chars`: Maximum number of text characters to return. Default: `12000`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `title`, `published_date`, `text`, `total_characters`, `next_offset`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/index.md#news_get_article).
