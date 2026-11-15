# STARS: MCP data types

[Service overview](../index.md) · [MCP reference](index.md)

## MCP data types

These named types describe nested fields in the [MCP tool reference](index.md). A required field may still be `null` when its type allows it.

<a id="mcp-type-availableroom"></a>
### `AvailableRoom`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `venue` | `string` | Yes | — |
| `room_type` | `"tutorial_room"`, `"seminar_room"`, `"lecture_theatre"`, `"laboratory"`, `"other"` | Yes | — |
| `aliases` | array of `string` | Yes | — |
| `observed_lesson_types` | array of `string` | Yes | — |
| `free_from` | `string` | Yes | — |
| `free_until` | `string` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-clashcheck"></a>
### `ClashCheck`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `against_session_count` | `integer` | Yes | — |
| `clashes_by_index` | object of array of [`ClashPair`](#mcp-type-clashpair) | Yes | — |
| `uncertain_comparisons_by_index` | object of `integer` | Yes | — |

<a id="mcp-type-clashpair"></a>
### `ClashPair`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_session` | [`CompactSession`](#mcp-type-compactsession) | Yes | — |
| `existing_session` | [`ExistingSession`](#mcp-type-existingsession) | Yes | — |

<a id="mcp-type-compactsession"></a>
### `CompactSession`

Course/index are inherited from the result; unfamiliar day/time text stays explicit.

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `lesson_type` | `string` or `null` | Yes | — |
| `group` | `string` or `null` | Yes | — |
| `day` | `string` or `null` | Yes | — |
| `start_time` | `string` or `null` | Yes | — |
| `end_time` | `string` or `null` | Yes | — |
| `venue` | `string` or `null` | Yes | — |
| `teaching_weeks` | array of `integer` or `null` | Yes | — |
| `remarks` | `string` or `null` | Yes | — |
| `raw_time` | `string` | No | — |
| `raw_day` | `string` | No | — |

<a id="mcp-type-constraintsresult"></a>
### `ConstraintsResult`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `avoid_days` | array of `string` | No | — |
| `earliest_start` | `string` | No | — |
| `latest_end` | `string` | No | — |
| `avoid_windows` | array of [`TimeWindowResult`](#mcp-type-timewindowresult) | No | — |
| `require_sessions` | array of [`SessionRule`](#mcp-type-sessionrule) | No | — |
| `teaching_weeks` | array of `integer` | No | — |

<a id="mcp-type-courseindex"></a>
### `CourseIndex`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `vacancy_status` | `"available"`, `"not_listed"`, `"closed"`, `"term_mismatch"`, `"unavailable"` | Yes | — |
| `vacancies_available` | `integer` or `null` | Yes | — |
| `waitlist_length` | `integer` or `null` | Yes | — |
| `index` | `string` | Yes | — |
| `schedule_complete` | `boolean` | Yes | — |
| `sessions` | array of [`CompactSession`](#mcp-type-compactsession) | Yes | — |

<a id="mcp-type-coursenote"></a>
### `CourseNote`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `label` | `string` | Yes | — |
| `text` | `string` | Yes | — |

<a id="mcp-type-coursesearchmatch"></a>
### `CourseSearchMatch`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_code` | `string` | Yes | — |
| `course_name` | `string` | Yes | — |
| `au` | `number` or `null` | Yes | — |

<a id="mcp-type-examresult"></a>
### `ExamResult`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `date` | `string` or `null` | Yes | — |
| `day` | `string` or `null` | Yes | — |
| `start_time` | `string` or `null` | Yes | — |
| `end_time` | `string` or `null` | Yes | — |
| `duration_minutes` | `integer` or `null` | Yes | — |
| `duration_text` | `string` | No | — |
| `raw_date` | `string` | No | — |
| `raw_day` | `string` or `null` | No | — |
| `raw_time` | `string` or `null` | No | — |

<a id="mcp-type-existingsession"></a>
### `ExistingSession`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `day` | `string` | No | — |
| `start_time` | `string` | No | — |
| `end_time` | `string` | No | — |
| `teaching_weeks` | array of `integer` | No | — |

<a id="mcp-type-graduateclassgroup"></a>
### `GraduateClassGroup`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `class_group` | `string` or `null` | Yes | — |
| `coordinator` | `string` or `null` | Yes | — |
| `sessions` | array of [`GraduateSession`](#mcp-type-graduatesession) | Yes | — |
| `schedule_remarks` | array of `string` | Yes | — |
| `schedule_text` | `string` or `null` | No | — |

<a id="mcp-type-graduatesession"></a>
### `GraduateSession`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `day` | `string` or `null` | Yes | — |
| `start_time` | `string` or `null` | Yes | — |
| `end_time` | `string` or `null` | Yes | — |
| `venue` | `string` or `null` | Yes | — |
| `commence_date` | `string` or `null` | Yes | — |
| `teaching_weeks` | array of `integer` or `null` | Yes | — |

<a id="mcp-type-matchingindex"></a>
### `MatchingIndex`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `index` | `string` | Yes | — |
| `status` | `"confirmed"`, `"uncertain"` | Yes | — |
| `uncertainties` | array of `string` | Yes | — |
| `schedule_complete` | `boolean` | Yes | — |
| `sessions` | array of [`CompactSession`](#mcp-type-compactsession) | Yes | — |

<a id="mcp-type-personaltable"></a>
### `PersonalTable`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `section` | `string` or `null` | Yes | — |
| `headers` | array of `string` | Yes | — |
| `rows` | array of array of `string` | No | — |
| `records` | array of object of `string` | Yes | — |

<a id="mcp-type-plannedcourse"></a>
### `PlannedCourse`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_code` | `string` | Yes | — |
| `index` | `string` or `null` | Yes | — |
| `course_type` | `string` or `null` | Yes | — |

<a id="mcp-type-plannedindex"></a>
### `PlannedIndex`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_code` | `string` | Yes | NTU undergraduate course code |
| `index` | `string` | Yes | Index number as a string; pattern: `^[0-9]{1,12}$` |

<a id="mcp-type-plannersession"></a>
### `PlannerSession`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_code` | `string` | Yes | — |
| `index` | `string` or `null` | No | — |
| `lesson_type` | `string` | Yes | — |
| `group` | `string` | Yes | — |
| `day` | `string` | Yes | — |
| `start_time` | `string` or `null` | Yes | — |
| `end_time` | `string` or `null` | Yes | — |
| `venue` | `string` | Yes | — |
| `teaching_weeks` | array of `integer` or `null` | Yes | — |
| `remarks` | `string` or `null` | Yes | — |
| `raw_time` | `string` or `null` | No | — |

<a id="mcp-type-prerequisitetreenode"></a>
### `PrerequisiteTreeNode`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_code` | `string` | Yes | — |
| `course_name` | `string` or `null` | Yes | — |
| `au` | `number` or `null` | Yes | — |
| `offered_this_term` | `boolean` | Yes | — |
| `course_data_status` | `"available"`, `"unavailable"`, `"not_loaded"` | Yes | — |
| `official_source` | `string` or `null` | Yes | — |
| `retrieved_at` | `string` or `null` | Yes | — |
| `depth` | `integer` | Yes | — |
| `match_status` | `"root"`, `"confirmed"`, `"possible"` | Yes | — |
| `path_status` | `"root"`, `"confirmed"`, `"possible"` | Yes | — |
| `matched_relations` | array of `string` | Yes | — |
| `prerequisite_status` | `"parsed"`, `"unparsed"`, `"not_listed"`, `"conflicting_records"`, `"unavailable"`, `"not_loaded"` | Yes | — |
| `prerequisite_text` | `string` or `null` | Yes | — |
| `prerequisite_texts` | array of `string` or `null` | Yes | — |
| `prerequisite_expression` | `object` or `null` | Yes | — |
| `eligibility_status` | `"eligible"`, `"not_eligible"`, `"unknown"`, `"not_evaluated"`, `"not_listed"` | Yes | — |
| `prerequisites` | array of `object` | Yes | — |
| `dependents` | array of `object` | Yes | — |
| `cycle_detected` | `boolean` | No | — |
| `prerequisites_truncated` | `boolean` | No | — |
| `dependents_truncated` | `boolean` | No | — |

<a id="mcp-type-roomcoverage"></a>
### `RoomCoverage`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `scope` | `"published_undergraduate_full_time_and_part_time_teaching"` | No | default: `"published_undergraduate_full_time_and_part_time_teaching"` |
| `course_count` | `integer` | Yes | — |
| `courses_without_published_indexes` | `integer` | Yes | — |
| `index_count` | `integer` | Yes | — |
| `lesson_count` | `integer` | Yes | — |
| `observed_room_count` | `integer` | Yes | — |
| `excluded_venue_label_count` | `integer` | Yes | — |
| `unplaced_lesson_count` | `integer` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-roomfilters"></a>
### `RoomFilters`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `room_types` | array of `"tutorial_room"`, `"seminar_room"`, `"lecture_theatre"`, `"laboratory"`, `"other"` or `null` | No | Inferred from venue codes, not lesson types or an official room inventory.; default: `null`; minimum items: `1`; maximum items: `5` |
| `venue_contains` | `string` or `null` | No | default: `null`; minimum length: `1`; maximum length: `80` |
| `venue_prefixes` | array of `string` or `null` | No | Venue-code prefixes such as LHN, LHS, SPMS or S4. No geographic location is inferred for bare TR/LT labels.; default: `null`; minimum items: `1`; maximum items: `20` |
| `exclude_venues` | array of `string` | No | maximum items: `100` |
| `used_for_lesson_types` | array of `string` or `null` | No | Candidate rooms must have at least one published lesson of these types. All lesson types still block availability.; default: `null`; minimum items: `1`; maximum items: `20` |

Unknown fields are not accepted.

<a id="mcp-type-roomidentity"></a>
### `RoomIdentity`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `venue` | `string` | Yes | — |
| `room_type` | `"tutorial_room"`, `"seminar_room"`, `"lecture_theatre"`, `"laboratory"`, `"other"` | Yes | — |
| `aliases` | array of `string` | Yes | — |
| `observed_lesson_types` | array of `string` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-roomlesson"></a>
### `RoomLesson`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_code` | `string` | Yes | — |
| `indexes` | array of `string` | Yes | — |
| `lesson_type` | `string` or `null` | Yes | — |
| `group` | `string` or `null` | Yes | — |
| `day` | `string` or `null` | Yes | — |
| `start_time` | `string` or `null` | Yes | — |
| `end_time` | `string` or `null` | Yes | — |
| `teaching_weeks` | array of `integer` or `null` | Yes | — |
| `remarks` | `string` or `null` | Yes | — |
| `raw_day` | `string` or `null` | Yes | — |
| `raw_time` | `string` or `null` | Yes | — |
| `source_venue_labels` | array of `string` | No | Original venue text when it differs from the enclosing canonical room, including multi-room cells. |

Unknown fields are not accepted.

<a id="mcp-type-roomwindow"></a>
### `RoomWindow`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `day` | `"MON"`, `"TUE"`, `"WED"`, `"THU"`, `"FRI"`, `"SAT"`, `"SUN"` | Yes | — |
| `start_time` | `string` | Yes | pattern: `^(?:[01]\d\|2[0-3]):[0-5]\d$` |
| `end_time` | `string` | Yes | pattern: `^(?:[01]\d\|2[0-3]):[0-5]\d$` |
| `teaching_weeks` | array of `integer` or `null` | No | Free in every requested teaching week. Omit to consider every published meeting, conservatively across the whole term.; default: `null`; minimum items: `1`; maximum items: `20` |
| `buffer_minutes` | `integer` | No | Additional teaching-free minutes required before and after the requested interval.; minimum: `0`; maximum: `120`; default: `0` |

Unknown fields are not accepted.

<a id="mcp-type-savedplan"></a>
### `SavedPlan`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `plan_number` | `integer` | Yes | — |
| `status` | `string` | Yes | — |
| `courses` | array of [`PlannedCourse`](#mcp-type-plannedcourse) | Yes | — |
| `sessions` | array of [`PlannerSession`](#mcp-type-plannersession) | Yes | — |
| `unparsed_sessions` | array of object of `string` | Yes | — |
| `timetable_status` | `string` | Yes | — |

<a id="mcp-type-searchconstraints"></a>
### `SearchConstraints`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `avoid_days` | array of `"MON"`, `"TUE"`, `"WED"`, `"THU"`, `"FRI"`, `"SAT"`, `"SUN"` | No | Reject indexes with a known class on these days |
| `earliest_start` | `string` or `null` | No | Every class must start at or after this time; default: `null`; 24-hour time in HH:MM format; pattern: `^(?:[01]\d\|2[0-3]):[0-5]\d$` |
| `latest_end` | `string` or `null` | No | Every class must end by this time; default: `null`; 24-hour time in HH:MM format; pattern: `^(?:[01]\d\|2[0-3]):[0-5]\d$` |
| `avoid_windows` | array of [`TimeWindow`](#mcp-type-timewindow) | No | Reject classes overlapping these day/time windows |
| `require_sessions` | array of [`SessionRequirement`](#mcp-type-sessionrequirement) | No | Each requirement must match at least one session |
| `teaching_weeks` | array of `integer` or `null` | No | Evaluate only sessions meeting in these teaching weeks; unspecified week rules remain uncertain; default: `null`; minimum items: `1`; maximum items: `20` |

<a id="mcp-type-sessionrequirement"></a>
### `SessionRequirement`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `lesson_type` | `string` or `null` | No | Exact NTU lesson type, such as TUT or LAB; default: `null` |
| `day` | `"MON"`, `"TUE"`, `"WED"`, `"THU"`, `"FRI"`, `"SAT"`, `"SUN"` or `null` | No | default: `null` |
| `starts_at_or_after` | `string` or `null` | No | default: `null`; 24-hour time in HH:MM format; pattern: `^(?:[01]\d\|2[0-3]):[0-5]\d$` |
| `starts_at_or_before` | `string` or `null` | No | default: `null`; 24-hour time in HH:MM format; pattern: `^(?:[01]\d\|2[0-3]):[0-5]\d$` |

<a id="mcp-type-sessionrule"></a>
### `SessionRule`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `lesson_type` | `string` | No | — |
| `day` | `string` | No | — |
| `starts_at_or_after` | `string` | No | — |
| `starts_at_or_before` | `string` | No | — |

<a id="mcp-type-timeslot"></a>
### `TimeSlot`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `day` | `"MON"`, `"TUE"`, `"WED"`, `"THU"`, `"FRI"`, `"SAT"`, `"SUN"` or `null` | No | default: `null` |
| `start_time` | `string` or `null` | No | default: `null`; 24-hour time in HH:MM format; pattern: `^(?:[01]\d\|2[0-3]):[0-5]\d$` |
| `end_time` | `string` or `null` | No | default: `null`; 24-hour time in HH:MM format; pattern: `^(?:[01]\d\|2[0-3]):[0-5]\d$` |
| `teaching_weeks` | array of `integer` or `null` | No | Known teaching weeks; omit if unknown. Overlapping times with unknown weeks remain uncertain.; default: `null`; minimum items: `1`; maximum items: `20` |

<a id="mcp-type-timewindow"></a>
### `TimeWindow`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `day` | `"MON"`, `"TUE"`, `"WED"`, `"THU"`, `"FRI"`, `"SAT"`, `"SUN"` | Yes | — |
| `start_time` | `string` | Yes | 24-hour time in HH:MM format; pattern: `^(?:[01]\d\|2[0-3]):[0-5]\d$` |
| `end_time` | `string` | Yes | 24-hour time in HH:MM format; pattern: `^(?:[01]\d\|2[0-3]):[0-5]\d$` |

<a id="mcp-type-timewindowresult"></a>
### `TimeWindowResult`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `day` | `string` | Yes | — |
| `start_time` | `string` | Yes | — |
| `end_time` | `string` | Yes | — |

<a id="mcp-type-vacancymetadata"></a>
### `VacancyMetadata`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `status` | `"available"`, `"closed"`, `"term_mismatch"`, `"unavailable"` | Yes | — |
| `retrieved_at` | `string` or `null` | Yes | — |
| `academic_year` | `integer` or `null` | No | — |
| `semester` | `string` or `null` | No | — |
| `source_url` | `string` | No | — |
| `from_cache` | `boolean` | No | — |
| `cache_age_seconds` | `number` or `null` | No | — |
| `message` | `string` | No | — |
