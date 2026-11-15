# News: MCP reference

[Service overview](../index.md) · [CLI reference](../cli/index.md) · [MCP reference](index.md)

## Tools

Inputs are required only where marked. Output fields marked required may still be `null` when their type allows it. See the [data types](types.md) for object fields.

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
| `stories` | array of [`Story`](types.md#mcp-type-story) | Yes | — |
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
| `categories` | array of [`FilterOption`](types.md#mcp-type-filteroption) | Yes | — |

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

See the [MCP data types](types.md) for nested object fields.
