# One Stop: Catalog and access MCP tools

[Service overview](../index.md) · [CLI reference](../cli/index.md) · [All MCP tools](index.md) · [Data types](types.md)

## Catalog and access

### `onestop_auth_status`

Report shared keyring availability and the last verified One Stop session without logging in or returning identity or credentials. An unavailable keyring reports credentials_configured=null.

**Inputs**

None.

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `credentials_configured` | `boolean` or `null` | Yes | — |
| `credential_storage` | `"os_keyring"` | No | default: `"os_keyring"` |
| `credential_error` | `string` or `null` | Yes | — |
| `session_verified` | `boolean` | Yes | — |
| `last_verified_at` | `string` or `null` | Yes | format: `date-time` |
| `session_storage` | `"in_memory_only"` | No | default: `"in_memory_only"` |
| `cache_ttl_seconds` | `integer` | No | default: `60` |

Unknown fields are not accepted.

### `onestop_list_catalog_categories`

List the signed-in student's visible One Stop catalog categories and subcategories, parent IDs and published item counts. Pass category_id to onestop_list_catalog_items. Requires saved NTU student credentials and Chromium.

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
| `categories` | array of [`Category`](types.md#mcp-type-category) | Yes | — |
| `root_count` | `integer` | Yes | — |
| `total_root_count` | `integer` | Yes | — |
| `complete` | `boolean` | Yes | — |

Unknown fields are not accepted.

### `onestop_list_catalog_items`

Search the student's One Stop service catalog with query, or browse one category_id. Supply at most one filter; no filter returns popular items. Distinguishes external links, knowledge and native forms; use form_item_id for get_catalog_item. Category results can be partial. next_offset pages retrieved records only; complete=false means the source does not establish full coverage.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `query` | `string` | No | maximum length: `200`; default: `""` |
| `category_id` | `string` or `null` | No | default: `null`; pattern: `^[0-9a-f]{32}$` |
| `limit` | `integer` | No | minimum: `1`; maximum: `100`; default: `20` |
| `offset` | `integer` | No | minimum: `0`; default: `0` |
| `refresh` | `boolean` | No | default: `false` |

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
| `scope` | `"popular"`, `"category"`, `"search"` | Yes | — |
| `query` | `string` | Yes | — |
| `category_id` | `string` or `null` | Yes | — |
| `items` | array of [`CatalogItem`](types.md#mcp-type-catalogitem) | Yes | — |

Unknown fields are not accepted.

### `onestop_get_catalog_item`

Read a native One Stop form's description, current visible field labels/types, mandatory flags and choices. Use form_item_id from list_catalog_items. Prefilled personal values are omitted. Conditional fields can change when answers change. Does not fill or submit the form or follow external applications.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `item_id` | `string` | Yes | pattern: `^[0-9a-f]{32}$` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `item_id` | `string` | Yes | — |
| `title` | `string` | Yes | — |
| `summary` | `string` or `null` | Yes | — |
| `description` | `string` | Yes | — |
| `mandatory_attachment` | `boolean` or `null` | Yes | — |
| `fields` | array of [`FormField`](types.md#mcp-type-formfield) | Yes | — |

Unknown fields are not accepted.

### `onestop_set_catalog_favourite`

Set a catalog item's favourite state through its category's native control. Both IDs must match a visible category item. Uses the desired state and verifies it against your favourites list.

MCP host confirmation is required before this action.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `category_id` | `string` | Yes | pattern: `^[0-9a-f]{32}$` |
| `item_id` | `string` | Yes | pattern: `^[0-9a-f]{32}$` |
| `favourite` | `boolean` | Yes | — |

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
