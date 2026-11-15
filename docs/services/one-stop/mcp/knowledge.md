# One Stop: Knowledge MCP tools

[Service overview](../index.md) · [CLI reference](../cli/index.md) · [All MCP tools](index.md) · [Data types](types.md)

## Knowledge

Knowledge articles and comments are visible to their permitted audience. Reading and searching are distinct from posting, rating, subscribing, or other changes, which require host confirmation.

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
| `articles` | array of [`KnowledgeResult`](types.md#mcp-type-knowledgeresult) | Yes | — |

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
| `links` | array of [`Link`](types.md#mcp-type-link) | Yes | — |

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
| `reasons` | array of [`Choice`](types.md#mcp-type-choice) | Yes | — |

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
| `comments` | array of [`ArticleComment`](types.md#mcp-type-articlecomment) | Yes | — |

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
| `references` | array of [`NamedValue`](types.md#mcp-type-namedvalue) | Yes | — |

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
| `references` | array of [`NamedValue`](types.md#mcp-type-namedvalue) | Yes | — |

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
| `references` | array of [`NamedValue`](types.md#mcp-type-namedvalue) | Yes | — |

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
| `references` | array of [`NamedValue`](types.md#mcp-type-namedvalue) | Yes | — |

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
| `references` | array of [`NamedValue`](types.md#mcp-type-namedvalue) | Yes | — |

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
| `references` | array of [`NamedValue`](types.md#mcp-type-namedvalue) | Yes | — |

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
| `references` | array of [`NamedValue`](types.md#mcp-type-namedvalue) | Yes | — |

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
| `references` | array of [`NamedValue`](types.md#mcp-type-namedvalue) | Yes | — |

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
| `references` | array of [`NamedValue`](types.md#mcp-type-namedvalue) | Yes | — |

Unknown fields are not accepted.
