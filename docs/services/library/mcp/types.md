# Library: MCP data types

[Service overview](../index.md) · [MCP reference](index.md)

## MCP data types

These named types describe nested fields in the [MCP tool reference](index.md). A required field may still be `null` when its type allows it.

<a id="mcp-type-electronicservice"></a>
### `ElectronicService`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `name` | `string` or `null` | Yes | — |
| `url` | `string` or `null` | Yes | — |
| `notes` | `string` or `null` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-facility"></a>
### `Facility`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `library` | `string` | Yes | — |
| `name` | `string` | Yes | — |
| `url` | `string` | Yes | — |
| `map_slug` | `string` or `null` | No | default: `null` |
| `space_id` | `integer` or `null` | No | default: `null` |
| `location_id` | `integer` or `null` | No | default: `null` |
| `group_id` | `integer` or `null` | No | default: `null` |

Unknown fields are not accepted.

<a id="mcp-type-holding"></a>
### `Holding`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `library` | `string` or `null` | Yes | — |
| `location` | `string` or `null` | Yes | — |
| `call_number` | `string` or `null` | Yes | — |
| `availability` | `string` or `null` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-link"></a>
### `Link`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `url` | `string` | Yes | — |
| `label` | `string` or `null` | Yes | — |
| `link_type` | `string` or `null` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-record"></a>
### `Record`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `record_id` | `string` | Yes | — |
| `context` | `"L"`, `"PC"` | Yes | — |
| `title` | `string` | Yes | — |
| `resource_types` | array of `string` | Yes | — |
| `authors` | array of `string` | Yes | — |
| `publication_dates` | array of `string` | Yes | — |
| `open_access` | `boolean` or `null` | Yes | — |
| `availability_codes` | array of `string` or `null` | Yes | — |
| `availability_label` | `string` or `null` | Yes | — |
| `catalogue_url` | `string` | Yes | — |
| `alternate_titles` | array of `string` | Yes | — |
| `contributors` | array of `string` | Yes | — |
| `publishers` | array of `string` | Yes | — |
| `editions` | array of `string` | Yes | — |
| `languages` | array of `string` | Yes | — |
| `subjects` | array of `string` | Yes | — |
| `descriptions` | array of `string` | Yes | — |
| `identifiers` | object of array of `string` | Yes | — |
| `links` | array of [`Link`](#mcp-type-link) | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-recordsummary"></a>
### `RecordSummary`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `record_id` | `string` | Yes | — |
| `context` | `"L"`, `"PC"` | Yes | — |
| `title` | `string` | Yes | — |
| `resource_types` | array of `string` | Yes | — |
| `authors` | array of `string` | Yes | — |
| `publication_dates` | array of `string` | Yes | — |
| `open_access` | `boolean` or `null` | Yes | — |
| `availability_codes` | array of `string` or `null` | Yes | — |
| `availability_label` | `string` or `null` | Yes | — |
| `catalogue_url` | `string` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-spaceschedule"></a>
### `SpaceSchedule`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `item_id` | `string` | Yes | — |
| `name` | `string` or `null` | Yes | — |
| `slots` | array of [`TimeSlot`](#mcp-type-timeslot) | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-spacestatus"></a>
### `SpaceStatus`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `space_id` | `integer` | Yes | — |
| `name` | `string` | Yes | — |
| `status` | `"available"`, `"available_later"`, `"unavailable"`, `"unknown"` | Yes | — |
| `source_status` | `integer` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-timeslot"></a>
### `TimeSlot`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `start` | `string` | Yes | format: `date-time` |
| `end` | `string` | Yes | format: `date-time` |
| `status` | `"available"`, `"unavailable"` | Yes | — |
| `source_classes` | `string` or `null` | Yes | — |

Unknown fields are not accepted.
