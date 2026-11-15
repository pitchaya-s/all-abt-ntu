# NTU Library tools

[CLI commands](#cli-commands) · [MCP tools](#mcp-tools) · [MCP data types](#mcp-data-types) · [Service notes](#service-notes)

For installation and shared authentication, see the [main README](../../README.md).

## CLI commands

The output column lists the JSON result fields; human-readable output is formatted for the terminal. Use `ntu library --help` and append `--help` to a command for option details. `VALUE` denotes an option value; required arguments and options are marked. See the [complete CLI reference](../COMMANDS.md) for shared settings and all services.

| Command | Arguments and options | Purpose | Output |
| --- | --- | --- | --- |
| `ntu library search` | `QUERY (required)`, `--field VALUE [any, title, creator, isbn, issn, sub] (default: any)`, `--match VALUE [contains, exact] (default: contains)`, `--resource-type VALUE`, `--limit/-l VALUE (default: 10)`, `--offset VALUE`, `--refresh/-r`, `--json/-j` | Search NTU OneSearch for books, articles, journals and other catalogue resources. | `retrieved_at`, `source_url`, `cached`, `query`, `records`, `offset`, `total_count`, `local_count`, `central_index_count`, `next_offset` ([schema](#library_search)) |
| `ntu library record` | `RECORD_ID (required)`, `--context VALUE [L, PC] (default: L)`, `--refresh/-r`, `--json/-j` | Read a OneSearch record's bibliographic metadata, descriptions, subjects, identifiers and published access links. | `retrieved_at`, `source_url`, `cached`, `record` ([schema](#library_get_record)) |
| `ntu library availability` | `RECORD_ID (required)`, `--context VALUE [L, PC] (default: L)`, `--refresh/-r`, `--json/-j` | Read published physical holdings with library, location, call number and status, plus institutional full-text service links and access notes. | `retrieved_at`, `source_url`, `cached`, `record_id`, `context`, `holdings`, `electronic_services`, `availability_codes`, `services_source_url` ([schema](#library_get_availability)) |
| `ntu library facilities schedule` | `--date VALUE (required)`, `--space VALUE`, `--location VALUE`, `--group VALUE`, `--refresh/-r`, `--json/-j` | Read a day's LibFacilities room/seat time grid, room description and source status classes. | `retrieved_at`, `source_url`, `cached`, `date`, `timezone`, `title`, `description`, `spaces`, `window_end` ([schema](#library_get_facility_schedule)) |
| `ntu library facilities list` | `--refresh/-r`, `--json/-j` | List NTU Library facility categories, library/floor maps and closure notices. | `retrieved_at`, `source_url`, `cached`, `facilities`, `notices` ([schema](#library_list_facilities)) |
| `ntu library map availability` | `MAP_SLUG (required)`, `--date VALUE (required)`, `--time VALUE (required)`, `--refresh/-r`, `--json/-j` | Read seat/room booking statuses for a library map at date YYYY-MM-DD and time HH:MM in Singapore. | `retrieved_at`, `source_url`, `cached`, `map_slug`, `at`, `spaces` ([schema](#library_get_map_availability)) |

## MCP tools

Inputs are required only where marked. Output fields marked required may still be `null` when their type allows it. See the nested data types below for object fields.

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
| `records` | array of [`RecordSummary`](#mcp-type-recordsummary) | Yes | — |
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
| `record` | [`Record`](#mcp-type-record) | Yes | — |

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
| `holdings` | array of [`Holding`](#mcp-type-holding) | Yes | — |
| `electronic_services` | array of [`ElectronicService`](#mcp-type-electronicservice) | Yes | — |
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
| `facilities` | array of [`Facility`](#mcp-type-facility) | Yes | — |
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
| `spaces` | array of [`SpaceStatus`](#mcp-type-spacestatus) | Yes | — |

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
| `spaces` | array of [`SpaceSchedule`](#mcp-type-spaceschedule) | Yes | — |
| `window_end` | `boolean` or `null` | Yes | — |

Unknown fields are not accepted.

## MCP data types

These named types are used by the tool input and output fields above.

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

## Service notes

Catalogue discovery and library facility information in the shared `all-abt-ntu-mcp` server. Public tools need no credentials or API key. Detailed facility schedules use the [shared credential store](../shared/README.md#credential-storage), also used by STARS and NTULearn, and the optional Chromium installation. See the [main README](../../README.md) for installation and client configuration.

`mcp.py` defines public operations. `personal_tools.py` defines the authenticated facility schedule operation only for the local personal profile; it is unavailable on the hosted public HTTP server. LibFacilities directory parsing, browser sessions, and schedule parsing are grouped under `facilities/`.

Results are typed and include `retrieved_at`, `source_url`, and `cached`. The shared public HTTP client caches responses for five minutes, bounds the cache to 64 entries, pools connections, permits up to two in-flight reads per client with 250 ms default pacing, applies a 20-second timeout, retries transient failures once, and limits each response to 8 MB. Public tools do not access account cookies, the keyring or a browser. Public HTTP settings are documented in the [shared runtime guide](../shared/README.md#public-http-reads).

### Sources and endpoint choice

The deployment is linked from [NTU Library](https://www.ntu.edu.sg/education/libraries/); see also the [NTU OneSearch guide](https://libguides.ntu.edu.sg/OneSearch).

| Endpoint | Purpose |
| --- | --- |
| `https://ntu-sp.primo.exlibrisgroup.com/primaws/rest/pub/pnxs` | Catalogue search |
| `https://ntu-sp.primo.exlibrisgroup.com/primaws/rest/pub/pnxs/{context}/{record_id}` | Local or central-index record details |
| `https://ntu-sp.primo.exlibrisgroup.com/primaws/rest/pub/edelivery/{record_id}` | Published institutional full-text services and access notes |
| `https://libcalendar.ntu.edu.sg/` | Facility directory and notices |
| `https://libcalendar.ntu.edu.sg/map/{slug}` | Public floor-map configuration |
| `https://libcalendar.ntu.edu.sg/maps/search/spaces` | Public date/time map availability |
| `https://libcalendar.ntu.edu.sg/space/{id}` and `/spaces?lid=…&gid=…` | Authenticated facility descriptions and resource configuration |
| `https://libcalendar.ntu.edu.sg/spaces/availability/grid` | Read-only daily time-grid query |

LibFacilities redirects through `au.libauth.com` to NTU's `loginfs.ntu.edu.sg/adfs/ls/` login. The implementation submits the saved password only to that NTU host using the verified student network-account format, and reuses the resulting session. The time-grid POST is a read query matching the page's request; booking endpoints are not called. OneSearch's separate Microsoft login required MFA during testing, so authenticated OneSearch account access and licensed full-text retrieval are not implemented.

Search parameters include `vid=65NTU_INST:65NTU_INST`, `tab=Everything`, `scope=MyInst_and_CI`, `q={field},{match},{query}`, `limit`, and `offset`. Resource filtering uses `qInclude=facet_rtype,exact,{resource_type}`.

The supplied `/rest/pub/pnxs` and `/rest/external/pnxs` endpoints were compared with an algorithms search, exact ISBN, and an article-filtered machine-learning search. Ordered canonical record IDs and total counts matched in those samples. The first two samples also had identical record payloads; the article comparison differed in some source, facet, ranking, and delivery metadata. This does not prove universal equivalence.

The implementation uses `/pub/pnxs` consistently because its search and both local/central record-detail workflows were verified. It avoids duplicate requests and does not switch endpoints to evade service errors. The separate Ex Libris API-key gateway is not used.

The [Ex Libris PNX API documentation](https://developers.exlibrisgroup.com/primo/apis/webservices/rest/pnxs/) and [search documentation](https://developers.exlibrisgroup.com/primo/apis/docs/primoSearch/R0VUIC9wcmltby92MS9zZWFyY2g%3D/) explain the general PNX/search conventions; the deployment-specific public routes and response formats were tested directly.

### Tests

Offline tests use synthetic catalogue and facility responses and cover normalization, query encoding, pagination, canonical IDs, the central adaptor, missing data, conflicting access signals, input rejection, source-status preservation, compact time grids, credential-cache checks, error redaction, and MCP schemas:

```sh
uv run python -m unittest discover -s tests/library -t . -v
```

Opt-in live stdio checks search pages, local and central record details, resource filtering, and ISBN search. Only statuses are printed:

```sh
uv run python -m tests.library.live_smoke
```

To also query a facility schedule using saved local credentials and Chromium:

```sh
uv run --extra personal python -m tests.library.live_smoke --personal
```

Live tests print statuses and counts only; they do not save credentials, bookings or account records.

### Limitation

These deployment-specific endpoints and HTML structures may change. No authenticated OneSearch account, loans, reservations, renewals, licensed file downloads or live copy-level loan checks are implemented. Catalogue and facility statuses are snapshots and may be incomplete or inconsistent. Personal facility reads stop at MFA/CAPTCHA; no bypass is attempted.
