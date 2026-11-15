# STARS: Room schedules MCP tools

[Service overview](../index.md) · [CLI reference](../cli/index.md) · [All MCP tools](index.md) · [Data types](types.md)

## Room schedules

Inputs are required only where marked. A required output field may still be `null` if its type allows it. See [data types](types.md) for nested objects.

### `stars_find_available_rooms`

Find rooms with no known published undergraduate teaching throughout a day/time interval and every requested teaching week. Covers all indexes from both full-time and part-time schedules, including all lesson types. Filters select room type inferred from venue code, venue text/prefix, excluded rooms or observed lesson types. Unknown conflicting schedules are excluded. Only teaching-observed rooms are returned; this does not establish occupancy, access, capacity or availability against graduate classes, exams or other bookings. Times are Singapore time and weeks are semester teaching weeks. Omit weeks for a conservative whole-term check. Follow has_more with offset.

Find a teaching-observed room with no known scheduled undergraduate classes throughout a requested interval.

**Inputs:** `academic_year`, `semester`, and `window` with `day`, `start_time`, and `end_time`. Optional `window.teaching_weeks` selects semester teaching weeks, from 1–20; the room must be free in **every** selected week. Omitting weeks checks every published meeting conservatively across the term. `window.buffer_minutes`, default 0 and maximum 120, requires additional teaching-free time before and after the interval. The interval plus buffer must fit in one day.

Optional `filters`:

| Field | Meaning |
| --- | --- |
| `room_types` | `tutorial_room`, `seminar_room`, `lecture_theatre`, `laboratory`, or `other`, inferred from venue labels |
| `venue_contains` | Case-insensitive literal text within a normalized venue code |
| `venue_prefixes` | Any matching code prefix, such as `LHN`, `LHS`, `SPMS`, or `S4` |
| `exclude_venues` | Exact venue codes or equivalent normalized aliases to omit |
| `used_for_lesson_types` | Require observed use for any listed lesson type, such as `TUT` or `LAB` |

All lesson types still block availability, regardless of filters. `limit` is 1–100, default 20; `offset` defaults to 0. `refresh: true` reloads the complete shared teaching snapshot.

**Returns:** room codes, inferred types, observed aliases/lesson types, `free_from`/`free_until` teaching-free bounds on that day, total `match_count`, and pagination. A `free_until` of `24:00` is the end of the day, not a building opening-hours statement. Conflicting unknown days, times or teaching weeks exclude a room and contribute to `excluded_uncertain_count`; known clashes contribute to `excluded_busy_count`.

The first lookup fetches two public schedule pages concurrently: a blank-course search for full-time offerings and another for part-time offerings. Every published index/session is checked; no course-by-course crawl, course-description lookup or vacancy request is needed. Both pages must parse successfully before results are returned. The normalized snapshot is shared with room timetable lookups, cached for `NTU_CACHE_TTL_SECONDS`, and bounded to four terms.

Only recognizable room labels actually observed in teaching are candidates. Online, placeholder, date-like, course-reference and unrecognized venue labels are excluded. Common punctuation, quotation and tutorial-number variants are merged conservatively; multi-room cells block each independently observed component. Unknown raw venue text is retained in room timetable results. Coverage reports course/index/lesson counts, courses without published indexes, observed room count, excluded venue-label count and unplaced lesson count. Empty official index tables remain missing data; they do not establish that a course has no classes.

