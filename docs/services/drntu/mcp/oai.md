# DR-NTU: OAI-PMH MCP tools

[Service overview](../index.md) · [CLI reference](../cli/index.md) · [All MCP tools](index.md) · [Data types](types.md)

## OAI-PMH

Inputs are required only where marked. A required output field may still be `null` if its type allows it. See [data types](types.md) for nested objects.

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
| `formats` | array of [`OAIMetadataFormat`](types.md#mcp-type-oaimetadataformat) | Yes | — |

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
| `sets` | array of [`OAISet`](types.md#mcp-type-oaiset) | Yes | — |
| `pagination` | [`OAIPagination`](types.md#mcp-type-oaipagination) | Yes | — |

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
| `records` | array of [`OAIRecord`](types.md#mcp-type-oairecord) | Yes | — |
| `pagination` | [`OAIPagination`](types.md#mcp-type-oaipagination) | Yes | — |

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
| `record` | [`OAIRecord`](types.md#mcp-type-oairecord) | Yes | — |

Unknown fields are not accepted.

See the [MCP data types](types.md) for nested object fields.
