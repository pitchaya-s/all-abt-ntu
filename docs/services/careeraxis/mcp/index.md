# CareerAxis: MCP reference

[Service overview](../index.md) · [CLI reference](../cli/index.md) · [MCP reference](index.md)

## Tools

Inputs are required only where marked. Output fields marked required may still be `null` when their type allows it. See the [data types](types.md) for object fields.

### `careeraxis_auth_status`

Report whether shared NTU keyring credentials can be read and whether this process has verified CareerAxis login; does not log in.

**Inputs**

None.

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `credentials_configured` | `boolean` or `null` | Yes | — |
| `credential_storage` | `string` | Yes | — |
| `credential_error` | `string` or `null` | Yes | — |
| `session_verified` | `boolean` | Yes | — |
| `last_verified_at` | `string` or `null` | Yes | format: `date-time` |

Unknown fields are not accepted.

### `careeraxis_search_opportunities`

Search your authenticated NTU CareerAxis job and internship listings by keyword. Omit query to browse current postings. Returns titles, the portal's visible posting text, direct CareerAxis links, pagination status and retrieval time. Pages start at 1; follow has_next_page. Does not apply for jobs or access employer sites.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `query` | `string` | No | maximum length: `200`; default: `""` |
| `page` | `integer` | No | minimum: `1`; maximum: `50`; default: `1` |
| `limit` | `integer` | No | minimum: `1`; maximum: `50`; default: `20` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `query` | `string` | Yes | — |
| `page` | `integer` | Yes | minimum: `1` |
| `opportunities` | array of [`Opportunity`](types.md#mcp-type-opportunity) | Yes | — |
| `has_next_page` | `boolean` | Yes | — |
| `truncated` | `boolean` | Yes | — |

Unknown fields are not accepted.

### `careeraxis_get_opportunity`

Read the full visible text for an opportunity URL returned by careeraxis_search_opportunities, including HTTPS application links. Does not follow external links, submit applications, or alter CareerAxis.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `url` | `string` | Yes | maximum length: `1000` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `title` | `string` | Yes | minimum length: `1`; maximum length: `500` |
| `url` | `string` | Yes | — |
| `text` | `string` | Yes | maximum length: `20000` |
| `application_links` | array of `string` | Yes | — |

Unknown fields are not accepted.

### `careeraxis_search_events`

Search authenticated CareerAxis events by keyword. Returns event titles, visible summaries, direct event URLs, and pagination status. Does not register or save events.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `query` | `string` | No | maximum length: `200`; default: `""` |
| `page` | `integer` | No | minimum: `1`; maximum: `50`; default: `1` |
| `limit` | `integer` | No | minimum: `1`; maximum: `50`; default: `20` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `section` | `"events"`, `"resources"`, `"organisations"`, `"appointment_topics"`, `"internship_jobs"` | Yes | — |
| `query` | `string` | Yes | — |
| `page` | `integer` | Yes | minimum: `1` |
| `items` | array of [`PortalItem`](types.md#mcp-type-portalitem) | Yes | — |
| `has_next_page` | `boolean` | Yes | — |
| `truncated` | `boolean` | Yes | — |

Unknown fields are not accepted.

### `careeraxis_search_resources`

Search CareerAxis career resources and training documents by keyword. Returns titles, visible summaries, and CareerAxis document URLs; use careeraxis_get_record to read a returned document page.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `query` | `string` | No | maximum length: `200`; default: `""` |
| `page` | `integer` | No | minimum: `1`; maximum: `50`; default: `1` |
| `limit` | `integer` | No | minimum: `1`; maximum: `50`; default: `20` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `section` | `"events"`, `"resources"`, `"organisations"`, `"appointment_topics"`, `"internship_jobs"` | Yes | — |
| `query` | `string` | Yes | — |
| `page` | `integer` | Yes | minimum: `1` |
| `items` | array of [`PortalItem`](types.md#mcp-type-portalitem) | Yes | — |
| `has_next_page` | `boolean` | Yes | — |
| `truncated` | `boolean` | Yes | — |

Unknown fields are not accepted.

### `careeraxis_search_organisations`

Search CareerAxis employer profiles by name, optionally limiting results to employers with current opportunities.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `name` | `string` | No | maximum length: `200`; default: `""` |
| `current_opportunities_only` | `boolean` | No | default: `false` |
| `page` | `integer` | No | minimum: `1`; maximum: `50`; default: `1` |
| `limit` | `integer` | No | minimum: `1`; maximum: `50`; default: `20` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `section` | `"events"`, `"resources"`, `"organisations"`, `"appointment_topics"`, `"internship_jobs"` | Yes | — |
| `query` | `string` | Yes | — |
| `page` | `integer` | Yes | minimum: `1` |
| `items` | array of [`PortalItem`](types.md#mcp-type-portalitem) | Yes | — |
| `has_next_page` | `boolean` | Yes | — |
| `truncated` | `boolean` | Yes | — |

Unknown fields are not accepted.

### `careeraxis_search_appointment_topics`

Search CareerAxis career-coaching appointment topics such as internship strategy, interview practice, and resume critique. Does not book an appointment.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `query` | `string` | No | maximum length: `200`; default: `""` |
| `page` | `integer` | No | minimum: `1`; maximum: `50`; default: `1` |
| `limit` | `integer` | No | minimum: `1`; maximum: `50`; default: `20` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `section` | `"events"`, `"resources"`, `"organisations"`, `"appointment_topics"`, `"internship_jobs"` | Yes | — |
| `query` | `string` | Yes | — |
| `page` | `integer` | Yes | minimum: `1` |
| `items` | array of [`PortalItem`](types.md#mcp-type-portalitem) | Yes | — |
| `has_next_page` | `boolean` | Yes | — |
| `truncated` | `boolean` | Yes | — |

Unknown fields are not accepted.

### `careeraxis_search_internship_jobs`

Search the authenticated CareerAxis Internship workgroup job board by keyword across its visible internship postings.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `query` | `string` | No | maximum length: `200`; default: `""` |
| `page` | `integer` | No | minimum: `1`; maximum: `50`; default: `1` |
| `limit` | `integer` | No | minimum: `1`; maximum: `50`; default: `20` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `section` | `"events"`, `"resources"`, `"organisations"`, `"appointment_topics"`, `"internship_jobs"` | Yes | — |
| `query` | `string` | Yes | — |
| `page` | `integer` | Yes | minimum: `1` |
| `items` | array of [`PortalItem`](types.md#mcp-type-portalitem) | Yes | — |
| `has_next_page` | `boolean` | Yes | — |
| `truncated` | `boolean` | Yes | — |

Unknown fields are not accepted.

### `careeraxis_get_record`

Read the visible details for a CareerAxis event, resource document, employer, appointment topic, or internship posting URL returned by a CareerAxis search tool. Does not follow external links.

**Inputs**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `url` | `string` | Yes | maximum length: `1000` |
| `refresh` | `boolean` | No | default: `false` |

**Output**

| Field | Type | Required | Details |
| --- | --- | --- | --- |
| `retrieved_at` | `string` | Yes | format: `date-time` |
| `source_url` | `string` | Yes | — |
| `cached` | `boolean` | Yes | — |
| `title` | `string` | Yes | minimum length: `1`; maximum length: `500` |
| `url` | `string` | Yes | — |
| `text` | `string` | Yes | maximum length: `20000` |
| `links` | array of `string` | Yes | — |

Unknown fields are not accepted.

See the [MCP data types](types.md) for nested object fields.
