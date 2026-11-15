# STARS: Indexes and timetables MCP tools

[Service overview](../index.md) · [CLI reference](../cli/index.md) · [All MCP tools](index.md) · [Data types](types.md)

## Indexes and timetables

Inputs are required only where marked. A required output field may still be `null` if its type allows it. See [data types](types.md) for nested objects.

### `stars_get_course_indexes`

List a page of indexes with timetable details and matching-term vacancies/waitlists. Follow next_offset to see the rest. Sessions inherit course_code and index from their enclosing result; null raw_day/raw_time are omitted.

**Inputs:** `course_code`, `academic_year`, `semester`.

**Returns:** one page of indexes, their associated sessions, schedule completeness, vacancies, waitlist length, and vacancy metadata. `index_count` is the total; follow `next_offset` until it is null. Shared lectures remain attached to each applicable index. Sessions include lesson type, group, day, times, venue, teaching weeks, and remarks.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_code` | `string` | Yes | — |
| `academic_year` | `integer` | Yes | — |
| `semester` | `1`, `2`, `"S"` | Yes | — |
| `limit` | `integer` | No | minimum: `1`; maximum: `50`; default: `10` |
| `offset` | `integer` | No | minimum: `0`; default: `0` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_code` | `string` | Yes | — |
| `academic_year` | `integer` or `null` | Yes | — |
| `semester` | `string` or `null` | Yes | — |
| `index_count` | `integer` | Yes | — |
| `offset` | `integer` | Yes | — |
| `next_offset` | `integer` or `null` | Yes | — |
| `vacancy_metadata` | [`VacancyMetadata`](types.md#mcp-type-vacancymetadata) | Yes | — |
| `indexes` | array of [`CourseIndex`](types.md#mcp-type-courseindex) | Yes | — |

### `stars_get_index`

Get one index's complete schedule, vacancies, and waitlist where matching-term counts are published.

**Inputs:** `course_code`, `index`, `academic_year`, `semester`.

**Returns:** one index's sessions and matching-term vacancy snapshot. Use an index returned by `stars_get_course_indexes`; an unknown index produces an error rather than an empty timetable.

```json
{"course_code":"ZZ0001","index":"00001","academic_year":2030,"semester":1}
```

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_code` | `string` | Yes | — |
| `index` | `string` | Yes | — |
| `academic_year` | `integer` | Yes | — |
| `semester` | `1`, `2`, `"S"` | Yes | — |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_code` | `string` | Yes | — |
| `academic_year` | `integer` or `null` | Yes | — |
| `semester` | `string` or `null` | Yes | — |
| `vacancy_status` | `"available"`, `"not_listed"`, `"closed"`, `"term_mismatch"`, `"unavailable"` | Yes | — |
| `vacancies_available` | `integer` or `null` | Yes | — |
| `waitlist_length` | `integer` or `null` | Yes | — |
| `index` | `string` | Yes | — |
| `vacancy_metadata` | [`VacancyMetadata`](types.md#mcp-type-vacancymetadata) | Yes | — |
| `schedule_complete` | `boolean` | Yes | — |
| `sessions` | array of [`CompactSession`](types.md#mcp-type-compactsession) | Yes | — |

### `stars_compare_indexes`

Compare shared and index-specific sessions; optionally check clashes with supplied time slots.

**Inputs:** `course_code`, `academic_year`, `semester`, at least two unique `indexes`; optional `against_sessions`.

**Returns:** `common_sessions`, `unique_sessions_by_index`, and an optional `clash_check`. Common sessions apply to every entry in `indexes_compared`. Clash checks distinguish definite overlaps from comparisons with unknown week/day/time information.

```json
{"course_code":"ZZ0001","academic_year":2030,"semester":1,"indexes":["00001","00002"],"against_sessions":[{"day":"TUE","start_time":"14:00","end_time":"16:00","teaching_weeks":[2,4,6]}]}
```

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_code` | `string` | Yes | — |
| `indexes` | array of `string` | Yes | — |
| `academic_year` | `integer` | Yes | — |
| `semester` | `1`, `2`, `"S"` | Yes | — |
| `against_sessions` | array of [`TimeSlot`](types.md#mcp-type-timeslot) or `null` | No | default: `null` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_code` | `string` | Yes | — |
| `academic_year` | `integer` or `null` | Yes | — |
| `semester` | `string` or `null` | Yes | — |
| `retrieved_at` | `string` or `null` | Yes | — |
| `official_source` | `string` or `null` | Yes | — |
| `indexes_compared` | array of `string` | Yes | — |
| `common_sessions` | array of [`CompactSession`](types.md#mcp-type-compactsession) | Yes | — |
| `unique_sessions_by_index` | object of array of [`CompactSession`](types.md#mcp-type-compactsession) | Yes | — |
| `clash_check` | [`ClashCheck`](types.md#mcp-type-clashcheck) or `null` | Yes | — |

### `stars_find_matching_indexes`

Find indexes matching day/time/lesson/week rules and avoiding supplied timetable clashes.

**Inputs:** `course_code`, `academic_year`, `semester`; optional `constraints` and `against_sessions`.

Supported constraints:

| Field | Meaning |
| --- | --- |
| `avoid_days` | Reject sessions on the listed days |
| `earliest_start` | Every session must start at or after this time |
| `latest_end` | Every session must end by this time |
| `avoid_windows` | Reject overlaps with listed day/start/end windows |
| `require_sessions` | Each rule must match a session by lesson type, day, or start-time bounds |
| `teaching_weeks` | Evaluate sessions in the specified weeks, from 1–20 |

Required-session rules accept `lesson_type`, `day`, `starts_at_or_after`, and `starts_at_or_before`. Supply at least one condition per rule. Use lesson types as returned by NTU.

**Returns:** matching indexes with schedules, `status` of `confirmed` or `uncertain`, and reasons for uncertainty. Against-schedule slots accept `day`, `start_time`, `end_time`, and optional `teaching_weeks`. Use slots from the same academic year and semester. Overlaps in disjoint known teaching weeks do not clash.

```json
{"course_code":"ZZ0001","academic_year":2030,"semester":1,"constraints":{"avoid_days":["FRI"],"latest_end":"17:00","require_sessions":[{"lesson_type":"TUT","day":"TUE","starts_at_or_after":"13:00"}]}}
```

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_code` | `string` | Yes | — |
| `academic_year` | `integer` | Yes | — |
| `semester` | `1`, `2`, `"S"` | Yes | — |
| `constraints` | [`SearchConstraints`](types.md#mcp-type-searchconstraints) or `null` | No | default: `null` |
| `against_sessions` | array of [`TimeSlot`](types.md#mcp-type-timeslot) or `null` | No | default: `null` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_code` | `string` | Yes | — |
| `academic_year` | `integer` or `null` | Yes | — |
| `semester` | `string` or `null` | Yes | — |
| `retrieved_at` | `string` or `null` | Yes | — |
| `official_source` | `string` or `null` | Yes | — |
| `constraints` | [`ConstraintsResult`](types.md#mcp-type-constraintsresult) | Yes | — |
| `against_session_count` | `integer` | Yes | — |
| `match_count` | `integer` | Yes | — |
| `matches` | array of [`MatchingIndex`](types.md#mcp-type-matchingindex) | Yes | — |
