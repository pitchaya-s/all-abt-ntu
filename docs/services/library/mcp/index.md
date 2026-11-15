# Library: MCP reference

[Service overview](../index.md) · [CLI reference](../cli/index.md) · [MCP reference](index.md)

## Tools

Inputs are required only where marked. Output fields marked required may still be `null` when their type allows it. See the [data types](types.md) for object fields.

### `library_search`

Search NTU OneSearch for books, articles, journals and other catalogue resources. Choose a field and contains/exact matching; resource_type is a Primo facet token such as books or articles. Returns canonical IDs, bibliographic summaries and published access signals. Follow next_offset; refine the query if the service limits deep paging.

Required: `query`. Optional: `field`, one of `any`, default, `title`, `creator`, `isbn`, `issn`, or `sub`; `match`, `contains`, default, or `exact`; `resource_type`; `limit`, 1–50, default 10; `offset`, default 0; and `refresh`.

Searches NTU's configured `Everything` tab with `MyInst_and_CI` scope, combining local records and the central discovery index. A result does not establish ownership, subscription entitlement, or full-text access. `resource_type` is a Primo resource-type facet token, such as `books` or `articles`.

Returns concise titles, resource types, authors, publication dates, canonical record IDs, search contexts, catalogue links, and published access signals. Follow `next_offset` until `null`. Local and central-index counts remain unknown when the source omits them. The service can limit deep paging; refine the query rather than assuming all millions of matches can be collected.

```json
{"query": "algorithms", "resource_type": "books", "limit": 5}
```

```json
{"query": "9780262046305", "field": "isbn", "match": "exact"}
```

