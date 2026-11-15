# MCP tools

The local MCP server runs with `ntu mcp` and requires the `mcp` package extra. MCP setup and tool management also require the `cli` extra. The hosted server provides public, read-only tools. Personal tools require the personal profile; actions and downloads require host confirmation. See the [CLI command reference](COMMANDS.md) for direct commands.

## STARS

| Tool | Purpose | Credentials |
| --- | --- | --- |
| `stars_search_courses` | Find undergraduate courses by partial code or title keywords in a published term | No |
| `stars_get_course_metadata` | Course name, AUs, prerequisites, description, and term metadata | No |
| `stars_get_prerequisite_tree` | Explore a course's prerequisites and dependent courses with separate depth limits | No |
| `stars_get_course_indexes` | Paginated indexes with schedules, vacancies, and waitlist lengths | No |
| `stars_get_index` | One index's complete schedule, vacancies, and waitlist length | No |
| `stars_compare_indexes` | Shared sessions, index-specific sessions, and optional clash checks | No |
| `stars_find_matching_indexes` | Filter by days, times, lesson types, teaching weeks, and supplied schedule clashes | No |
| `stars_get_graduate_course_schedule` | Graduate course class groups and scheduled sessions | No |
| `stars_get_undergraduate_exam_schedule` | Undergraduate exam date, time, duration, and published-term notice | No |
| `stars_find_available_rooms` | Teaching-observed rooms with no scheduled classes in a time/week window | No |
| `stars_get_room_schedule` | Courses, indexes and lessons using a room | No |
| `stars_auth_status` | Whether optional WISH credentials are configured and a session has been verified | No |
| `stars_get_stars_planner` | Your registered courses and saved Plans 1–3 with timetables | Yes |
| `stars_get_degree_audit` | Your AU requirements, results, and registered courses | Yes |
| `stars_save_stars_plan` | Replace a saved plan's course/index list and verify the saved result | Yes |

See the [STARS guide](stars/README.md) for details, parameters, and limitations.

## NTULearn

| Tool | Purpose | Credentials |
| --- | --- | --- |
| `ntulearn_auth_status` | Credential configuration and last verified session | No |
| `ntulearn_list_courses` | Your enrolled courses and organizations, with availability and IDs | Yes |
| `ntulearn_get_course_contents` | One level of course content, with 'parent_id' to open a folder | Yes |
| `ntulearn_get_announcements` | Published announcements for one course | Yes |
| `ntulearn_get_calendar` | Calendar entries and published deadlines | Yes |
| `ntulearn_get_gradebook` | Gradebook columns and your own visible scores and status | Yes |
| `ntulearn_get_content_attachments` | Attached files for a leaf content item | Yes |
| `ntulearn_get_upcoming` | All calendar pages across enrolled or selected courses | Yes |
| `ntulearn_read_file_content` | Read PDF, Office, and text attachments inline | Yes |
| `ntulearn_list_messages` | List inbox or sent messages from course conversations | Yes |
| `ntulearn_read_message` | Full message body and published conversation recipients | Yes |
| `ntulearn_list_course_users` | Visible course users and their roles | Yes |
| `ntulearn_list_course_groups` | Course groups and group sets | Yes |
| `ntulearn_get_group_members` | Visible members of a course group | Yes |
| `ntulearn_search_course_content` | Recursive substring search within one course | Yes |
| `ntulearn_search_all_courses` | Search course content with course IDs and breadcrumbs | Yes |
| `ntulearn_get_content_tree` | Nested course content tree bounded by depth and size | Yes |
| `ntulearn_whats_new` | Recent announcements, upcoming events, and grade snapshots | Yes |
| `ntulearn_download_file` | Save an attachment to a new, explicit local file path | Yes |
| `ntulearn_download_video` | Save a Kaltura video embedded in a course content item | Yes |
| `ntulearn_download_course` | Download course attachments into local folders | Yes |

See the [NTULearn guide](ntulearn/README.md) for details, parameters, and limitations.

## CareerAxis

