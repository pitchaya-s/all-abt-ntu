# NTULearn: CLI reference

[Service overview](../index.md) · [CLI reference](index.md) · [MCP reference](../mcp/index.md)

## Example

Use a course code such as `ZZ0001` or a Blackboard course ID such as `_100_1` for course arguments, `--course`, and each entry in `--course-ids`. Codes are case-insensitive. If a code matches multiple enrolled course sites, use the Blackboard ID shown by `ntu learn courses` to pick one.

```sh
ntu learn courses --limit 20
ntu learn content ZZ0001 --limit 20
```

## Commands

Choose a command for its arguments, examples and result fields. Use `ntu learn --help` and append `--help` to a command for option details. Each command page identifies required arguments and any defaults. See the [complete CLI reference](../../../cli/commands.md) for shared settings and all services.

For `learn attachments`, `learn files read`, `learn files download`, and `learn videos download`, a quoted NTULearn document or lecture launch URL can supply the course and content IDs. When a separate course is also supplied, it must identify the same course as the URL. File commands still require an attachment ID, which can be found with `learn attachments`. Content browsing accepts a document URL in `--parent`.

For videos, recognizing a URL only extracts its IDs. The downloader still requires a supported Kaltura player or wrapper in the content item; it does not open arbitrary LTI tools. See [known issues](../../../known-issues.md#ntulearn-lecture-launch-urls).

### Find a content or attachment ID

1. Use your course code or run `ntu learn courses` and copy the Blackboard course ID.
2. Run `ntu learn content COURSE_ID` to list the top level. The displayed items include their content IDs.
3. If the item is inside a folder, run `ntu learn content COURSE_ID --parent FOLDER_ID` until you find it. Alternatively, use `ntu learn content tree COURSE_ID` for a nested view.
4. For a file, run `ntu learn attachments COURSE_ID CONTENT_ID` and copy the attachment ID. For a video, use the content ID with `ntu learn videos download`.

The normal terminal output includes these IDs; `--json` is optional. A supported content URL can supply the course and content IDs, but a file command still needs its attachment ID.

### Courses, folders and search

Use a course code or Blackboard ID to browse content or search. `content tree` walks nested folders within the configured limits.

| Command | What it does |
| --- | --- |
| [`ntu learn auth status`](courses.md#cmd-learn-auth-status) | Sign in to NTULearn and report whether access is verified. |
| [`ntu learn content tree`](courses.md#cmd-learn-content-tree) | Read a course's nested content tree. |
| [`ntu learn content show`](courses.md#cmd-learn-content-show) | Read one level of course content. |
| [`ntu learn courses list`](courses.md#cmd-learn-courses-list) | List your enrolled NTULearn courses and organizations, including published availability and course IDs. |
| [`ntu learn search all`](courses.md#cmd-learn-search-all) | Recursively search content across available enrolled courses, or selected course_ids. |
| [`ntu learn search course`](courses.md#cmd-learn-search-course) | Recursively search one course's content titles, body and description for a case-insensitive substring. |

### Attachments and downloads

List attachments to obtain an attachment ID. Downloads need an explicit destination and confirmation; a supported NTULearn URL can supply the course and content IDs.

| Command | What it does |
| --- | --- |
| [`ntu learn attachments`](files.md#cmd-learn-attachments) | List files attached to a course content item. |
| [`ntu learn courses download`](files.md#cmd-learn-courses-download) | Recursively save readable Blackboard attachments under destination/course_id with content folder names and stable file IDs. |
| [`ntu learn files read`](files.md#cmd-learn-files-read) | Read an attachment inline as text: PDF, DOCX, PPTX, XLSX and UTF text/code. |
| [`ntu learn files download`](files.md#cmd-learn-files-download) | Download a Blackboard attachment to an explicit local file path, up to 20 MB. |
| [`ntu learn videos download`](files.md#cmd-learn-videos-download) | Download a Kaltura video embedded in an NTULearn content item to a new local file. |

### Announcements, calendar and grades

Read activity for a course or collect information across enrolled courses. Date and time inputs without a timezone use Singapore time.

| Command | What it does |
| --- | --- |
| [`ntu learn announcements`](activity.md#cmd-learn-announcements) | Read published announcements for one enrolled course. |
| [`ntu learn grades`](activity.md#cmd-learn-grades) | Read visible gradebook columns and your own scores/status. |
| [`ntu learn calendar`](activity.md#cmd-learn-calendar) | Read calendar entries and published deadlines, across your courses or for one course. |
| [`ntu learn upcoming`](activity.md#cmd-learn-upcoming) | Collect all calendar pages across your enrolled courses. |
| [`ntu learn digest`](activity.md#cmd-learn-digest) | Digest of recent announcements, upcoming calendar items and your gradebook across courses. |

### Messages, participants and groups

Browse participants, groups and messages visible to your account.

| Command | What it does |
| --- | --- |
| [`ntu learn users`](people.md#cmd-learn-users) | List course users visible to your account, with their published names and roles. |
| [`ntu learn groups members`](people.md#cmd-learn-groups-members) | List visible members of a course group through Blackboard's browser membership API. |
| [`ntu learn groups list`](people.md#cmd-learn-groups-list) | List groups and group sets defined in a course. |
| [`ntu learn messages list`](people.md#cmd-learn-messages-list) | List Blackboard inbox/sent messages through readable course conversations, without marking them read. |
| [`ntu learn messages read`](people.md#cmd-learn-messages-read) | Read a message's full body and published conversation recipients. |
