# NTU Omnibus: CLI reference

[Service overview](../index.md) · [CLI reference](index.md) · [MCP reference](../mcp/index.md)

## Example

Check shuttle routes and arrival estimates.

```sh
ntu bus routes
ntu bus arrivals --route Blue --stop "North Spine" --source shuttle
```

## Commands

Choose a command for its arguments, examples and result fields. Use `ntu bus --help` and append `--help` to a command for option details. Each command page identifies required arguments and any defaults. See the [complete CLI reference](../../../cli/commands.md) for shared settings and all services.

| Command | What it does |
| --- | --- |
| [`ntu bus routes`](index.md#cmd-bus-routes) | List public NTU shuttle routes and their published display colors. |
| [`ntu bus stops`](index.md#cmd-bus-stops) | Search NTU shuttle and LTA bus stops by stop name or code, optionally limited to a route/service. |
| [`ntu bus arrivals`](index.md#cmd-bus-arrivals) | Get arrival estimates for NTU shuttles and LTA buses. |
| [`ntu bus live`](index.md#cmd-bus-live) | Get current live vehicle positions for one NTU campus shuttle route. |
| [`ntu bus status`](index.md#cmd-bus-status) | Get the published first/last bus schedule, public-holiday/special-day flags, and temporary notices for an NTU campus shuttle route. |

## Command details

<a id="cmd-bus-routes"></a>
### `ntu bus routes`

List public NTU shuttle routes and their published display colors.

#### Usage

```sh
ntu bus routes
```

Use `ntu bus routes --help` for the current interface.

#### Arguments and options

- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_urls`, `cached`, `routes`, `colors`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/index.md#omnibus_list_routes).

<a id="cmd-bus-stops"></a>
### `ntu bus stops`

Search NTU shuttle and LTA bus stops by stop name or code, optionally limited to a route/service.

The terminal shows stop names and their routes. A stop can appear on a later page if it serves several routes.

#### Usage

```sh
ntu bus stops "Lee Wee Nam" --route 179
```

Use `ntu bus stops --help` for the current interface.

#### Arguments and options

- `QUERY`: The search terms. Quote multiword text so the shell passes it as one argument.
- `--route`: Campus shuttle route or LTA service. Choices: `Blue`, `Brown`, `Green`, `Grey`, `Red`, `179`, `179A`, `179B`, `199`.
- `--limit`, `-l`: Maximum number of results to return in this page. Default: `20`.
- `--offset`: Number of results to skip before this page. Default: `0`.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_urls`, `cached`, `stops`, `total_count`, `next_offset`, `routes_without_stop_data`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/index.md#omnibus_list_stops).

<a id="cmd-bus-arrivals"></a>
### `ntu bus arrivals`

Get arrival estimates for NTU shuttles and LTA services 179, 179A, 179B, and 199.

#### Usage

```sh
ntu bus arrivals --route Blue --stop "North Spine" --source shuttle
ntu bus arrivals --stop "Lee Wee Nam" --source lta
```

Use `ntu bus arrivals --help` for the current interface.

#### Arguments and options

- `--route`: Campus shuttle route or LTA service. Choices: `Blue`, `Brown`, `Green`, `Grey`, `Red`, `179`, `179A`, `179B`, `199`.
- `--stop`: Search by stop name.
- `--source`: Which arrival-data source to use. Choices: `all`, `shuttle`, `lta`. Default: `all`.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_urls`, `cached`, `route_filter`, `stop_query`, `shuttle_arrivals`, `lta_arrivals`, `routes_without_stop_data`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/index.md#omnibus_get_arrivals).

<a id="cmd-bus-live"></a>
### `ntu bus live`

Get current live vehicle positions for one NTU campus shuttle route.

#### Usage

```sh
ntu bus live
```

Use `ntu bus live --help` for the current interface.

#### Arguments and options

- `--route`: The published shuttle route or supported bus service. Choices: `Blue`, `Brown`, `Green`, `Grey`, `Red`. Default: `Blue`.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_urls`, `cached`, `route_code`, `reported_bus_count`, `source_timestamp`, `buses`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/index.md#omnibus_get_live_buses).

<a id="cmd-bus-status"></a>
### `ntu bus status`

Get the published first/last bus schedule, public-holiday/special-day flags, and temporary notices for an NTU campus shuttle route.

#### Usage

```sh
ntu bus status
```

Use `ntu bus status --help` for the current interface.

#### Arguments and options

- `--route`: The published shuttle route or supported bus service. Choices: `Blue`, `Brown`, `Green`, `Grey`, `Red`. Default: `Blue`.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_urls`, `cached`, `route_code`, `schedules`, `schedule_from_local_db`, `is_public_holiday`, `is_special_day`, `special_day_notice`, `has_temporary_message`, `temporary_message`, `no_active_bus_message`, `no_operations_message`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/index.md#omnibus_get_service_status).
