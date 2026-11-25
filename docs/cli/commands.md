# CLI commands

Choose a command name for its arguments, options and an example. You can also append `--help` to any command. CLI commands require the `cli` package extra; MCP setup and tool management also require `mcp`. Direct commands share [service settings](config.md) with local MCP and run independently of its profile and tool selection. Command pages identify where `--json` is available. JSON writes results to stdout; diagnostics go to stderr. Personal operations require authentication. Actions and downloads require local confirmation.

Some resource groups also run their `list` or `show` command when the subcommand is omitted (for example, `ntu learn courses` and `ntu onestop appointments`).

NTULearn attachment, file, and video commands also accept a quoted NTULearn document or lecture launch URL instead of the course and content IDs. File commands still require an attachment ID. A content URL can also be used with `learn content --parent`.

Common short options are `-h` for help, `-j` for JSON, `-r` for refresh, `-l` for limit, `-p` for page, `-y` for academic year, `-s` for semester, and `-o` for a download destination, wherever the corresponding long option is supported.

One Stop request applications, appointment bookings and cart checkout run as standalone interactive workflows. Their temporary state remains in the process. Attachments must be selected from the configured upload directory.

## cli

| Command | Purpose |
| --- | --- |
| `ntu cli setup` | Interactively choose whether to save credentials and install Chromium for personal services. |

## mcp

