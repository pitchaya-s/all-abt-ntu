# STARS: Rooms CLI commands

[Back to STARS CLI](index.md) · [MCP reference](../mcp/index.md)

- [`ntu stars rooms schedule`](#cmd-stars-rooms-schedule)
- [`ntu stars rooms available`](#cmd-stars-rooms-available)

## Command details

<a id="cmd-stars-rooms-schedule"></a>
### `ntu stars rooms schedule`

Get all published undergraduate course/index lessons using one observed room, including full-time and part-time offerings.

#### Usage

```sh
ntu stars rooms schedule VENUE --year 2026 --semester 1
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu stars rooms schedule --help` for the current interface.

#### Arguments and options

- `VENUE`: **Required.** The published room or venue name.
- `--year`, `-y`: **Required.** The first year of the academic year; `2026` means AY2026/27.
- `--semester`, `-s`: **Required.** Semester within the selected academic year. Choices: `1`, `2`, `S`.
- `--day`: Day of the week for the requested schedule. Choices: `MON`, `TUE`, `WED`, `THU`, `FRI`, `SAT`, `SUN`.
- `--week`: A teaching week to include; repeat `--week` for multiple weeks.
- `--start-time`: Start time in 24-hour `HH:MM` format.
- `--end-time`: End time in 24-hour `HH:MM` format.
- `--limit`, `-l`: Maximum number of results to return in this page. Default: `50`.
- `--offset`: Number of results to skip before this page. Default: `0`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `academic_year`, `semester`, `source_url`, `retrieved_at`, `cached`, `coverage`, `room`, `session_count`, `offset`, `has_more`, `sessions`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/rooms.md#stars_get_room_schedule).

<a id="cmd-stars-rooms-available"></a>
### `ntu stars rooms available`

Find teaching-free rooms; this does not establish occupancy or bookability.

#### Usage

```sh
ntu stars rooms available --year 2026 --semester 1 --day MON --from 14:00 --until 16:00
```

Use `ntu stars rooms available --help` for the current interface.

#### Arguments and options

- `--year`, `-y`: **Required.** The first year of the academic year; `2026` means AY2026/27.
- `--semester`, `-s`: **Required.** Semester within the selected academic year. Choices: `1`, `2`, `S`.
- `--day`: **Required.** Day of the week for the requested schedule. Choices: `MON`, `TUE`, `WED`, `THU`, `FRI`, `SAT`, `SUN`.
- `--from`: **Required.** Start time in 24-hour `HH:MM` format.
- `--until`: **Required.** End time in 24-hour `HH:MM` format.
- `--week`: A teaching week to include; repeat `--week` for multiple weeks.
- `--buffer-minutes`: Extra minutes to keep clear around the requested room window. Default: `0`.
- `--room-type`: A room type to include; repeat the option for multiple types. Values are `tutorial_room`, `seminar_room`, `lecture_theatre`, `laboratory` and `other`.
- `--venue-contains`: Require the venue name to contain this text.
- `--venue-prefix`: A venue-name prefix to include; repeat the option for multiple prefixes.
- `--exclude-venue`: A venue to exclude; repeat the option for multiple venues.
- `--filters`: Structured filters as a JSON value.
- `--limit`, `-l`: Maximum number of results to return in this page. Default: `20`.
- `--offset`: Number of results to skip before this page. Default: `0`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `academic_year`, `semester`, `source_url`, `retrieved_at`, `cached`, `coverage`, `availability_basis`, `window`, `match_count`, `offset`, `has_more`, `rooms`, `excluded_busy_count`, `excluded_uncertain_count`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/rooms.md#stars_find_available_rooms).
