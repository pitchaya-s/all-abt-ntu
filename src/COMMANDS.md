# CLI commands

Run `ntu --help` or append `--help` to any command for current details and shell completion. CLI commands require the `cli` package extra; MCP setup and tool management also require `mcp`. `VALUE` denotes an option value; required arguments and options are marked. Direct commands use service defaults and environment variables, independently of MCP profiles and tool settings. Commands accept `--json` where listed. JSON writes results to stdout; diagnostics go to stderr. Personal operations require authentication. Actions and downloads require local confirmation.

Some resource groups also run their `list` or `show` command when the subcommand is omitted (for example, `ntu learn courses` and `ntu onestop appointments`).

Common short options are `-h` for help, `-j` for JSON, `-r` for refresh, `-l` for limit, `-p` for page, `-y` for academic year, `-s` for semester, and `-o` for a download destination, wherever the corresponding long option is supported.

One Stop request applications, appointment bookings and cart checkout run as standalone interactive workflows. Their temporary state remains in the process. Attachments must be selected from the configured upload directory.

## mcp

| Command | Arguments and options | Purpose |
| --- | --- | --- |
| `ntu mcp setup` | — | See command help. |
| `ntu mcp tools list` | `--all` | See command help. |
| `ntu mcp tools enable` | `NAMES... (required)` | See command help. |
| `ntu mcp tools disable` | `NAMES... (required)` | See command help. |

## auth

| Command | Arguments and options | Purpose |
| --- | --- | --- |
| `ntu auth save` | — | See command help. |
| `ntu auth status` | — | See command help. |
| `ntu auth delete` | — | See command help. |

## config

| Command | Arguments and options | Purpose |
| --- | --- | --- |
| `ntu config list` | — | See command help. |
| `ntu config set` | `NAME (required)`, `VALUE (required)` | See command help. |
| `ntu config unset` | `NAME (required)` | See command help. |

## stars

| Command | Arguments and options | Purpose |
| --- | --- | --- |
| `ntu stars course` | `COURSE_CODE (required)`, `--year/-y VALUE (required)`, `--semester/-s VALUE [1, 2, S] (required)`, `--json/-j` | Get course name, AUs, prerequisites, description, and term metadata. |
| `ntu stars prerequisites` | `COURSE_CODE (required)`, `--year/-y VALUE (required)`, `--semester/-s VALUE [1, 2, S] (required)`, `--prerequisite-depth VALUE (default: 2)`, `--dependent-depth VALUE (default: 2)`, `--completed VALUE`, `--eligible-only`, `--include-corequisites`, `--max-nodes VALUE (default: 100)`, `--json/-j` | Build before and after branches around a course, with separate depth limits.  The before branch follows the course's prerequisite rules; the after branch finds courses that depend on it in the selected term. |
| `ntu stars index` | `COURSE_CODE (required)`, `INDEX (required)`, `--year/-y VALUE (required)`, `--semester/-s VALUE [1, 2, S] (required)`, `--json/-j` | Get one index's complete schedule, vacancies, and waitlist where matching-term counts are published. |
| `ntu stars exams` | `COURSE_CODE (required)`, `--year/-y VALUE`, `--semester/-s VALUE [1, 2]`, `--json/-j` | Get public General Access exam dates and times for a course in the latest or specified published term. |
| `ntu stars graduate` | `COURSE_CODE (required)`, `--json/-j` | Get a graduate course's class groups for NTU's currently published academic term. |
| `ntu stars audit` | `--json/-j` | Get your degree requirements, examination results, and registered courses from Degree Audit. |
| `ntu stars auth status` | `--json/-j` | Report whether WISH credentials are configured and whether this process has verified a session. |
| `ntu stars courses search` | `QUERY (required)`, `--year/-y VALUE (required)`, `--semester/-s VALUE [1, 2, S] (required)`, `--study-mode VALUE [full_time, part_time] (default: full_time)`, `--limit/-l VALUE (default: 20)`, `--offset VALUE`, `--json/-j` | Search NTU's public undergraduate Class Schedule by partial code or title keywords. |
| `ntu stars indexes compare` | `COURSE_CODE (required)`, `INDEXES... (required)`, `--year/-y VALUE (required)`, `--semester/-s VALUE [1, 2, S] (required)`, `--against VALUE`, `--json/-j` | Compare shared and index-specific sessions; optionally check clashes with supplied time slots. |
| `ntu stars indexes match` | `COURSE_CODE (required)`, `--year/-y VALUE (required)`, `--semester/-s VALUE [1, 2, S] (required)`, `--constraints VALUE`, `--against VALUE`, `--json/-j` | Find indexes matching day/time/lesson/week rules and avoiding supplied timetable clashes. |
| `ntu stars indexes list` | `COURSE_CODE (required)`, `--year/-y VALUE (required)`, `--semester/-s VALUE [1, 2, S] (required)`, `--limit/-l VALUE (default: 10)`, `--offset VALUE`, `--json/-j` | List a page of indexes with timetable details and matching-term vacancies/waitlists. |
| `ntu stars planner show` | `--refresh/-r`, `--json/-j` | Get registered courses, the published term, and saved Plans 1–3 with indexes and timetables. |
| `ntu stars planner save` | `PLAN_NUMBER (required)`, `--courses VALUE (required)`, `--year/-y VALUE (required)`, `--semester/-s VALUE [1, 2] (required)`, `--json/-j` | Replace saved Plan 1, 2, or 3 with the complete supplied course/index list for the current Planner term. |
| `ntu stars rooms schedule` | `VENUE (required)`, `--year/-y VALUE (required)`, `--semester/-s VALUE [1, 2, S] (required)`, `--day VALUE [MON, TUE, WED, THU, FRI, SAT, SUN]`, `--week VALUE`, `--start-time VALUE`, `--end-time VALUE`, `--limit/-l VALUE (default: 50)`, `--offset VALUE`, `--refresh/-r`, `--json/-j` | Get all published undergraduate course/index lessons using one observed room, including full-time and part-time offerings. |
| `ntu stars rooms available` | `--year/-y VALUE (required)`, `--semester/-s VALUE [1, 2, S] (required)`, `--day VALUE [MON, TUE, WED, THU, FRI, SAT, SUN] (required)`, `--from VALUE (required)`, `--until VALUE (required)`, `--week VALUE`, `--buffer-minutes VALUE`, `--room-type VALUE`, `--venue-contains VALUE`, `--venue-prefix VALUE`, `--exclude-venue VALUE`, `--filters VALUE`, `--limit/-l VALUE (default: 20)`, `--offset VALUE`, `--refresh/-r`, `--json/-j` | Find teaching-free rooms; this does not establish occupancy or bookability. |