```json
{"academic_year":2030,"semester":1,"window":{"day":"WED","start_time":"14:00","end_time":"16:00","teaching_weeks":[7],"buffer_minutes":10},"filters":{"room_types":["tutorial_room","seminar_room"],"venue_prefixes":["LHN","LHS"]}}
```

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `academic_year` | `integer` | Yes | minimum: `2000`; maximum: `2100` |
| `semester` | `1`, `2`, `"S"` | Yes | — |
| `window` | [`RoomWindow`](types.md#mcp-type-roomwindow) | Yes | — |
| `filters` | [`RoomFilters`](types.md#mcp-type-roomfilters) or `null` | No | default: `null` |
| `limit` | `integer` | No | minimum: `1`; maximum: `100`; default: `20` |
| `offset` | `integer` | No | minimum: `0`; default: `0` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `academic_year` | `integer` | Yes | — |
| `semester` | `string` | Yes | — |
| `source_url` | `string` | Yes | — |
| `retrieved_at` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `coverage` | [`RoomCoverage`](types.md#mcp-type-roomcoverage) | Yes | — |
| `availability_basis` | `"no_known_scheduled_teaching"` | No | default: `"no_known_scheduled_teaching"` |
| `window` | [`RoomWindow`](types.md#mcp-type-roomwindow) | Yes | — |
| `match_count` | `integer` | Yes | — |
| `offset` | `integer` | Yes | — |
| `has_more` | `boolean` | Yes | — |
| `rooms` | array of [`AvailableRoom`](types.md#mcp-type-availableroom) | Yes | — |
| `excluded_busy_count` | `integer` | Yes | — |
| `excluded_uncertain_count` | `integer` | Yes | — |

Unknown fields are not accepted.

### `stars_get_room_schedule`

Get all published undergraduate course/index lessons using one observed room, including full-time and part-time offerings. Accepts a venue code or returned alias. Shared lessons carry all associated index numbers. Optional day, teaching weeks and overlapping time interval filter the result; uncertain lessons remain included. Missing weeks/times are unknown. Paginate with offset/limit and has_more. This is teaching data, not room bookings or actual occupancy.

Retrieve the courses and indexes using a room, from the same complete full-time/part-time undergraduate teaching snapshot.

**Inputs:** `venue`, `academic_year`, `semester`. Optional `day`, `teaching_weeks`, and both `start_time`/`end_time` restrict the result to potentially overlapping lessons. Unknown timing/week data remains included rather than being silently discarded. `limit` is 1–100, default 50; `offset` defaults to 0. `refresh` reloads the shared snapshot.

**Returns:** the canonical venue and aliases, inferred room type, observed lesson types, and paginated sessions. Shared sessions are grouped with every associated index in `indexes`. Course codes and indexes remain strings. Sessions retain teaching weeks, unusual remarks, raw day/time values and original venue labels when they differ from the enclosing room. An unidentified venue returns an error rather than an empty or apparently free timetable.

```json
{"venue":"TR+7","academic_year":2030,"semester":1,"day":"TUE","teaching_weeks":[7]}
```

These tools report **no known scheduled undergraduate teaching**, not guaranteed room availability or occupancy. Graduate classes, exams, private bookings, closures and access restrictions are outside coverage. Room types are inferred from names; capacities, equipment, accessibility and opening hours are not supplied by this source. Bare `TR`/`LT` codes do not establish North/South Spine or a building location; use MazeMap for verified location information.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `venue` | `string` | Yes | minimum length: `1`; maximum length: `80` |
| `academic_year` | `integer` | Yes | minimum: `2000`; maximum: `2100` |
| `semester` | `1`, `2`, `"S"` | Yes | — |
| `day` | `"MON"`, `"TUE"`, `"WED"`, `"THU"`, `"FRI"`, `"SAT"`, `"SUN"` or `null` | No | default: `null` |
| `teaching_weeks` | array of `integer` or `null` | No | default: `null`; minimum items: `1`; maximum items: `20` |
| `start_time` | `string` or `null` | No | default: `null`; pattern: `^(?:[01]\d\|2[0-3]):[0-5]\d$` |
| `end_time` | `string` or `null` | No | default: `null`; pattern: `^(?:[01]\d\|2[0-3]):[0-5]\d$` |
| `limit` | `integer` | No | minimum: `1`; maximum: `100`; default: `50` |
| `offset` | `integer` | No | minimum: `0`; default: `0` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `academic_year` | `integer` | Yes | — |
| `semester` | `string` | Yes | — |
| `source_url` | `string` | Yes | — |
| `retrieved_at` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `coverage` | [`RoomCoverage`](types.md#mcp-type-roomcoverage) | Yes | — |
| `room` | [`RoomIdentity`](types.md#mcp-type-roomidentity) | Yes | — |
| `session_count` | `integer` | Yes | — |
| `offset` | `integer` | Yes | — |
| `has_more` | `boolean` | Yes | — |
| `sessions` | array of [`RoomLesson`](types.md#mcp-type-roomlesson) | Yes | — |

Unknown fields are not accepted.
