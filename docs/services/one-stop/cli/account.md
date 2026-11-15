# One Stop: Dashboard and profile CLI commands

[One Stop overview](../index.md) · [All One Stop CLI topics](index.md) · [MCP reference](../mcp/index.md)

View your dashboard and profile, or change editable preferences after confirmation.

```sh
ntu onestop dashboard
ntu onestop profile show
```

Replace capitalized placeholders with values returned by the service. Use `--help` after a command for its current options. Choose a command to see its arguments, examples and result fields.

| Command | What it does |
| --- | --- |
| [`ntu onestop dashboard`](account.md#cmd-onestop-dashboard) | Read your One Stop homepage announcements, actions/payment links, upcoming appointments and popular links. |
| [`ntu onestop announcements`](account.md#cmd-onestop-announcements) | Read One Stop announcements, summaries and links from the native announcements collection with local pagination. |
| [`ntu onestop actions`](account.md#cmd-onestop-actions) | Read your One Stop to-do/billing actions and their published due dates and payment links. |
| [`ntu onestop links`](account.md#cmd-onestop-links) | List links on One Stop's Popular Sites page, preserving native catalog, knowledge and external destinations. |
| [`ntu onestop auth status`](account.md#cmd-onestop-auth-status) | Report shared keyring availability and the last verified One Stop session without logging in or returning identity or credentials. |
| [`ntu onestop profile set`](account.md#cmd-onestop-profile-set) | Update one displayed editable own-profile field through its native inline editor. |
| [`ntu onestop profile picture`](account.md#cmd-onestop-profile-picture) | Upload the explicitly selected local image as your own ServiceNow profile picture using the native file input. |
| [`ntu onestop profile notifications`](account.md#cmd-onestop-profile-notifications) | Enable or disable your ServiceNow notification preference. |
| [`ntu onestop profile preference`](account.md#cmd-onestop-profile-preference) | Set an enabled own preference returned by get_profile. |
| [`ntu onestop profile show`](account.md#cmd-onestop-profile-show) | Read your own displayed profile fields, editable flags, preferences/choices, notification setting and picture-upload capability. |

## Command details

<a id="cmd-onestop-dashboard"></a>
### `ntu onestop dashboard`

Read your One Stop homepage announcements, actions/payment links, upcoming appointments and popular links.

#### Usage

```sh
ntu onestop dashboard
```

Use `ntu onestop dashboard --help` for the current interface.

#### Arguments and options

- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `announcements`, `actions`, `appointments`, `popular_links`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/account.md#onestop_get_dashboard).

<a id="cmd-onestop-announcements"></a>
### `ntu onestop announcements`

Read One Stop announcements, summaries and links from the native announcements collection with local pagination.

#### Usage

```sh
ntu onestop announcements
```

Use `ntu onestop announcements --help` for the current interface.

#### Arguments and options

- `--limit`, `-l`: Maximum number of results to return in this page. Default: `20`.
- `--offset`: Number of results to skip before this page. Default: `0`.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `offset`, `available_count`, `total_count`, `complete`, `next_offset`, `retrieved_at`, `source_url`, `cached`, `records`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/account.md#onestop_list_announcements).

<a id="cmd-onestop-actions"></a>
### `ntu onestop actions`

Read your One Stop to-do/billing actions and their published due dates and payment links.

#### Usage

```sh
ntu onestop actions
```

Use `ntu onestop actions --help` for the current interface.

#### Arguments and options

- `--limit`, `-l`: Maximum number of results to return in this page. Default: `20`.
- `--offset`: Number of results to skip before this page. Default: `0`.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `offset`, `available_count`, `total_count`, `complete`, `next_offset`, `retrieved_at`, `source_url`, `cached`, `records`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/account.md#onestop_list_my_actions).

<a id="cmd-onestop-links"></a>
### `ntu onestop links`

List links on One Stop's Popular Sites page, preserving native catalog, knowledge and external destinations.

#### Usage

```sh
ntu onestop links
```

Use `ntu onestop links --help` for the current interface.

#### Arguments and options

- `--limit`, `-l`: Maximum number of results to return in this page. Default: `20`.
- `--offset`: Number of results to skip before this page. Default: `0`.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `offset`, `available_count`, `total_count`, `complete`, `next_offset`, `retrieved_at`, `source_url`, `cached`, `records`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/account.md#onestop_list_popular_links).

<a id="cmd-onestop-auth-status"></a>
### `ntu onestop auth status`

Report shared keyring availability and the last verified One Stop session without logging in or returning identity or credentials.

#### Usage

```sh
ntu onestop auth status
```

Use `ntu onestop auth status --help` for the current interface.

#### Arguments and options

- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `credentials_configured`, `credential_storage`, `credential_error`, `session_verified`, `last_verified_at`, `session_storage`, `cache_ttl_seconds`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/catalog.md#onestop_auth_status).

<a id="cmd-onestop-profile-set"></a>
### `ntu onestop profile set`

Update one displayed editable own-profile field through its native inline editor.

This operation requires local confirmation and is refused when confirmation cannot be obtained interactively.

#### Usage

```sh
ntu onestop profile set FIELD_NAME VALUE
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu onestop profile set --help` for the current interface.

#### Arguments and options

- `FIELD_NAME`: **Required.** The name of the field to update.
- `VALUE`: **Required.** The value to set for the named field or preference.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/account.md#onestop_update_profile).

<a id="cmd-onestop-profile-picture"></a>
### `ntu onestop profile picture`

Upload the explicitly selected local image as your own ServiceNow profile picture using the native file input.

This operation requires local confirmation and is refused when confirmation cannot be obtained interactively.

#### Usage

```sh
ntu onestop profile picture /absolute/path/to/onestop-uploads/upload.pdf
```

Use `ntu onestop profile picture --help` for the current interface.

#### Arguments and options

- `FILE_PATH`: **Required.** The path of the local file to upload.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/account.md#onestop_update_profile_picture).

<a id="cmd-onestop-profile-notifications"></a>
### `ntu onestop profile notifications`

Enable or disable your ServiceNow notification preference.

This operation requires local confirmation and is refused when confirmation cannot be obtained interactively.

#### Usage

```sh
ntu onestop profile notifications on
```

Use `ntu onestop profile notifications --help` for the current interface.

#### Arguments and options

- `ENABLED`: **Required.** Choose `on` to enable the setting or `off` to disable it. Choices: `on`, `off`.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/account.md#onestop_set_notifications).

<a id="cmd-onestop-profile-preference"></a>
### `ntu onestop profile preference`

Set an enabled own preference returned by get_profile.

This operation requires local confirmation and is refused when confirmation cannot be obtained interactively.

#### Usage

```sh
ntu onestop profile preference accessibility VALUE
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu onestop profile preference --help` for the current interface.

#### Arguments and options

- `NAME`: **Required.** The name of the item, setting or field to use. Choices: `accessibility`, `voice_input`, `analytics`, `timezone`, `language`, `communication_channels`.
- `VALUE`: **Required.** The value to set for the named field or preference.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/account.md#onestop_set_user_preference).

<a id="cmd-onestop-profile-show"></a>
### `ntu onestop profile show`

Read your own displayed profile fields, editable flags, preferences/choices, notification setting and picture-upload capability.

#### Usage

```sh
ntu onestop profile show
```

Use `ntu onestop profile show --help` for the current interface.

#### Arguments and options

- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `fields`, `preferences`, `notifications_enabled`, `can_update_picture`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/account.md#onestop_get_profile).