## learn

| Command | Arguments and options | Purpose |
| --- | --- | --- |
| `ntu learn attachments` | `COURSE_ID (required)`, `CONTENT_ID (required)`, `--limit/-l VALUE (default: 50)`, `--offset VALUE`, `--refresh/-r`, `--json/-j` | List files attached to a course content item. |
| `ntu learn announcements` | `COURSE_ID (required)`, `--limit/-l VALUE (default: 50)`, `--offset VALUE`, `--refresh/-r`, `--json/-j` | Read published announcements for one enrolled course. |
| `ntu learn grades` | `COURSE_ID (required)`, `--limit/-l VALUE (default: 50)`, `--offset VALUE`, `--grades-offset VALUE`, `--refresh/-r`, `--json/-j` | Read visible gradebook columns and your own scores/status. |
| `ntu learn calendar` | `--since VALUE`, `--until VALUE`, `--course VALUE`, `--limit/-l VALUE (default: 50)`, `--offset VALUE`, `--refresh/-r`, `--json/-j` | Read calendar entries and published deadlines, across your courses or for one course. |
| `ntu learn upcoming` | `--since VALUE`, `--until VALUE`, `--course-ids VALUE`, `--item-type VALUE`, `--max-requests VALUE (default: 100)`, `--refresh/-r`, `--json/-j` | Collect all calendar pages across your enrolled courses. |
| `ntu learn digest` | `--since VALUE`, `--until VALUE`, `--course-ids VALUE`, `--max-items VALUE (default: 200)`, `--max-requests VALUE (default: 100)`, `--refresh/-r`, `--json/-j` | Digest of recent announcements, upcoming calendar items and your gradebook across courses. |
| `ntu learn users` | `COURSE_ID (required)`, `--limit/-l VALUE (default: 50)`, `--offset VALUE`, `--refresh/-r`, `--json/-j` | List course users visible to your account, with their published names and roles. |
| `ntu learn auth status` | `--json/-j` | Report credential configuration and this process's last verified login, without logging in. |
| `ntu learn content tree` | `COURSE_ID (required)`, `--max-depth VALUE (default: 5)`, `--max-nodes VALUE (default: 1000)`, `--max-requests VALUE (default: 100)`, `--refresh/-r`, `--json/-j` | Read a course's nested content tree. |
| `ntu learn content show` | `COURSE_ID (required)`, `--parent VALUE`, `--limit/-l VALUE (default: 50)`, `--offset VALUE`, `--refresh/-r`, `--json/-j` | Read one level of course content. |
| `ntu learn courses download` | `COURSE_ID (required)`, `--output/-o VALUE (required)`, `--max-depth VALUE (default: 5)`, `--max-nodes VALUE (default: 1000)`, `--max-files VALUE (default: 100)`, `--max-total-mb VALUE (default: 200)`, `--max-requests VALUE (default: 200)`, `--refresh/-r`, `--json/-j` | Recursively save readable Blackboard attachments under destination/course_id with content folder names and stable file IDs. |
| `ntu learn courses list` | `--limit/-l VALUE (default: 50)`, `--offset VALUE`, `--refresh/-r`, `--json/-j` | List your enrolled NTULearn courses and organizations, including published availability and course IDs. |
| `ntu learn files read` | `COURSE_ID (required)`, `CONTENT_ID (required)`, `ATTACHMENT_ID (required)`, `--max-chars VALUE (default: 20000)`, `--max-pages VALUE (default: 20)`, `--json/-j` | Read an attachment inline as text: PDF, DOCX, PPTX, XLSX and UTF text/code. |
| `ntu learn files download` | `COURSE_ID (required)`, `CONTENT_ID (required)`, `ATTACHMENT_ID (required)`, `--output/-o VALUE (required)`, `--max-bytes VALUE (default: 20000000)`, `--json/-j` | Download a Blackboard attachment to an explicit local file path, up to 20 MB. |
| `ntu learn groups members` | `COURSE_ID (required)`, `GROUP_ID (required)`, `--limit/-l VALUE (default: 50)`, `--offset VALUE`, `--refresh/-r`, `--json/-j` | List visible members of a course group through Blackboard's browser membership API. |
| `ntu learn groups list` | `COURSE_ID (required)`, `--limit/-l VALUE (default: 50)`, `--offset VALUE`, `--refresh/-r`, `--json/-j` | List groups and group sets defined in a course. |
| `ntu learn messages list` | `--folder VALUE [inbox, sent] (default: inbox)`, `--course VALUE`, `--since VALUE`, `--unread-only`, `--limit/-l VALUE (default: 50)`, `--offset VALUE`, `--max-requests VALUE (default: 100)`, `--refresh/-r`, `--json/-j` | List Blackboard inbox/sent messages through readable course conversations, without marking them read. |
| `ntu learn messages read` | `MESSAGE_ID (required)`, `--course VALUE`, `--conversation-id VALUE`, `--max-requests VALUE (default: 100)`, `--refresh/-r`, `--json/-j` | Read a message's full body and published conversation recipients. |
| `ntu learn search all` | `QUERY (required)`, `--course-ids VALUE`, `--max-depth VALUE (default: 5)`, `--max-nodes VALUE (default: 1000)`, `--max-results VALUE (default: 50)`, `--max-requests VALUE (default: 100)`, `--refresh/-r`, `--json/-j` | Recursively search content across available enrolled courses, or selected course_ids. |
| `ntu learn search course` | `COURSE_ID (required)`, `QUERY (required)`, `--max-depth VALUE (default: 5)`, `--max-nodes VALUE (default: 1000)`, `--max-results VALUE (default: 50)`, `--max-requests VALUE (default: 100)`, `--refresh/-r`, `--json/-j` | Recursively search one course's content titles, body and description for a case-insensitive substring. |
| `ntu learn videos download` | `COURSE_ID (required)`, `CONTENT_ID (required)`, `--output/-o VALUE (required)`, `--max-mb VALUE (default: 1000)`, `--json/-j` | Download a Kaltura video embedded in an NTULearn content item to a new local file. |