Search text must be nonblank, at most 500 characters, and contain no semicolons or control characters, which could alter Primo's multi-clause query syntax. Use the structured field/match inputs for these lookups.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `query` | `string` | Yes | minimum length: `1`; maximum length: `500` |
| `field` | `"any"`, `"title"`, `"creator"`, `"isbn"`, `"issn"`, `"sub"` | No | default: `"any"` |
| `match` | `"contains"`, `"exact"` | No | default: `"contains"` |
| `resource_type` | `string` or `null` | No | default: `null`; pattern: `^[A-Za-z][A-Za-z0-9_-]{0,49}$` |
| `limit` | `integer` | No | minimum: `1`; maximum: `50`; default: `10` |
| `offset` | `integer` | No | minimum: `0`; default: `0` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `query` | `string` | Yes | — |
| `records` | array of [`RecordSummary`](types.md#mcp-type-recordsummary) | Yes | — |
| `offset` | `integer` | Yes | minimum: `0` |
| `total_count` | `integer` | Yes | minimum: `0` |
| `local_count` | `integer` or `null` | Yes | minimum: `0` |
| `central_index_count` | `integer` or `null` | Yes | minimum: `0` |
| `next_offset` | `integer` or `null` | Yes | minimum: `0` |

Unknown fields are not accepted.

### `library_get_record`

Read a OneSearch record's bibliographic metadata, descriptions, subjects, identifiers and published access links. Pass record_id and context from library_search; L is local, PC is central-index content. No file is downloaded and reported availability does not guarantee access or a loanable copy.

Required: `record_id`. Optional: `context`, `L`, default, for local records, or `PC` for central-index records; and `refresh`.

Copy both values from search results. Returns bibliographic metadata including alternate titles, contributors, publishers, editions, languages, subjects, descriptions, ISBN/ISSN/DOI identifiers, and published access links when supplied. Search-highlight HTML and the secondary `$$Q` indexing form are removed from visible text. Cover-thumbnail links are omitted.

Primo's internal `@id` link can contain a numeric source ID that does not work for record retrieval. The tool uses the canonical PNX `control.recordid`, including prefixes such as `alma`, and supplies `adaptor=Primo Central` for central-index retrieval. An HTTP 200 response with an empty record set is treated as not found.

`open_access`, `availability_codes`, and `availability_label` preserve separate source statements. In testing, the source could simultaneously report open-access or `not_restricted` metadata and a display label of `Not available`. Those values are returned without converting them into a confirmed available copy or anonymous download entitlement. Missing fields remain `null`.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `record_id` | `string` | Yes | pattern: `^[A-Za-z0-9][A-Za-z0-9_.:-]{0,299}$` |
| `context` | `"L"`, `"PC"` | No | default: `"L"` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `record` | [`Record`](types.md#mcp-type-record) | Yes | — |

Unknown fields are not accepted.

### `library_get_availability`

Read published physical holdings with library, location, call number and status, plus institutional full-text service links and access notes. Use the record ID/context from library_search. No login is needed; absence does not establish no copies or no access. Links do not prove full-text entitlement, and no file, loan or hold is requested.

Required: `record_id`. Optional: `context`, default `L`, and `refresh`.

Returns published physical holdings with library, sublocation, call number and source availability. Electronic records can include institutional service links and access notes, such as concurrent-user or download restrictions. Service links come from the same resolver used by OneSearch. The tool does not follow them, download licensed books or verify subscription entitlement. Missing holdings/services do not establish that none exist. Copy-level counts, personal loans and hold requests are not exposed.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `record_id` | `string` | Yes | pattern: `^[A-Za-z0-9][A-Za-z0-9_.:-]{0,299}$` |
| `context` | `"L"`, `"PC"` | No | default: `"L"` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `record_id` | `string` | Yes | — |
| `context` | `"L"`, `"PC"` | Yes | — |
| `holdings` | array of [`Holding`](types.md#mcp-type-holding) | Yes | — |
| `electronic_services` | array of [`ElectronicService`](types.md#mcp-type-electronicservice) | Yes | — |
| `availability_codes` | array of `string` or `null` | Yes | — |
| `services_source_url` | `string` or `null` | No | default: `null` |

Unknown fields are not accepted.

### `library_list_facilities`

List NTU Library facility categories, library/floor maps and closure notices. Public and read-only. Use map_slug for map availability; space_id and location_id/group_id identify directory entries.

Optional: `refresh`. Lists facilities by library, floor-map identifiers, direct room IDs or location/group IDs, and published closure notices from the LibFacilities homepage.

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
| `facilities` | array of [`Facility`](types.md#mcp-type-facility) | Yes | — |
| `notices` | array of `string` | Yes | — |

Unknown fields are not accepted.

### `library_get_map_availability`

Read seat/room booking statuses for a library map at date YYYY-MM-DD and time HH:MM in Singapore. Copy map_slug from library_list_facilities. No credentials needed. Available_later is not available at the requested time; a point status does not establish availability for a whole interval or physical occupancy.

Required: `map_slug` from the directory, `date` as `YYYY-MM-DD`, and `time` as `HH:MM`. Optional: `refresh`.

Returns public seat/room booking statuses for that Singapore date and time: `available`, `available_later`, `unavailable`, or `unknown`. Original numeric source statuses are retained; non-bookable map amenities are excluded. Availability at one instant is not availability throughout an interval or actual occupancy.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `map_slug` | `string` | Yes | pattern: `^[a-f0-9]{12}$` |
| `date` | `string` | Yes | pattern: `^\d{4}-\d{2}-\d{2}$` |
| `time` | `string` | Yes | pattern: `^(?:[01]\d\|2[0-3]):[0-5]\d$` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `map_slug` | `string` | Yes | — |
| `at` | `string` | Yes | format: `date-time` |
| `spaces` | array of [`SpaceStatus`](types.md#mcp-type-spacestatus) | Yes | — |

Unknown fields are not accepted.

### `library_get_facility_schedule`

Read a day's LibFacilities room/seat time grid, room description and source status classes. Supply space_id, or both location_id and group_id, from facility/map results. Requires saved local NTU student credentials and Chromium. Reuses an in-memory session and caches for 60 seconds. MFA/CAPTCHA returns an error; no booking, cart, checkout, loan, or hold is submitted. Missing slots are unknown, not free.

Required: `date` as `YYYY-MM-DD`, and either `space_id` or both `location_id` and `group_id`, copied from facility results. Optional: `refresh`.

Uses saved NTU student network credentials to read a facility's description and daily room/seat time grid. Slots have `available` or `unavailable` status, matching the page's verified `formatEventsForFullCalendar` convention: a nonempty `className` marks unavailability, and an absent/empty class marks availability. Original classes remain in `source_classes`. Adjacent slots with identical classes are combined without losing timing information. Omitted intervals remain unknown. All times include Singapore's UTC offset. Booking identities and checksums are excluded.

The browser starts only for authenticated calls and is reused with in-memory cookies. Results are cached in memory for 60 seconds, with at most 32 entries; deleting or updating keyring credentials invalidates access to cached personal results. Session expiry initiates a fresh login, with a one-minute cooldown against repeated password submissions. CAPTCHA, MFA, unexpected login hosts and rejected credentials stop the operation. Staff/NIE login formats are not verified. No booking, cart, checkout, loan, hold or renewal action is exposed.

One request covers one day and up to 180 resources, following resource pages. For larger groups, request a particular `space_id`. Empty grids do not prove spaces are free or within the booking window.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `date` | `string` | Yes | pattern: `^\d{4}-\d{2}-\d{2}$` |
| `space_id` | `integer` or `null` | No | default: `null`; minimum: `1`; maximum: `9999999999` |
| `location_id` | `integer` or `null` | No | default: `null`; minimum: `1`; maximum: `9999999999` |
| `group_id` | `integer` or `null` | No | default: `null`; minimum: `1`; maximum: `9999999999` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `date` | `string` | Yes | — |
| `timezone` | `"Asia/Singapore"` | No | default: `"Asia/Singapore"` |
| `title` | `string` | Yes | — |
| `description` | `string` or `null` | Yes | — |
| `spaces` | array of [`SpaceSchedule`](types.md#mcp-type-spaceschedule) | Yes | — |
| `window_end` | `boolean` or `null` | Yes | — |

Unknown fields are not accepted.

See the [MCP data types](types.md) for nested object fields.