| Tool | Purpose | Credentials |
| --- | --- | --- |
| `careeraxis_auth_status` | Report keyring availability and whether this process has verified CareerAxis login | No |
| `careeraxis_search_opportunities` | Search NTU jobs and internship postings by keyword; follow 'has_next_page' | Yes |
| `careeraxis_get_opportunity` | Read visible posting text and HTTPS application links from a returned CareerAxis URL | Yes |
| `careeraxis_search_events` | Search events by keyword | Yes |
| `careeraxis_search_resources` | Search career guides, training, and downloadable resources | Yes |
| `careeraxis_search_organisations` | Search employer profiles, optionally requiring current opportunities | Yes |
| `careeraxis_search_appointment_topics` | Find career coaching topics, including interview practice and resume critique | Yes |
| `careeraxis_search_internship_jobs` | Search the Internship workgroup job board | Yes |
| `careeraxis_get_record` | Read details for returned events, resources, employers, appointment topics, or Internship postings | Yes |

See the [CareerAxis guide](careeraxis/README.md) for details, parameters, and limitations.

## MazeMap

| Tool | Purpose | Credentials |
| --- | --- | --- |
| `mazemap_list_campuses` | NTU campuses and their map IDs | No |
| `mazemap_list_buildings` | Buildings and floor IDs, names, and levels | No |
| `mazemap_search_places` | Find rooms, venues, and amenities by code or name | No |
| `mazemap_get_place` | One place's location, aliases, building, and floor | No |
| `mazemap_get_directions` | Walking instructions, distance, time, and accessibility | No |

See the [MazeMap guide](mazemap/README.md) for details, parameters, and limitations.

## DR-NTU

| Tool | Purpose | Credentials |
| --- | --- | --- |
| `drntu_search` | Find publications by keywords, repository scope, and facet filters | No |
| `drntu_get_item` | Published metadata, abstracts, citations, and rights | No |
| `drntu_browse` | Explore communities, subcommunities, and collections | No |
| `drntu_get_facets` | Available search filters, values, and result counts | No |
| `drntu_list_bundles` | An item's file groups, including original documents | No |
| `drntu_list_files` | File names, sizes, checksums, rights, and content links | No |
| `drntu_get_dataset` | Published dataset metadata, versions, and file inventories | No |
| `drntu_oai_identify` | Repository identity, date precision, and deletion policy | No |
| `drntu_oai_list_metadata_formats` | Available OAI metadata formats and schemas | No |
| `drntu_oai_list_sets` | OAI collection and community sets | No |
| `drntu_oai_list_records` | Metadata or identifiers filtered by modification date and set | No |
| `drntu_oai_get_record` | One record by its OAI identifier | No |

See the [DR-NTU guide](drntu/README.md) for details, parameters, and limitations.

## Library

| Tool | Purpose | Credentials |
| --- | --- | --- |
| `library_search` | Search OneSearch by keywords, title, author, ISBN, or resource type | No |
| `library_get_record` | Bibliographic metadata, identifiers, descriptions, and access links | No |
| `library_get_availability` | Physical holdings and institutional full-text service links | No |
| `library_list_facilities` | Library facilities, floor maps, and closure notices | No |
| `library_get_map_availability` | Seat and room statuses at a Singapore date and time | No |
| `library_get_facility_schedule` | Daily room and seat time grids and facility descriptions | Yes |

See the [Library guide](library/README.md) for details, parameters, and limitations.

## Faculty

| Tool | Purpose | Credentials |
| --- | --- | --- |
| `faculty_search` | Find faculty by name or research interest, with public profile details | No |
| `faculty_list_interests` | Research-interest labels and IDs for faculty search | No |

See the [Faculty guide](faculty/README.md) for details, parameters, and limitations.

## News

| Tool | Purpose | Credentials |
| --- | --- | --- |
| `news_search` | Search news by keyword, category, and latest or oldest order | No |
| `news_list_categories` | Published news category labels and filter IDs | No |
| `news_get_article` | Read an article's text in bounded chunks | No |