## career

| Command | Arguments and options | Purpose |
| --- | --- | --- |
| `ntu career record` | `URL (required)`, `--refresh/-r`, `--json/-j` | Read the visible details for a CareerAxis event, resource document, employer, appointment topic, or internship posting URL returned by a CareerAxis search tool. |
| `ntu career appointments topics` | `QUERY (optional)`, `--page/-p VALUE (default: 1)`, `--limit/-l VALUE (default: 20)`, `--refresh/-r`, `--json/-j` | Search CareerAxis career-coaching appointment topics such as internship strategy, interview practice, and resume critique. |
| `ntu career auth status` | `--json/-j` | Report whether shared NTU keyring credentials can be read and whether this process has verified CareerAxis login; does not log in. |
| `ntu career employers search` | `NAME (optional)`, `--current-only`, `--page/-p VALUE (default: 1)`, `--limit/-l VALUE (default: 20)`, `--refresh/-r`, `--json/-j` | Search CareerAxis employer profiles by name, optionally limiting results to employers with current opportunities. |
| `ntu career events search` | `QUERY (optional)`, `--page/-p VALUE (default: 1)`, `--limit/-l VALUE (default: 20)`, `--refresh/-r`, `--json/-j` | Search authenticated CareerAxis events by keyword. |
| `ntu career internships search` | `QUERY (optional)`, `--page/-p VALUE (default: 1)`, `--limit/-l VALUE (default: 20)`, `--refresh/-r`, `--json/-j` | Search the authenticated CareerAxis Internship workgroup job board by keyword across its visible internship postings. |
| `ntu career opportunities search` | `QUERY (optional)`, `--page/-p VALUE (default: 1)`, `--limit/-l VALUE (default: 20)`, `--refresh/-r`, `--json/-j` | Search your authenticated NTU CareerAxis job and internship listings by keyword. |
| `ntu career opportunities show` | `URL (required)`, `--refresh/-r`, `--json/-j` | Read the full visible text for an opportunity URL returned by careeraxis_search_opportunities, including HTTPS application links. |
| `ntu career resources search` | `QUERY (optional)`, `--page/-p VALUE (default: 1)`, `--limit/-l VALUE (default: 20)`, `--refresh/-r`, `--json/-j` | Search CareerAxis career resources and training documents by keyword. |

