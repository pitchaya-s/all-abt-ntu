# STARS: Courses, prerequisites and exams MCP tools

[Service overview](../index.md) · [CLI reference](../cli/index.md) · [All MCP tools](index.md) · [Data types](types.md)

## Courses, prerequisites and exams

Inputs are required only where marked. A required output field may still be `null` if its type allows it. See [data types](types.md) for nested objects.

### `stars_search_courses`

Search NTU's public undergraduate Class Schedule by partial code or title keywords. Returns course codes, names and AUs for the requested term and study mode. Use offset/limit to page through matches, then stars_get_course_metadata or stars_get_course_indexes for details. This is not a graduate or all-catalogue search.

Find scheduled undergraduate offerings by partial code or title words.

**Inputs:** `query` of 2–80 characters, `academic_year`, `semester`; optional `study_mode` of `"full_time"` or `"part_time"`, `limit` of 1–100 with default 20, and nonnegative `offset` with default 0. Wildcards are not accepted.

**Returns:** course codes, names, AUs, `total_count`, `has_more`, and source/retrieval metadata. Continue with a larger offset to read another page. Results cover scheduled offerings for that term and study mode, rather than the entire historical catalogue or graduate courses.

```json
{"query":"ZZ00","academic_year":2030,"semester":1,"limit":20}
```

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `query` | `string` | Yes | Partial course code or title words, such as SC20 or DATA STRUCTURES; no wildcards; minimum length: `2`; maximum length: `80` |
| `academic_year` | `integer` | Yes | — |
| `semester` | `1`, `2`, `"S"` | Yes | — |
| `study_mode` | `"full_time"`, `"part_time"` | No | default: `"full_time"` |
| `limit` | `integer` | No | minimum: `1`; maximum: `100`; default: `20` |
| `offset` | `integer` | No | minimum: `0`; default: `0` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `query` | `string` | Yes | — |
| `academic_year` | `integer` | Yes | — |
| `semester` | `string` | Yes | — |
| `study_mode` | `"full_time"`, `"part_time"` | Yes | — |
| `total_count` | `integer` | Yes | — |
| `offset` | `integer` | Yes | — |
| `has_more` | `boolean` | Yes | — |
| `courses` | array of [`CourseSearchMatch`](types.md#mcp-type-coursesearchmatch) | Yes | — |
| `source_url` | `string` | Yes | — |
| `retrieved_at` | `string` | Yes | — |

### `stars_get_course_metadata`

Get course name, AUs, prerequisites, description, and term metadata.

**Inputs:** `course_code`, `academic_year`, `semester`, optional `limit` (1–50, default 10) and non-negative `offset`.

**Returns:** course name, AU, prerequisites when published, course description, course notes, term, and source metadata. `course_description_status` distinguishes `available`, `not_listed`, and `unavailable`. This tool returns metadata rather than index timetables.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_code` | `string` | Yes | — |
| `academic_year` | `integer` | Yes | — |
| `semester` | `1`, `2`, `"S"` | Yes | — |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_code` | `string` | Yes | — |
| `academic_year` | `integer` or `null` | Yes | — |
| `semester` | `string` or `null` | Yes | — |
| `course_name` | `string` | Yes | — |
| `au` | `number` or `null` | Yes | — |
| `course_description` | `string` or `null` | Yes | — |
| `course_description_status` | `"available"`, `"not_listed"`, `"unavailable"` | Yes | — |
| `course_description_source` | `string` or `null` | Yes | — |
| `prerequisites` | `string` or `null` | Yes | — |
| `course_notes` | array of [`CourseNote`](types.md#mcp-type-coursenote) | Yes | — |
| `retrieved_at` | `string` or `null` | Yes | — |
| `official_source` | `string` or `null` | Yes | — |

### `stars_get_prerequisite_tree`

Build before and after branches around a course, with separate depth limits.      The before branch follows the course's prerequisite rules; the after branch finds courses     that depend on it in the selected term. The center course is treated as completed for eligibility.

Build a tree around one course, with a **before** branch for its prerequisites and an **after** branch for courses that depend on it.

**Inputs:** `course_code`, `academic_year`, `semester`; optional `prerequisite_depth` and `dependent_depth`, each 0–5 with default 2; `completed_courses` (up to 100 course codes); `only_eligible` (default false); `include_corequisites` (default false); and `max_nodes` per branch, 1–100 with default 100. The center course is treated as completed for eligibility evaluation. `only_eligible` requires `completed_courses` and filters the **after** branch.

**Returns:** a nested tree with published prerequisite expressions on each course. Recognized `AND`/`OR` rules preserve their alternative paths; `completed_courses` marks which paths are satisfied. The **before** branch uses NTU course-content metadata for prerequisite courses that are not offered in the selected term. The **after** branch searches scheduled undergraduate offerings in that term across full-time and part-time study modes. `source_urls` lists the official endpoints used, and each expanded course includes its source when available.

Unrecognized expressions, conflicting full-time/part-time records, and unavailable off-term course metadata remain labeled uncertain. Possible text matches are not treated as confirmed prerequisite rules. The tree is bounded by both depth inputs and `max_nodes`; `prerequisites_truncated` and `dependents_truncated` identify a branch cut short. This is not a historical or complete course-catalogue search.

```json
{"course_code":"ZZ0001","academic_year":2030,"semester":1,"prerequisite_depth":2,"dependent_depth":2,"completed_courses":["MH1812"]}
```

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_code` | `string` | Yes | Course at the center of the prerequisite tree; minimum length: `2`; maximum length: `10` |
| `academic_year` | `integer` | Yes | — |
| `semester` | `1`, `2`, `"S"` | Yes | — |
| `prerequisite_depth` | `integer` | No | How many prerequisite levels to expand before the center course; minimum: `0`; maximum: `5`; default: `2` |
| `dependent_depth` | `integer` | No | How many dependent-course levels to expand after the center course; minimum: `0`; maximum: `5`; default: `2` |
| `completed_courses` | array of `string` or `null` | No | Courses already completed; the center course is added automatically for eligibility evaluation; default: `null`; maximum items: `100` |
| `only_eligible` | `boolean` | No | Keep only dependent courses whose parsed prerequisite rules are satisfied by completed_courses; default: `false` |
| `include_corequisites` | `boolean` | No | Also follow co-requisite links in both directions; default: `false` |
| `max_nodes` | `integer` | No | Maximum nodes per before/after branch; minimum: `1`; maximum: `100`; default: `100` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_code` | `string` | Yes | — |
| `academic_year` | `integer` | Yes | — |
| `semester` | `string` | Yes | — |
| `prerequisite_depth` | `integer` | Yes | — |
| `dependent_depth` | `integer` | Yes | — |
| `include_corequisites` | `boolean` | Yes | — |
| `only_eligible` | `boolean` | Yes | — |
| `completed_courses` | array of `string` or `null` | Yes | — |
| `prerequisite_course_count` | `integer` | Yes | — |
| `dependent_course_count` | `integer` | Yes | — |
| `tree_node_count` | `integer` | Yes | — |
| `prerequisites_truncated` | `boolean` | Yes | — |
| `dependents_truncated` | `boolean` | Yes | — |
| `truncated` | `boolean` | Yes | — |
| `coverage` | object of `integer` | Yes | — |
| `root` | [`PrerequisiteTreeNode`](types.md#mcp-type-prerequisitetreenode) | Yes | — |
| `source_urls` | array of `string` | Yes | — |
| `retrieved_at` | `string` | Yes | — |

### `stars_get_graduate_course_schedule`

Get a graduate course's class groups for NTU's currently published academic term.

**Input:** `course_code`.

**Returns:** the latest published graduate term, class groups, coordinators when provided, sessions, commencement dates, and schedule remarks. Graduate results use class groups rather than undergraduate indexes. GSLink/PGR does not publish teaching-week rules through this lookup.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_code` | `string` | Yes | — |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_code` | `string` | Yes | — |
| `course_name` | `string` | Yes | — |
| `au` | `number` or `null` | Yes | — |
| `academic_year` | `integer` | Yes | — |
| `term` | `string` | Yes | — |
| `schedule_complete` | `boolean` | Yes | — |
| `class_groups` | array of [`GraduateClassGroup`](types.md#mcp-type-graduateclassgroup) | Yes | — |
| `source_url` | `string` | Yes | — |

### `stars_get_undergraduate_exam_schedule`

Get public General Access exam dates and times for a course in the latest or specified published term.

**Inputs:** `course_code`; optionally both `academic_year` and `semester` of `1` or `2`. Omitting both selects NTU's latest published exam term.

**Returns:** exam date, day, start/end time, duration, published venue when available, publication notice, source, and retrieval time. `exam_status` distinguishes `available` from `not_listed`. General Access does not provide personal exam-seat assignments.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_code` | `string` | Yes | — |
| `academic_year` | `integer` or `null` | No | default: `null` |
| `semester` | `1`, `2` or `null` | No | default: `null` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `course_code` | `string` | Yes | — |
| `course_name` | `string` or `null` | Yes | — |
| `academic_year` | `integer` | Yes | — |
| `semester` | `string` | Yes | — |
| `exam_status` | `"available"`, `"not_listed"` | Yes | — |
| `exam_count` | `integer` | Yes | — |
| `exams` | array of [`ExamResult`](types.md#mcp-type-examresult) | Yes | — |
| `notice` | `string` or `null` | Yes | — |
| `source_url` | `string` | Yes | — |
| `retrieved_at` | `string` | Yes | — |
