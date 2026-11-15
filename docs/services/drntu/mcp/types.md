# DR-NTU: MCP data types

[Service overview](../index.md) · [MCP reference](index.md)

## MCP data types

These named types describe nested fields in the [MCP tool reference](index.md). A required field may still be `null` when its type allows it.

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