## map

| Command | Arguments and options | Purpose |
| --- | --- | --- |
| `ntu map campuses` | `--refresh/-r`, `--json/-j` | List campuses in NTU's MazeMap collection with IDs and center coordinates. |
| `ntu map buildings` | `--campus VALUE (default: 2123)`, `--query VALUE`, `--refresh/-r`, `--json/-j` | List campus buildings and their floor IDs/names/levels. |
| `ntu map search` | `QUERY (required)`, `--campus VALUE`, `--limit/-l VALUE (default: 10)`, `--offset VALUE`, `--refresh/-r`, `--json/-j` | Search NTU rooms, venues and amenities by code, name or category, including aliases such as TR+7. |
| `ntu map place` | `POI_ID (required)`, `--refresh/-r`, `--json/-j` | Read one NTU place's location, aliases, building, floor, categories and published description/capacity. |
| `ntu map directions` | `FROM_POI_ID (required)`, `TO_POI_ID (required)`, `--constraint VALUE [NO_CONSTRAINT, PREFER_ACCESSIBLE, REQUIRE_ACCESSIBLE] (default: NO_CONSTRAINT)`, `--refresh/-r`, `--accessible`, `--json/-j` | Get walking routes between two NTU POIs, estimated metres/seconds and English instructions where available. |

## research

| Command | Arguments and options | Purpose |
| --- | --- | --- |
| `ntu research search` | `QUERY (required)`, `--scope VALUE`, `--entity-type VALUE [Publication, Person, all] (default: Publication)`, `--filters VALUE`, `--page/-p VALUE`, `--page-size VALUE (default: 10)`, `--refresh/-r`, `--json/-j` | Search DR-NTU publications by keywords or Solr query. |
| `ntu research facets` | `--facet VALUE`, `--query VALUE (default: )`, `--scope VALUE`, `--entity-type VALUE [Publication, Person, all] (default: Publication)`, `--filters VALUE`, `--page/-p VALUE`, `--page-size VALUE (default: 10)`, `--refresh/-r`, `--json/-j` | Discover search facet names, or supply a facet name to list its values and counts for the query/scope/filters. |
| `ntu research dataset` | `PERSISTENT_ID (required)`, `--version VALUE`, `--limit/-l VALUE (default: 50)`, `--offset VALUE`, `--refresh/-r`, `--json/-j` | Read a published DR-NTU Data dataset by doi: identifier: title, authors, descriptions, subjects, license and paginated file inventory. |
| `ntu research browse communities` | `--community VALUE`, `--page/-p VALUE`, `--page-size VALUE (default: 20)`, `--refresh/-r`, `--json/-j` | Browse repository communities or collections. |
| `ntu research browse collections` | `--community VALUE`, `--page/-p VALUE`, `--page-size VALUE (default: 20)`, `--refresh/-r`, `--json/-j` | Browse repository communities or collections. |
| `ntu research bundle files` | `BUNDLE_ID (required)`, `--page/-p VALUE`, `--page-size VALUE (default: 20)`, `--refresh/-r`, `--json/-j` | List a bundle's file metadata: names, byte sizes, checksums, published rights and content URLs. |
| `ntu research item bundles` | `ITEM_ID (required)`, `--page/-p VALUE`, `--page-size VALUE (default: 20)`, `--refresh/-r`, `--json/-j` | List an item's file groups. |
| `ntu research item show` | `ITEM_ID (required)`, `--refresh/-r`, `--json/-j` | Read a repository item's published metadata, including abstracts, citations, DOI, subjects and rights where supplied. |
| `ntu research oai info` | `--refresh/-r`, `--json/-j` | Describe DR-NTU's OAI-PMH repository, modification-date precision, deletion policy and earliest datestamp. |
| `ntu research oai formats` | `IDENTIFIER (optional)`, `--refresh/-r`, `--json/-j` | List OAI metadata prefixes, namespaces and schemas. |
| `ntu research oai sets` | `--token VALUE`, `--limit/-l VALUE (default: 20)`, `--offset VALUE`, `--refresh/-r`, `--json/-j` | List OAI collection/community sets. |
| `ntu research oai records` | `--prefix VALUE`, `--set VALUE`, `--from-date VALUE`, `--until-date VALUE`, `--token VALUE`, `--headers-only`, `--limit/-l VALUE (default: 10)`, `--offset VALUE`, `--refresh/-r`, `--json/-j` | Read one bounded OAI records page, defaulting to oai_dc. |
| `ntu research oai record` | `IDENTIFIER (required)`, `--prefix VALUE (default: oai_dc)`, `--refresh/-r`, `--json/-j` | Get one record by its OAI identifier, not a REST UUID. |

