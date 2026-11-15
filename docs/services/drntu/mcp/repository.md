# DR-NTU: Repository search and metadata MCP tools

[Service overview](../index.md) · [CLI reference](../cli/index.md) · [All MCP tools](index.md) · [Data types](types.md)

## Repository search and metadata

Inputs are required only where marked. A required output field may still be `null` if its type allows it. See [data types](types.md) for nested objects.

### `drntu_search`

Search DR-NTU publications by keywords or Solr query. Returns concise titles, authors, dates, identifiers and rights. Scope to a community/collection UUID, or apply facet filters using field/value/operator. Set entity_type=Person or all explicitly for broader searches.

Required: `query`, up to 500 characters. Optional: `scope_id`, `entity_type`, `filters`, `page`, `page_size`, default 10, and `refresh`.

Searches publications by default. General DR-NTU search also returns researcher profiles; select `entity_type: "Person"` or `"all"` explicitly for those results. Each match returns the item UUID, title, entity type, authors, dates, identifiers, published rights, and repository URL. Use `drntu_get_item` for full published metadata and abstracts.

Queries support the repository's Solr syntax. `scope_id` restricts results to a community or collection UUID from `drntu_browse`. Structured filters have `field`, `value`, and `operator`, one of `equals`, `contains`, or `authority`, default `equals`. Up to ten filters are accepted; repeated fields are retained. Facet operators and field support depend on repository configuration.

```json
{"query": "machine learning", "page_size": 5}
```

