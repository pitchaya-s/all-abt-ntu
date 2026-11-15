# One Stop: Dashboard and profile MCP tools

[Service overview](../index.md) · [CLI reference](../cli/index.md) · [All MCP tools](index.md) · [Data types](types.md)

## Dashboard and profile

### `onestop_get_dashboard`

Read your One Stop homepage announcements, actions/payment links, upcoming appointments and popular links. Homepage groups may be limited; use the dedicated list tools for their full pages.

**Inputs**

None.

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `announcements` | array of [`PortalRecord`](types.md#mcp-type-portalrecord) | Yes | — |
| `actions` | array of [`PortalRecord`](types.md#mcp-type-portalrecord) | Yes | — |
| `appointments` | array of [`PortalRecord`](types.md#mcp-type-portalrecord) | Yes | — |
| `popular_links` | array of [`PortalRecord`](types.md#mcp-type-portalrecord) | Yes | — |

Unknown fields are not accepted.

### `onestop_list_announcements`

Read One Stop announcements, summaries and links from the native announcements collection with local pagination.

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

### `onestop_list_my_actions`

Read your One Stop to-do/billing actions and their published due dates and payment links. Source counts can be capped; inspect complete. Does not perform an action or pay a bill.

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

### `onestop_list_popular_links`

List links on One Stop's Popular Sites page, preserving native catalog, knowledge and external destinations.

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

### `onestop_get_profile`

Read your own displayed profile fields, editable flags, preferences/choices, notification setting and picture-upload capability. Does not retrieve another user's profile or change identity/security settings.

**Inputs**

None.

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `fields` | array of [`ProfileField`](types.md#mcp-type-profilefield) | Yes | — |
| `preferences` | array of [`Preference`](types.md#mcp-type-preference) | Yes | — |
| `notifications_enabled` | `boolean` or `null` | Yes | — |
| `can_update_picture` | `boolean` | Yes | — |

Unknown fields are not accepted.

### `onestop_update_profile`

Update one displayed editable own-profile field through its native inline editor. Copy field_name from get_profile; bio addresses the live-profile description. Read-only, hidden and password fields are not editable. The server's field validation and permissions apply.

MCP host confirmation is required before this action.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `field_name` | `string` | Yes | — |
| `value` | `string` | Yes | maximum length: `10000` |

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

### `onestop_update_profile_picture`

Upload the explicitly selected local image as your own ServiceNow profile picture using the native file input. Requires an absolute path, a supported image MIME type and a file at most 20 MB. This changes your profile picture.

MCP host confirmation is required before this action.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `file_path` | `string` | Yes | — |

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

### `onestop_set_notifications`

Enable or disable your ServiceNow notification preference. Reads the current setting first; an already matching value is unchanged.

MCP host confirmation is required before this action.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `enabled` | `boolean` | Yes | — |

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

### `onestop_set_user_preference`

Set an enabled own preference returned by get_profile. Use 'true'/'false' for booleans and published choice values for other settings; communication channels are comma-separated choice values. Disabled preferences and identity/MFA/certificate settings are excluded.

MCP host confirmation is required before this action.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `name` | `"accessibility"`, `"voice_input"`, `"analytics"`, `"timezone"`, `"language"`, `"communication_channels"` | Yes | — |
| `value` | `string` | Yes | maximum length: `500` |

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