## library

| Command | Arguments and options | Purpose |
| --- | --- | --- |
| `ntu library search` | `QUERY (required)`, `--field VALUE [any, title, creator, isbn, issn, sub] (default: any)`, `--match VALUE [contains, exact] (default: contains)`, `--resource-type VALUE`, `--limit/-l VALUE (default: 10)`, `--offset VALUE`, `--refresh/-r`, `--json/-j` | Search NTU OneSearch for books, articles, journals and other catalogue resources. |
| `ntu library record` | `RECORD_ID (required)`, `--context VALUE [L, PC] (default: L)`, `--refresh/-r`, `--json/-j` | Read a OneSearch record's bibliographic metadata, descriptions, subjects, identifiers and published access links. |
| `ntu library availability` | `RECORD_ID (required)`, `--context VALUE [L, PC] (default: L)`, `--refresh/-r`, `--json/-j` | Read published physical holdings with library, location, call number and status, plus institutional full-text service links and access notes. |
| `ntu library facilities schedule` | `--date VALUE (required)`, `--space VALUE`, `--location VALUE`, `--group VALUE`, `--refresh/-r`, `--json/-j` | Read a day's LibFacilities room/seat time grid, room description and source status classes. |
| `ntu library facilities list` | `--refresh/-r`, `--json/-j` | List NTU Library facility categories, library/floor maps and closure notices. |
| `ntu library map availability` | `MAP_SLUG (required)`, `--date VALUE (required)`, `--time VALUE (required)`, `--refresh/-r`, `--json/-j` | Read seat/room booking statuses for a library map at date YYYY-MM-DD and time HH:MM in Singapore. |

## faculty

| Command | Arguments and options | Purpose |
| --- | --- | --- |
| `ntu faculty search` | `QUERY (optional)`, `--interest VALUE`, `--page/-p VALUE (default: 1)`, `--refresh/-r`, `--json/-j` | Search NTU's public faculty directory by name, optionally filtered by one research interest. |
| `ntu faculty interests` | `QUERY (optional)`, `--limit/-l VALUE (default: 50)`, `--offset VALUE`, `--refresh/-r`, `--json/-j` | List current faculty research-interest labels and filter IDs from NTU's directory form. |

## news

| Command | Arguments and options | Purpose |
| --- | --- | --- |
| `ntu news search` | `QUERY (optional)`, `--category VALUE`, `--sort VALUE [latest, oldest] (default: latest)`, `--page/-p VALUE (default: 1)`, `--refresh/-r`, `--json/-j` | Search public NTU news by keyword and optional category, sorted latest or oldest. |
| `ntu news categories` | `--refresh/-r`, `--json/-j` | List current news category labels and filter IDs from NTU's official news form. |
| `ntu news article` | `URL (required)`, `--offset VALUE`, `--max-chars VALUE (default: 12000)`, `--refresh/-r`, `--json/-j` | Read the published text of an NTU /news/detail/ article URL returned by news_search. |

## services

