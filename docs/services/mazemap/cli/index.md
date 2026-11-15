# MazeMap: CLI reference

[Service overview](../index.md) · [CLI reference](index.md) · [MCP reference](../mcp/index.md)

## Example

Search for a place, then use a returned POI ID for details or directions.

```sh
ntu map search "LT1" --limit 10
```

## Commands

Choose a command for its arguments, examples and result fields. Use `ntu map --help` and append `--help` to a command for option details. Each command page identifies required arguments and any defaults. See the [complete CLI reference](../../../cli/commands.md) for shared settings and all services.

| Command | What it does |
| --- | --- |
| [`ntu map campuses`](index.md#cmd-map-campuses) | List campuses in NTU's MazeMap collection with IDs and center coordinates. |
| [`ntu map buildings`](index.md#cmd-map-buildings) | List campus buildings and their floor IDs/names/levels. |
| [`ntu map search`](index.md#cmd-map-search) | Search NTU rooms, venues and amenities by code, name or category, including aliases such as TR+7. |
| [`ntu map place`](index.md#cmd-map-place) | Read one NTU place's location, aliases, building, floor, categories and published description/capacity. |
| [`ntu map directions`](index.md#cmd-map-directions) | Get walking routes between two NTU POIs, estimated metres/seconds and English instructions where available. |

## Command details

<a id="cmd-map-campuses"></a>
### `ntu map campuses`

List campuses in NTU's MazeMap collection with IDs and center coordinates.

#### Usage

```sh
ntu map campuses
```

Use `ntu map campuses --help` for the current interface.

#### Arguments and options

- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `campuses`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/index.md#mazemap_list_campuses).

<a id="cmd-map-buildings"></a>
### `ntu map buildings`

List campus buildings and their floor IDs/names/levels.

#### Usage

```sh
ntu map buildings
```

Use `ntu map buildings --help` for the current interface.

#### Arguments and options

- `--campus`: The campus ID; use the campus listing to find available IDs. Default: `2123`.
- `--query`: The search terms. Quote multiword text so the shell passes it as one argument.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `campus_id`, `buildings`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/index.md#mazemap_list_buildings).

<a id="cmd-map-search"></a>
### `ntu map search`

Search NTU rooms, venues and amenities by code, name or category, including aliases such as TR+7.

#### Usage

```sh
ntu map search "LT1" --limit 10
```

Use `ntu map search --help` for the current interface.

#### Arguments and options

- `QUERY`: **Required.** The search terms. Quote multiword text so the shell passes it as one argument.
- `--campus`: The campus ID; use the campus listing to find available IDs.
- `--limit`, `-l`: Maximum number of results to return in this page. Default: `10`.
- `--offset`: Number of results to skip before this page. Default: `0`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `query`, `places`, `next_offset`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/index.md#mazemap_search_places).

<a id="cmd-map-place"></a>
### `ntu map place`

Read one NTU place's location, aliases, building, floor, categories and published description/capacity.

#### Usage

```sh
ntu map place 12345
```

Use `ntu map place --help` for the current interface.

#### Arguments and options

- `POI_ID`: **Required.** The place's POI ID, returned by the place search.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `place`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/index.md#mazemap_get_place).

<a id="cmd-map-directions"></a>
### `ntu map directions`

Get walking routes between two NTU POIs, estimated metres/seconds and English instructions where available.

#### Usage

```sh
ntu map directions 12345 67890
```

The POI IDs are examples; replace them with IDs returned by `ntu map search`. Use `ntu map directions --help` for the current interface.

#### Arguments and options

- `FROM_POI_ID`: **Required.** The starting place's POI ID, returned by the place search.
- `TO_POI_ID`: **Required.** The destination place's POI ID, returned by the place search.
- `--constraint`: The route accessibility constraint. Choices: `NO_CONSTRAINT`, `PREFER_ACCESSIBLE`, `REQUIRE_ACCESSIBLE`. Default: `NO_CONSTRAINT`.
- `--refresh`, `-r`: Fetch fresh data instead of using an available cached result.
- `--accessible`: Require an accessible walking route. Use this or `--constraint`, not both.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `from_poi_id`, `to_poi_id`, `constraint`, `routes`, `buildings`, `floors`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/index.md#mazemap_get_directions).
