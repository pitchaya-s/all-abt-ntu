# STARS: Personal planner and audit MCP tools

[Service overview](../index.md) · [CLI reference](../cli/index.md) · [All MCP tools](index.md) · [Data types](types.md)

## Personal planner and audit

Inputs are required only where marked. A required output field may still be `null` if its type allows it. See [data types](types.md) for nested objects.

### `stars_auth_status`

Report whether WISH credentials are configured and whether this process has verified a session.

**Inputs:** none. Does not log in.

**Returns:** whether a shared keyring account is stored, `credential_storage` of `os_keyring`, a sanitized `credential_error` when unavailable, whether this process has verified a WISH session, its last verification time, and personal-cache settings. No credential or cookie values are returned.

`credentials_configured: null` means the store could not be read; it does not mean the account was never saved. `false` means a readable store has no account.

**Inputs**

None.

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `credentials_configured` | `boolean` or `null` | Yes | — |
| `credential_storage` | `"os_keyring"` | Yes | — |
| `credential_error` | `string` or `null` | Yes | — |
| `session_verified` | `boolean` | Yes | — |
| `last_verified_at` | `string` or `null` | Yes | — |
| `session_storage` | `string` | Yes | — |
| `personal_cache_ttl_seconds` | `integer` | Yes | — |

### `stars_get_stars_planner`

Get registered courses, the published term, and saved Plans 1–3 with indexes and timetables. Use refresh after editing a plan.

**Input:** optional `refresh`, default `false`. Requires credentials.

**Returns:** the published Planner term, registered courses and timetable information, and saved Plans 1–3 with their course/index lists and sessions. Registered courses and saved plans are separate sections. Status fields distinguish empty, parsed, and unavailable data. Use `refresh: true` after editing a plan.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `service` | `string` | Yes | — |
| `page_title` | `string` or `null` | Yes | — |
| `academic_year` | `integer` or `null` | Yes | — |
| `semester` | `integer` or `null` | Yes | — |
| `registration_notice` | `string` or `null` | Yes | — |
| `registered_courses` | array of object of `string` | Yes | — |
| `registered_courses_status` | `string` | Yes | — |
| `planner_tables` | array of [`PersonalTable`](types.md#mcp-type-personaltable) | Yes | — |
| `timetable_tables` | array of [`PersonalTable`](types.md#mcp-type-personaltable) | Yes | — |
| `timetable_status` | `string` | Yes | — |
| `saved_plans` | array of [`SavedPlan`](types.md#mcp-type-savedplan) | Yes | — |
| `source_url` | `string` | Yes | — |
| `retrieved_at` | `string` | Yes | — |
| `from_cache` | `boolean` | Yes | — |
| `cache_age_seconds` | `integer` | Yes | — |

### `stars_get_degree_audit`

Get your degree requirements, examination results, and registered courses from Degree Audit.

**Inputs:** none. Requires credentials.

**Returns:** published degree/AU requirements, examination results, registered courses, and status/source/cache metadata. Academic tables retain their published headers and records. Identity/contact tables are excluded; unknown or missing academic information is not inferred.

**Inputs**

None.

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `service` | `string` | Yes | — |
| `page_title` | `string` or `null` | Yes | — |
| `requirements` | array of [`PersonalTable`](types.md#mcp-type-personaltable) | Yes | — |
| `requirements_status` | `string` | Yes | — |
| `examination_results` | array of [`PersonalTable`](types.md#mcp-type-personaltable) | Yes | — |
| `examination_results_status` | `string` | Yes | — |
| `courses_registered` | array of [`PersonalTable`](types.md#mcp-type-personaltable) | Yes | — |
| `courses_registered_status` | `string` | Yes | — |
| `source_url` | `string` | Yes | — |
| `retrieved_at` | `string` | Yes | — |
| `from_cache` | `boolean` | Yes | — |
| `cache_age_seconds` | `integer` | Yes | — |

### `stars_save_stars_plan`

Replace saved Plan 1, 2, or 3 with the complete supplied course/index list for the current Planner term. Omitted courses are removed from that plan. Verifies persistence by loading the saved plan. Does not perform course registration, dropping, or index swapping.

**Inputs:** `plan_number` of 1–3, the complete `courses` list of 1–13 course/index pairs, `academic_year`, and `semester` of `1` or `2`. Requires credentials, and the term must match the Planner's current term.

**Returns:** the saved plan and verification time after reloading it. This replaces the plan's entire course/index list; omitted courses are removed. It does not register, drop, or swap registered courses. If persistence is uncertain, refresh the Planner before retrying; an uncertain save is not automatically repeated.

```json
{"plan_number":1,"academic_year":2030,"semester":1,"courses":[{"course_code":"ZZ0001","index":"00001"}]}
```

MCP host confirmation is required before this action.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `plan_number` | `1`, `2`, `3` | Yes | — |
| `courses` | array of [`PlannedIndex`](types.md#mcp-type-plannedindex) | Yes | minimum items: `1`; maximum items: `13` |
| `academic_year` | `integer` | Yes | — |
| `semester` | `1`, `2` | Yes | — |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `status` | `string` | Yes | — |
| `academic_year` | `integer` | Yes | — |
| `semester` | `integer` | Yes | — |
| `saved_plan` | [`SavedPlan`](types.md#mcp-type-savedplan) | Yes | — |
| `verified_at` | `string` | Yes | — |
| `source_url` | `string` | Yes | — |

See the [MCP data types](types.md) for nested object fields.