| Command | Arguments and options | Purpose |
| --- | --- | --- |
| `ntu services search` | `QUERY (optional)`, `--type VALUE`, `--category VALUE`, `--location VALUE (default: )`, `--limit/-l VALUE (default: 20)`, `--offset VALUE`, `--refresh/-r`, `--json/-j` | Find NTU food outlets, shops, clinics and campus services by name/address keyword and optional location substring. |
| `ntu services filters` | `--refresh/-r`, `--json/-j` | List official campus service type and category labels with filter IDs. |

## bus

| Command | Arguments and options | Purpose |
| --- | --- | --- |
| `ntu bus routes` | `--json/-j` | List public NTU shuttle routes and their published display colors. |
| `ntu bus stops` | `QUERY (optional)`, `--route VALUE [Blue, Brown, Green, Grey, Red, 179, 179A, 199]`, `--limit/-l VALUE (default: 20)`, `--offset VALUE`, `--json/-j` | Search NTU shuttle and LTA bus stops by stop name or code, optionally limited to a route/service. |
| `ntu bus arrivals` | `--route VALUE [Blue, Brown, Green, Grey, Red, 179, 179A, 199]`, `--stop VALUE (default: )`, `--source VALUE [all, shuttle, lta] (default: all)`, `--json/-j` | Get arrival estimates for NTU shuttles and/or LTA services 179, 179A, and 199. |
| `ntu bus live` | `--route VALUE [Blue, Brown, Green, Grey, Red] (default: Blue)`, `--json/-j` | Get current live vehicle positions for one NTU campus shuttle route. |
| `ntu bus status` | `--route VALUE [Blue, Brown, Green, Grey, Red] (default: Blue)`, `--json/-j` | Get the published first/last bus schedule, public-holiday/special-day flags, and temporary notices for an NTU campus shuttle route. |

## onestop

