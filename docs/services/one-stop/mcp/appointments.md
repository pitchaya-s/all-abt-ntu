# One Stop: Appointments MCP tools

[Service overview](../index.md) · [CLI reference](../cli/index.md) · [All MCP tools](index.md) · [Data types](types.md)

## Appointments

Appointment slots belong to a prepared draft and can change before booking. Review the returned options and confirm the selected slot. The available tools do not support cancellation or rescheduling.

### `onestop_list_my_appointments`

Read your native upcoming appointment list with appointment numbers, published dates/times and locations. This listing exposes no cancellation/rescheduling controls; no appointment is changed.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `limit` | `integer` | No | minimum: `1`; maximum: `100`; default: `20` |
| `offset` | `integer` | No | minimum: `0`; default: `0` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `offset` | `integer` | Yes | minimum: `0` |
| `available_count` | `integer` | Yes | minimum: `0` |
| `total_count` | `integer` or `null` | Yes | minimum: `0` |
| `complete` | `boolean` | Yes | — |
| `next_offset` | `integer` or `null` | Yes | minimum: `0` |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `records` | array of [`PortalRecord`](types.md#mcp-type-portalrecord) | Yes | — |

Unknown fields are not accepted.

### `onestop_get_appointment_configuration`

Read the native appointment selector's configuration on a local catalog draft: enabled/mandatory flags, duration, booking horizon and weekdays. Use an appointment service's form_item_id to prepare the draft.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `draft_id` | `string` | Yes | minimum length: `16`; maximum length: `100` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `draft_id` | `string` | Yes | — |
| `item_id` | `string` | Yes | — |
| `enabled` | `boolean` | Yes | — |
| `duration_minutes` | `integer` or `null` | Yes | — |
| `future_bookable_days` | `integer` or `null` | Yes | — |
| `bookable_weekdays` | `string` or `null` | Yes | — |
| `mandatory` | `boolean` | Yes | — |

Unknown fields are not accepted.

### `onestop_get_appointment_slots`

Read available appointment windows for one day using the draft's current native location/contact/reason configuration. Returned slot IDs are bound to this draft's latest lookup. No time is reserved or booked; availability can change until submission.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `draft_id` | `string` | Yes | minimum length: `16`; maximum length: `100` |
| `date` | `string` | Yes | pattern: `^\d{4}-\d{2}-\d{2}$` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `draft_id` | `string` | Yes | — |
| `date` | `string` | Yes | — |
| `timezone` | `string` or `null` | Yes | — |
| `slots` | array of [`AppointmentSlot`](types.md#mcp-type-appointmentslot) | Yes | — |
| `retrieved_at` | `string` | Yes | format: `date-time` |

Unknown fields are not accepted.

### `onestop_select_appointment_slot`

Select a slot from this draft's latest availability lookup using the native appointment event. Updates the local form and validation preview only. Changing draft answers requires another availability lookup and selection.

This tool changes local workflow state.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `draft_id` | `string` | Yes | minimum length: `16`; maximum length: `100` |
| `slot_id` | `string` | Yes | minimum length: `16`; maximum length: `100` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `draft_id` | `string` | Yes | — |
| `item_id` | `string` | Yes | — |
| `title` | `string` | Yes | — |
| `source_url` | `string` | Yes | — |
| `expires_at` | `string` | Yes | format: `date-time` |
| `state` | `"prepared"`, `"submitting"`, `"submitted"`, `"uncertain"` | Yes | — |
| `ready` | `boolean` | Yes | — |
| `missing_fields` | array of `string` | Yes | — |
| `invalid_fields` | array of `string` | Yes | — |
| `fields` | array of [`DraftField`](types.md#mcp-type-draftfield) | Yes | — |
| `available_actions` | array of `string` | Yes | — |
| `receipt_id` | `string` or `null` | No | default: `null` |

Unknown fields are not accepted.

### `onestop_book_appointment`

Book an appointment by optionally selecting a verified slot and submitting the reviewed native catalog draft once. All native mandatory questions must be complete. Reusing a completed draft returns its receipt; uncertain bookings are never auto-retried.

MCP host confirmation is required before this action.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `draft_id` | `string` | Yes | minimum length: `16`; maximum length: `100` |
| `slot_id` | `string` or `null` | No | default: `null`; minimum length: `16`; maximum length: `100` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `operation` | `string` | Yes | — |
| `completed_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `resource_id` | `string` or `null` | Yes | — |
| `outcome` | `"completed"`, `"unchanged"`, `"uncertain"`, `"requires_user_action"` | Yes | — |
| `verified` | `boolean` | Yes | — |
| `message` | `string` or `null` | Yes | — |
| `references` | array of [`NamedValue`](types.md#mcp-type-namedvalue) | Yes | — |

Unknown fields are not accepted.

See the [MCP data types](types.md) for nested object fields.
