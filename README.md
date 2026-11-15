# All About NTU

Explore NTU services from your terminal or connect them to an AI assistant. Search courses and library resources, navigate campus, check shuttle arrivals, and access your own learning materials and student services through a single application.

[Documentation](https://pitchaya-s.github.io/all-abt-ntu/) · [CLI guide](docs/cli/index.md) · [MCP setup](docs/mcp/index.md) · [Service reference](docs/services/index.md) · [Report an issue](https://github.com/pitchaya-s/all-abt-ntu/issues)

All About NTU provides two interfaces to the same services:

- **CLI:** run `ntu` commands directly in your terminal, with readable output or JSON for scripts.
- **MCP:** give a compatible AI client access to selected NTU tools through a local server or the hosted public server.

## Quickstart

Install [uv](https://docs.astral.sh/uv/) and Python 3.10 or newer. Then choose how you want to use All About NTU:

**Use the CLI**

```sh
uv tool install 'all-abt-ntu-mcp[cli,personal]@latest'
ntu cli setup
ntu --help
```

**Connect an MCP client**

```sh
uvx --from 'all-abt-ntu-mcp[cli,mcp,personal]@latest' ntu mcp setup
```

Setup lets you choose a profile, enable tools, and configure Codex, Claude Code, or OpenCode. You can also [connect to the hosted public server](#hosted-public-server) without installing anything locally.

For personal services such as NTULearn and One Stop, use CLI setup to save your credentials and install Chromium. You can skip these steps if you only use public services; no NTU account is needed for those.

**Your password stays in your OS keyring.** It is entered through a hidden prompt, stored locally with no plaintext fallback, and sent only to NTU or its Microsoft sign-in service when needed. It is never returned through MCP or shared with your AI client.

## Available services

| Service | What you can do | CLI | Reference |
| --- | --- | --- | --- |
| **STARS** | Search courses, explore prerequisites and indexes, view schedules and manage plans | `ntu stars` | [STARS](docs/services/stars/index.md) |
| **NTULearn** | Browse enrolled courses, learning materials, announcements, grades and calendars | `ntu learn` | [NTULearn](docs/services/ntulearn/index.md) |
| **CareerAxis** | Find opportunities, employers, career events and resources | `ntu career` | [CareerAxis](docs/services/careeraxis/index.md) |
| **MazeMap** | Search campus places and get walking directions | `ntu map` | [MazeMap](docs/services/mazemap/index.md) |
| **DR-NTU** | Discover research publications, repository collections and datasets | `ntu research` | [DR-NTU](docs/services/drntu/index.md) |
| **Library** | Search the catalogue, inspect records and explore facilities | `ntu library` | [Library](docs/services/library/index.md) |
| **Faculty** | Find faculty members and research interests | `ntu faculty` | [Faculty](docs/services/faculty/index.md) |
| **News** | Browse and search NTU news | `ntu news` | [News](docs/services/news/index.md) |
| **Campus Services** | Find food, shops, clinics and other campus services | `ntu services` | [Campus Services](docs/services/campus-services/index.md) |
| **Omnibus** | Check shuttle routes, stops, arrivals and service status | `ntu bus` | [Omnibus](docs/services/omnibus/index.md) |
| **One Stop @ SAC** | Explore the catalog and manage requests, appointments and other student services | `ntu onestop` | [One Stop](docs/services/one-stop/index.md) |

The service references include CLI commands, MCP tools, arguments, outputs and service-specific limits.

## Authentication

If you saved your credentials during setup, you do not need to save them again. To save or manage them later, run:

```sh
ntu auth save
ntu auth status
ntu auth delete
```

Your password is entered through a hidden prompt and stored locally in your OS keyring; there is no plaintext fallback. Your keyring must be available and unlocked. Never enter a password into an AI conversation or MCP client configuration.

If you use MCP through `uvx` without installing the CLI, save credentials with:

```sh
uvx --from 'all-abt-ntu-mcp[cli,personal]@latest' ntu auth save
```

See [credentials and platform setup](docs/getting-started.md#credentials) for more details.

## CLI

### Installation

For public and authenticated services:

```sh
uv tool install 'all-abt-ntu-mcp[cli,personal]@latest'
```

For public services only, install the smaller CLI extra:

```sh
uv tool install 'all-abt-ntu-mcp[cli]@latest'
```

See the [CLI installation guide](docs/cli/index.md#installation) for browser-cookie support.

### Manual CLI installation

To run the CLI from a local checkout:

```sh
git clone https://github.com/pitchaya-s/all-abt-ntu.git
cd all-abt-ntu
uv sync --no-default-groups --extra cli --extra personal
uv run --no-sync playwright install chromium
uv run --no-sync ntu --help
```

For public services only, omit `--extra personal` and the Chromium installation. Use `uv run --no-sync ntu auth save` to save credentials for personal services. See the [manual CLI guide](docs/cli/index.md#manual-install) for environment activation and platform-specific details.

### Examples

Search courses, inspect a course and explore its indexes and prerequisites:

```sh
ntu stars courses search "data structures" --year 2026 --semester 1 --limit 10 --offset 0
ntu stars course ZZ0001 --year 2026 --semester 1
ntu stars indexes ZZ0001 --year 2026 --semester 1 --limit 10 --offset 0
ntu stars prerequisites ZZ0001 --year 2026 --semester 1 --prerequisite-depth 2 --dependent-depth 2
```

Browse NTULearn content and download a file or video:

```sh
ntu learn courses --limit 20 --offset 0
ntu learn content ZZ0001 --limit 20 --offset 0
ntu learn attachments ZZ0001 "_67890_1" --limit 20 --offset 0
ntu learn files download ZZ0001 "_67890_1" "_24680_1" --output "./lecture.pdf" --max-bytes 20000000
ntu learn videos download ZZ0001 "_67890_1" --output "./lecture.mp4" --max-mb 500
```

`ZZ0001` and the IDs above are fictional. Replace them with your course and content IDs from the preceding commands. Supported NTULearn content URLs can also be used in place of course and content IDs; see the [NTULearn CLI guide](docs/services/ntulearn/cli/files.md). Downloads require confirmation.

Explore the rest of campus:

```sh
ntu map search "LT1" --limit 10 --offset 0
ntu bus arrivals --route Blue --stop "North Spine" --source shuttle
ntu library search "machine learning" --field title --match contains --limit 10 --offset 0
ntu news search "artificial intelligence" --sort latest --page 1
ntu services search "coffee" --location "North Spine" --limit 10 --offset 0
```

Run `ntu --help`, `ntu stars --help`, or add `--help` to a command to see its available arguments. Many data commands support `--json`, pagination options and `--refresh` where applicable:

```sh
ntu map search "LT1" --limit 10 --offset 0 --json
```

See the [CLI guide](docs/cli/index.md) and [complete command reference](docs/cli/commands.md) for more examples and options.

## MCP

MCP connects NTU tools to compatible AI clients. The local server offers a **public** profile and a **personal** profile; personal tools use your locally saved credentials. You choose which tools are available, and actions and downloads require confirmation.

### Local setup

```sh
uvx --from 'all-abt-ntu-mcp[cli,mcp,personal]@latest' ntu mcp setup
```

To review or change tools later:

```sh
uvx --from 'all-abt-ntu-mcp[cli,mcp,personal]@latest' ntu mcp tools list
uvx --from 'all-abt-ntu-mcp[cli,mcp,personal]@latest' ntu mcp tools list --all
uvx --from 'all-abt-ntu-mcp[cli,mcp,personal]@latest' ntu mcp tools disable news
uvx --from 'all-abt-ntu-mcp[cli,mcp,personal]@latest' ntu mcp tools enable stars
```

To run a public stdio server directly:

```sh
uvx --from 'all-abt-ntu-mcp[mcp]@latest' ntu mcp --profile public
```

The [MCP setup guide](docs/mcp/index.md) covers client configuration, profiles, Chromium and manual installation. See the [tool reference](docs/mcp/tools.md) for available tools.

### Manual MCP installation

For interactive setup and personal tools from a local checkout:

```sh
git clone https://github.com/pitchaya-s/all-abt-ntu.git
cd all-abt-ntu
uv sync --no-default-groups --extra cli --extra mcp --extra personal
uv run --no-sync ntu mcp setup
```

For a public server, install only the MCP extra and start the server directly:

```sh
uv sync --no-default-groups --extra mcp
uv run --no-sync ntu mcp --profile public
```

If you didn't save credentials during setup, use `uv run --no-sync ntu auth save`. The [manual MCP guide](docs/mcp/index.md#manual-install) has more details.

### Hosted public server

Add the following URL to a client that supports remote MCP servers, using Streamable HTTP and no authentication:

```text
https://all-abt-ntu-mcp.vercel.app/mcp
```

The hosted server provides public, read-only information. Personal services require the local server. See the [hosted MCP guide](docs/mcp/hosting.md) for details.

## Documentation and contributing

Browse the [documentation site](https://pitchaya-s.github.io/all-abt-ntu/) for [getting started](docs/getting-started.md), [service guides](docs/services/index.md), [architecture and security](docs/architecture/index.md), [known issues](docs/known-issues.md), and [limitations](docs/limitations.md).

To work on the project, see the [development guide](docs/development.md), [testing guide](docs/testing.md), and [contributing guide](docs/contributing.md). Preview the documentation locally with:

```sh
uvx --from mkdocs-material mkdocs serve
```

## Disclaimer

This is an independent project and is not affiliated with, sponsored by, or endorsed by Nanyang Technological University (NTU), Singapore.

Your NTU credentials are retrieved locally from your OS keyring and submitted over HTTPS to NTU or its Microsoft sign-in service. They are never returned through MCP. Academic data returned by tools is visible to the AI client. Keyring storage protects credentials at rest; it does not isolate them from other programs or agents allowed to access your unlocked keyring or the server process.

Use this software only to access accounts and materials you are authorized to access. Do not download, copy, store, or redistribute course recordings, lecture files, library resources, research data, or other restricted or copyrighted material unless you have permission. Follow NTU policies, copyright and license notices, source-service terms, and applicable law. Do not bypass authentication, CAPTCHA, DRM, paywalls, or other access restrictions. **You are responsible for ensuring your access, downloads, retention, and reuse are authorized.**
