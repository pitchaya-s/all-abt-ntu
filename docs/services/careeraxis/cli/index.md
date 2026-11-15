# CareerAxis: CLI reference

[Service overview](../index.md) · [CLI reference](index.md) · [MCP reference](../mcp/index.md)

## Example

Search opportunities available to your signed-in account.

```sh
ntu career opportunities search "software engineer" --page 1 --limit 10
```

## Commands

Choose a command for its arguments, examples and result fields. Use `ntu career --help` and append `--help` to a command for option details. Each command page identifies required arguments and any defaults. See the [complete CLI reference](../../../cli/commands.md) for shared settings and all services.

| Command | What it does |
| --- | --- |
| [`ntu career record`](index.md#cmd-career-record) | Read the visible details for a CareerAxis event, resource document, employer, appointment topic, or internship posting URL returned by a CareerAxis search tool. |
| [`ntu career appointments topics`](index.md#cmd-career-appointments-topics) | Search CareerAxis career-coaching appointment topics such as internship strategy, interview practice, and resume critique. |
| [`ntu career auth status`](index.md#cmd-career-auth-status) | Report whether shared NTU keyring credentials can be read and whether this process has verified CareerAxis login; does not log in. |
| [`ntu career employers search`](index.md#cmd-career-employers-search) | Search CareerAxis employer profiles by name, optionally limiting results to employers with current opportunities. |
| [`ntu career events search`](index.md#cmd-career-events-search) | Search authenticated CareerAxis events by keyword. |
| [`ntu career internships search`](index.md#cmd-career-internships-search) | Search the authenticated CareerAxis Internship workgroup job board by keyword across its visible internship postings. |
| [`ntu career opportunities search`](index.md#cmd-career-opportunities-search) | Search your authenticated NTU CareerAxis job and internship listings by keyword. |
| [`ntu career opportunities show`](index.md#cmd-career-opportunities-show) | Read the full visible text for an opportunity URL returned by careeraxis_search_opportunities, including HTTPS application links. |
| [`ntu career resources search`](index.md#cmd-career-resources-search) | Search CareerAxis career resources and training documents by keyword. |

## Command details

<a id="cmd-career-record"></a>
### `ntu career record`

Read the visible details for a CareerAxis event, resource document, employer, appointment topic, or internship posting URL returned by a CareerAxis search tool.

#### Usage

```sh
ntu career record URL
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu career record --help` for the current interface.

#### Arguments and options

- `URL`: **Required.** The URL of the record or article returned by a search.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `title`, `url`, `text`, `links`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/index.md#careeraxis_get_record).

<a id="cmd-career-appointments-topics"></a>
### `ntu career appointments topics`

Search CareerAxis career-coaching appointment topics such as internship strategy, interview practice, and resume critique.

#### Usage

```sh
ntu career appointments topics example
```

Use `ntu career appointments topics --help` for the current interface.

#### Arguments and options

- `QUERY`: The search terms. Quote multiword text so the shell passes it as one argument.
- `--page`, `-p`: Page number to request; page numbering depends on the service. Default: `1`.
- `--limit`, `-l`: Maximum number of results to return in this page. Default: `20`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `section`, `query`, `page`, `items`, `has_next_page`, `truncated`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/index.md#careeraxis_search_appointment_topics).

<a id="cmd-career-auth-status"></a>
### `ntu career auth status`

Report whether shared NTU keyring credentials can be read and whether this process has verified CareerAxis login; does not log in.

#### Usage

```sh
ntu career auth status
```

Use `ntu career auth status --help` for the current interface.

#### Arguments and options

- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `credentials_configured`, `credential_storage`, `credential_error`, `session_verified`, `last_verified_at`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/index.md#careeraxis_auth_status).

<a id="cmd-career-employers-search"></a>
### `ntu career employers search`

Search CareerAxis employer profiles by name, optionally limiting results to employers with current opportunities.

#### Usage

```sh
ntu career employers search
```

Use `ntu career employers search --help` for the current interface.

#### Arguments and options

- `NAME`: The name of the item, setting or field to use.
- `--current-only`: Limit employers to those with current opportunities.
- `--page`, `-p`: Page number to request; page numbering depends on the service. Default: `1`.
- `--limit`, `-l`: Maximum number of results to return in this page. Default: `20`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `section`, `query`, `page`, `items`, `has_next_page`, `truncated`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/index.md#careeraxis_search_organisations).

<a id="cmd-career-events-search"></a>
### `ntu career events search`

Search authenticated CareerAxis events by keyword.

#### Usage

```sh
ntu career events search example
```

Use `ntu career events search --help` for the current interface.

#### Arguments and options

- `QUERY`: The search terms. Quote multiword text so the shell passes it as one argument.
- `--page`, `-p`: Page number to request; page numbering depends on the service. Default: `1`.
- `--limit`, `-l`: Maximum number of results to return in this page. Default: `20`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `section`, `query`, `page`, `items`, `has_next_page`, `truncated`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/index.md#careeraxis_search_events).

<a id="cmd-career-internships-search"></a>
### `ntu career internships search`

Search the authenticated CareerAxis Internship workgroup job board by keyword across its visible internship postings.

#### Usage

```sh
ntu career internships search example
```

Use `ntu career internships search --help` for the current interface.

#### Arguments and options

- `QUERY`: The search terms. Quote multiword text so the shell passes it as one argument.
- `--page`, `-p`: Page number to request; page numbering depends on the service. Default: `1`.
- `--limit`, `-l`: Maximum number of results to return in this page. Default: `20`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `section`, `query`, `page`, `items`, `has_next_page`, `truncated`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/index.md#careeraxis_search_internship_jobs).

<a id="cmd-career-opportunities-search"></a>
### `ntu career opportunities search`

Search your authenticated NTU CareerAxis job and internship listings by keyword.

#### Usage

```sh
ntu career opportunities search "software engineer" --page 1 --limit 10
```

Use `ntu career opportunities search --help` for the current interface.

#### Arguments and options

- `QUERY`: The search terms. Quote multiword text so the shell passes it as one argument.
- `--page`, `-p`: Page number to request; page numbering depends on the service. Default: `1`.
- `--limit`, `-l`: Maximum number of results to return in this page. Default: `20`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `query`, `page`, `opportunities`, `has_next_page`, `truncated`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/index.md#careeraxis_search_opportunities).

<a id="cmd-career-opportunities-show"></a>
### `ntu career opportunities show`

Read the full visible text for an opportunity URL returned by careeraxis_search_opportunities, including HTTPS application links.

#### Usage

```sh
ntu career opportunities show URL
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu career opportunities show --help` for the current interface.

#### Arguments and options

- `URL`: **Required.** The URL of the record or article returned by a search.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `title`, `url`, `text`, `application_links`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/index.md#careeraxis_get_opportunity).

<a id="cmd-career-resources-search"></a>
### `ntu career resources search`

Search CareerAxis career resources and training documents by keyword.

#### Usage

```sh
ntu career resources search example
```

Use `ntu career resources search --help` for the current interface.

#### Arguments and options

- `QUERY`: The search terms. Quote multiword text so the shell passes it as one argument.
- `--page`, `-p`: Page number to request; page numbering depends on the service. Default: `1`.
- `--limit`, `-l`: Maximum number of results to return in this page. Default: `20`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `section`, `query`, `page`, `items`, `has_next_page`, `truncated`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/index.md#careeraxis_search_resources).
