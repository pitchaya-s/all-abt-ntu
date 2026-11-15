# News

[CLI commands](#cli-commands) · [MCP tools](#mcp-tools) · [MCP data types](#mcp-data-types) · [Service notes](#service-notes)

For installation and shared authentication, see the [main README](../../README.md).

## CLI commands

The output column lists the JSON result fields; human-readable output is formatted for the terminal. Use `ntu news --help` and append `--help` to a command for option details. `VALUE` denotes an option value; required arguments and options are marked. See the [complete CLI reference](../COMMANDS.md) for shared settings and all services.

| Command | Arguments and options | Purpose | Output |
| --- | --- | --- | --- |
| `ntu news search` | `QUERY (optional)`, `--category VALUE`, `--sort VALUE [latest, oldest] (default: latest)`, `--page/-p VALUE (default: 1)`, `--refresh/-r`, `--json/-j` | Search public NTU news by keyword and optional category, sorted latest or oldest. | `retrieved_at`, `source_url`, `cached`, `stories`, `page`, `total_count`, `total_pages`, `next_page` ([schema](#news_search)) |
| `ntu news categories` | `--refresh/-r`, `--json/-j` | List current news category labels and filter IDs from NTU's official news form. | `retrieved_at`, `source_url`, `cached`, `categories` ([schema](#news_list_categories)) |
| `ntu news article` | `URL (required)`, `--offset VALUE`, `--max-chars VALUE (default: 12000)`, `--refresh/-r`, `--json/-j` | Read the published text of an NTU /news/detail/ article URL returned by news_search. | `retrieved_at`, `source_url`, `cached`, `title`, `published_date`, `text`, `total_characters`, `next_offset` ([schema](#news_get_article)) |

## MCP tools

Inputs are required only where marked. Output fields marked required may still be `null` when their type allows it. See the nested data types below for object fields.

### `news_search`

Search public NTU news by keyword and optional category, sorted latest or oldest. Omit query to browse. Copy category_id from news_list_categories. Returns titles, dates, URLs and summaries where supplied; pages start at 1 with up to ten stories. Follow next_page, then pass a story URL to news_get_article.

Optional inputs: `query`, `category_id`, `sort`, `page`, and `refresh`.

Search by keyword, up to 200 characters, or omit `query` to browse. `sort` is `latest`, the default, or `oldest`. `category_id` must be an ID from `news_list_categories`. Pages start at 1 and contain up to ten stories. Follow `next_page` until it is `null`; out-of-range pages return an error because NTU otherwise reports misleading zero totals.

```json
{"query": "quantum", "sort": "latest", "page": 1}
```

Returns story titles, URLs, published dates, summaries where supplied, total counts, and pagination. Dates retain NTU's display format, such as `21 Oct 2026`. A missing summary remains `null`.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `query` | `string` | No | maximum length: `200`; default: `""` |
| `category_id` | `string` or `null` | No | default: `null`; pattern: `^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$` |
| `sort` | `"latest"`, `"oldest"` | No | default: `"latest"` |
| `page` | `integer` | No | minimum: `1`; maximum: `10000`; default: `1` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `stories` | array of [`Story`](#mcp-type-story) | Yes | — |
| `page` | `integer` | Yes | minimum: `1` |
| `total_count` | `integer` | Yes | minimum: `0` |
| `total_pages` | `integer` | Yes | minimum: `0` |
| `next_page` | `integer` or `null` | Yes | minimum: `1` |

Unknown fields are not accepted.

### `news_list_categories`

List current news category labels and filter IDs from NTU's official news form. Pass a returned id as news_search.category_id; display labels are not filter values.

Optional input: `refresh`.

Lists current category labels and IDs from the official news page, including research, university, education, sustainability, and other published categories. Pass one returned `id` as `news_search.category_id`. Unknown IDs are rejected instead of returning an unfiltered listing.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `categories` | array of [`FilterOption`](#mcp-type-filteroption) | Yes | — |

Unknown fields are not accepted.

### `news_get_article`

Read the published text of an NTU /news/detail/ article URL returned by news_search. Returns its title, display date and bounded text, excluding navigation, related stories and scripts. Follow next_offset to continue reading. Does not download linked documents or fetch external articles.

Required: `url` from a search result. Optional: `offset`, default 0; `max_chars`, default 12000 and maximum 50000; and `refresh`.

Reads one `https://www.ntu.edu.sg/news/detail/…` article and extracts its title, display date, and text. Navigation, related stories, scripts, and styling are excluded. Returns `total_characters` and `next_offset`; pass the latter as `offset` to continue reading. Text slices retain their original boundaries so consecutive slices reconstruct the extracted text.

Only supported NTU news URLs are fetched. External pages, linked PDFs, images, and video are not retrieved. Unexpected or incomplete article markup returns an error rather than unrelated page text.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `url` | `string` | Yes | maximum length: `600`; pattern: `^https://www\.ntu\.edu\.sg/news/detail/[A-Za-z0-9][A-Za-z0-9_.-]{0,499}/?$` |
| `offset` | `integer` | No | minimum: `0`; default: `0` |
| `max_chars` | `integer` | No | minimum: `1`; maximum: `50000`; default: `12000` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `title` | `string` | Yes | minimum length: `1` |
| `published_date` | `string` or `null` | Yes | — |
| `text` | `string` | Yes | — |
| `total_characters` | `integer` | Yes | minimum: `1` |
| `next_offset` | `integer` or `null` | Yes | minimum: `0` |

Unknown fields are not accepted.

## MCP data types

These named types are used by the tool input and output fields above.

<a id="mcp-type-filteroption"></a>
### `FilterOption`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `id` | `string` | Yes | — |
| `name` | `string` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-story"></a>
### `Story`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `title` | `string` | Yes | minimum length: `1` |
| `url` | `string` | Yes | — |
| `published_date` | `string` or `null` | Yes | — |
| `summary` | `string` or `null` | Yes | — |

Unknown fields are not accepted.

## Service notes

Read-only tools for NTU's public news listing and article pages. No credentials or Chromium required.

### Requests and limitations

All results include `retrieved_at`, `source_url`, and `cached`. Responses are cached in memory for five minutes; `refresh: true` fetches them again. The shared public HTTP client pools connections, bounds responses to 8 MB, uses a 20-second timeout, and permits up to two in-flight requests per client with 250 ms default pacing. Public HTTP settings are documented in the [shared runtime guide](../shared/README.md#public-http-reads). Published news may be corrected or removed; cached results are snapshots.

### Sources

- [NTU news page](https://www.ntu.edu.sg/news/) supplies category labels and IDs, plus the supported sort values.
- [GetStories](https://www.ntu.edu.sg/news/GetStories/?categories=all&page=1&listingKeyword=&sort=latest) returns story cards and pagination. Verified parameters: `categories`, `page`, `listingKeyword`, and `sort`.
- Article URLs returned by the API supply the full published HTML text.

### Tests

Run from the repository root:

```sh
uv run python -m unittest discover -s tests/news -t . -v
uv run python -m tests.news.live_smoke
```

Offline tests use synthetic stories, category forms, and article markup. The opt-in live stdio smoke checks keyword search, categories, pagination, oldest-first ordering, empty results, current and older article text, chunking, and caching. It prints statuses without saving article bodies.
