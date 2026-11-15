# One Stop: Payments, cart and favourites MCP tools

[Service overview](../index.md) · [CLI reference](../cli/index.md) · [All MCP tools](index.md) · [Data types](types.md)

## Payments, cart and favourites

Payment tools prepare a link to the native gateway; they do not complete a payment. Checkout preparation and submission are separate operations, and submission requires host confirmation. Saved-cart loading appends items, while replacement replaces the current cart.

### `onestop_list_payment_services`

Search/browse services in the student's native payment directory, preserving its active/category/access filter. Use leading * for substring search. Does not create a payment or charge anything.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `query` | `string` | No | maximum length: `100`; default: `""` |
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

### `onestop_get_payment_service`

Read a visible payment service's native fixed-amount information. The ID must appear in your payment directory. Variable amounts are completed at the separate payment gateway.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `service_id` | `string` | Yes | pattern: `^[0-9a-f]{32}$` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `service_id` | `string` | Yes | — |
| `title` | `string` | Yes | — |
| `fixed_amount` | `string` or `null` | Yes | — |

Unknown fields are not accepted.

### `onestop_get_cart`

Read your native shopping cart, item quantities/prices, saved-cart IDs/names and checkout defaults. Does not order, load or alter any cart.

**Inputs**

None.

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `items` | array of [`CartItem`](types.md#mcp-type-cartitem) | Yes | — |
| `saved_carts` | array of [`SavedCart`](types.md#mcp-type-savedcart) | Yes | — |
| `delivery_address` | `string` or `null` | Yes | — |
| `special_instructions` | `string` or `null` | Yes | — |
| `two_step_checkout` | `boolean` | Yes | — |

Unknown fields are not accepted.

### `onestop_get_saved_cart`

Inspect items in a verified own saved cart before loading it. Does not merge or replace the active cart.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `saved_cart_id` | `string` | Yes | pattern: `^[0-9a-f]{32}$` |

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

### `onestop_list_favourites`

Read your saved catalog favourites and which are pinned to the homepage. The native portal permits up to four pins.

**Inputs**

None.

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `items` | array of [`Favourite`](types.md#mcp-type-favourite) | Yes | — |
| `pinned_count` | `integer` | Yes | — |
| `maximum_pins` | `integer` | No | default: `4` |

Unknown fields are not accepted.

### `onestop_prepare_cart_checkout`

Create a 15-minute local checkout preview with the current own cart, delivery address and instructions. Does not order anything. submit_cart_checkout rechecks that cart contents have not changed.

This tool changes local workflow state.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `delivery_address` | `string` or `null` | No | default: `null`; maximum length: `10000` |
| `special_instructions` | `string` or `null` | No | default: `null`; maximum length: `10000` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `checkout_id` | `string` | Yes | — |
| `source_url` | `string` | Yes | — |
| `expires_at` | `string` | Yes | format: `date-time` |
| `items` | array of [`CartItem`](types.md#mcp-type-cartitem) | Yes | — |
| `delivery_address` | `string` | Yes | — |
| `special_instructions` | `string` | Yes | — |

Unknown fields are not accepted.

### `onestop_prepare_payment`

Ask One Stop to prepare a checkout link for a visible payment service. Returns the native HTTPS gateway URL for the user to open and complete. Does not enter bank/card credentials, authenticate with a bank, or confirm a charge.

MCP host confirmation is required before this action.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `service_id` | `string` | Yes | pattern: `^[0-9a-f]{32}$` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `service_id` | `string` | Yes | — |
| `title` | `string` | Yes | — |
| `checkout_url` | `string` | Yes | — |
| `requires_browser_completion` | `true` | No | default: `true` |

Unknown fields are not accepted.

### `onestop_update_cart`

Change your native cart: set a permitted quantity, remove/clear items, append a saved cart, replace with a saved cart, or delete a saved cart. IDs must appear in get_cart. replace_with_saved replaces current contents; load_saved appends. Does not checkout.

MCP host confirmation is required before this action.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `action` | `"set_quantity"`, `"remove"`, `"clear"`, `"load_saved"`, `"replace_with_saved"`, `"delete_saved"` | Yes | — |
| `item_id` | `string` or `null` | No | default: `null`; pattern: `^[0-9a-f]{32}$` |
| `quantity` | `integer` or `null` | No | default: `null`; minimum: `1`; maximum: `100` |
| `saved_cart_id` | `string` or `null` | No | default: `null`; pattern: `^[0-9a-f]{32}$` |

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

### `onestop_save_cart`

Save the current cart, or selected own cart item IDs, as a new named cart using native name/selection validation. Existing saved names are not overwritten. Does not submit an order.

MCP host confirmation is required before this action.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `name` | `string` | Yes | minimum length: `1`; maximum length: `100` |
| `item_ids` | array of `string` or `null` | No | default: `null` |

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

### `onestop_submit_cart_checkout`

Submit a reviewed cart checkout exactly once after checking account identity, expiry and unchanged cart contents. Returns the native request receipt. Accounts requiring an additional two-step form receive a portal handoff. Uncertain submissions must be inspected before another checkout.

MCP host confirmation is required before this action.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `checkout_id` | `string` | Yes | minimum length: `16`; maximum length: `100` |

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

### `onestop_update_favourite`

Pin/unpin/remove one own saved favourite or clear all favourites. The native four-pin limit and unpin-before-removal rules apply. clear affects every unpinned favourite; it does not clear the shopping cart.

MCP host confirmation is required before this action.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `action` | `"pin"`, `"unpin"`, `"remove"`, `"clear"` | Yes | — |
| `favourite_id` | `string` or `null` | No | default: `null`; pattern: `^[0-9a-f]{32}$` |

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