| Command | What it does |
| --- | --- |
| [`ntu mcp`](mcp.md#cmd-mcp) | Start the local stdio server using the saved or selected profile. |
| [`ntu mcp setup`](mcp.md#cmd-mcp-setup) | Choose a profile, tool families and MCP clients interactively. |
| [`ntu mcp tools list`](mcp.md#cmd-mcp-tools-list) | List enabled families, or individual tools with `--all`. |
| [`ntu mcp tools enable`](mcp.md#cmd-mcp-tools-enable) | Enable the named tool families or individual tools. |
| [`ntu mcp tools disable`](mcp.md#cmd-mcp-tools-disable) | Disable the named tool families or individual tools. |

## auth

| Command | What it does |
| --- | --- |
| [`ntu auth save`](auth.md#cmd-auth-save) | Prompt for an account and password and save them in the native OS keyring. |
| [`ntu auth status`](auth.md#cmd-auth-status) | Check whether credentials are stored without displaying them. |
| [`ntu auth delete`](auth.md#cmd-auth-delete) | Confirm and remove the saved credentials from the keyring. |

## config

| Command | What it does |
| --- | --- |
| [`ntu config list`](config.md#cmd-config-list) | Show saved service settings. |
| [`ntu config set`](config.md#cmd-config-set) | Save a service setting, such as `ntulearn.headless`. |
| [`ntu config unset`](config.md#cmd-config-unset) | Remove a saved service setting. |

## stars

[Examples and detailed stars commands](../services/stars/cli/index.md)

| Command | What it does |
| --- | --- |
| [`ntu stars course`](../services/stars/cli/courses.md#cmd-stars-course) | Get course name, AUs, prerequisites, description, and term metadata. |
| [`ntu stars prerequisites`](../services/stars/cli/courses.md#cmd-stars-prerequisites) | Build before and after branches around a course, with separate depth limits.  The before branch follows the course's prerequisite rules; the after branch finds courses that depend on it in the selected term. |
| [`ntu stars index`](../services/stars/cli/indexes.md#cmd-stars-index) | Get one index's complete schedule, vacancies, and waitlist where matching-term counts are published. |
| [`ntu stars exams`](../services/stars/cli/courses.md#cmd-stars-exams) | Get public General Access exam dates and times for a course in the latest or specified published term. |
| [`ntu stars graduate`](../services/stars/cli/courses.md#cmd-stars-graduate) | Get a graduate course's class groups for NTU's currently published academic term. |
| [`ntu stars audit`](../services/stars/cli/personal.md#cmd-stars-audit) | Get your degree requirements, examination results, and registered courses from Degree Audit. |
| [`ntu stars auth status`](../services/stars/cli/personal.md#cmd-stars-auth-status) | Sign in to STARS and report whether access is verified. |
| [`ntu stars courses search`](../services/stars/cli/courses.md#cmd-stars-courses-search) | Search NTU's public undergraduate Class Schedule by partial code or title keywords. |
| [`ntu stars indexes compare`](../services/stars/cli/indexes.md#cmd-stars-indexes-compare) | Compare shared and index-specific sessions; optionally check clashes with supplied time slots. |
| [`ntu stars indexes match`](../services/stars/cli/indexes.md#cmd-stars-indexes-match) | Find indexes matching day/time/lesson/week rules and avoiding supplied timetable clashes. |
| [`ntu stars indexes list`](../services/stars/cli/indexes.md#cmd-stars-indexes-list) | List a page of indexes with timetable details and matching-term vacancies/waitlists. |
| [`ntu stars planner show`](../services/stars/cli/personal.md#cmd-stars-planner-show) | Get registered courses, the published term, and saved Plans 1–3 with indexes and timetables. |
| [`ntu stars planner save`](../services/stars/cli/personal.md#cmd-stars-planner-save) | Replace saved Plan 1, 2, or 3 with the complete supplied course/index list for the current Planner term. |
| [`ntu stars rooms schedule`](../services/stars/cli/rooms.md#cmd-stars-rooms-schedule) | Get all published undergraduate course/index lessons using one observed room, including full-time and part-time offerings. |
| [`ntu stars rooms available`](../services/stars/cli/rooms.md#cmd-stars-rooms-available) | Find teaching-free rooms; this does not establish occupancy or bookability. |

## learn

[Examples and detailed learn commands](../services/ntulearn/cli/index.md)

| Command | What it does |
| --- | --- |
| [`ntu learn attachments`](../services/ntulearn/cli/files.md#cmd-learn-attachments) | List files attached to a course content item. |
| [`ntu learn announcements`](../services/ntulearn/cli/activity.md#cmd-learn-announcements) | Read published announcements for one enrolled course. |
| [`ntu learn grades`](../services/ntulearn/cli/activity.md#cmd-learn-grades) | Read visible gradebook columns and your own scores/status. |
| [`ntu learn calendar`](../services/ntulearn/cli/activity.md#cmd-learn-calendar) | Read calendar entries and published deadlines, across your courses or for one course. |
| [`ntu learn upcoming`](../services/ntulearn/cli/activity.md#cmd-learn-upcoming) | Collect all calendar pages across your enrolled courses. |
| [`ntu learn digest`](../services/ntulearn/cli/activity.md#cmd-learn-digest) | Digest of recent announcements, upcoming calendar items and your gradebook across courses. |
| [`ntu learn users`](../services/ntulearn/cli/people.md#cmd-learn-users) | List course users visible to your account, with their published names and roles. |
| [`ntu learn auth status`](../services/ntulearn/cli/courses.md#cmd-learn-auth-status) | Sign in to NTULearn and report whether access is verified. |
| [`ntu learn content tree`](../services/ntulearn/cli/courses.md#cmd-learn-content-tree) | Read a course's nested content tree. |
| [`ntu learn content show`](../services/ntulearn/cli/courses.md#cmd-learn-content-show) | Read one level of course content. |
| [`ntu learn courses download`](../services/ntulearn/cli/files.md#cmd-learn-courses-download) | Recursively save readable Blackboard attachments under destination/course_id with content folder names and stable file IDs. |
| [`ntu learn courses list`](../services/ntulearn/cli/courses.md#cmd-learn-courses-list) | List your enrolled NTULearn courses and organizations, including published availability and course IDs. |
| [`ntu learn files read`](../services/ntulearn/cli/files.md#cmd-learn-files-read) | Read an attachment inline as text: PDF, DOCX, PPTX, XLSX and UTF text/code. |
| [`ntu learn files download`](../services/ntulearn/cli/files.md#cmd-learn-files-download) | Download a Blackboard attachment to an explicit local file path, up to 20 MB. |
| [`ntu learn groups members`](../services/ntulearn/cli/people.md#cmd-learn-groups-members) | List visible members of a course group through Blackboard's browser membership API. |
| [`ntu learn groups list`](../services/ntulearn/cli/people.md#cmd-learn-groups-list) | List groups and group sets defined in a course. |
| [`ntu learn messages list`](../services/ntulearn/cli/people.md#cmd-learn-messages-list) | List Blackboard inbox/sent messages through readable course conversations, without marking them read. |
| [`ntu learn messages read`](../services/ntulearn/cli/people.md#cmd-learn-messages-read) | Read a message's full body and published conversation recipients. |
| [`ntu learn search all`](../services/ntulearn/cli/courses.md#cmd-learn-search-all) | Recursively search content across available enrolled courses, or selected course_ids. |
| [`ntu learn search course`](../services/ntulearn/cli/courses.md#cmd-learn-search-course) | Recursively search one course's content titles, body and description for a case-insensitive substring. |
| [`ntu learn videos download`](../services/ntulearn/cli/files.md#cmd-learn-videos-download) | Download a Kaltura video embedded in an NTULearn content item to a new local file. |

## career

[Examples and detailed career commands](../services/careeraxis/cli/index.md)

| Command | What it does |
| --- | --- |
| [`ntu career record`](../services/careeraxis/cli/index.md#cmd-career-record) | Read the visible details for a CareerAxis event, resource document, employer, appointment topic, or internship posting URL returned by a CareerAxis search tool. |
| [`ntu career appointments topics`](../services/careeraxis/cli/index.md#cmd-career-appointments-topics) | Search CareerAxis career-coaching appointment topics such as internship strategy, interview practice, and resume critique. |
| [`ntu career auth status`](../services/careeraxis/cli/index.md#cmd-career-auth-status) | Sign in to CareerAxis and report whether access is verified. |
| [`ntu career employers search`](../services/careeraxis/cli/index.md#cmd-career-employers-search) | Search CareerAxis employer profiles by name, optionally limiting results to employers with current opportunities. |
| [`ntu career events search`](../services/careeraxis/cli/index.md#cmd-career-events-search) | Search authenticated CareerAxis events by keyword. |
| [`ntu career internships search`](../services/careeraxis/cli/index.md#cmd-career-internships-search) | Search the authenticated CareerAxis Internship workgroup job board by keyword across its visible internship postings. |
| [`ntu career opportunities search`](../services/careeraxis/cli/index.md#cmd-career-opportunities-search) | Search your authenticated NTU CareerAxis job and internship listings by keyword. |
| [`ntu career opportunities show`](../services/careeraxis/cli/index.md#cmd-career-opportunities-show) | Read the full visible text for an opportunity URL returned by careeraxis_search_opportunities, including HTTPS application links. |
| [`ntu career resources search`](../services/careeraxis/cli/index.md#cmd-career-resources-search) | Search CareerAxis career resources and training documents by keyword. |

## map

[Examples and detailed map commands](../services/mazemap/cli/index.md)

| Command | What it does |
| --- | --- |
| [`ntu map campuses`](../services/mazemap/cli/index.md#cmd-map-campuses) | List campuses in NTU's MazeMap collection with IDs and center coordinates. |
| [`ntu map buildings`](../services/mazemap/cli/index.md#cmd-map-buildings) | List campus buildings and their floor IDs/names/levels. |
| [`ntu map search`](../services/mazemap/cli/index.md#cmd-map-search) | Search NTU rooms, venues and amenities by code, name or category, including aliases such as TR+7. |
| [`ntu map place`](../services/mazemap/cli/index.md#cmd-map-place) | Read one NTU place's location, aliases, building, floor, categories and published description/capacity. |
| [`ntu map directions`](../services/mazemap/cli/index.md#cmd-map-directions) | Get walking routes between two NTU POIs, estimated metres/seconds and English instructions where available. |

## research

[Examples and detailed research commands](../services/drntu/cli/index.md)

| Command | What it does |
| --- | --- |
| [`ntu research search`](../services/drntu/cli/repository.md#cmd-research-search) | Search DR-NTU publications by keywords or Solr query. |
| [`ntu research facets`](../services/drntu/cli/repository.md#cmd-research-facets) | Discover search facet names, or supply a facet name to list its values and counts for the query/scope/filters. |
| [`ntu research dataset`](../services/drntu/cli/repository.md#cmd-research-dataset) | Read a published DR-NTU Data dataset by doi: identifier: title, authors, descriptions, subjects, license and paginated file inventory. |
| [`ntu research browse communities`](../services/drntu/cli/repository.md#cmd-research-browse-communities) | Browse repository communities or collections. |
| [`ntu research browse collections`](../services/drntu/cli/repository.md#cmd-research-browse-collections) | Browse repository communities or collections. |
| [`ntu research bundle files`](../services/drntu/cli/repository.md#cmd-research-bundle-files) | List a bundle's file metadata: names, byte sizes, checksums, published rights and content URLs. |
| [`ntu research item bundles`](../services/drntu/cli/repository.md#cmd-research-item-bundles) | List an item's file groups. |
| [`ntu research item show`](../services/drntu/cli/repository.md#cmd-research-item-show) | Read a repository item's published metadata, including abstracts, citations, DOI, subjects and rights where supplied. |
| [`ntu research oai info`](../services/drntu/cli/oai.md#cmd-research-oai-info) | Describe DR-NTU's OAI-PMH repository, modification-date precision, deletion policy and earliest datestamp. |
| [`ntu research oai formats`](../services/drntu/cli/oai.md#cmd-research-oai-formats) | List OAI metadata prefixes, namespaces and schemas. |
| [`ntu research oai sets`](../services/drntu/cli/oai.md#cmd-research-oai-sets) | List OAI collection/community sets. |
| [`ntu research oai records`](../services/drntu/cli/oai.md#cmd-research-oai-records) | Read one bounded OAI records page, defaulting to oai_dc. |
| [`ntu research oai record`](../services/drntu/cli/oai.md#cmd-research-oai-record) | Get one record by its OAI identifier, not a REST UUID. |

## library

[Examples and detailed library commands](../services/library/cli/index.md)

| Command | What it does |
| --- | --- |
| [`ntu library search`](../services/library/cli/index.md#cmd-library-search) | Search NTU OneSearch for books, articles, journals and other catalogue resources. |
| [`ntu library record`](../services/library/cli/index.md#cmd-library-record) | Read a OneSearch record's bibliographic metadata, descriptions, subjects, identifiers and published access links. |
| [`ntu library availability`](../services/library/cli/index.md#cmd-library-availability) | Read published physical holdings with library, location, call number and status, plus institutional full-text service links and access notes. |
| [`ntu library facilities schedule`](../services/library/cli/index.md#cmd-library-facilities-schedule) | Read a day's LibFacilities room/seat time grid, room description and source status classes. |
| [`ntu library facilities list`](../services/library/cli/index.md#cmd-library-facilities-list) | List NTU Library facility categories, library/floor maps and closure notices. |
| [`ntu library map availability`](../services/library/cli/index.md#cmd-library-map-availability) | Read seat/room booking statuses for a library map at date YYYY-MM-DD and time HH:MM in Singapore. |

## faculty

[Examples and detailed faculty commands](../services/faculty/cli/index.md)

| Command | What it does |
| --- | --- |
| [`ntu faculty search`](../services/faculty/cli/index.md#cmd-faculty-search) | Search NTU's public faculty directory by name, optionally filtered by one research interest. |
| [`ntu faculty interests`](../services/faculty/cli/index.md#cmd-faculty-interests) | List current faculty research-interest labels and filter IDs from NTU's directory form. |

## news

[Examples and detailed news commands](../services/news/cli/index.md)

| Command | What it does |
| --- | --- |
| [`ntu news search`](../services/news/cli/index.md#cmd-news-search) | Search public NTU news by keyword and optional category, sorted latest or oldest. |
| [`ntu news categories`](../services/news/cli/index.md#cmd-news-categories) | List current news category labels and filter IDs from NTU's official news form. |
| [`ntu news article`](../services/news/cli/index.md#cmd-news-article) | Read the published text of an NTU /news/detail/ article URL returned by news_search. |

## services

[Examples and detailed services commands](../services/campus-services/cli/index.md)

| Command | What it does |
| --- | --- |
| [`ntu services search`](../services/campus-services/cli/index.md#cmd-services-search) | Find NTU food outlets, shops, clinics and campus services by name/address keyword and optional location substring. |
| [`ntu services filters`](../services/campus-services/cli/index.md#cmd-services-filters) | List official campus service type and category labels with filter IDs. |

## bus

[Examples and detailed bus commands](../services/omnibus/cli/index.md)

| Command | What it does |
| --- | --- |
| [`ntu bus routes`](../services/omnibus/cli/index.md#cmd-bus-routes) | List NTU campus shuttle routes. |
| [`ntu bus stops`](../services/omnibus/cli/index.md#cmd-bus-stops) | Search NTU shuttle and LTA bus stops by stop name or code, optionally limited to a route/service. |
| [`ntu bus arrivals`](../services/omnibus/cli/index.md#cmd-bus-arrivals) | Get arrival estimates for NTU shuttles and LTA buses. |
| [`ntu bus live`](../services/omnibus/cli/index.md#cmd-bus-live) | Get current live vehicle positions for one NTU campus shuttle route. |
| [`ntu bus status`](../services/omnibus/cli/index.md#cmd-bus-status) | Get the published first/last bus schedule, public-holiday/special-day flags, and temporary notices for an NTU campus shuttle route. |

## onestop

For examples, output fields and workflow guidance, use the [One Stop CLI guide](../services/one-stop/cli/index.md).

### Catalog

[Details and examples](../services/one-stop/cli/catalog.md)

| Command | What it does |
| --- | --- |
| [`ntu onestop catalog categories`](../services/one-stop/cli/catalog.md#cmd-onestop-catalog-categories) | List the signed-in student's visible One Stop catalog categories and subcategories, parent IDs and published item counts. |
| [`ntu onestop catalog search`](../services/one-stop/cli/catalog.md#cmd-onestop-catalog-search) | Search the student's One Stop service catalog with query, or browse one category_id. |
| [`ntu onestop catalog item`](../services/one-stop/cli/catalog.md#cmd-onestop-catalog-item) | Read a native One Stop form's description, current visible field labels/types, mandatory flags and choices. |
| [`ntu onestop catalog favourite`](../services/one-stop/cli/catalog.md#cmd-onestop-catalog-favourite) | Set a catalog item's favourite state through its category's native control. |

### Requests

[Details and examples](../services/one-stop/cli/requests.md)

| Command | What it does |
| --- | --- |
| [`ntu onestop requests list`](../services/one-stop/cli/requests.md#cmd-onestop-requests-list) | Read your own open/closed One Stop cases and service requests, expanding native lists up to 500 records. |
| [`ntu onestop requests show`](../services/one-stop/cli/requests.md#cmd-onestop-requests-show) | Read one of your requests after checking request_id against your retrieved personal lists. |
| [`ntu onestop requests activity`](../services/one-stop/cli/requests.md#cmd-onestop-requests-activity) | Read visible comments and attachment events on a verified own request/item, plus current reply/upload/state-action permissions. |
| [`ntu onestop requests reply`](../services/one-stop/cli/requests.md#cmd-onestop-requests-reply) | Post a real additional comment to a verified own ticket/item when its current native state permits replying. |
| [`ntu onestop requests action`](../services/one-stop/cli/requests.md#cmd-onestop-requests-action) | Execute a state action currently offered by the native own-ticket page. |
| [`ntu onestop requests apply`](../services/one-stop/cli/requests.md#cmd-onestop-requests-apply) | Prepare, fill, review and submit a native request in one session. |

### Appointments

[Details and examples](../services/one-stop/cli/appointments.md)

| Command | What it does |
| --- | --- |
| [`ntu onestop appointments book`](../services/one-stop/cli/appointments.md#cmd-onestop-appointments-book) | Prepare an appointment form, choose a slot and book it in one session. |
| [`ntu onestop appointments list`](../services/one-stop/cli/appointments.md#cmd-onestop-appointments-list) | Read your native upcoming appointment list with appointment numbers, published dates/times and locations. |

### Knowledge

[Details and examples](../services/one-stop/cli/knowledge.md)

| Command | What it does |
| --- | --- |
| [`ntu onestop knowledge search`](../services/one-stop/cli/knowledge.md#cmd-onestop-knowledge-search) | Search the signed-in student's One Stop knowledge base. |
| [`ntu onestop knowledge article`](../services/one-stop/cli/knowledge.md#cmd-onestop-knowledge-article) | Read a knowledge article's text, text-template sections or wiki body by article_id from search_knowledge, with text pagination and source links. |
| [`ntu onestop knowledge feedback`](../services/one-stop/cli/knowledge.md#cmd-onestop-knowledge-feedback) | Read native knowledge capabilities: ratings, helpfulness, comments, flags/reasons, subscription/inheritance, favourites and self-delivery channels. |
| [`ntu onestop knowledge rate`](../services/one-stop/cli/knowledge.md#cmd-onestop-knowledge-rate) | Submit a 1–5 star knowledge rating when the native control is enabled. |
| [`ntu onestop knowledge helpful`](../services/one-stop/cli/knowledge.md#cmd-onestop-knowledge-helpful) | Submit helpful/not-helpful feedback only when the article offers that native control. |
| [`ntu onestop knowledge flag`](../services/one-stop/cli/knowledge.md#cmd-onestop-knowledge-flag) | Flag a knowledge article with the user's explanation when the native flag control is available. |
| [`ntu onestop knowledge subscribe`](../services/one-stop/cli/knowledge.md#cmd-onestop-knowledge-subscribe) | Subscribe/unsubscribe to article updates. |
| [`ntu onestop knowledge favourite`](../services/one-stop/cli/knowledge.md#cmd-onestop-knowledge-favourite) | Set an article's native favourite state when its Favourite control is enabled. |
| [`ntu onestop knowledge send-to-self`](../services/one-stop/cli/knowledge.md#cmd-onestop-knowledge-send-to-self) | Send this article to your registered email/SMS channel using the native Send to myself action. |
| [`ntu onestop knowledge comments add`](../services/one-stop/cli/knowledge.md#cmd-onestop-knowledge-comments-add) | Publish plain-text feedback to a knowledge article, or reply to a visible parent comment. |
| [`ntu onestop knowledge comments delete`](../services/one-stop/cli/knowledge.md#cmd-onestop-knowledge-comments-delete) | Delete a visible article comment only when the native menu permits deletion by the current user. |
| [`ntu onestop knowledge comments like`](../services/one-stop/cli/knowledge.md#cmd-onestop-knowledge-comments-like) | Like or unlike a visible knowledge comment using a desired state. |
| [`ntu onestop knowledge comments list`](../services/one-stop/cli/knowledge.md#cmd-onestop-knowledge-comments-list) | Read visible knowledge comments/replies, author display names, text, dates, reactions, attachment IDs and delete permissions. |

### Attachments

[Details and examples](../services/one-stop/cli/attachments.md)

| Command | What it does |
| --- | --- |
| [`ntu onestop attachments list`](../services/one-stop/cli/attachments.md#cmd-onestop-attachments-list) | List attachments on a verified own request/item, a readable knowledge article/comment, or an active local draft. |
| [`ntu onestop attachments upload`](../services/one-stop/cli/attachments.md#cmd-onestop-attachments-upload) | Upload an explicitly selected file from the configured One Stop upload directory to the verified target. |
| [`ntu onestop attachments download`](../services/one-stop/cli/attachments.md#cmd-onestop-attachments-download) | Download a listed attachment of the verified target to a new explicit absolute file path, up to 20 MB. |
| [`ntu onestop attachments delete`](../services/one-stop/cli/attachments.md#cmd-onestop-attachments-delete) | Delete an attachment only when it is listed on the verified target and native editing is allowed. |
| [`ntu onestop attachments rename`](../services/one-stop/cli/attachments.md#cmd-onestop-attachments-rename) | Rename a listed editable attachment using the native attachment service. |

### Payments, cart and favourites

[Details and examples](../services/one-stop/cli/commerce.md)

| Command | What it does |
| --- | --- |
| [`ntu onestop cart quantity`](../services/one-stop/cli/commerce.md#cmd-onestop-cart-quantity) | Set the quantity of an item in your active cart. |
| [`ntu onestop cart remove`](../services/one-stop/cli/commerce.md#cmd-onestop-cart-remove) | Remove an item from your active cart. |
| [`ntu onestop cart clear`](../services/one-stop/cli/commerce.md#cmd-onestop-cart-clear) | Remove all items from your active cart. |
| [`ntu onestop cart checkout`](../services/one-stop/cli/commerce.md#cmd-onestop-cart-checkout) | Review and submit a cart checkout in one session. |
| [`ntu onestop cart show`](../services/one-stop/cli/commerce.md#cmd-onestop-cart-show) | Read your native shopping cart, item quantities/prices, saved-cart IDs/names and checkout defaults. |
| [`ntu onestop cart saved show`](../services/one-stop/cli/commerce.md#cmd-onestop-cart-saved-show) | Inspect items in a verified own saved cart before loading it. |
| [`ntu onestop cart saved load`](../services/one-stop/cli/commerce.md#cmd-onestop-cart-saved-load) | Append the items from a saved cart to your active cart. |
| [`ntu onestop cart saved replace`](../services/one-stop/cli/commerce.md#cmd-onestop-cart-saved-replace) | Replace your active cart with the items from a saved cart. |
| [`ntu onestop cart saved delete`](../services/one-stop/cli/commerce.md#cmd-onestop-cart-saved-delete) | Delete a saved cart. |
| [`ntu onestop cart saved create`](../services/one-stop/cli/commerce.md#cmd-onestop-cart-saved-create) | Save the current cart, or selected own cart item IDs, as a new named cart using native name/selection validation. |
| [`ntu onestop favourites pin`](../services/one-stop/cli/commerce.md#cmd-onestop-favourites-pin) | Pin a saved favourite to the homepage. |
| [`ntu onestop favourites unpin`](../services/one-stop/cli/commerce.md#cmd-onestop-favourites-unpin) | Unpin a favourite from the homepage. |
| [`ntu onestop favourites remove`](../services/one-stop/cli/commerce.md#cmd-onestop-favourites-remove) | Remove a saved favourite. |
| [`ntu onestop favourites clear`](../services/one-stop/cli/commerce.md#cmd-onestop-favourites-clear) | Remove eligible saved favourites. |
| [`ntu onestop favourites list`](../services/one-stop/cli/commerce.md#cmd-onestop-favourites-list) | Read your saved catalog favourites and which are pinned to the homepage. |
| [`ntu onestop payments services`](../services/one-stop/cli/commerce.md#cmd-onestop-payments-services) | Search/browse services in the student's native payment directory, preserving its active/category/access filter. |
| [`ntu onestop payments service`](../services/one-stop/cli/commerce.md#cmd-onestop-payments-service) | Read a visible payment service's native fixed-amount information. |
| [`ntu onestop payments checkout-link`](../services/one-stop/cli/commerce.md#cmd-onestop-payments-checkout-link) | Ask One Stop to prepare a checkout link for a visible payment service. |

### Dashboard and profile

[Details and examples](../services/one-stop/cli/account.md)

| Command | What it does |
| --- | --- |
| [`ntu onestop dashboard`](../services/one-stop/cli/account.md#cmd-onestop-dashboard) | Read your One Stop homepage announcements, actions/payment links, upcoming appointments and popular links. |
| [`ntu onestop announcements`](../services/one-stop/cli/account.md#cmd-onestop-announcements) | Read One Stop announcements, summaries and links from the native announcements collection with local pagination. |
| [`ntu onestop actions`](../services/one-stop/cli/account.md#cmd-onestop-actions) | Read your One Stop to-do/billing actions and their published due dates and payment links. |
| [`ntu onestop links`](../services/one-stop/cli/account.md#cmd-onestop-links) | List links on One Stop's Popular Sites page, preserving native catalog, knowledge and external destinations. |
| [`ntu onestop auth status`](../services/one-stop/cli/account.md#cmd-onestop-auth-status) | Sign in to One Stop and report whether access is verified. |
| [`ntu onestop profile set`](../services/one-stop/cli/account.md#cmd-onestop-profile-set) | Update one displayed editable own-profile field through its native inline editor. |
| [`ntu onestop profile picture`](../services/one-stop/cli/account.md#cmd-onestop-profile-picture) | Upload the explicitly selected local image as your own ServiceNow profile picture using the native file input. |
| [`ntu onestop profile notifications`](../services/one-stop/cli/account.md#cmd-onestop-profile-notifications) | Enable or disable your ServiceNow notification preference. |
| [`ntu onestop profile preference`](../services/one-stop/cli/account.md#cmd-onestop-profile-preference) | Set an enabled own preference returned by get_profile. |
| [`ntu onestop profile show`](../services/one-stop/cli/account.md#cmd-onestop-profile-show) | Read your own displayed profile fields, editable flags, preferences/choices, notification setting and picture-upload capability. |

Run `ntu mcp` to start the stdio server; `ntu mcp --profile public` and `ntu mcp --profile personal` select a profile. Run `ntu --version` to display the version. Run `ntu --install-completion` to install shell completion.
