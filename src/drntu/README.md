# DR-NTU tools

[CLI commands](#cli-commands) · [MCP tools](#mcp-tools) · [MCP data types](#mcp-data-types) · [Service notes](#service-notes)

For installation and shared authentication, see the [main README](../../README.md).

## CLI commands

The output column lists the JSON result fields; human-readable output is formatted for the terminal. Use `ntu research --help` and append `--help` to a command for option details. `VALUE` denotes an option value; required arguments and options are marked. See the [complete CLI reference](../COMMANDS.md) for shared settings and all services.

| Command | Arguments and options | Purpose | Output |
| --- | --- | --- | --- |
| `ntu research search` | `QUERY (required)`, `--scope VALUE`, `--entity-type VALUE [Publication, Person, all] (default: Publication)`, `--filters VALUE`, `--page/-p VALUE`, `--page-size VALUE (default: 10)`, `--refresh/-r`, `--json/-j` | Search DR-NTU publications by keywords or Solr query. | `retrieved_at`, `source_url`, `cached`, `query`, `items`, `pagination` ([schema](#drntu_search)) |
| `ntu research facets` | `--facet VALUE`, `--query VALUE (default: )`, `--scope VALUE`, `--entity-type VALUE [Publication, Person, all] (default: Publication)`, `--filters VALUE`, `--page/-p VALUE`, `--page-size VALUE (default: 10)`, `--refresh/-r`, `--json/-j` | Discover search facet names, or supply a facet name to list its values and counts for the query/scope/filters. | `retrieved_at`, `source_url`, `cached`, `facet`, `definitions`, `values`, `pagination` ([schema](#drntu_get_facets)) |
| `ntu research dataset` | `PERSISTENT_ID (required)`, `--version VALUE`, `--limit/-l VALUE (default: 50)`, `--offset VALUE`, `--refresh/-r`, `--json/-j` | Read a published DR-NTU Data dataset by doi: identifier: title, authors, descriptions, subjects, license and paginated file inventory. | `retrieved_at`, `source_url`, `cached`, `persistent_id`, `dataset_id`, `version`, `version_state`, `title`, `authors`, `descriptions`, `subjects`, `publication_date`, `license_name`, `license_url`, `url`, `files`, `total_files`, `next_offset` ([schema](#drntu_get_dataset)) |
| `ntu research browse communities` | `--community VALUE`, `--page/-p VALUE`, `--page-size VALUE (default: 20)`, `--refresh/-r`, `--json/-j` | Browse repository communities or collections. | `retrieved_at`, `source_url`, `cached`, `kind`, `containers`, `pagination` ([schema](#drntu_browse)) |
| `ntu research browse collections` | `--community VALUE`, `--page/-p VALUE`, `--page-size VALUE (default: 20)`, `--refresh/-r`, `--json/-j` | Browse repository communities or collections. | `retrieved_at`, `source_url`, `cached`, `kind`, `containers`, `pagination` ([schema](#drntu_browse)) |
| `ntu research bundle files` | `BUNDLE_ID (required)`, `--page/-p VALUE`, `--page-size VALUE (default: 20)`, `--refresh/-r`, `--json/-j` | List a bundle's file metadata: names, byte sizes, checksums, published rights and content URLs. | `retrieved_at`, `source_url`, `cached`, `bundle_id`, `files`, `pagination` ([schema](#drntu_list_files)) |
| `ntu research item bundles` | `ITEM_ID (required)`, `--page/-p VALUE`, `--page-size VALUE (default: 20)`, `--refresh/-r`, `--json/-j` | List an item's file groups. | `retrieved_at`, `source_url`, `cached`, `item_id`, `bundles`, `pagination` ([schema](#drntu_list_bundles)) |
| `ntu research item show` | `ITEM_ID (required)`, `--refresh/-r`, `--json/-j` | Read a repository item's published metadata, including abstracts, citations, DOI, subjects and rights where supplied. | `retrieved_at`, `source_url`, `cached`, `item_id`, `title`, `entity_type`, `url`, `last_modified`, `withdrawn`, `metadata` ([schema](#drntu_get_item)) |
| `ntu research oai info` | `--refresh/-r`, `--json/-j` | Describe DR-NTU's OAI-PMH repository, modification-date precision, deletion policy and earliest datestamp. | `retrieved_at`, `source_url`, `cached`, `response_date`, `repository_name`, `base_url`, `protocol_version`, `admin_emails`, `earliest_datestamp`, `deleted_record`, `granularity`, `descriptions_xml` ([schema](#drntu_oai_identify)) |
| `ntu research oai formats` | `IDENTIFIER (optional)`, `--refresh/-r`, `--json/-j` | List OAI metadata prefixes, namespaces and schemas. | `retrieved_at`, `source_url`, `cached`, `response_date`, `formats` ([schema](#drntu_oai_list_metadata_formats)) |
| `ntu research oai sets` | `--token VALUE`, `--limit/-l VALUE (default: 20)`, `--offset VALUE`, `--refresh/-r`, `--json/-j` | List OAI collection/community sets. | `retrieved_at`, `source_url`, `cached`, `response_date`, `sets`, `pagination` ([schema](#drntu_oai_list_sets)) |
| `ntu research oai records` | `--prefix VALUE`, `--set VALUE`, `--from-date VALUE`, `--until-date VALUE`, `--token VALUE`, `--headers-only`, `--limit/-l VALUE (default: 10)`, `--offset VALUE`, `--refresh/-r`, `--json/-j` | Read one bounded OAI records page, defaulting to oai_dc. | `retrieved_at`, `source_url`, `cached`, `response_date`, `headers_only`, `records`, `pagination` ([schema](#drntu_oai_list_records)) |
| `ntu research oai record` | `IDENTIFIER (required)`, `--prefix VALUE (default: oai_dc)`, `--refresh/-r`, `--json/-j` | Get one record by its OAI identifier, not a REST UUID. | `retrieved_at`, `source_url`, `cached`, `response_date`, `metadata_prefix`, `record` ([schema](#drntu_oai_get_record)) |

## MCP tools

Inputs are required only where marked. Output fields marked required may still be `null` when their type allows it. See the nested data types below for object fields.

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
| `filters` | array of [`SearchFilter`](#mcp-type-searchfilter) or `null` | No | default: `null`; maximum items: `10` |
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
| `items` | array of [`ItemSummary`](#mcp-type-itemsummary) | Yes | — |
| `pagination` | [`Page`](#mcp-type-page) | Yes | — |

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
| `metadata` | object of array of [`MetadataValue`](#mcp-type-metadatavalue) | Yes | — |

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
| `containers` | array of [`Container`](#mcp-type-container) | Yes | — |
| `pagination` | [`Page`](#mcp-type-page) | Yes | — |

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
| `filters` | array of [`SearchFilter`](#mcp-type-searchfilter) or `null` | No | default: `null`; maximum items: `10` |
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
| `definitions` | array of [`FacetDefinition`](#mcp-type-facetdefinition) | Yes | — |
| `values` | array of [`FacetValue`](#mcp-type-facetvalue) | Yes | — |
| `pagination` | [`Page`](#mcp-type-page) or `null` | Yes | — |

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
| `bundles` | array of [`Bundle`](#mcp-type-bundle) | Yes | — |
| `pagination` | [`Page`](#mcp-type-page) | Yes | — |

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
| `files` | array of [`File`](#mcp-type-file) | Yes | — |
| `pagination` | [`Page`](#mcp-type-page) | Yes | — |

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
| `files` | array of [`DatasetFile`](#mcp-type-datasetfile) | Yes | — |
| `total_files` | `integer` | Yes | minimum: `0` |
| `next_offset` | `integer` or `null` | Yes | minimum: `0` |

Unknown fields are not accepted.

### `drntu_oai_identify`

Describe DR-NTU's OAI-PMH repository, modification-date precision, deletion policy and earliest datestamp. Public metadata only.

Optional: `refresh`.

Returns the OAI repository name, base URL, protocol version, administrator contacts, earliest modification datestamp, deletion policy, date precision, response date, and repository descriptions as XML. These are public repository details, not a student's profile.

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
| `response_date` | `string` | Yes | — |
| `repository_name` | `string` | Yes | — |
| `base_url` | `string` | Yes | — |
| `protocol_version` | `"2.0"` | Yes | — |
| `admin_emails` | array of `string` | Yes | — |
| `earliest_datestamp` | `string` | Yes | — |
| `deleted_record` | `"no"`, `"transient"`, `"persistent"` | Yes | — |
| `granularity` | `"YYYY-MM-DD"`, `"YYYY-MM-DDThh:mm:ssZ"` | Yes | — |
| `descriptions_xml` | array of `string` | Yes | — |

Unknown fields are not accepted.

### `drntu_oai_list_metadata_formats`

List OAI metadata prefixes, namespaces and schemas. Optionally supply an OAI identifier to discover formats available for one record.

Optional: `identifier`, an OAI identifier from the record tools, and `refresh`.

Lists metadata prefixes, schema URLs, and namespaces supported by the repository, or by one identifier. Schemas are reported without downloading or resolving them. The current public endpoint advertises formats including `oai_dc`, `qdc`, `mods`, and `dim`; discover available values instead of assuming a format applies to every record.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `identifier` | `string` or `null` | No | default: `null`; maximum length: `500`; pattern: `^oai:dr\.ntu\.edu\.sg:[^\s\x00-\x1f\x7f]+$` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `response_date` | `string` | Yes | — |
| `formats` | array of [`OAIMetadataFormat`](#mcp-type-oaimetadataformat) | Yes | — |

Unknown fields are not accepted.

### `drntu_oai_list_sets`

List OAI collection/community sets. limit/offset slice one NTU response page. Follow next_offset first, then resumption_token with offset=0. Use returned set_spec to filter OAI records.

Optional: `resumption_token`, `limit` from 1–50, default 20, `offset`, default 0, and `refresh`.

Lists OAI sets with `set_spec`, name, and any descriptions as XML. Set specs are OAI identifiers, not REST community/collection UUIDs. Use them as `set_spec` in record listings.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `resumption_token` | `string` or `null` | No | default: `null`; minimum length: `1`; maximum length: `8192`; pattern: `^[^\x00-\x1f\x7f]+$` |
| `limit` | `integer` | No | minimum: `1`; maximum: `50`; default: `20` |
| `offset` | `integer` | No | minimum: `0`; maximum: `100000`; default: `0` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `response_date` | `string` | Yes | — |
| `sets` | array of [`OAISet`](#mcp-type-oaiset) | Yes | — |
| `pagination` | [`OAIPagination`](#mcp-type-oaipagination) | Yes | — |

Unknown fields are not accepted.

### `drntu_oai_list_records`

Read one bounded OAI records page, defaulting to oai_dc. Set headers_only=true for ListIdentifiers. Dates filter inclusive modification/deletion datestamps, not publication dates; use matching precision. Follow next_offset with unchanged arguments before using the next resumption_token. A token excludes metadata_prefix, set_spec and both dates; reset offset=0 and keep headers_only unchanged. Deleted records have no metadata. No automatic bulk harvest.

Optional: `metadata_prefix`, defaulting to `oai_dc` when omitted on an initial request; `set_spec`; `from_date`; `until_date`; `resumption_token`; `headers_only`, default false; `limit` from 1–50, default 10; `offset`, default 0; and `refresh`.

Uses `ListRecords`, or `ListIdentifiers` when `headers_only` is true. Date bounds are inclusive repository modification/deletion datestamps, **not publication dates**. Use valid `YYYY-MM-DD` dates or UTC `YYYY-MM-DDTHH:MM:SSZ` timestamps. When both bounds are present, their precision must match and the start must not exceed the end.

```json
{"from_date": "2026-01-01", "until_date": "2026-01-02", "limit": 5}
```

Each result preserves the OAI identifier, datestamp, set specs, and deleted status. Deleted records and identifier-only listings have no metadata. Flat Dublin Core is normalized into repeated `dc.*` fields with values and language tags. Other formats, nested metadata, and unknown field attributes retain `metadata_xml`; provenance is preserved in `about_xml`. Identifiers and rights inside metadata do not establish permission to download the underlying files. `noRecordsMatch` returns an empty result; malformed responses and other OAI errors fail clearly.

OAI pagination differs from REST pagination. NTU chooses its own response-page size; `limit` and `offset` slice that page locally. `pagination.page_count` is the number of records in that provider page, not the repository total. Follow `next_offset` using the same arguments, including the current token and filters. Once it is null, use the returned `resumption_token` with `offset: 0`, omit **all** selection filters including `metadata_prefix`, and keep `headers_only` unchanged. A null token means no further provider page. Cursor, complete-list size, and token expiration are returned only when supplied by NTU; cursor values are preserved without interpreting them as local offsets.

```json
{"resumption_token": "TOKEN_RETURNED_BY_NTU", "limit": 5}
```

Tokens are opaque and can expire. On `badResumptionToken`, restart with the original filters and `refresh: true`. The server never follows every continuation automatically or stores a harvested database.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `metadata_prefix` | `string` or `null` | No | default: `null`; maximum length: `100`; pattern: `^[A-Za-z0-9_.-]+$` |
| `set_spec` | `string` or `null` | No | default: `null`; maximum length: `500`; pattern: `^[^\s\x00-\x1f\x7f]+$` |
| `from_date` | `string` or `null` | No | default: `null`; Inclusive OAI modification datestamp, in UTC; not a publication date; pattern: `^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}Z)?$` |
| `until_date` | `string` or `null` | No | default: `null`; Inclusive OAI modification datestamp, in UTC; not a publication date; pattern: `^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}Z)?$` |
| `resumption_token` | `string` or `null` | No | default: `null`; minimum length: `1`; maximum length: `8192`; pattern: `^[^\x00-\x1f\x7f]+$` |
| `headers_only` | `boolean` | No | default: `false` |
| `limit` | `integer` | No | minimum: `1`; maximum: `50`; default: `10` |
| `offset` | `integer` | No | minimum: `0`; maximum: `100000`; default: `0` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `response_date` | `string` | Yes | — |
| `headers_only` | `boolean` | Yes | — |
| `records` | array of [`OAIRecord`](#mcp-type-oairecord) | Yes | — |
| `pagination` | [`OAIPagination`](#mcp-type-oaipagination) | Yes | — |

Unknown fields are not accepted.

### `drntu_oai_get_record`

Get one record by its OAI identifier, not a REST UUID. Dublin Core returns repeated fields and language tags; other advertised formats return metadata_xml. Deleted records preserve their header without inferring metadata or file access.

Required: `identifier`. Optional: `metadata_prefix`, default `oai_dc`, and `refresh`.

Retrieves one OAI record in the same representation as record listings. Supply an OAI identifier returned by OAI listing, **not** a UUID from `drntu_search`. A deleted record preserves its header without inventing metadata.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `identifier` | `string` | Yes | maximum length: `500`; pattern: `^oai:dr\.ntu\.edu\.sg:[^\s\x00-\x1f\x7f]+$` |
| `metadata_prefix` | `string` | No | maximum length: `100`; pattern: `^[A-Za-z0-9_.-]+$`; default: `"oai_dc"` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `response_date` | `string` | Yes | — |
| `metadata_prefix` | `string` | Yes | — |
| `record` | [`OAIRecord`](#mcp-type-oairecord) | Yes | — |

Unknown fields are not accepted.

## MCP data types

These named types are used by the tool input and output fields above.

<a id="mcp-type-bundle"></a>
### `Bundle`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `bundle_id` | `string` | Yes | — |
| `name` | `string` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-checksum"></a>
### `Checksum`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `algorithm` | `string` | Yes | — |
| `value` | `string` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-container"></a>
### `Container`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `container_id` | `string` | Yes | — |
| `name` | `string` | Yes | — |
| `description` | array of `string` | Yes | — |
| `archived_items_count` | `integer` or `null` | Yes | minimum: `0` |
| `url` | `string` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-datasetfile"></a>
### `DatasetFile`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `file_id` | `integer` | Yes | greater than: `0` |
| `name` | `string` | Yes | — |
| `directory` | `string` or `null` | Yes | — |
| `media_type` | `string` or `null` | Yes | — |
| `size_bytes` | `integer` or `null` | Yes | minimum: `0` |
| `restricted` | `boolean` or `null` | Yes | — |
| `checksum` | [`Checksum`](#mcp-type-checksum) or `null` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-facetdefinition"></a>
### `FacetDefinition`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `name` | `string` | Yes | — |
| `facet_type` | `string` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-facetvalue"></a>
### `FacetValue`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `label` | `string` | Yes | — |
| `count` | `integer` | Yes | minimum: `0` |
| `authority_key` | `string` or `null` | Yes | — |
| `filter` | [`SearchFilter`](#mcp-type-searchfilter) or `null` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-file"></a>
### `File`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `file_id` | `string` | Yes | — |
| `name` | `string` | Yes | — |
| `bundle_name` | `string` or `null` | Yes | — |
| `size_bytes` | `integer` or `null` | Yes | minimum: `0` |
| `checksum` | [`Checksum`](#mcp-type-checksum) or `null` | Yes | — |
| `rights` | array of `string` | Yes | — |
| `content_url` | `string` or `null` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-itemsummary"></a>
### `ItemSummary`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `item_id` | `string` | Yes | — |
| `title` | `string` | Yes | — |
| `entity_type` | `string` or `null` | Yes | — |
| `authors` | array of `string` | Yes | — |
| `dates_issued` | array of `string` | Yes | — |
| `identifiers` | array of `string` | Yes | — |
| `rights` | array of `string` | Yes | — |
| `url` | `string` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-metadatavalue"></a>
### `MetadataValue`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `value` | `string` | Yes | — |
| `language` | `string` or `null` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-oaimetadataformat"></a>
### `OAIMetadataFormat`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `metadata_prefix` | `string` | Yes | — |
| `schema_url` | `string` | Yes | — |
| `metadata_namespace` | `string` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-oaipagination"></a>
### `OAIPagination`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `offset` | `integer` | Yes | — |
| `page_count` | `integer` | Yes | — |
| `next_offset` | `integer` or `null` | Yes | — |
| `resumption_token` | `string` or `null` | Yes | — |
| `cursor` | `integer` or `null` | Yes | — |
| `complete_list_size` | `integer` or `null` | Yes | — |
| `expiration_date` | `string` or `null` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-oairecord"></a>
### `OAIRecord`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `identifier` | `string` | Yes | — |
| `datestamp` | `string` | Yes | — |
| `set_specs` | array of `string` | Yes | — |
| `deleted` | `boolean` | Yes | — |
| `metadata` | object of array of [`MetadataValue`](#mcp-type-metadatavalue) or `null` | Yes | — |
| `metadata_xml` | `string` or `null` | Yes | — |
| `about_xml` | array of `string` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-oaiset"></a>
### `OAISet`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `set_spec` | `string` | Yes | — |
| `name` | `string` | Yes | — |
| `descriptions_xml` | array of `string` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-page"></a>
### `Page`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `page` | `integer` | Yes | minimum: `0` |
| `page_size` | `integer` | Yes | greater than: `0` |
| `total_elements` | `integer` or `null` | Yes | minimum: `0` |
| `total_pages` | `integer` or `null` | Yes | minimum: `0` |
| `next_page` | `integer` or `null` | Yes | minimum: `0` |

Unknown fields are not accepted.

<a id="mcp-type-searchfilter"></a>
### `SearchFilter`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `field` | `string` | Yes | pattern: `^[A-Za-z][A-Za-z0-9_.-]{0,79}$` |
| `value` | `string` | Yes | minimum length: `1`; maximum length: `500` |
| `operator` | `"equals"`, `"contains"`, `"authority"` | No | default: `"equals"` |

Unknown fields are not accepted.

## Service notes

Public publication, dataset, and OAI-PMH metadata lookups in the shared `all-abt-ntu-mcp` server. No credentials, keyring, Chromium, or extra dependencies are needed. See the [main README](../../README.md) for installation and MCP client configuration.

All results have `retrieved_at`, `source_url`, and `cached`. Responses are cached in memory for five minutes, with at most 64 entries and 16 MB per REST/OAI client. `refresh: true` refetches the requested response. Each client pools HTTPS connections, permits up to two in-flight reads with 250 ms default request pacing, limits responses to 8 MB, and uses a 20-second timeout. Requests to `researchdata.ntu.edu.sg` are spaced at least 60 seconds apart per process. It retries transient failures once and honors short `Retry-After` delays; longer server-requested delays return an error rather than retrying early. Public HTTP settings are documented in the [shared runtime guide](../shared/README.md#public-http-reads).

### Access policy review

Reviewed 6 November 2026: [DR-NTU (Data) general terms](https://libguides.ntu.edu.sg/drntudataguidespolicies/TermsOfUse) require scraper bots to follow robots.txt and prohibit excessive load; the [API terms](https://libguides.ntu.edu.sg/drntudataguidespolicies/APITermsOfUse) require an identifiable application and prohibit unreasonable bandwidth and impairment. The public client identifies itself as `all-abt-ntu-mcp/0.1 (public NTU lookup)` and does not retrieve dataset file bodies. The [research-data robots policy](https://researchdata.ntu.edu.sg/robots.txt) specifies a 60-second crawl delay and disallows crawling paths other than listed exceptions, including the dataset API. The dataset tool is intended for individual API lookups, not crawling or bulk harvesting; the conservative 60-second pacing also applies to those API requests. The [publication repository policy](https://dr.ntu.edu.sg/robots.txt) restricts specific UI paths and `/server/opensearch`; the REST and OAI paths used here were not listed as disallowed at review time. Recheck both policies and applicable terms before release or any broader usage. These process-local limits do not coordinate multiple replicas.

DSpace listings use zero-based `page` and `page_size` from 1–50. Follow `pagination.next_page` until `null`. Total counts remain `null` when the source omits them, as happens with individual search facets. Malformed records or inconsistent result pages fail rather than silently appearing complete.

### Sources

| Endpoint | Purpose |
| --- | --- |
| `https://dr.ntu.edu.sg/server/api/discover/search/objects` | Paginated publication/profile search, scopes, and facet filters |
| `https://dr.ntu.edu.sg/server/api/core/items/{uuid}` | Published item metadata, abstracts, and rights |
| `https://dr.ntu.edu.sg/server/api/core/communities` | Community browsing |
| `https://dr.ntu.edu.sg/server/api/core/collections` | Collection browsing |
| `https://dr.ntu.edu.sg/server/api/core/communities/{uuid}/subcommunities` | Community hierarchy |
| `https://dr.ntu.edu.sg/server/api/core/communities/{uuid}/collections` | Collections within a community |
| `https://dr.ntu.edu.sg/server/api/discover/facets` | Filter definitions |
| `https://dr.ntu.edu.sg/server/api/discover/facets/{name}` | Filter values, counts, and exact query filters |
| `https://dr.ntu.edu.sg/server/api/core/items/{uuid}/bundles` | Item file-group discovery |
| `https://dr.ntu.edu.sg/server/api/core/bundles/{uuid}/bitstreams` | File metadata and content links |
| `https://researchdata.ntu.edu.sg/api/datasets/:persistentId` | Latest dataset metadata with `persistentId=doi:...` |
| `https://researchdata.ntu.edu.sg/api/datasets/:persistentId/versions/{version}` | Explicit published dataset release |
| `https://dr.ntu.edu.sg/server/oai/request` | OAI-PMH Identify, ListMetadataFormats, ListSets, ListRecords, ListIdentifiers, and GetRecord |

The API root was checked to identify the repository's DSpace/CRIS format. Bundle details and individual bitstream metadata repeat fields already included in listings; separate format lookups were inspected but are omitted to avoid a request for every file. OAI-PMH supports incremental metadata retrieval, while the REST search tools provide keyword and facet searches.

Primary references: [DSpace REST contract](https://github.com/DSpace/RestContract), [search contract](https://github.com/DSpace/RestContract/blob/main/search-endpoint.md), [Dataverse Native API](https://guides.dataverse.org/en/6.6/api/native-api.html), and [OAI-PMH 2.0](https://www.openarchives.org/OAI/openarchivesprotocol.html). Current NTU response shapes were also checked directly over HTTPS.

### Tests

Offline parsers, pagination, filters, caching, network failures, CAPTCHA/error handling, and MCP schemas use synthetic records:

```sh
uv run python -m unittest discover -s tests/drntu -t . -v
```

Opt-in live stdio checks search pages, publication filtering, item abstracts, browsing, facets and their filters, file discovery, and both dataset version endpoints. Prints statuses and never downloads research file bodies:

```sh
uv run python -m tests.drntu.live_smoke
```

OAI-only live stdio checks exercise all six protocol verbs, provider continuation, date filters, alternate-format XML, empty results, and expired/invalid token errors. Prints statuses and counts without saving or printing research metadata:

```sh
uv run python -m tests.drntu.live_oai_smoke
```

### Limitation

Only publicly exposed metadata is supported. No file downloads, full-text extraction, authenticated repository access, dataset search, or automatic repository-wide OAI harvesting is implemented. OAI timestamps describe repository changes, not publication dates. Continuation tokens can expire and NTU controls source-page sizes. Metadata may describe restricted or embargoed content. Dataset access can be interrupted by CAPTCHA; availability during one smoke test is not a guarantee of continued automated access.
