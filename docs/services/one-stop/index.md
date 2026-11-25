# One Stop @ SAC

[Service overview](index.md) · [CLI reference](cli/index.md) · [MCP reference](mcp/index.md)

Access One Stop catalog items, requests, appointments and other student services. The CLI keeps temporary form and checkout state within a single interactive workflow; submissions and other changes require confirmation.

## Service notes


59 tools for NTU's student ServiceNow portal, available through the **local stdio personal profile**. They use the shared OS keyring account, the `personal` extra and Playwright Chromium. Capabilities depend on the native controls and permissions offered to the signed-in student. MCP marks 27 tools as read-only, five as local draft changes, and 27 as writes, including local file downloads. Use writes only for the user's requested effect.

The saved account must be an NTU student network account. Login uses `loginfs.ntu.edu.sg` and the student network realm. Interactive MFA/CAPTCHA and staff/NIE portals require the browser. Password rejection stops the attempt; incomplete login has a one-minute cooldown. On Linux, use the desktop D-Bus session and unlocked native keyring described in the [credential guide](../../architecture/credentials.md#linux-keyring-access). An unreadable store reports `credentials_configured: null`.

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