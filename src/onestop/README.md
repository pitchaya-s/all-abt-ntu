# One Stop @ SAC

[CLI commands](#cli-commands) · [MCP tools](#mcp-tools) · [MCP data types](#mcp-data-types) · [Service notes](#service-notes)

For installation and shared authentication, see the [main README](../../README.md).

## CLI commands

The output column lists the JSON result fields; human-readable output is formatted for the terminal. Use `ntu onestop --help` and append `--help` to a command for option details. `VALUE` denotes an option value; required arguments and options are marked. See the [complete CLI reference](../COMMANDS.md) for shared settings and all services.

| Command | Arguments and options | Purpose | Output |
| --- | --- | --- | --- |
| `ntu onestop dashboard` | `--json/-j` | Read your One Stop homepage announcements, actions/payment links, upcoming appointments and popular links. | `retrieved_at`, `source_url`, `cached`, `announcements`, `actions`, `appointments`, `popular_links` ([schema](#onestop_get_dashboard)) |
| `ntu onestop announcements` | `--limit/-l VALUE (default: 20)`, `--offset VALUE`, `--json/-j` | Read One Stop announcements, summaries and links from the native announcements collection with local pagination. | `offset`, `available_count`, `total_count`, `complete`, `next_offset`, `retrieved_at`, `source_url`, `cached`, `records` ([schema](#onestop_list_announcements)) |
| `ntu onestop actions` | `--limit/-l VALUE (default: 20)`, `--offset VALUE`, `--json/-j` | Read your One Stop to-do/billing actions and their published due dates and payment links. | `offset`, `available_count`, `total_count`, `complete`, `next_offset`, `retrieved_at`, `source_url`, `cached`, `records` ([schema](#onestop_list_my_actions)) |
| `ntu onestop links` | `--limit/-l VALUE (default: 20)`, `--offset VALUE`, `--json/-j` | List links on One Stop's Popular Sites page, preserving native catalog, knowledge and external destinations. | `offset`, `available_count`, `total_count`, `complete`, `next_offset`, `retrieved_at`, `source_url`, `cached`, `records` ([schema](#onestop_list_popular_links)) |
| `ntu onestop appointments book` | `ITEM_ID (required)` | Prepare an appointment form, choose a slot and book it in one session. | `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references` ([schema](#onestop_book_appointment)) |
| `ntu onestop appointments list` | `--limit/-l VALUE (default: 20)`, `--offset VALUE`, `--json/-j` | Read your native upcoming appointment list with appointment numbers, published dates/times and locations. | `offset`, `available_count`, `total_count`, `complete`, `next_offset`, `retrieved_at`, `source_url`, `cached`, `records` ([schema](#onestop_list_my_appointments)) |
| `ntu onestop attachments list` | `TARGET (required)`, `--record-id VALUE`, `--json/-j` | List attachments on a verified own request/item or a readable knowledge article/comment. | `retrieved_at`, `source_url`, `cached`, `attachments`, `can_upload`, `max_upload_bytes` ([schema](#onestop_list_attachments)) |
| `ntu onestop attachments upload` | `TARGET (required)`, `FILE_PATH (required)`, `--record-id VALUE`, `--json/-j` | Upload an explicitly selected file from the configured One Stop upload directory to the verified target. | `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references` ([schema](#onestop_upload_attachment)) |
| `ntu onestop attachments download` | `TARGET (required)`, `ATTACHMENT_ID (required)`, `--output/-o VALUE (required)`, `--record-id VALUE`, `--json/-j` | Download a listed attachment of the verified target to a new explicit absolute file path, up to 20 MB. | `attachment_id`, `path`, `bytes_written`, `sha256`, `downloaded_at` ([schema](#onestop_download_attachment)) |
| `ntu onestop attachments delete` | `TARGET (required)`, `ATTACHMENT_ID (required)`, `--record-id VALUE`, `--json/-j` | Delete an attachment only when it is listed on the verified target and native editing is allowed. | `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references` ([schema](#onestop_delete_attachment)) |
| `ntu onestop attachments rename` | `TARGET (required)`, `ATTACHMENT_ID (required)`, `FILE_NAME (required)`, `--record-id VALUE`, `--json/-j` | Rename a listed editable attachment using the native attachment service. | `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references` ([schema](#onestop_rename_attachment)) |
| `ntu onestop auth status` | `--json/-j` | Report shared keyring availability and the last verified One Stop session without logging in or returning identity or credentials. | `credentials_configured`, `credential_storage`, `credential_error`, `session_verified`, `last_verified_at`, `session_storage`, `cache_ttl_seconds` ([schema](#onestop_auth_status)) |
| `ntu onestop cart quantity` | `ITEM_ID (required)`, `QUANTITY (required)`, `--json/-j` | Change your native cart: set a permitted quantity, remove/clear items, append a saved cart, replace with a saved cart, or delete a saved cart. | `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references` ([schema](#onestop_update_cart)) |
| `ntu onestop cart remove` | `ITEM_ID (required)`, `--json/-j` | Change your native cart: set a permitted quantity, remove/clear items, append a saved cart, replace with a saved cart, or delete a saved cart. | `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references` ([schema](#onestop_update_cart)) |
| `ntu onestop cart clear` | `--json/-j` | Change your native cart: set a permitted quantity, remove/clear items, append a saved cart, replace with a saved cart, or delete a saved cart. | `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references` ([schema](#onestop_update_cart)) |
| `ntu onestop cart checkout` | — | Review and submit a cart checkout in one session. | `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references` ([schema](#onestop_submit_cart_checkout)) |
| `ntu onestop cart show` | `--json/-j` | Read your native shopping cart, item quantities/prices, saved-cart IDs/names and checkout defaults. | `retrieved_at`, `source_url`, `cached`, `items`, `saved_carts`, `delivery_address`, `special_instructions`, `two_step_checkout` ([schema](#onestop_get_cart)) |
| `ntu onestop cart saved show` | `SAVED_CART_ID (required)`, `--json/-j` | Inspect items in a verified own saved cart before loading it. | `offset`, `available_count`, `total_count`, `complete`, `next_offset`, `retrieved_at`, `source_url`, `cached`, `records` ([schema](#onestop_get_saved_cart)) |
| `ntu onestop cart saved load` | `SAVED_CART_ID (required)`, `--json/-j` | Change your native cart: set a permitted quantity, remove/clear items, append a saved cart, replace with a saved cart, or delete a saved cart. | `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references` ([schema](#onestop_update_cart)) |
| `ntu onestop cart saved replace` | `SAVED_CART_ID (required)`, `--json/-j` | Change your native cart: set a permitted quantity, remove/clear items, append a saved cart, replace with a saved cart, or delete a saved cart. | `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references` ([schema](#onestop_update_cart)) |
| `ntu onestop cart saved delete` | `SAVED_CART_ID (required)`, `--json/-j` | Change your native cart: set a permitted quantity, remove/clear items, append a saved cart, replace with a saved cart, or delete a saved cart. | `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references` ([schema](#onestop_update_cart)) |
| `ntu onestop cart saved create` | `NAME (required)`, `--item-ids VALUE`, `--json/-j` | Save the current cart, or selected own cart item IDs, as a new named cart using native name/selection validation. | `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references` ([schema](#onestop_save_cart)) |
| `ntu onestop catalog categories` | `--refresh/-r`, `--json/-j` | List the signed-in student's visible One Stop catalog categories and subcategories, parent IDs and published item counts. | `retrieved_at`, `source_url`, `cached`, `categories`, `root_count`, `total_root_count`, `complete` ([schema](#onestop_list_catalog_categories)) |
| `ntu onestop catalog search` | `QUERY (optional)`, `--category VALUE`, `--limit/-l VALUE (default: 20)`, `--offset VALUE`, `--refresh/-r`, `--json/-j` | Search the student's One Stop service catalog with query, or browse one category_id. | `offset`, `available_count`, `total_count`, `complete`, `next_offset`, `retrieved_at`, `source_url`, `cached`, `scope`, `query`, `category_id`, `items` ([schema](#onestop_list_catalog_items)) |
| `ntu onestop catalog item` | `ITEM_ID (required)`, `--refresh/-r`, `--json/-j` | Read a native One Stop form's description, current visible field labels/types, mandatory flags and choices. | `retrieved_at`, `source_url`, `cached`, `item_id`, `title`, `summary`, `description`, `mandatory_attachment`, `fields` ([schema](#onestop_get_catalog_item)) |
| `ntu onestop catalog favourite` | `ITEM_ID (required)`, `--category VALUE (required)`, `--state VALUE [on, off] (required)`, `--json/-j` | Set a catalog item's favourite state through its category's native control. | `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references` ([schema](#onestop_set_catalog_favourite)) |
| `ntu onestop favourites pin` | `FAVOURITE_ID (required)`, `--json/-j` | Pin/unpin/remove one own saved favourite or clear all favourites. | `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references` ([schema](#onestop_update_favourite)) |
| `ntu onestop favourites unpin` | `FAVOURITE_ID (required)`, `--json/-j` | Pin/unpin/remove one own saved favourite or clear all favourites. | `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references` ([schema](#onestop_update_favourite)) |
| `ntu onestop favourites remove` | `FAVOURITE_ID (required)`, `--json/-j` | Pin/unpin/remove one own saved favourite or clear all favourites. | `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references` ([schema](#onestop_update_favourite)) |
| `ntu onestop favourites clear` | `--json/-j` | Pin/unpin/remove one own saved favourite or clear all favourites. | `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references` ([schema](#onestop_update_favourite)) |
| `ntu onestop favourites list` | `--json/-j` | Read your saved catalog favourites and which are pinned to the homepage. | `retrieved_at`, `source_url`, `cached`, `items`, `pinned_count`, `maximum_pins` ([schema](#onestop_list_favourites)) |
| `ntu onestop knowledge search` | `QUERY (required)`, `--limit/-l VALUE (default: 20)`, `--offset VALUE`, `--refresh/-r`, `--json/-j` | Search the signed-in student's One Stop knowledge base. | `offset`, `available_count`, `total_count`, `complete`, `next_offset`, `retrieved_at`, `source_url`, `cached`, `query`, `articles` ([schema](#onestop_search_knowledge)) |
| `ntu onestop knowledge article` | `ARTICLE_ID (required)`, `--offset VALUE`, `--max-chars VALUE (default: 12000)`, `--refresh/-r`, `--json/-j` | Read a knowledge article's text, text-template sections or wiki body by article_id from search_knowledge, with text pagination and source links. | `retrieved_at`, `source_url`, `cached`, `article_id`, `number`, `title`, `updated_on`, `text`, `total_characters`, `offset`, `next_offset`, `links` ([schema](#onestop_get_knowledge_article)) |
| `ntu onestop knowledge feedback` | `ARTICLE_ID (required)`, `--json/-j` | Read native knowledge capabilities: ratings, helpfulness, comments, flags/reasons, subscription/inheritance, favourites and self-delivery channels. | `retrieved_at`, `source_url`, `cached`, `article_id`, `can_rate`, `can_mark_helpful`, `can_comment`, `can_flag`, `can_subscribe`, `subscribed`, `inherited_subscription`, `can_favourite`, `favourite`, `send_channels`, `reasons` ([schema](#onestop_get_article_feedback)) |
| `ntu onestop knowledge rate` | `ARTICLE_ID (required)`, `RATING (required)`, `--reason-id VALUE`, `--details VALUE (default: )`, `--json/-j` | Submit a 1–5 star knowledge rating when the native control is enabled. | `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references` ([schema](#onestop_rate_article)) |
| `ntu onestop knowledge helpful` | `ARTICLE_ID (required)`, `HELPFUL (required)`, `--reason-id VALUE`, `--details VALUE (default: )`, `--json/-j` | Submit helpful/not-helpful feedback only when the article offers that native control. | `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references` ([schema](#onestop_set_article_helpful)) |
| `ntu onestop knowledge flag` | `ARTICLE_ID (required)`, `--text VALUE (required)`, `--json/-j` | Flag a knowledge article with the user's explanation when the native flag control is available. | `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references` ([schema](#onestop_flag_article)) |
| `ntu onestop knowledge subscribe` | `ARTICLE_ID (required)`, `--state VALUE [on, off] (required)`, `--include-knowledge-base`, `--json/-j` | Subscribe/unsubscribe to article updates. | `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references` ([schema](#onestop_set_article_subscription)) |
| `ntu onestop knowledge favourite` | `ARTICLE_ID (required)`, `--state VALUE [on, off] (required)`, `--json/-j` | Set an article's native favourite state when its Favourite control is enabled. | `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references` ([schema](#onestop_set_article_favourite)) |
| `ntu onestop knowledge send-to-self` | `ARTICLE_ID (required)`, `--channel VALUE [email, sms] (default: email)`, `--json/-j` | Send this article to your registered email/SMS channel using the native Send to myself action. | `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references` ([schema](#onestop_send_article_to_self)) |
| `ntu onestop knowledge comments add` | `ARTICLE_ID (required)`, `--text VALUE (required)`, `--parent VALUE`, `--json/-j` | Publish plain-text feedback to a knowledge article, or reply to a visible parent comment. | `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references` ([schema](#onestop_add_article_comment)) |
| `ntu onestop knowledge comments delete` | `ARTICLE_ID (required)`, `COMMENT_ID (required)`, `--json/-j` | Delete a visible article comment only when the native menu permits deletion by the current user. | `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references` ([schema](#onestop_delete_article_comment)) |
| `ntu onestop knowledge comments like` | `ARTICLE_ID (required)`, `COMMENT_ID (required)`, `--state VALUE [on, off] (required)`, `--json/-j` | Like or unlike a visible knowledge comment using a desired state. | `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references` ([schema](#onestop_set_article_comment_like)) |
| `ntu onestop knowledge comments list` | `ARTICLE_ID (required)`, `--limit/-l VALUE (default: 20)`, `--offset VALUE`, `--json/-j` | Read visible knowledge comments/replies, author display names, text, dates, reactions, attachment IDs and delete permissions. | `offset`, `available_count`, `total_count`, `complete`, `next_offset`, `retrieved_at`, `source_url`, `cached`, `article_id`, `comments` ([schema](#onestop_list_article_comments)) |
| `ntu onestop payments services` | `QUERY (optional)`, `--limit/-l VALUE (default: 20)`, `--offset VALUE`, `--json/-j` | Search/browse services in the student's native payment directory, preserving its active/category/access filter. | `offset`, `available_count`, `total_count`, `complete`, `next_offset`, `retrieved_at`, `source_url`, `cached`, `records` ([schema](#onestop_list_payment_services)) |
| `ntu onestop payments service` | `SERVICE_ID (required)`, `--json/-j` | Read a visible payment service's native fixed-amount information. | `retrieved_at`, `source_url`, `cached`, `service_id`, `title`, `fixed_amount` ([schema](#onestop_get_payment_service)) |
| `ntu onestop payments checkout-link` | `SERVICE_ID (required)`, `--json/-j` | Ask One Stop to prepare a checkout link for a visible payment service. | `service_id`, `title`, `checkout_url`, `requires_browser_completion` ([schema](#onestop_prepare_payment)) |
| `ntu onestop profile set` | `FIELD_NAME (required)`, `VALUE (required)`, `--json/-j` | Update one displayed editable own-profile field through its native inline editor. | `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references` ([schema](#onestop_update_profile)) |
| `ntu onestop profile picture` | `FILE_PATH (required)`, `--json/-j` | Upload the explicitly selected local image as your own ServiceNow profile picture using the native file input. | `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references` ([schema](#onestop_update_profile_picture)) |
| `ntu onestop profile notifications` | `ENABLED (required)`, `--json/-j` | Enable or disable your ServiceNow notification preference. | `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references` ([schema](#onestop_set_notifications)) |
| `ntu onestop profile preference` | `NAME (required)`, `VALUE (required)`, `--json/-j` | Set an enabled own preference returned by get_profile. | `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references` ([schema](#onestop_set_user_preference)) |
| `ntu onestop profile show` | `--json/-j` | Read your own displayed profile fields, editable flags, preferences/choices, notification setting and picture-upload capability. | `retrieved_at`, `source_url`, `cached`, `fields`, `preferences`, `notifications_enabled`, `can_update_picture` ([schema](#onestop_get_profile)) |
| `ntu onestop requests list` | `--status VALUE [all, open, closed] (default: all)`, `--kind VALUE [all, case, request] (default: all)`, `--limit/-l VALUE (default: 20)`, `--offset VALUE`, `--refresh/-r`, `--json/-j` | Read your own open/closed One Stop cases and service requests, expanding native lists up to 500 records. | `offset`, `available_count`, `total_count`, `complete`, `next_offset`, `retrieved_at`, `source_url`, `cached`, `requests`, `coverage` ([schema](#onestop_list_my_requests)) |
| `ntu onestop requests show` | `REQUEST_ID (required)`, `--refresh/-r`, `--json/-j` | Read one of your requests after checking request_id against your retrieved personal lists. | `retrieved_at`, `source_url`, `cached`, `request`, `records`, `requested_items` ([schema](#onestop_get_my_request)) |
| `ntu onestop requests activity` | `REQUEST_ID (required)`, `--record-id VALUE`, `--json/-j` | Read visible comments and attachment events on a verified own request/item, plus current reply/upload/state-action permissions. | `retrieved_at`, `source_url`, `cached`, `request_id`, `record_id`, `entries`, `available_actions`, `can_reply`, `can_upload_attachment` ([schema](#onestop_get_request_activity)) |
| `ntu onestop requests reply` | `REQUEST_ID (required)`, `--text VALUE (required)`, `--record-id VALUE`, `--json/-j` | Post a real additional comment to a verified own ticket/item when its current native state permits replying. | `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references` ([schema](#onestop_reply_to_request)) |
| `ntu onestop requests action` | `REQUEST_ID (required)`, `ACTION (required)`, `--record-id VALUE`, `--json/-j` | Execute a state action currently offered by the native own-ticket page. | `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references` ([schema](#onestop_take_request_action)) |
| `ntu onestop requests apply` | `ITEM_ID (required)` | Prepare, fill, review and submit a native request in one session. | `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references` ([schema](#onestop_submit_request)) |

## MCP tools

Inputs are required only where marked. Output fields marked required may still be `null` when their type allows it. See the nested data types below for object fields.

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
| `categories` | array of [`Category`](#mcp-type-category) | Yes | — |
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
| `items` | array of [`CatalogItem`](#mcp-type-catalogitem) | Yes | — |

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
| `fields` | array of [`FormField`](#mcp-type-formfield) | Yes | — |

Unknown fields are not accepted.

### `onestop_search_knowledge`

Search the signed-in student's One Stop knowledge base. Returns article IDs, numbers, titles, snippets, published dates and portal links. Follows NTU search relevance; results need not contain the query in their title. Coverage is not guaranteed exhaustive; next_offset pages retrieved matches only.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `query` | `string` | Yes | minimum length: `1`; maximum length: `200` |
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
| `query` | `string` | Yes | — |
| `articles` | array of [`KnowledgeResult`](#mcp-type-knowledgeresult) | Yes | — |

Unknown fields are not accepted.

### `onestop_get_knowledge_article`

Read a knowledge article's text, text-template sections or wiki body by article_id from search_knowledge, with text pagination and source links. The portal may resolve an older ID to its current version. Does not fetch linked files or images, rate, subscribe to, or comment on articles. Unsupported templates return an explicit error.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `article_id` | `string` | Yes | pattern: `^[0-9a-f]{32}$` |
| `offset` | `integer` | No | minimum: `0`; default: `0` |
| `max_chars` | `integer` | No | minimum: `1`; maximum: `50000`; default: `12000` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `article_id` | `string` | Yes | — |
| `number` | `string` | Yes | — |
| `title` | `string` | Yes | — |
| `updated_on` | `string` or `null` | Yes | — |
| `text` | `string` | Yes | — |
| `total_characters` | `integer` | Yes | — |
| `offset` | `integer` | Yes | — |
| `next_offset` | `integer` or `null` | Yes | — |
| `links` | array of [`Link`](#mcp-type-link) | Yes | — |

Unknown fields are not accepted.

### `onestop_list_my_requests`

Read your own open/closed One Stop cases and service requests, expanding native lists up to 500 records. Inspect per-list coverage and complete. next_offset only pages retrieved records, not older portal history. Returns IDs, status labels, creation dates and links without changing requests.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `status` | `"all"`, `"open"`, `"closed"` | No | default: `"all"` |
| `kind` | `"all"`, `"case"`, `"request"` | No | default: `"all"` |
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
| `requests` | array of [`RequestSummary`](#mcp-type-requestsummary) | Yes | — |
| `coverage` | array of [`ListCoverage`](#mcp-type-listcoverage) | Yes | — |

Unknown fields are not accepted.

### `onestop_get_my_request`

Read one of your requests after checking request_id against your retrieved personal lists. Returns visible fields/answers as separate records for the request or its verified child items, and item stages (up to 20 children). Older records outside those lists and unsupported detail pages need the portal. Does not return conversations, work notes or attachments, or change the request.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `request_id` | `string` | Yes | pattern: `^[0-9a-f]{32}$` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `request` | [`RequestSummary`](#mcp-type-requestsummary) | Yes | — |
| `records` | array of [`RequestRecordDetails`](#mcp-type-requestrecorddetails) | Yes | — |
| `requested_items` | array of [`RequestItemStage`](#mcp-type-requestitemstage) | Yes | — |

Unknown fields are not accepted.

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
| `announcements` | array of [`PortalRecord`](#mcp-type-portalrecord) | Yes | — |
| `actions` | array of [`PortalRecord`](#mcp-type-portalrecord) | Yes | — |
| `appointments` | array of [`PortalRecord`](#mcp-type-portalrecord) | Yes | — |
| `popular_links` | array of [`PortalRecord`](#mcp-type-portalrecord) | Yes | — |

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
| `records` | array of [`PortalRecord`](#mcp-type-portalrecord) | Yes | — |

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
| `records` | array of [`PortalRecord`](#mcp-type-portalrecord) | Yes | — |

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
| `records` | array of [`PortalRecord`](#mcp-type-portalrecord) | Yes | — |

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
| `fields` | array of [`ProfileField`](#mcp-type-profilefield) | Yes | — |
| `preferences` | array of [`Preference`](#mcp-type-preference) | Yes | — |
| `notifications_enabled` | `boolean` or `null` | Yes | — |
| `can_update_picture` | `boolean` | Yes | — |

Unknown fields are not accepted.

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
| `records` | array of [`PortalRecord`](#mcp-type-portalrecord) | Yes | — |

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

### `onestop_get_article_feedback`

Read native knowledge capabilities: ratings, helpfulness, comments, flags/reasons, subscription/inheritance, favourites and self-delivery channels. Only controls actually offered for the article can be used.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `article_id` | `string` | Yes | pattern: `^[0-9a-f]{32}$` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `article_id` | `string` | Yes | — |
| `can_rate` | `boolean` | Yes | — |
| `can_mark_helpful` | `boolean` | Yes | — |
| `can_comment` | `boolean` | Yes | — |
| `can_flag` | `boolean` | Yes | — |
| `can_subscribe` | `boolean` | Yes | — |
| `subscribed` | `boolean` | Yes | — |
| `inherited_subscription` | `boolean` | Yes | — |
| `can_favourite` | `boolean` | Yes | — |
| `favourite` | `boolean` | Yes | — |
| `send_channels` | array of `string` | Yes | — |
| `reasons` | array of [`Choice`](#mcp-type-choice) | Yes | — |

Unknown fields are not accepted.

### `onestop_list_article_comments`

Read visible knowledge comments/replies, author display names, text, dates, reactions, attachment IDs and delete permissions. Pagination covers the retrieved tree; exhaustive coverage is not promised.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `article_id` | `string` | Yes | pattern: `^[0-9a-f]{32}$` |
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
| `article_id` | `string` | Yes | — |
| `comments` | array of [`ArticleComment`](#mcp-type-articlecomment) | Yes | — |

Unknown fields are not accepted.

### `onestop_get_request_activity`

Read visible comments and attachment events on a verified own request/item, plus current reply/upload/state-action permissions. Work notes are excluded. Select record_id from get_my_request when it has multiple records.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `request_id` | `string` | Yes | pattern: `^[0-9a-f]{32}$` |
| `record_id` | `string` or `null` | No | default: `null`; pattern: `^[0-9a-f]{32}$` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `request_id` | `string` | Yes | — |
| `record_id` | `string` | Yes | — |
| `entries` | array of [`ActivityEntry`](#mcp-type-activityentry) | Yes | — |
| `available_actions` | array of `string` | Yes | — |
| `can_reply` | `boolean` | Yes | — |
| `can_upload_attachment` | `boolean` | Yes | — |

Unknown fields are not accepted.

### `onestop_list_attachments`

List attachments on a verified own request/item, a readable knowledge article/comment, or an active local draft. Returns IDs, names, sizes, URLs and upload/delete permissions. Article assets are read-only; comments are editable only when the native menu permits it.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `target` | [`RequestAttachmentTarget`](#mcp-type-requestattachmenttarget) or [`ArticleAttachmentTarget`](#mcp-type-articleattachmenttarget) or [`CommentAttachmentTarget`](#mcp-type-commentattachmenttarget) or [`DraftAttachmentTarget`](#mcp-type-draftattachmenttarget) | Yes | — |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `attachments` | array of [`Attachment`](#mcp-type-attachment) | Yes | — |
| `can_upload` | `boolean` | Yes | — |
| `max_upload_bytes` | `integer` | Yes | — |

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
| `items` | array of [`CartItem`](#mcp-type-cartitem) | Yes | — |
| `saved_carts` | array of [`SavedCart`](#mcp-type-savedcart) | Yes | — |
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
| `records` | array of [`PortalRecord`](#mcp-type-portalrecord) | Yes | — |

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
| `items` | array of [`Favourite`](#mcp-type-favourite) | Yes | — |
| `pinned_count` | `integer` | Yes | — |
| `maximum_pins` | `integer` | No | default: `4` |

Unknown fields are not accepted.

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
| `records` | array of [`PortalRecord`](#mcp-type-portalrecord) | Yes | — |

Unknown fields are not accepted.

### `onestop_get_request_draft`

Inspect a local catalog draft's current visible fields, caller-supplied values, choices, missing requirements, native actions and any submission receipt. Personal defaults are omitted. Does not submit.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `draft_id` | `string` | Yes | minimum length: `16`; maximum length: `100` |

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
| `fields` | array of [`DraftField`](#mcp-type-draftfield) | Yes | — |
| `available_actions` | array of `string` | Yes | — |
| `receipt_id` | `string` or `null` | No | default: `null` |

Unknown fields are not accepted.

### `onestop_search_form_references`

Search a visible reference question using its native picker and original reference qualifier. Use returned value IDs in update_request_draft. Supports the portal's leading * wildcard. Encoded-query operators and arbitrary tables/filters are refused.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `draft_id` | `string` | Yes | minimum length: `16`; maximum length: `100` |
| `field_name` | `string` | Yes | — |
| `query` | `string` | Yes | minimum length: `1`; maximum length: `100` |
| `limit` | `integer` | No | minimum: `1`; maximum: `100`; default: `20` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `draft_id` | `string` | Yes | — |
| `field_name` | `string` | Yes | — |
| `query` | `string` | Yes | — |
| `choices` | array of [`ReferenceChoice`](#mcp-type-referencechoice) | Yes | — |
| `complete` | `boolean` | Yes | — |

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
| `slots` | array of [`AppointmentSlot`](#mcp-type-appointmentslot) | Yes | — |
| `retrieved_at` | `string` | Yes | format: `date-time` |

Unknown fields are not accepted.

### `onestop_prepare_request`

Prepare a native catalog form in a private in-memory browser tab. Use form_item_id from catalog results. values maps visible editable question names to strings. Runs native change scripts and reports missing/invalid questions without submitting. Password fields, hidden/read-only values and scripts are refused. Drafts expire after 15 minutes; at most four are open.

This tool changes local workflow state.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `item_id` | `string` | Yes | pattern: `^[0-9a-f]{32}$` |
| `values` | object of `string` or `null` | No | default: `null` |

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
| `fields` | array of [`DraftField`](#mcp-type-draftfield) | Yes | — |
| `available_actions` | array of `string` | Yes | — |
| `receipt_id` | `string` or `null` | No | default: `null` |

Unknown fields are not accepted.

### `onestop_update_request_draft`

Change editable questions on an in-memory draft and rerun native change scripts. Set controlling questions first when conditional questions are hidden. Updating answers invalidates the latest appointment slots; select a slot again before booking.

This tool changes local workflow state.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `draft_id` | `string` | Yes | minimum length: `16`; maximum length: `100` |
| `values` | object of `string` | Yes | — |

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
| `fields` | array of [`DraftField`](#mcp-type-draftfield) | Yes | — |
| `available_actions` | array of `string` | Yes | — |
| `receipt_id` | `string` or `null` | No | default: `null` |

Unknown fields are not accepted.

### `onestop_discard_request_draft`

Close and discard a local draft. This does not withdraw submitted requests. Previously uploaded server attachments follow ServiceNow retention; use delete_attachment first to remove editable temporary attachments.

This tool changes local workflow state.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `draft_id` | `string` | Yes | minimum length: `16`; maximum length: `100` |

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
| `references` | array of [`NamedValue`](#mcp-type-namedvalue) | Yes | — |

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
| `items` | array of [`CartItem`](#mcp-type-cartitem) | Yes | — |
| `delivery_address` | `string` | Yes | — |
| `special_instructions` | `string` | Yes | — |

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
| `fields` | array of [`DraftField`](#mcp-type-draftfield) | Yes | — |
| `available_actions` | array of `string` | Yes | — |
| `receipt_id` | `string` or `null` | No | default: `null` |

Unknown fields are not accepted.

### `onestop_submit_request`

Execute a native action on a reviewed local draft: submit a real request, add it to your cart, or save it to favourites when that button is offered. Uses native form validation and one submission attempt. Reusing a completed draft returns its receipt. An uncertain result must be checked in the portal before another submission.

MCP host confirmation is required before this action.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `draft_id` | `string` | Yes | minimum length: `16`; maximum length: `100` |
| `action` | `"submit"`, `"add_to_cart"`, `"save_favourite"` | No | default: `"submit"` |

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
| `references` | array of [`NamedValue`](#mcp-type-namedvalue) | Yes | — |

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
| `references` | array of [`NamedValue`](#mcp-type-namedvalue) | Yes | — |

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
| `references` | array of [`NamedValue`](#mcp-type-namedvalue) | Yes | — |

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
| `references` | array of [`NamedValue`](#mcp-type-namedvalue) | Yes | — |

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
| `references` | array of [`NamedValue`](#mcp-type-namedvalue) | Yes | — |

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

### `onestop_add_article_comment`

Publish plain-text feedback to a knowledge article, or reply to a visible parent comment. This is visible to the article's audience. Use only when the user requests publication; returns the server's comment receipt. Attach files afterward using an article_comment attachment target.

MCP host confirmation is required before this action.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `article_id` | `string` | Yes | pattern: `^[0-9a-f]{32}$` |
| `text` | `string` | Yes | minimum length: `1`; maximum length: `20000` |
| `parent_id` | `string` or `null` | No | default: `null`; pattern: `^[0-9a-f]{32}$` |

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
| `references` | array of [`NamedValue`](#mcp-type-namedvalue) | Yes | — |

Unknown fields are not accepted.

### `onestop_delete_article_comment`

Delete a visible article comment only when the native menu permits deletion by the current user. This removes published content; it never accepts an unrelated comment ID.

MCP host confirmation is required before this action.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `article_id` | `string` | Yes | pattern: `^[0-9a-f]{32}$` |
| `comment_id` | `string` | Yes | pattern: `^[0-9a-f]{32}$` |

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
| `references` | array of [`NamedValue`](#mcp-type-namedvalue) | Yes | — |

Unknown fields are not accepted.

### `onestop_set_article_comment_like`

Like or unlike a visible knowledge comment using a desired state. A matching current state is unchanged.

MCP host confirmation is required before this action.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `article_id` | `string` | Yes | pattern: `^[0-9a-f]{32}$` |
| `comment_id` | `string` | Yes | pattern: `^[0-9a-f]{32}$` |
| `liked` | `boolean` | Yes | — |

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
| `references` | array of [`NamedValue`](#mcp-type-namedvalue) | Yes | — |

Unknown fields are not accepted.

### `onestop_rate_article`

Submit a 1–5 star knowledge rating when the native control is enabled. Low ratings can require reason_id from get_article_feedback and optional details; this can create a native feedback task. Does not retry rate-limited or uncertain submissions.

MCP host confirmation is required before this action.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `article_id` | `string` | Yes | pattern: `^[0-9a-f]{32}$` |
| `rating` | `integer` | Yes | minimum: `1`; maximum: `5` |
| `reason_id` | `string` or `null` | No | default: `null` |
| `details` | `string` | No | maximum length: `10000`; default: `""` |

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
| `references` | array of [`NamedValue`](#mcp-type-namedvalue) | Yes | — |

Unknown fields are not accepted.

### `onestop_set_article_helpful`

Submit helpful/not-helpful feedback only when the article offers that native control. Negative feedback may require a published reason and create a native feedback task.

MCP host confirmation is required before this action.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `article_id` | `string` | Yes | pattern: `^[0-9a-f]{32}$` |
| `helpful` | `boolean` | Yes | — |
| `reason_id` | `string` or `null` | No | default: `null` |
| `details` | `string` | No | maximum length: `10000`; default: `""` |

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
| `references` | array of [`NamedValue`](#mcp-type-namedvalue) | Yes | — |

Unknown fields are not accepted.

### `onestop_flag_article`

Flag a knowledge article with the user's explanation when the native flag control is available. Sends feedback to the knowledge owners.

MCP host confirmation is required before this action.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `article_id` | `string` | Yes | pattern: `^[0-9a-f]{32}$` |
| `text` | `string` | Yes | minimum length: `1`; maximum length: `10000` |

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
| `references` | array of [`NamedValue`](#mcp-type-namedvalue) | Yes | — |

Unknown fields are not accepted.

### `onestop_set_article_subscription`

Subscribe/unsubscribe to article updates. An inherited knowledge-base subscription can only be removed with include_knowledge_base=true, which affects the whole knowledge base. Use that option only when the user explicitly requests that broader change.

MCP host confirmation is required before this action.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `article_id` | `string` | Yes | pattern: `^[0-9a-f]{32}$` |
| `subscribed` | `boolean` | Yes | — |
| `include_knowledge_base` | `boolean` | No | default: `false` |

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
| `references` | array of [`NamedValue`](#mcp-type-namedvalue) | Yes | — |

Unknown fields are not accepted.

### `onestop_set_article_favourite`

Set an article's native favourite state when its Favourite control is enabled. Reads current state and avoids toggling an already matching value.

MCP host confirmation is required before this action.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `article_id` | `string` | Yes | pattern: `^[0-9a-f]{32}$` |
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
| `references` | array of [`NamedValue`](#mcp-type-namedvalue) | Yes | — |

Unknown fields are not accepted.

### `onestop_send_article_to_self`

Send this article to your registered email/SMS channel using the native Send to myself action. Use only after the user explicitly requests sending; no alternate recipient is accepted. Acknowledgement does not guarantee delivery.

MCP host confirmation is required before this action.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `article_id` | `string` | Yes | pattern: `^[0-9a-f]{32}$` |
| `channel` | `"email"`, `"sms"` | No | default: `"email"` |

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
| `references` | array of [`NamedValue`](#mcp-type-namedvalue) | Yes | — |

Unknown fields are not accepted.

### `onestop_reply_to_request`

Post a real additional comment to a verified own ticket/item when its current native state permits replying. Sends only to the comments journal, never work notes. Do not repeat an uncertain reply; inspect activity first.

MCP host confirmation is required before this action.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `request_id` | `string` | Yes | pattern: `^[0-9a-f]{32}$` |
| `text` | `string` | Yes | minimum length: `1`; maximum length: `20000` |
| `record_id` | `string` or `null` | No | default: `null`; pattern: `^[0-9a-f]{32}$` |

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
| `references` | array of [`NamedValue`](#mcp-type-namedvalue) | Yes | — |

Unknown fields are not accepted.

### `onestop_take_request_action`

Execute a state action currently offered by the native own-ticket page. Read get_request_activity.available_actions first. Does not invent unavailable close/reopen/solution actions or accept arbitrary state/table values.

MCP host confirmation is required before this action.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `request_id` | `string` | Yes | pattern: `^[0-9a-f]{32}$` |
| `action` | `"close"`, `"reopen"`, `"accept_solution"`, `"reject_solution"` | Yes | — |
| `record_id` | `string` or `null` | No | default: `null`; pattern: `^[0-9a-f]{32}$` |

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
| `references` | array of [`NamedValue`](#mcp-type-namedvalue) | Yes | — |

Unknown fields are not accepted.

### `onestop_upload_attachment`

Upload an explicitly selected file from the configured One Stop upload directory to the verified target. The default is the dedicated onestop-uploads folder in the app configuration directory; NTU_ONESTOP_UPLOAD_DIR can override it. Requires an absolute path and obeys the smaller of the source limit and 20 MB. Article-comment uploads are visible to the article audience. Never chooses files automatically.

MCP host confirmation is required before this action.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `target` | [`RequestAttachmentTarget`](#mcp-type-requestattachmenttarget) or [`ArticleAttachmentTarget`](#mcp-type-articleattachmenttarget) or [`CommentAttachmentTarget`](#mcp-type-commentattachmenttarget) or [`DraftAttachmentTarget`](#mcp-type-draftattachmenttarget) | Yes | — |
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
| `references` | array of [`NamedValue`](#mcp-type-namedvalue) | Yes | — |

Unknown fields are not accepted.

### `onestop_download_attachment`

Download a listed attachment of the verified target to a new explicit absolute file path, up to 20 MB. Existing files and symbolic-link destinations are refused. Returns file size and SHA-256; does not execute or automatically open files.

MCP host confirmation is required before this action.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `target` | [`RequestAttachmentTarget`](#mcp-type-requestattachmenttarget) or [`ArticleAttachmentTarget`](#mcp-type-articleattachmenttarget) or [`CommentAttachmentTarget`](#mcp-type-commentattachmenttarget) or [`DraftAttachmentTarget`](#mcp-type-draftattachmenttarget) | Yes | — |
| `attachment_id` | `string` | Yes | pattern: `^[0-9a-f]{32}$` |
| `destination` | `string` | Yes | — |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `attachment_id` | `string` | Yes | — |
| `path` | `string` | Yes | — |
| `bytes_written` | `integer` | Yes | — |
| `sha256` | `string` | Yes | — |
| `downloaded_at` | `string` | Yes | format: `date-time` |

Unknown fields are not accepted.

### `onestop_delete_attachment`

Delete an attachment only when it is listed on the verified target and native editing is allowed. Knowledge article assets and closed/read-only ticket attachments cannot be deleted.

MCP host confirmation is required before this action.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `target` | [`RequestAttachmentTarget`](#mcp-type-requestattachmenttarget) or [`ArticleAttachmentTarget`](#mcp-type-articleattachmenttarget) or [`CommentAttachmentTarget`](#mcp-type-commentattachmenttarget) or [`DraftAttachmentTarget`](#mcp-type-draftattachmenttarget) | Yes | — |
| `attachment_id` | `string` | Yes | pattern: `^[0-9a-f]{32}$` |

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
| `references` | array of [`NamedValue`](#mcp-type-namedvalue) | Yes | — |

Unknown fields are not accepted.

### `onestop_rename_attachment`

Rename a listed editable attachment using the native attachment service. The new name cannot contain path separators or control characters.

MCP host confirmation is required before this action.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `target` | [`RequestAttachmentTarget`](#mcp-type-requestattachmenttarget) or [`ArticleAttachmentTarget`](#mcp-type-articleattachmenttarget) or [`CommentAttachmentTarget`](#mcp-type-commentattachmenttarget) or [`DraftAttachmentTarget`](#mcp-type-draftattachmenttarget) | Yes | — |
| `attachment_id` | `string` | Yes | pattern: `^[0-9a-f]{32}$` |
| `file_name` | `string` | Yes | minimum length: `1`; maximum length: `200` |

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
| `references` | array of [`NamedValue`](#mcp-type-namedvalue) | Yes | — |

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
| `references` | array of [`NamedValue`](#mcp-type-namedvalue) | Yes | — |

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
| `references` | array of [`NamedValue`](#mcp-type-namedvalue) | Yes | — |

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
| `references` | array of [`NamedValue`](#mcp-type-namedvalue) | Yes | — |

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
| `references` | array of [`NamedValue`](#mcp-type-namedvalue) | Yes | — |

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
| `references` | array of [`NamedValue`](#mcp-type-namedvalue) | Yes | — |

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
| `references` | array of [`NamedValue`](#mcp-type-namedvalue) | Yes | — |

Unknown fields are not accepted.

## MCP data types

These named types are used by the tool input and output fields above.

<a id="mcp-type-activityentry"></a>
### `ActivityEntry`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `entry_id` | `string` | Yes | — |
| `author` | `string` or `null` | Yes | — |
| `created_on` | `string` or `null` | Yes | — |
| `kind` | `"comment"`, `"attachment"` | Yes | — |
| `text` | `string` | Yes | — |
| `attachment_id` | `string` or `null` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-appointmentslot"></a>
### `AppointmentSlot`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `slot_id` | `string` | Yes | — |
| `start` | `string` | Yes | — |
| `end` | `string` | Yes | — |
| `start_utc` | `string` or `null` | Yes | — |
| `end_utc` | `string` or `null` | Yes | — |
| `label` | `string` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-articleattachmenttarget"></a>
### `ArticleAttachmentTarget`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `kind` | `"article"` | Yes | — |
| `article_id` | `string` | Yes | pattern: `^[0-9a-f]{32}$` |

Unknown fields are not accepted.

<a id="mcp-type-articlecomment"></a>
### `ArticleComment`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `comment_id` | `string` | Yes | — |
| `parent_id` | `string` or `null` | Yes | — |
| `author` | `string` or `null` | Yes | — |
| `created_on` | `string` or `null` | Yes | — |
| `text` | `string` | Yes | — |
| `liked` | `boolean` | Yes | — |
| `can_delete` | `boolean` | Yes | — |
| `attachment_ids` | array of `string` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-attachment"></a>
### `Attachment`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `attachment_id` | `string` | Yes | — |
| `file_name` | `string` | Yes | — |
| `size_bytes` | `integer` or `null` | Yes | — |
| `size_label` | `string` or `null` | Yes | — |
| `content_type` | `string` or `null` | Yes | — |
| `url` | `string` | Yes | — |
| `can_delete` | `boolean` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-cartitem"></a>
### `CartItem`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `cart_item_id` | `string` | Yes | — |
| `item_id` | `string` or `null` | Yes | — |
| `title` | `string` | Yes | — |
| `quantity` | `integer` | Yes | — |
| `quantity_editable` | `boolean` | Yes | — |
| `price_label` | `string` or `null` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-catalogitem"></a>
### `CatalogItem`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `item_id` | `string` | Yes | — |
| `title` | `string` | Yes | — |
| `summary` | `string` or `null` | Yes | — |
| `kind` | `"form"`, `"external"`, `"knowledge"`, `"content"` | Yes | — |
| `url` | `string` | Yes | — |
| `form_item_id` | `string` or `null` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-category"></a>
### `Category`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `category_id` | `string` | Yes | — |
| `title` | `string` | Yes | — |
| `parent_id` | `string` or `null` | Yes | — |
| `item_count` | `integer` | Yes | — |
| `total_item_count` | `integer` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-choice"></a>
### `Choice`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `value` | `string` | Yes | — |
| `label` | `string` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-commentattachmenttarget"></a>
### `CommentAttachmentTarget`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `kind` | `"article_comment"` | Yes | — |
| `article_id` | `string` | Yes | pattern: `^[0-9a-f]{32}$` |
| `comment_id` | `string` | Yes | pattern: `^[0-9a-f]{32}$` |

Unknown fields are not accepted.

<a id="mcp-type-draftattachmenttarget"></a>
### `DraftAttachmentTarget`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `kind` | `"draft"` | Yes | — |
| `draft_id` | `string` | Yes | minimum length: `16`; maximum length: `100` |

Unknown fields are not accepted.

<a id="mcp-type-draftfield"></a>
### `DraftField`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `name` | `string` | Yes | — |
| `label` | `string` | Yes | — |
| `type` | `string` | Yes | — |
| `mandatory` | `boolean` | Yes | — |
| `read_only` | `boolean` | Yes | — |
| `choices` | array of [`Choice`](#mcp-type-choice) | Yes | — |
| `value` | `string` or `null` | Yes | — |
| `display_value` | `string` or `null` | Yes | — |
| `reference` | `boolean` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-favourite"></a>
### `Favourite`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `favourite_id` | `string` | Yes | — |
| `item_id` | `string` | Yes | — |
| `title` | `string` | Yes | — |
| `pinned` | `boolean` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-formfield"></a>
### `FormField`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `name` | `string` | Yes | — |
| `label` | `string` | Yes | — |
| `type` | `string` | Yes | — |
| `mandatory` | `boolean` | Yes | — |
| `read_only` | `boolean` | Yes | — |
| `choices` | array of [`Choice`](#mcp-type-choice) | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-knowledgeresult"></a>
### `KnowledgeResult`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `article_id` | `string` | Yes | — |
| `number` | `string` | Yes | — |
| `title` | `string` | Yes | — |
| `summary` | `string` or `null` | Yes | — |
| `published` | `string` or `null` | Yes | — |
| `url` | `string` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-link"></a>
### `Link`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `label` | `string` | Yes | — |
| `url` | `string` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-listcoverage"></a>
### `ListCoverage`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `kind` | `"case"`, `"request"` | Yes | — |
| `state_group` | `"open"`, `"closed"` | Yes | — |
| `available_count` | `integer` | Yes | — |
| `source_count` | `integer` | Yes | — |
| `source_count_is_lower_bound` | `boolean` | Yes | — |
| `complete` | `boolean` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-namedvalue"></a>
### `NamedValue`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `name` | `string` | Yes | — |
| `label` | `string` | Yes | — |
| `value` | `string` or `null` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-portalrecord"></a>
### `PortalRecord`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `record_id` | `string` or `null` | Yes | — |
| `title` | `string` | Yes | — |
| `url` | `string` or `null` | Yes | — |
| `fields` | array of [`NamedValue`](#mcp-type-namedvalue) | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-preference"></a>
### `Preference`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `name` | `string` | Yes | — |
| `label` | `string` | Yes | — |
| `value` | `string` or `null` | Yes | — |
| `enabled` | `boolean` | Yes | — |
| `choices` | array of [`Choice`](#mcp-type-choice) | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-profilefield"></a>
### `ProfileField`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `name` | `string` | Yes | — |
| `label` | `string` | Yes | — |
| `value` | `string` or `null` | Yes | — |
| `type` | `string` | Yes | — |
| `read_only` | `boolean` | Yes | — |
| `choices` | array of [`Choice`](#mcp-type-choice) | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-referencechoice"></a>
### `ReferenceChoice`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `value` | `string` | Yes | — |
| `label` | `string` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-requestattachmenttarget"></a>
### `RequestAttachmentTarget`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `kind` | `"request"` | Yes | — |
| `request_id` | `string` | Yes | pattern: `^[0-9a-f]{32}$` |
| `record_id` | `string` or `null` | No | default: `null`; pattern: `^[0-9a-f]{32}$` |

Unknown fields are not accepted.

<a id="mcp-type-requestitemstage"></a>
### `RequestItemStage`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `item_id` | `string` | Yes | — |
| `stage` | `string` or `null` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-requestrecorddetails"></a>
### `RequestRecordDetails`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `record_id` | `string` | Yes | — |
| `record_type` | `string` | Yes | — |
| `fields` | array of [`NamedValue`](#mcp-type-namedvalue) | Yes | — |
| `variables` | array of [`NamedValue`](#mcp-type-namedvalue) | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-requestsummary"></a>
### `RequestSummary`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `request_id` | `string` | Yes | — |
| `kind` | `"case"`, `"request"` | Yes | — |
| `state_group` | `"open"`, `"closed"` | Yes | — |
| `title` | `string` | Yes | — |
| `number` | `string` or `null` | Yes | — |
| `state` | `string` or `null` | Yes | — |
| `created_on` | `string` or `null` | Yes | — |
| `record_type` | `string` | Yes | — |
| `url` | `string` | Yes | — |
| `detail_supported` | `boolean` | Yes | — |

Unknown fields are not accepted.

<a id="mcp-type-savedcart"></a>
### `SavedCart`

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `cart_id` | `string` | Yes | — |
| `name` | `string` | Yes | — |

Unknown fields are not accepted.

## Service notes

59 tools for NTU's student ServiceNow portal, available through the **local stdio personal profile**. They use the shared OS keyring account, the `personal` extra and Playwright Chromium. Capabilities depend on the native controls and permissions offered to the signed-in student. MCP marks 27 tools as read-only, five as local draft changes, and 27 as writes, including local file downloads. Use writes only for the user's requested effect.

The saved account must be an NTU student network account. Login uses `loginfs.ntu.edu.sg` and the student network realm. Interactive MFA/CAPTCHA and staff/NIE portals require the browser. Password rejection stops the attempt; incomplete login has a one-minute cooldown. On Linux, use the desktop D-Bus session and unlocked native keyring described in the [credential guide](../shared/README.md#linux-keyring-access). An unreadable store reports `credentials_configured: null`.

The existing `service_` namespace covers the public campus outlet directory. `onestop_` covers student administration.

### Catalog and drafts

Use **`form_item_id`** from catalog results for form reads/drafts; wrapper IDs can differ. External applications, including certification-letter and transcript systems, are returned as links. These tools do not automate those separate systems.

Drafts last 15 minutes, with at most four open. `values` maps visible editable names to strings. Hidden, read-only, layout and password inputs are refused. Personal defaults are omitted from previews. Set controlling questions first if another question is hidden. Reference searches preserve the native qualifier, support leading `*` and refuse encoded-query operators. Inspect the draft before submission: native validation runs again and additional confirmations may need the browser. Completed drafts return their receipt on reuse; uncertain submissions block another attempt. **Never automatically retry an uncertain mutation.**

### Own requests and files

Request details verify membership in your own lists. Child IDs must appear on the verified parent; at most 20 children are supported. Supply `record_id` from details when multiple records make the target ambiguous. Work notes are excluded. Arbitrary tables, users, states and unrelated IDs are not accepted.

Attachment targets are discriminated objects:

```json
{"kind":"request","request_id":"<32 hex characters>","record_id":"<optional verified item ID>"}
{"kind":"draft","draft_id":"<local draft token>"}
{"kind":"article","article_id":"<32 hex characters>"}
{"kind":"article_comment","article_id":"<32 hex characters>","comment_id":"<visible comment ID>"}
```

Article assets are read-only. Comment files are editable only when the native menu permits it. Uploads, including profile pictures, use the dedicated `onestop-uploads` folder under the app configuration directory by default. Set `NTU_ONESTOP_UPLOAD_DIR` to an absolute directory to override it, or to an empty string to disable uploads. Files must be regular files directly inside the approved directory; the directory and upload file cannot be symbolic links. Uploads require host confirmation and obey the smaller of the native limit and 20 MB; downloads are capped at 20 MB and refuse existing files or symbolic-link destinations. Tools never choose upload files automatically. Discarding a draft does not delete uploaded server files; remove editable temporary attachments explicitly when needed.

### Knowledge

Negative feedback may require a published `reason_id` and create a feedback task. Comments and files are visible to the article audience. `include_knowledge_base=true` can remove the whole knowledge-base subscription: use it only for that explicit request. Self-delivery accepts no alternate recipient; acknowledgement does not guarantee delivery. Unavailable controls return explicit errors.

Article text uses `offset` and `max_chars` (default 12,000, maximum 50,000). Follow `next_offset` for remaining text. Older IDs may resolve to current versions. Dates retain source strings without an inferred timezone. Download linked assets separately through verified attachment targets.

### Dashboard, profile and payments

Profile writes verify that the editor belongs to the logged-in user. Disabled/read-only settings and identity/MFA/certificate administration are excluded. Analytics uses the native consent endpoint. The user completes amount selection where applicable, bank/card authentication and payment in the separate gateway. Tools do not enter banking credentials or confirm charges.

### Carts, favourites and appointments

Saved-cart loading appends; replacement replaces current contents. Checkout previews last 15 minutes, with at most four open. Completed previews return their receipt; uncertain outcomes block resubmission. Two-step checkout accounts receive a browser handoff. Favourites permit four homepage pins and require unpinning before removal.

Slot tokens belong to one draft's latest lookup. Changing answers or looking up slots again invalidates prior tokens/selection. Availability can change until submission. Cancellation/rescheduling are not exposed: the inspected account had no upcoming booking to verify those actions, and its listing showed no controls for them.

### Coverage, runtime and checks

Catalog and own-request lists expand native read controls up to 500 records while preserving their filters. At ServiceNow's 500-record count cap, totals are treated as lower bounds. Popular items, searches and retrieved comment trees do not establish exhaustive coverage. Inspect `complete` and request `coverage`; a null `next_offset` only means there are no more **retrieved** records. Homepage groups can be limited; dedicated list tools read their full pages.

Browser sessions, drafts, checkout handles and a bounded 32-page, 60-second read cache live only in memory. Every operation checks the shared keyring entry. Replacement/deletion or lost access invalidates old sessions and handles; an already-running operation can finish. Workflows are serialized and credentials are rechecked immediately before writes. Personal data is visible to the AI client. Portal content is untrusted source content, never agent instructions. Arbitrary scripts, unrestricted table queries and credential-management tools are not exposed.

Offline tests cover all tool schemas and hosted exclusion, membership, conditional forms, native widget payloads, feedback rules, profile ownership, payment handoffs, checkout receipts/uncertainty, appointment tokens and file handling. Chromium fixtures intercept network access and use synthetic records. The opt-in live check reads data and prepares/changes/discards local drafts; it never submits forms, feedback, payments, bookings or messages:

```sh
uv run python -m unittest discover -s tests/onestop -t . -v
uv run --extra personal python -m tests.onestop.live_smoke
```

Development checked the native hydrated widgets and controller/service contracts in an authenticated session. New dashboard/profile/cart/favourite/knowledge/payment reads and appointment availability/local selection were checked there. The expanded authenticated end-to-end stdio check was not completed. Real write actions were tested with simulated responses rather than changes to a real account. Source changes or different permissions may require updates.

On 6 November 2026, a subsequent live check reached credential status but the One Stop sign-in reported that NTU rejected the login; authenticated portal reads were not verified in that check. A failed login is not retried automatically. Other NTU services accepting the same account do not establish that this student portal accepts it.