| Command | Arguments and options | Purpose |
| --- | --- | --- |
| `ntu onestop dashboard` | `--json/-j` | Read your One Stop homepage announcements, actions/payment links, upcoming appointments and popular links. |
| `ntu onestop announcements` | `--limit/-l VALUE (default: 20)`, `--offset VALUE`, `--json/-j` | Read One Stop announcements, summaries and links from the native announcements collection with local pagination. |
| `ntu onestop actions` | `--limit/-l VALUE (default: 20)`, `--offset VALUE`, `--json/-j` | Read your One Stop to-do/billing actions and their published due dates and payment links. |
| `ntu onestop links` | `--limit/-l VALUE (default: 20)`, `--offset VALUE`, `--json/-j` | List links on One Stop's Popular Sites page, preserving native catalog, knowledge and external destinations. |
| `ntu onestop appointments book` | `ITEM_ID (required)` | Prepare an appointment form, choose a slot and book it in one session. |
| `ntu onestop appointments list` | `--limit/-l VALUE (default: 20)`, `--offset VALUE`, `--json/-j` | Read your native upcoming appointment list with appointment numbers, published dates/times and locations. |
| `ntu onestop attachments list` | `TARGET (required)`, `--record-id VALUE`, `--json/-j` | List attachments on a verified own request/item, a readable knowledge article/comment, or an active local draft. |
| `ntu onestop attachments upload` | `TARGET (required)`, `FILE_PATH (required)`, `--record-id VALUE`, `--json/-j` | Upload an explicitly selected file from the configured One Stop upload directory to the verified target. |
| `ntu onestop attachments download` | `TARGET (required)`, `ATTACHMENT_ID (required)`, `--output/-o VALUE (required)`, `--record-id VALUE`, `--json/-j` | Download a listed attachment of the verified target to a new explicit absolute file path, up to 20 MB. |
| `ntu onestop attachments delete` | `TARGET (required)`, `ATTACHMENT_ID (required)`, `--record-id VALUE`, `--json/-j` | Delete an attachment only when it is listed on the verified target and native editing is allowed. |
| `ntu onestop attachments rename` | `TARGET (required)`, `ATTACHMENT_ID (required)`, `FILE_NAME (required)`, `--record-id VALUE`, `--json/-j` | Rename a listed editable attachment using the native attachment service. |
| `ntu onestop auth status` | `--json/-j` | Report shared keyring availability and the last verified One Stop session without logging in or returning identity or credentials. |
| `ntu onestop cart quantity` | `ITEM_ID (required)`, `QUANTITY (required)`, `--json/-j` | Change your native cart: set a permitted quantity, remove/clear items, append a saved cart, replace with a saved cart, or delete a saved cart. |
| `ntu onestop cart remove` | `ITEM_ID (required)`, `--json/-j` | Change your native cart: set a permitted quantity, remove/clear items, append a saved cart, replace with a saved cart, or delete a saved cart. |
| `ntu onestop cart clear` | `--json/-j` | Change your native cart: set a permitted quantity, remove/clear items, append a saved cart, replace with a saved cart, or delete a saved cart. |
| `ntu onestop cart checkout` | — | Review and submit a cart checkout in one session. |
| `ntu onestop cart show` | `--json/-j` | Read your native shopping cart, item quantities/prices, saved-cart IDs/names and checkout defaults. |
| `ntu onestop cart saved show` | `SAVED_CART_ID (required)`, `--json/-j` | Inspect items in a verified own saved cart before loading it. |
| `ntu onestop cart saved load` | `SAVED_CART_ID (required)`, `--json/-j` | Change your native cart: set a permitted quantity, remove/clear items, append a saved cart, replace with a saved cart, or delete a saved cart. |
| `ntu onestop cart saved replace` | `SAVED_CART_ID (required)`, `--json/-j` | Change your native cart: set a permitted quantity, remove/clear items, append a saved cart, replace with a saved cart, or delete a saved cart. |
| `ntu onestop cart saved delete` | `SAVED_CART_ID (required)`, `--json/-j` | Change your native cart: set a permitted quantity, remove/clear items, append a saved cart, replace with a saved cart, or delete a saved cart. |
| `ntu onestop cart saved create` | `NAME (required)`, `--item-ids VALUE`, `--json/-j` | Save the current cart, or selected own cart item IDs, as a new named cart using native name/selection validation. |
| `ntu onestop catalog categories` | `--refresh/-r`, `--json/-j` | List the signed-in student's visible One Stop catalog categories and subcategories, parent IDs and published item counts. |
| `ntu onestop catalog search` | `QUERY (optional)`, `--category VALUE`, `--limit/-l VALUE (default: 20)`, `--offset VALUE`, `--refresh/-r`, `--json/-j` | Search the student's One Stop service catalog with query, or browse one category_id. |
| `ntu onestop catalog item` | `ITEM_ID (required)`, `--refresh/-r`, `--json/-j` | Read a native One Stop form's description, current visible field labels/types, mandatory flags and choices. |
| `ntu onestop catalog favourite` | `ITEM_ID (required)`, `--category VALUE (required)`, `--state VALUE [on, off] (required)`, `--json/-j` | Set a catalog item's favourite state through its category's native control. |
| `ntu onestop favourites pin` | `FAVOURITE_ID (required)`, `--json/-j` | Pin/unpin/remove one own saved favourite or clear all favourites. |
| `ntu onestop favourites unpin` | `FAVOURITE_ID (required)`, `--json/-j` | Pin/unpin/remove one own saved favourite or clear all favourites. |
| `ntu onestop favourites remove` | `FAVOURITE_ID (required)`, `--json/-j` | Pin/unpin/remove one own saved favourite or clear all favourites. |
| `ntu onestop favourites clear` | `--json/-j` | Pin/unpin/remove one own saved favourite or clear all favourites. |
| `ntu onestop favourites list` | `--json/-j` | Read your saved catalog favourites and which are pinned to the homepage. |
| `ntu onestop knowledge search` | `QUERY (required)`, `--limit/-l VALUE (default: 20)`, `--offset VALUE`, `--refresh/-r`, `--json/-j` | Search the signed-in student's One Stop knowledge base. |
| `ntu onestop knowledge article` | `ARTICLE_ID (required)`, `--offset VALUE`, `--max-chars VALUE (default: 12000)`, `--refresh/-r`, `--json/-j` | Read a knowledge article's text, text-template sections or wiki body by article_id from search_knowledge, with text pagination and source links. |
| `ntu onestop knowledge feedback` | `ARTICLE_ID (required)`, `--json/-j` | Read native knowledge capabilities: ratings, helpfulness, comments, flags/reasons, subscription/inheritance, favourites and self-delivery channels. |
| `ntu onestop knowledge rate` | `ARTICLE_ID (required)`, `RATING (required)`, `--reason-id VALUE`, `--details VALUE (default: )`, `--json/-j` | Submit a 1–5 star knowledge rating when the native control is enabled. |
| `ntu onestop knowledge helpful` | `ARTICLE_ID (required)`, `HELPFUL (required)`, `--reason-id VALUE`, `--details VALUE (default: )`, `--json/-j` | Submit helpful/not-helpful feedback only when the article offers that native control. |
| `ntu onestop knowledge flag` | `ARTICLE_ID (required)`, `--text VALUE (required)`, `--json/-j` | Flag a knowledge article with the user's explanation when the native flag control is available. |
| `ntu onestop knowledge subscribe` | `ARTICLE_ID (required)`, `--state VALUE [on, off] (required)`, `--include-knowledge-base`, `--json/-j` | Subscribe/unsubscribe to article updates. |
| `ntu onestop knowledge favourite` | `ARTICLE_ID (required)`, `--state VALUE [on, off] (required)`, `--json/-j` | Set an article's native favourite state when its Favourite control is enabled. |
| `ntu onestop knowledge send-to-self` | `ARTICLE_ID (required)`, `--channel VALUE [email, sms] (default: email)`, `--json/-j` | Send this article to your registered email/SMS channel using the native Send to myself action. |
| `ntu onestop knowledge comments add` | `ARTICLE_ID (required)`, `--text VALUE (required)`, `--parent VALUE`, `--json/-j` | Publish plain-text feedback to a knowledge article, or reply to a visible parent comment. |
| `ntu onestop knowledge comments delete` | `ARTICLE_ID (required)`, `COMMENT_ID (required)`, `--json/-j` | Delete a visible article comment only when the native menu permits deletion by the current user. |
| `ntu onestop knowledge comments like` | `ARTICLE_ID (required)`, `COMMENT_ID (required)`, `--state VALUE [on, off] (required)`, `--json/-j` | Like or unlike a visible knowledge comment using a desired state. |
| `ntu onestop knowledge comments list` | `ARTICLE_ID (required)`, `--limit/-l VALUE (default: 20)`, `--offset VALUE`, `--json/-j` | Read visible knowledge comments/replies, author display names, text, dates, reactions, attachment IDs and delete permissions. |
| `ntu onestop payments services` | `QUERY (optional)`, `--limit/-l VALUE (default: 20)`, `--offset VALUE`, `--json/-j` | Search/browse services in the student's native payment directory, preserving its active/category/access filter. |
| `ntu onestop payments service` | `SERVICE_ID (required)`, `--json/-j` | Read a visible payment service's native fixed-amount information. |
| `ntu onestop payments checkout-link` | `SERVICE_ID (required)`, `--json/-j` | Ask One Stop to prepare a checkout link for a visible payment service. |
| `ntu onestop profile set` | `FIELD_NAME (required)`, `VALUE (required)`, `--json/-j` | Update one displayed editable own-profile field through its native inline editor. |
| `ntu onestop profile picture` | `FILE_PATH (required)`, `--json/-j` | Upload the explicitly selected local image as your own ServiceNow profile picture using the native file input. |
| `ntu onestop profile notifications` | `ENABLED (required)`, `--json/-j` | Enable or disable your ServiceNow notification preference. |
| `ntu onestop profile preference` | `NAME (required)`, `VALUE (required)`, `--json/-j` | Set an enabled own preference returned by get_profile. |
| `ntu onestop profile show` | `--json/-j` | Read your own displayed profile fields, editable flags, preferences/choices, notification setting and picture-upload capability. |
| `ntu onestop requests list` | `--status VALUE [all, open, closed] (default: all)`, `--kind VALUE [all, case, request] (default: all)`, `--limit/-l VALUE (default: 20)`, `--offset VALUE`, `--refresh/-r`, `--json/-j` | Read your own open/closed One Stop cases and service requests, expanding native lists up to 500 records. |
| `ntu onestop requests show` | `REQUEST_ID (required)`, `--refresh/-r`, `--json/-j` | Read one of your requests after checking request_id against your retrieved personal lists. |
| `ntu onestop requests activity` | `REQUEST_ID (required)`, `--record-id VALUE`, `--json/-j` | Read visible comments and attachment events on a verified own request/item, plus current reply/upload/state-action permissions. |
| `ntu onestop requests reply` | `REQUEST_ID (required)`, `--text VALUE (required)`, `--record-id VALUE`, `--json/-j` | Post a real additional comment to a verified own ticket/item when its current native state permits replying. |
| `ntu onestop requests action` | `REQUEST_ID (required)`, `ACTION (required)`, `--record-id VALUE`, `--json/-j` | Execute a state action currently offered by the native own-ticket page. |
| `ntu onestop requests apply` | `ITEM_ID (required)` | Prepare, fill, review and submit a native request in one session. |

Run `ntu mcp` to start the stdio server; `ntu mcp --profile public` and `ntu mcp --profile personal` select a profile. Run `ntu --version` to display the version. Run `ntu --install-completion` to install shell completion.