```json
{"query": "machine learning", "filters": [{"field": "dateIssued", "value": "[2020 TO 2026]", "operator": "equals"}]}
```

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `query` | `string` | Yes | maximum length: `500` |
| `scope_id` | `string` or `null` | No | default: `null`; pattern: `^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$` |
| `entity_type` | `"Publication"`, `"Person"`, `"all"` | No | default: `"Publication"` |
| `filters` | array of [`SearchFilter`](types.md#mcp-type-searchfilter) or `null` | No | default: `null`; maximum items: `10` |
| `page` | `integer` | No | minimum: `0`; maximum: `100000`; default: `0` |
| `page_size` | `integer` | No | minimum: `1`; maximum: `50`; default: `10` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `query` | `string` | Yes | — |
| `items` | array of [`ItemSummary`](types.md#mcp-type-itemsummary) | Yes | — |
| `pagination` | [`Page`](types.md#mcp-type-page) | Yes | — |

Unknown fields are not accepted.

### `drntu_get_item`

Read a repository item's published metadata, including abstracts, citations, DOI, subjects and rights where supplied. Metadata values retain language tags. Public metadata does not establish full-text access.

Required: `item_id`, a UUID from search results. Optional: `refresh`.

Returns title, entity type, repository URL, last-modified/withdrawn information when supplied, and a dictionary of published metadata fields. Metadata values retain their language tags. Abstracts are normally in `dc.description.abstract`; citations, DOI, subjects, degree information, and rights appear when the source provides them. Unknown field names are retained. A single title identical to the top-level title is omitted from metadata only when it has no language tag; alternative and multilingual titles remain.

Public metadata does not prove that a paper's full text is publicly downloadable.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `item_id` | `string` | Yes | pattern: `^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `item_id` | `string` | Yes | — |
| `title` | `string` | Yes | — |
| `entity_type` | `string` or `null` | Yes | — |
| `url` | `string` | Yes | — |
| `last_modified` | `string` or `null` | Yes | — |
| `withdrawn` | `boolean` or `null` | Yes | — |
| `metadata` | object of array of [`MetadataValue`](types.md#mcp-type-metadatavalue) | Yes | — |

Unknown fields are not accepted.

### `drntu_browse`

Browse repository communities or collections. Omit community_id for all; supply it for subcommunities or collections within that community. Use returned container_id as search scope_id. Negative/unavailable archived item counts become null.

Optional: `kind`, either `communities`, default, or `collections`; `community_id`; pagination; and `refresh`.

Without `community_id`, lists repository communities or collections. With a community UUID, lists its subcommunities or collections. Returns container IDs, names, published descriptions, and archived-item counts when known. DSpace's `-1` count means unavailable and becomes `null`. Use a returned `container_id` as `drntu_search.scope_id`.

```json
{"kind": "collections", "page_size": 10}
```

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `kind` | `"communities"`, `"collections"` | No | default: `"communities"` |
| `community_id` | `string` or `null` | No | default: `null`; pattern: `^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$` |
| `page` | `integer` | No | minimum: `0`; maximum: `100000`; default: `0` |
| `page_size` | `integer` | No | minimum: `1`; maximum: `50`; default: `20` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `kind` | `"communities"`, `"collections"` | Yes | — |
| `containers` | array of [`Container`](types.md#mcp-type-container) | Yes | — |
| `pagination` | [`Page`](types.md#mcp-type-page) | Yes | — |

Unknown fields are not accepted.

### `drntu_get_facets`

Discover search facet names, or supply a facet name to list its values and counts for the query/scope/filters. Facet definitions have no counts. Copy each value's filter object into search filters; date range labels can differ from their query values.

Optional: `facet`, `query`, `scope_id`, `entity_type`, `filters`, pagination, and `refresh`. The query/scope/filter options match search; entity type defaults to `Publication`.

Omit `facet` to discover filter definitions, such as `author`, `subject`, `dateIssued`, or `entityType`. Supply a name to get values and counts. Definitions are configuration metadata and have no result counts.

Each value includes a ready-to-use `filter` object extracted from the repository's own search link, when supplied. Copy it into `drntu_search.filters`. Display labels can differ from query values: a date label such as `2020 - 2026` may require `[2020 TO 2026]`. Authority-based values can also differ from their labels. Missing filter links remain `null`.

```json
{"facet": "dateIssued", "query": "machine learning", "page_size": 5}
```

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `facet` | `string` or `null` | No | default: `null`; pattern: `^[A-Za-z][A-Za-z0-9_.-]{0,79}$` |
| `query` | `string` | No | maximum length: `500`; default: `""` |
| `scope_id` | `string` or `null` | No | default: `null`; pattern: `^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$` |
| `entity_type` | `"Publication"`, `"Person"`, `"all"` | No | default: `"Publication"` |
| `filters` | array of [`SearchFilter`](types.md#mcp-type-searchfilter) or `null` | No | default: `null`; maximum items: `10` |
| `page` | `integer` | No | minimum: `0`; maximum: `100000`; default: `0` |
| `page_size` | `integer` | No | minimum: `1`; maximum: `50`; default: `10` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `facet` | `string` or `null` | Yes | — |
| `definitions` | array of [`FacetDefinition`](types.md#mcp-type-facetdefinition) | Yes | — |
| `values` | array of [`FacetValue`](types.md#mcp-type-facetvalue) | Yes | — |
| `pagination` | [`Page`](types.md#mcp-type-page) or `null` | Yes | — |

Unknown fields are not accepted.

### `drntu_list_bundles`

List an item's file groups. ORIGINAL usually holds deposited papers; TEXT, THUMBNAIL and LICENSE are separate bundles. Pass a returned bundle_id to drntu_list_files.

Required: `item_id`. Optional: pagination and `refresh`.

Returns named file groups and their UUIDs. `ORIGINAL` usually contains deposited papers; `TEXT`, `LICENSE`, and `THUMBNAIL` are different groups. Pass a returned `bundle_id` to `drntu_list_files`. Follow bundle pagination before assuming an item has no originals.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `item_id` | `string` | Yes | pattern: `^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$` |
| `page` | `integer` | No | minimum: `0`; maximum: `100000`; default: `0` |
| `page_size` | `integer` | No | minimum: `1`; maximum: `50`; default: `20` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `item_id` | `string` | Yes | — |
| `bundles` | array of [`Bundle`](types.md#mcp-type-bundle) | Yes | — |
| `pagination` | [`Page`](types.md#mcp-type-page) | Yes | — |

Unknown fields are not accepted.

### `drntu_list_files`

List a bundle's file metadata: names, byte sizes, checksums, published rights and content URLs. Does not fetch file bytes or verify download permission. Restricted content remains restricted even when its metadata is public.

Required: `bundle_id`. Optional: pagination and `refresh`.

Returns published file UUIDs, names, byte sizes, checksums, rights, and content URLs. No file bodies are fetched, and download permission is not tested. The example supplied for development has public metadata with `restricted` rights; the integration preserves those rights. Missing rights remain an empty list of published statements, which does not establish open access.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `bundle_id` | `string` | Yes | pattern: `^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$` |
| `page` | `integer` | No | minimum: `0`; maximum: `100000`; default: `0` |
| `page_size` | `integer` | No | minimum: `1`; maximum: `50`; default: `20` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `bundle_id` | `string` | Yes | — |
| `files` | array of [`File`](types.md#mcp-type-file) | Yes | — |
| `pagination` | [`Page`](types.md#mcp-type-page) | Yes | — |

Unknown fields are not accepted.

### `drntu_get_dataset`

Read a published DR-NTU Data dataset by doi: identifier: title, authors, descriptions, subjects, license and paginated file inventory. Omit version for latest, or use a release such as 1.0. CAPTCHA/access denials are returned as actionable errors without bypass or login.

Required: `persistent_id` in `doi:` form. Optional: `version` such as `1.0`, `limit` from 1–50, default 50, `offset`, default 0, and `refresh`.

Reads a published DR-NTU (Data) dataset's citation metadata and file inventory: title, authors, descriptions, subjects, release version/state, publication date, license, filenames, sizes, media types, directory labels, restriction flags, and checksums where provided. Omit `version` for the latest published version. Draft versions are unsupported. Unknown restriction flags remain `null`.

The dataset API returns the complete version metadata; `limit` and `offset` bound the files returned through MCP. Follow `next_offset` until `null`. Very large source responses may exceed the HTTP size limit. Additional discipline-specific dataset metadata is not exposed by this concise citation view.

```json
{"persistent_id": "doi:10.21979/N9/UD1IM9", "version": "1.0", "limit": 10}
```

HTML responses, including CAPTCHA pages with HTTP 200, and access denials stop retrieval with an actionable error. The integration does not start a browser, collect credentials, solve CAPTCHA, or reuse personal NTU sessions.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `persistent_id` | `string` | Yes | maximum length: `250`; pattern: `^doi:10\.[0-9]{4,9}/[^\s?#]+$` |
| `version` | `string` or `null` | No | default: `null`; maximum length: `20`; pattern: `^[0-9]+\.[0-9]+$` |
| `limit` | `integer` | No | minimum: `1`; maximum: `50`; default: `50` |
| `offset` | `integer` | No | minimum: `0`; default: `0` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `persistent_id` | `string` | Yes | — |
| `dataset_id` | `integer` | Yes | greater than: `0` |
| `version` | `string` | Yes | — |
| `version_state` | `string` | Yes | — |
| `title` | `string` or `null` | Yes | — |
| `authors` | array of `string` | Yes | — |
| `descriptions` | array of `string` | Yes | — |
| `subjects` | array of `string` | Yes | — |
| `publication_date` | `string` or `null` | Yes | — |
| `license_name` | `string` or `null` | Yes | — |
| `license_url` | `string` or `null` | Yes | — |
| `url` | `string` | Yes | — |
| `files` | array of [`DatasetFile`](types.md#mcp-type-datasetfile) | Yes | — |
| `total_files` | `integer` | Yes | minimum: `0` |
| `next_offset` | `integer` or `null` | Yes | minimum: `0` |

Unknown fields are not accepted.