See the [News guide](news/README.md) for details, parameters, and limitations.

## NTU Omnibus

| Tool | Purpose | Credentials |
| --- | --- | --- |
| `omnibus_get_live_buses` | Current positions for an NTU shuttle route | No |
| `omnibus_list_routes` | Shuttle route names and published colors | No |
| `omnibus_list_stops` | Search NTU shuttle and LTA stop associations | No |
| `omnibus_get_arrivals` | NTU shuttle and LTA arrival estimates, including services 179 and 199 when present in the feed | No |
| `omnibus_get_service_status` | Shuttle schedules, special-day flags, and temporary notices | No |

See the [NTU Omnibus guide](omnibus/README.md) for details, parameters, and limitations.

## Campus services

| Tool | Purpose | Credentials |
| --- | --- | --- |
| `service_search` | Find food outlets, shops, clinics, and services with hours and contacts | No |
| `service_list_filters` | Official directory type and category filter IDs | No |

See the [Campus services guide](service/README.md) for details, parameters, and limitations.

## One Stop @ SAC

| Tool | Purpose | Credentials |
| --- | --- | --- |
| `onestop_auth_status` | Credential availability and last verified session | No |
| `onestop_list_catalog_categories` | Visible service categories and subcategories | Yes |
| `onestop_list_catalog_items` | Catalog search, category browsing, and popular services | Yes |
| `onestop_get_catalog_item` | Form instructions and fields, excluding personal defaults | Yes |
| `onestop_search_knowledge` | Search student knowledge articles | Yes |
| `onestop_get_knowledge_article` | Read article text and links | Yes |
| `onestop_list_my_requests` | Your open/closed cases and requests, with coverage information | Yes |
| `onestop_get_my_request` | Visible fields, answers and stages for verified own requests/items | Yes |
| `onestop_get_request_draft` | Inspect a local catalog draft's current visible fields, caller-supplied values, choices, missing requirements, native actions and any submission receipt | Yes |
| `onestop_search_form_references` | Search a visible reference question using its native picker and original reference qualifier | Yes |
| `onestop_get_dashboard` | Read your One Stop homepage announcements, actions/payment links, upcoming appointments and popular links | Yes |
| `onestop_list_announcements` | Read One Stop announcements, summaries and links from the native announcements collection with local pagination | Yes |
| `onestop_list_my_actions` | Read your One Stop to-do/billing actions and their published due dates and payment links | Yes |
| `onestop_list_popular_links` | List links on One Stop's Popular Sites page, preserving native catalog, knowledge and external destinations | Yes |
| `onestop_get_profile` | Read your own displayed profile fields, editable flags, preferences/choices, notification setting and picture-upload capability | Yes |
| `onestop_list_payment_services` | Search/browse services in the student's native payment directory, preserving its active/category/access filter | Yes |
| `onestop_get_payment_service` | Read a visible payment service's native fixed-amount information | Yes |
| `onestop_get_article_feedback` | Read native knowledge capabilities: ratings, helpfulness, comments, flags/reasons, subscription/inheritance, favourites and self-delivery channels | Yes |
| `onestop_list_article_comments` | Read visible knowledge comments/replies, author display names, text, dates, reactions, attachment IDs and delete permissions | Yes |
| `onestop_get_request_activity` | Read visible comments and attachment events on a verified own request/item, plus current reply/upload/state-action permissions | Yes |
| `onestop_list_attachments` | List attachments on a verified own request/item, a readable knowledge article/comment, or an active local draft | Yes |
| `onestop_get_cart` | Read your native shopping cart, item quantities/prices, saved-cart IDs/names and checkout defaults | Yes |
| `onestop_get_saved_cart` | Inspect items in a verified own saved cart before loading it | Yes |
| `onestop_list_favourites` | Read your saved catalog favourites and which are pinned to the homepage | Yes |
| `onestop_list_my_appointments` | Read your native upcoming appointment list with appointment numbers, published dates/times and locations | Yes |
| `onestop_get_appointment_configuration` | Read the native appointment selector's configuration on a local catalog draft: enabled/mandatory flags, duration, booking horizon and weekdays | Yes |
| `onestop_get_appointment_slots` | Read available appointment windows for one day using the draft's current native location/contact/reason configuration | Yes |
| `onestop_prepare_request` | Prepare a native catalog form in a private in-memory browser tab | Yes |
| `onestop_update_request_draft` | Change editable questions on an in-memory draft and rerun native change scripts | Yes |
| `onestop_discard_request_draft` | Close and discard a local draft | Yes |
| `onestop_prepare_cart_checkout` | Create a 15-minute local checkout preview with the current own cart, delivery address and instructions | Yes |
| `onestop_select_appointment_slot` | Select a slot from this draft's latest availability lookup using the native appointment event | Yes |
| `onestop_submit_request` | Execute a native action on a reviewed local draft: submit a real request, add it to your cart, or save it to favourites when that button is offered | Yes |
| `onestop_update_profile` | Update one displayed editable own-profile field through its native inline editor | Yes |
| `onestop_update_profile_picture` | Upload the explicitly selected local image as your own ServiceNow profile picture using the native file input | Yes |
| `onestop_set_notifications` | Enable or disable your ServiceNow notification preference | Yes |
| `onestop_set_user_preference` | Set an enabled own preference returned by get_profile | Yes |
| `onestop_prepare_payment` | Ask One Stop to prepare a checkout link for a visible payment service | Yes |
| `onestop_add_article_comment` | Publish plain-text feedback to a knowledge article, or reply to a visible parent comment | Yes |
| `onestop_delete_article_comment` | Delete a visible article comment only when the native menu permits deletion by the current user | Yes |
| `onestop_set_article_comment_like` | Like or unlike a visible knowledge comment using a desired state | Yes |
| `onestop_rate_article` | Submit a 1–5 star knowledge rating when the native control is enabled | Yes |
| `onestop_set_article_helpful` | Submit helpful/not-helpful feedback only when the article offers that native control | Yes |
| `onestop_flag_article` | Flag a knowledge article with the user's explanation when the native flag control is available | Yes |
| `onestop_set_article_subscription` | Subscribe/unsubscribe to article updates | Yes |
| `onestop_set_article_favourite` | Set an article's native favourite state when its Favourite control is enabled | Yes |
| `onestop_send_article_to_self` | Send this article to your registered email/SMS channel using the native Send to myself action | Yes |
| `onestop_reply_to_request` | Post a real additional comment to a verified own ticket/item when its current native state permits replying | Yes |
| `onestop_take_request_action` | Execute a state action currently offered by the native own-ticket page | Yes |
| `onestop_upload_attachment` | Upload an explicitly selected file from the configured One Stop upload directory to the verified target | Yes |
| `onestop_download_attachment` | Download a listed attachment of the verified target to a new explicit absolute file path, up to 20 MB | Yes |
| `onestop_delete_attachment` | Delete an attachment only when it is listed on the verified target and native editing is allowed | Yes |
| `onestop_rename_attachment` | Rename a listed editable attachment using the native attachment service | Yes |
| `onestop_update_cart` | Change your native cart: set a permitted quantity, remove/clear items, append a saved cart, replace with a saved cart, or delete a saved cart | Yes |
| `onestop_save_cart` | Save the current cart, or selected own cart item IDs, as a new named cart using native name/selection validation | Yes |
| `onestop_submit_cart_checkout` | Submit a reviewed cart checkout exactly once after checking account identity, expiry and unchanged cart contents | Yes |
| `onestop_update_favourite` | Pin/unpin/remove one own saved favourite or clear all favourites | Yes |
| `onestop_set_catalog_favourite` | Set a catalog item's favourite state through its category's native control | Yes |
| `onestop_book_appointment` | Book an appointment by optionally selecting a verified slot and submitting the reviewed native catalog draft once | Yes |

See the [One Stop @ SAC guide](onestop/README.md) for details, parameters, and limitations.
