# All About NTU

Explore NTU services from your terminal or connect them to an AI assistant. Search courses and library resources, navigate campus, check shuttle arrivals, and access your own learning materials and student services through a single application.

[Documentation](https://pitchaya-s.github.io/all-abt-ntu/) · [CLI guide](https://pitchaya-s.github.io/all-abt-ntu/cli/) · [MCP setup](https://pitchaya-s.github.io/all-abt-ntu/mcp/) · [Service reference](https://pitchaya-s.github.io/all-abt-ntu/services/) · [Report an issue](https://github.com/pitchaya-s/all-abt-ntu/issues)

All About NTU provides two interfaces to the same services:

- **CLI:** run `ntu` commands directly in your terminal, with readable output or JSON for scripts.
- **MCP:** give a compatible AI client access to selected NTU tools through a local server or the hosted public server.

## Quickstart

Install [uv](https://docs.astral.sh/uv/) and Python 3.10 or newer. Then choose how you want to use All About NTU:

**Use the CLI**

```sh
uv tool install 'all-abt-ntu[cli,personal]@latest'
ntu cli setup
ntu --help
```

**Connect an MCP client**

```sh
uvx --from 'all-abt-ntu[cli,mcp,personal]@latest' ntu mcp setup
```

Setup lets you choose a profile, enable tools, and configure Codex, Claude Code, or OpenCode. You can also [connect to the hosted public server](#hosted-public-server) without installing anything locally.

For personal services such as NTULearn and One Stop, use CLI setup to save your credentials and install Chromium. You can skip these steps if you only use public services; no NTU account is needed for those.

**Your password stays in your OS keyring.** It is entered through a hidden prompt, stored locally with no plaintext fallback, and sent only to NTU or its Microsoft sign-in service when needed. It is never returned through MCP or shared with your AI client.

## Available services

| Service | What you can do | CLI | Reference |
| --- | --- | --- | --- |
| **STARS** | Search courses, explore prerequisites and indexes, view schedules and manage plans | `ntu stars` | [STARS](https://pitchaya-s.github.io/all-abt-ntu/services/stars/) |
| **NTULearn** | Browse enrolled courses, learning materials, announcements, grades and calendars | `ntu learn` | [NTULearn](https://pitchaya-s.github.io/all-abt-ntu/services/ntulearn/) |
| **CareerAxis** | Find opportunities, employers, career events and resources | `ntu career` | [CareerAxis](https://pitchaya-s.github.io/all-abt-ntu/services/careeraxis/) |
| **MazeMap** | Search campus places and get walking directions | `ntu map` | [MazeMap](https://pitchaya-s.github.io/all-abt-ntu/services/mazemap/) |
| **DR-NTU** | Discover research publications, repository collections and datasets | `ntu research` | [DR-NTU](https://pitchaya-s.github.io/all-abt-ntu/services/drntu/) |
| **Library** | Search the catalogue, inspect records and explore facilities | `ntu library` | [Library](https://pitchaya-s.github.io/all-abt-ntu/services/library/) |
| **Faculty** | Find faculty members and research interests | `ntu faculty` | [Faculty](https://pitchaya-s.github.io/all-abt-ntu/services/faculty/) |
| **News** | Browse and search NTU news | `ntu news` | [News](https://pitchaya-s.github.io/all-abt-ntu/services/news/) |
| **Campus Services** | Find food, shops, clinics and other campus services | `ntu services` | [Campus Services](https://pitchaya-s.github.io/all-abt-ntu/services/campus-services/) |
| **Omnibus** | Check shuttle routes, stops, arrivals and service status | `ntu bus` | [Omnibus](https://pitchaya-s.github.io/all-abt-ntu/services/omnibus/) |
| **One Stop @ SAC** | Explore the catalog and manage requests, appointments and other student services | `ntu onestop` | [One Stop](https://pitchaya-s.github.io/all-abt-ntu/services/one-stop/) |

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
uvx --from 'all-abt-ntu[cli,personal]@latest' ntu auth save
```

See [credentials and platform setup](https://pitchaya-s.github.io/all-abt-ntu/getting-started/#credentials) for more details.

## CLI

### Installation

For public and authenticated services:

```sh
uv tool install 'all-abt-ntu[cli,personal]@latest'
```

For public services only, install the smaller CLI extra:

```sh
uv tool install 'all-abt-ntu[cli]@latest'
```

See the [CLI installation guide](https://pitchaya-s.github.io/all-abt-ntu/cli/#installation) for browser-cookie support.

### Manual CLI installation

To run the CLI from a local checkout:

```sh
git clone https://github.com/pitchaya-s/all-abt-ntu.git
cd all-abt-ntu
uv sync --no-default-groups --extra cli --extra personal
uv run --no-sync playwright install chromium
uv run --no-sync ntu --help
```

For public services only, omit `--extra personal` and the Chromium installation. Use `uv run --no-sync ntu auth save` to save credentials for personal services. See the [manual CLI guide](https://pitchaya-s.github.io/all-abt-ntu/cli/#manual-install) for environment activation and platform-specific details.

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

`ZZ0001` and the IDs above are fictional. Replace them with your course and content IDs from the preceding commands. Supported NTULearn content URLs can also be used in place of course and content IDs; see the [NTULearn CLI guide](https://pitchaya-s.github.io/all-abt-ntu/services/ntulearn/cli/files/). Downloads require confirmation.

Explore the rest of campus:

```sh
ntu map search "LT1" --limit 10 --offset 0
ntu bus arrivals --route Blue --stop "Hall 6"
ntu library search "machine learning" --field title --match contains --limit 10 --offset 0
ntu news search "artificial intelligence" --sort latest --page 1
ntu services search "coffee" --location "North Spine" --limit 10 --offset 0
```

Run `ntu --help`, `ntu stars --help`, or add `--help` to a command to see its available arguments. Many data commands support `--json`, pagination options and `--refresh` where applicable:

```sh
ntu map search "LT1" --limit 10 --offset 0 --json
```

See the [CLI guide](https://pitchaya-s.github.io/all-abt-ntu/cli/) and [complete command reference](https://pitchaya-s.github.io/all-abt-ntu/cli/commands/) for more examples and options.

## MCP

MCP connects NTU tools to compatible AI clients. The local server offers a **public** profile and a **personal** profile; personal tools use your locally saved credentials. You choose which tools are available, and actions and downloads require confirmation.

### Local setup

```sh
uvx --from 'all-abt-ntu[cli,mcp,personal]@latest' ntu mcp setup
```

To review or change tools later:

```sh
uvx --from 'all-abt-ntu[cli,mcp,personal]@latest' ntu mcp tools list
uvx --from 'all-abt-ntu[cli,mcp,personal]@latest' ntu mcp tools list --all
uvx --from 'all-abt-ntu[cli,mcp,personal]@latest' ntu mcp tools disable news
uvx --from 'all-abt-ntu[cli,mcp,personal]@latest' ntu mcp tools enable stars
```

To run a public stdio server directly:

```sh
uvx --from 'all-abt-ntu[mcp]@latest' ntu mcp --profile public
```

The [MCP setup guide](https://pitchaya-s.github.io/all-abt-ntu/mcp/) covers client configuration, profiles, Chromium and manual installation. See the [tool reference](https://pitchaya-s.github.io/all-abt-ntu/mcp/tools/) for available tools.

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

If you didn't save credentials during setup, use `uv run --no-sync ntu auth save`. The [manual MCP guide](https://pitchaya-s.github.io/all-abt-ntu/mcp/#manual-install) has more details.

### Hosted public server

Add the following URL to a client that supports remote MCP servers, using Streamable HTTP and no authentication:

```text
https://all-abt-ntu-mcp.vercel.app/mcp
```

The hosted server provides public, read-only information. Personal services require the local server. See the [hosted MCP guide](https://pitchaya-s.github.io/all-abt-ntu/mcp/hosting/) for details.

## Documentation and contributing

Browse the [documentation site](https://pitchaya-s.github.io/all-abt-ntu/) for [getting started](https://pitchaya-s.github.io/all-abt-ntu/getting-started/), [service guides](https://pitchaya-s.github.io/all-abt-ntu/services/), [architecture and security](https://pitchaya-s.github.io/all-abt-ntu/architecture/), [known issues](https://pitchaya-s.github.io/all-abt-ntu/known-issues/), and [limitations](https://pitchaya-s.github.io/all-abt-ntu/limitations/).

To work on the project, see the [development guide](https://pitchaya-s.github.io/all-abt-ntu/development/), [testing guide](https://pitchaya-s.github.io/all-abt-ntu/testing/), and [contributing guide](https://pitchaya-s.github.io/all-abt-ntu/contributing/). Preview the documentation locally with:

```sh
uvx --from mkdocs-material mkdocs serve
```

## Disclaimer

This is an independent project and is not affiliated with, sponsored by, or endorsed by Nanyang Technological University (NTU), Singapore.

Your NTU credentials are retrieved locally from your OS keyring and submitted over HTTPS to NTU or its Microsoft sign-in service. They are never returned through MCP. Academic data returned by tools is visible to the AI client. Keyring storage protects credentials at rest; it does not isolate them from other programs or agents allowed to access your unlocked keyring or the server process.

Use this software only to access accounts and materials you are authorized to access. Do not download, copy, store, or redistribute course recordings, lecture files, library resources, research data, or other restricted or copyrighted material unless you have permission. Follow NTU policies, copyright and license notices, source-service terms, and applicable law. Do not bypass authentication, CAPTCHA, DRM, paywalls, or other access restrictions. **You are responsible for ensuring your access, downloads, retention, and reuse are authorized.**
