# All About NTU CLI and MCP

A CLI and MCP server for NTU Singapore schedules, learning materials, campus navigation, research, faculty, library discovery, career opportunities, news, campus services, shuttle arrivals, and student administration.

**Available services:** [STARS](docs/services/stars/index.md) · [NTULearn](docs/services/ntulearn/index.md) · [CareerAxis](docs/services/careeraxis/index.md) · [MazeMap](docs/services/mazemap/index.md) · [DR-NTU](docs/services/drntu/index.md) · [Library](docs/services/library/index.md) · [Faculty](docs/services/faculty/index.md) · [News](docs/services/news/index.md) · [Campus Services](docs/services/campus-services/index.md) · [Omnibus](docs/services/omnibus/index.md) · [One Stop @ SAC](docs/services/one-stop/index.md).

## Quickstart

Install [uv](https://docs.astral.sh/uv/) and Python 3.10 or newer.

Install the CLI:

```sh
uv tool install 'all-abt-ntu-mcp[cli,personal]@latest'
```

Or set up the MCP server and select your client:

```sh
uvx --from 'all-abt-ntu-mcp[cli,mcp,personal]@latest' ntu mcp setup
```

For authenticated services, follow the [credentials and Chromium instructions](docs/getting-started.md).

## CLI

```sh
# STARS
ntu stars courses search "data structures" --year 2026 --semester 1 --limit 10 --offset 0
ntu stars course ZZ0001 --year 2026 --semester 1
ntu stars indexes ZZ0001 --year 2026 --semester 1 --limit 10 --offset 0

# NTULearn
ntu learn courses --limit 20 --offset 0
ntu learn content ZZ0001 --limit 20 --offset 0
ntu learn attachments ZZ0001 "_67890_1" --limit 20 --offset 0
ntu learn files download ZZ0001 "_67890_1" "_24680_1" --output "./lecture.pdf" --max-bytes 20000000
ntu learn videos download ZZ0001 "_67890_1" --output "./lecture.mp4" --max-mb 500
```

`ZZ0001` and the example IDs are fictional. Replace them with the IDs returned by NTULearn. Downloads require local confirmation.

See the [CLI guide](docs/cli/index.md), [command reference](docs/cli/commands.md), and [service references](docs/services/index.md).

## MCP

Run `ntu mcp setup` to choose a profile, tools, and client. The hosted MCP server provides public, read-only information; personal tools require a local server.

See [MCP setup](docs/mcp/index.md), the [tool reference](docs/mcp/tools.md), and the [service references](docs/services/index.md).

## Documentation

Browse the [documentation site](https://pitchaya-s.github.io/all-abt-ntu/) or read the guides in this repository:

- [Getting started](docs/getting-started.md)
- [CLI guide and commands](docs/cli/index.md)
- [MCP setup and tools](docs/mcp/index.md)
- [Service guides](docs/services/index.md)
- [Development and testing](docs/development.md)
- [Contributing](docs/contributing.md)
- [Known issues](docs/known-issues.md)
- [Limitations and disclaimer](docs/limitations.md)

To preview the documentation locally, run `uvx --from mkdocs==1.6.1 mkdocs serve` from the repository root. See the [documentation build and deployment instructions](docs/development.md#documentation).

This independent project is not affiliated with or endorsed by Nanyang Technological University. Use it only for accounts and materials you are authorized to access.
