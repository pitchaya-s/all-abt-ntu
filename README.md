# All About NTU CLI and MCP

A CLI and MCP server for NTU Singapore schedules, learning materials, campus navigation, research, faculty, library discovery, career opportunities, news, campus services, shuttle arrivals, and student administration.

[CLI](#cli) · [MCP](#mcp)

**Available services**

[STARS](https://github.com/pitchaya-s/all-abt-ntu-mcp/blob/main/src/stars/README.md) · [NTULearn](https://github.com/pitchaya-s/all-abt-ntu-mcp/blob/main/src/ntulearn/README.md) · [CareerAxis](src/careeraxis/README.md) · [MazeMap](https://github.com/pitchaya-s/all-abt-ntu-mcp/blob/main/src/mazemap/README.md) · [DR-NTU](https://github.com/pitchaya-s/all-abt-ntu-mcp/blob/main/src/drntu/README.md) · [Library](https://github.com/pitchaya-s/all-abt-ntu-mcp/blob/main/src/library/README.md) · [Faculty](https://github.com/pitchaya-s/all-abt-ntu-mcp/blob/main/src/faculty/README.md) · [News](https://github.com/pitchaya-s/all-abt-ntu-mcp/blob/main/src/news/README.md) · [Campus services](https://github.com/pitchaya-s/all-abt-ntu-mcp/blob/main/src/service/README.md) · [NTU Omnibus](https://github.com/pitchaya-s/all-abt-ntu-mcp/blob/main/src/omnibus/README.md) · [One Stop @ SAC](src/onestop/README.md).

## Installation

Install [uv](https://docs.astral.sh/uv/) and Python 3.10 or newer. To make `ntu` available as a command, run:

```sh
uv tool install 'all-abt-ntu-mcp[personal]@latest'
```

The `personal` extra supports authenticated services. Follow the [Chromium instructions](#chromium) if you use them. For public services only, install `all-abt-ntu-mcp@latest` without the extra. You can also run the MCP setup with `uvx` without installing the command globally, as shown below.

To enable optional NTULearn browser-cookie discovery, install with both extras: `uv tool install 'all-abt-ntu-mcp[personal,browser-cookies]@latest'`.

## Credentials

Public services need no credentials. For authenticated services, manage your account **yourself in a local terminal**:

```sh
ntu auth save
```

Your password is hidden while typing and stored encrypted locally in your OS keyring. The server never includes it in MCP responses sent to the LLM.

The prompts save one account for STARS, NTULearn, LibFacilities, One Stop and CareerAxis and enable automatic login/session recovery. Run `ntu auth save` again to update it, `ntu auth status` to check storage without revealing credentials, or `ntu auth delete` to remove it. MCP setup can also offer to save credentials when you enable personal tools.

The keyring must be available and unlocked: Secret Service or KWallet on Linux, Keychain on macOS, Credential Manager on Windows. There is no plaintext fallback. Passwords are not accepted through MCP, command arguments, environment variables, `.env`, or client configuration. Remove any credentials left in your old configuration; the server no longer reads them. More details: [shared credential storage](https://github.com/pitchaya-s/all-abt-ntu-mcp/blob/main/src/shared/README.md#credential-storage).

Some Linux installations do not include a keyring service. Install a provider such as GNOME Keyring or KWallet using your distribution's package manager, then follow your desktop's setup instructions to start and unlock it before running `ntu auth save`.

## CLI

Use `ntu --help` to explore all eleven service families. For example:

```sh
ntu stars courses search "data structures" -y 2026 -s 1 -j
ntu map search LT1
ntu bus arrivals --route Blue
ntu learn courses
```

Use `-h` for help. Common options also have short forms, including `-r` for refresh, `-l` for limit, `-p` for page, `-j` for JSON, and `-o` for a download destination. The CLI shares OS keyring credentials with MCP. MCP profiles and tool settings apply only to the MCP server; direct commands use service defaults and environment variables. Use `ntu onestop requests apply ITEM_ID`, `ntu onestop appointments book ITEM_ID`, and `ntu onestop cart checkout` for interactive workflows. See the [complete command reference](src/COMMANDS.md) for all commands and options.

### Manual install (CLI)

To run the CLI from a local checkout:

```sh
git clone https://github.com/pitchaya-s/all-abt-ntu-mcp.git
cd all-abt-ntu-mcp
uv sync
uv run ntu --help
```

For authenticated services, run `uv sync --extra personal`, follow the [Chromium instructions](#chromium), and save credentials with `uv run ntu auth save`. Run commands from the checkout with `uv run ntu`, for example `uv run ntu map search LT1`.

## MCP

### Local setup

Run setup in your terminal:

```sh
uvx --from 'all-abt-ntu-mcp[personal]@latest' ntu mcp setup
```

Choose a profile and select the tool families you want, such as STARS or NTULearn. Setup saves your choices on this machine. Follow the prompts for any additional setup, then connect your client using one of the examples below. If you installed `ntu` above, you can run `ntu mcp setup` instead.

### Choose tools

To list or change families and individual tools later, run:

```sh
uvx --from 'all-abt-ntu-mcp[personal]@latest' ntu mcp tools list
uvx --from 'all-abt-ntu-mcp[personal]@latest' ntu mcp tools list --all
uvx --from 'all-abt-ntu-mcp[personal]@latest' ntu mcp tools disable ntulearn
uvx --from 'all-abt-ntu-mcp[personal]@latest' ntu mcp tools enable ntulearn
uvx --from 'all-abt-ntu-mcp[personal]@latest' ntu mcp tools disable mazemap_get_directions
uvx --from 'all-abt-ntu-mcp[personal]@latest' ntu mcp tools enable mazemap_get_directions
```

Run `setup` again to change your profile or family selection. `tools list` shows families; `--all` shows individual tools. `[~]` means a family is partially enabled. Commands manage tools available in the active profile. Disabling a family also disables tools added to it later. Explicitly enabling a family enables all its tools in the active profile, including actions and downloads; individual tools can then be disabled. Restart the MCP server after changes. Settings do not affect the hosted server.

Without saved settings, the server uses the public profile. See [Configuration file](#configuration-file) for the file format and service settings.

### Profiles

Profiles limit which tools a local server can offer:

- **public:** public information only.
- **personal:** public and authenticated tools, with action and download tools unchecked until you enable them. Newly added action tools also start unchecked.

Setup saves your choice, so you do not need to pass `--profile` normally. The optional flag overrides the saved profile for a particular invocation; disabled tools remain disabled. Actions and downloads require MCP host confirmation; configure your client to show these requests, since a host may answer automatically.

### Custom MCP for Cloud AI

Use this server only if you trust the author of this repository.

In a cloud AI client that supports custom remote MCP servers:

1. Open the MCP or connector settings and add a server with any name you like.
2. Enter this server URL:

   ```text
   https://all-abt-ntu-mcp.vercel.app/mcp
   ```

3. Select **No authentication** and, if asked, **Streamable HTTP** as the transport.
4. Save and enable the server.

The hosted server provides **public tools only**. No NTU credentials are needed. Personal tools, such as NTULearn and saving STARS plans, require the [local setup](#local-setup).

For self-hosting, start with [Manual install](#manual-install). To connect a private server to ChatGPT or other supported OpenAI products, we recommend [OpenAI's `tunnel-client` (Secure MCP Tunnel)](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels). It supports the local stdio server without exposing a public HTTP endpoint.

With other methods, use HTTPS and authentication and review how your data is handled. **Do not expose personal tools through an unauthenticated public endpoint**: they can access private NTU data and act through your saved account.

### Codex

Add to `~/.codex/config.toml`:

```toml
[mcp_servers.all-abt-ntu-mcp]
command = "uvx"
args = ["--from", "all-abt-ntu-mcp[personal]@latest", "ntu", "mcp"]
startup_timeout_sec = 120
tool_timeout_sec = 240
```

On Linux, depending on your distribution and Secret Service or KWallet setup, you may need to add this optional line to the same MCP server block for keyring access:

```toml
env_vars = ["DBUS_SESSION_BUS_ADDRESS", "XDG_RUNTIME_DIR"]
```

These variables forward the current desktop session; they contain no NTU credentials. Start Codex from a terminal where `ntu auth status` succeeds. Restart Codex and check `codex mcp list`. Personal tools use your locally saved keyring account.

### Claude Code

Register for your user:

```sh
claude mcp add --scope user all-abt-ntu-mcp \
  -- uvx --from 'all-abt-ntu-mcp[personal]@latest' ntu mcp
claude mcp list
```

Personal tools use your locally saved keyring account. Check `claude mcp list` or `/mcp` inside Claude Code. See [Claude Code's MCP guide](https://code.claude.com/docs/en/mcp) for details.

### OpenCode

Add to `~/.config/opencode/opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "all-abt-ntu-mcp": {
      "type": "local",
      "command": ["uvx", "--from", "all-abt-ntu-mcp[personal]@latest", "ntu", "mcp"],
      "enabled": true,
      "timeout": 240000
    }
  }
}
```

Personal tools use your locally saved keyring account. Check `opencode mcp list`. See [OpenCode's MCP guide](https://docs.opencode.ai/docs/mcp-servers/) for details.

### Manual install

Clone the repository and run the server from a local checkout:

```sh
git clone --branch main https://github.com/pitchaya-s/all-abt-ntu-mcp.git all-abt-ntu-mcp
cd all-abt-ntu-mcp
uv sync
uv run ntu mcp
```

For personal tools, run `uv sync --extra personal`, then `uv run ntu mcp setup` to choose your tools. See [Credentials](#credentials) to manage your account.

The process uses MCP stdio, so it stays open while its MCP client is connected. Course responses are cached in memory for one hour by default; vacancy snapshots are cached for at most 60 seconds. Set `NTU_CACHE_TTL_SECONDS` to change the cache time or use `0` to disable caching.

### Chromium

Authenticated CLI services that use a browser and the MCP personal profile need Playwright and its matching Chromium build. If you use the PyPI package, install Chromium from the same package environment:

```sh
uvx --from 'all-abt-ntu-mcp[personal]@latest' playwright install chromium
```

For a repository checkout, run `uv sync --extra personal` followed by `uv run --no-sync playwright install chromium`. Playwright versions can require different Chromium builds, so repeat the matching command after upgrading. NTULearn can optionally reuse an existing browser session without launching Chromium, although the shared personal profiles still require Chromium for their other tools.

### Run an HTTP server on localhost

To connect an MCP client using Streamable HTTP, start the public server from the repository root:

```sh
uv run uvicorn api.index:app --host 127.0.0.1 --port 8000
```

Configure the client with `http://127.0.0.1:8000/mcp` and select **Streamable HTTP**. The server listens only on this computer. This HTTP endpoint provides public tools; personal tools require the local stdio command above.

### Configuration file

MCP settings are stored in `$XDG_CONFIG_HOME/all-abt-ntu/tools.json` (normally `~/.config/all-abt-ntu/tools.json`), or `%APPDATA%\all-abt-ntu\tools.json` on Windows. MCP setup and the configuration commands update this file. Direct service commands do not read it. For example:

```json
{
  "profile": "personal",
  "tools": {
    "enabled": ["stars_save_stars_plan"],
    "disabled": ["mazemap_get_directions"],
    "families": {
      "enabled": ["stars", "mazemap"],
      "disabled": ["news"]
    }
  },
  "env": {
    "stars": {"cache_ttl_seconds": 3600},
    "ntulearn": {"headless": false},
    "onestop": {"upload_dir": "/home/me/ntu-uploads"}
  }
}
```

Family settings apply to tools added later. An individually enabled tool can be used within a disabled family; an individually disabled tool stays off within an enabled family. Personal actions and downloads remain disabled unless explicitly enabled. `tools enable` and `tools disable` accept families or individual names and update the file.

All sections are optional; omitted values use their defaults. You can edit the file or use the CLI:

```sh
uv run ntu config set ntulearn.headless false
uv run ntu config set stars.cache_ttl_seconds 600
uv run ntu config list
uv run ntu config unset ntulearn.headless
```

For a PyPI install, use the same `uvx --from 'all-abt-ntu-mcp[personal]@latest'` prefix as in [local setup](#local-setup) instead of `uv run`. The supported settings under `env` are:

| Group | Settings |
| --- | --- |
| `stars` | `cache_ttl_seconds`, `personal_cache_ttl_seconds` |
| `ntulearn` | `cache_ttl_seconds`, `headless`, `browser_cookies`, `request_concurrency`, `request_interval_seconds`, `timeout_seconds` |
| `careeraxis` | `cache_ttl_seconds`, `headless` |
| `onestop` | `upload_dir` |
| `public_http` | `concurrency`, `interval_seconds`, `timeout_seconds`, `max_retry_delay_seconds` |
| `browser` | `browsers_path` for Playwright |

Use JSON booleans for switches, numbers for durations and limits, and strings for paths. Other environment variables can be stored under `env.other`, for example with `config set other.CUSTOM_SETTING value`. Configuration-location variables such as `XDG_CONFIG_HOME` must be set outside the file. Process environment variables take precedence over saved settings. Restart the server after changing settings. This file is plain text; use the keyring for credentials.

## Source layout

```text
src/
├── cli/                    CLI commands, dispatch, and rendering
├── application.py          Lazy service resources and cleanup
├── server.py               Local public/personal stdio server
├── public_server.py        Public tool registry
├── public_http_server.py   Hosted ASGI app and transport security
├── public_http_client.py   Pooled public HTTP client
├── shared/                 Operation catalog, MCP adapter, credentials, and shared helpers
├── stars/
│   ├── tools/               Academic, personal, and teaching-room tool groups
│   ├── schemas/             Course and room tool schemas
│   ├── domain/             Course models, timetable matching and room searches
│   ├── client/             Public NTU requests and caching
│   ├── parser/             Schedule and personal-page parsing
│   └── wish/               WISH login and saved-plan editing
├── ntulearn/
│   ├── mcp.py       Shared NTULearn operations and input schemas
│   ├── models/             Typed responses grouped by domain
│   ├── client/             Login, sessions, and REST requests
│   ├── parser/             Response and document parsing
│   └── services/           Content, files, mailbox, people, and activity
├── careeraxis/
│   ├── mcp.py       Authenticated CareerAxis operations
│   ├── client.py            Section searches and record detail requests
│   ├── browser/             ADFS login, browser session, and page snapshots
│   ├── parser.py            Rendered section and record normalization
│   └── models.py            Search, detail, and auth status responses
├── mazemap/
│   ├── mcp.py       Public map operations and input schemas
│   ├── models.py           Typed place and direction responses
│   ├── client.py           HTTP requests, pacing, and caching
│   └── parser.py           Place and route normalization
├── drntu/
│   ├── mcp.py       Public repository operations and schemas
│   ├── models.py           Shared metadata, snapshots, and errors
│   ├── rest/               DSpace search, files, and Dataverse datasets
│   └── oai/                OAI-PMH client, parser, models, and service
├── library/
│   ├── mcp.py       Public library operations and schemas
│   ├── personal_tools.py    Local authenticated facility tool
│   ├── models.py           Catalogue, access and facility responses
│   ├── client.py           OneSearch requests and pagination
│   ├── facilities/         Directory, map availability, browser, and schedules
│   └── parser.py           Primo record normalization
├── faculty/
│   ├── mcp.py       Public faculty operations and input schemas
│   ├── models.py           Typed profile and research-interest responses
│   ├── client.py           Directory requests, filters, and pagination
│   └── parser.py           Profile cards and interest form parsing
├── news/
│   ├── mcp.py       Public news operations and input schemas
│   ├── models.py           Typed story, category, and article responses
│   ├── client.py           News search and bounded article retrieval
│   └── parser.py           Story cards and article body extraction
├── service/
│   ├── mcp.py       Public campus service operations and input schemas
│   ├── models.py           Typed location and filter responses
│   ├── client.py           Complete directory collection and local search
│   └── parser.py           Contact, hours, and map normalization
├── omnibus/                Public shuttle and LTA stops, positions, arrivals and schedules
└── onestop/                Local ServiceNow reads and native workflows
    ├── services/           Catalog, form, ticket, cart, knowledge, and portal workflows
    └── attachments/        Verified attachment actions and safe local-file handling
tests/
├── stars/                  STARS tests and fictionalized fixtures
├── ntulearn/               NTULearn tests and synthetic fixtures
├── mazemap/                MazeMap tests and synthetic fixtures
├── repository/             DR-NTU tests and synthetic fixtures
├── library/                OneSearch and LibFacilities tests and fixtures
├── faculty/                Faculty directory tests and synthetic fixtures
├── news/                   News search and article tests with synthetic fixtures
├── service/                Campus directory tests and synthetic fixtures
├── hosted/                 Public HTTP protocol, isolation, and deployment checks
├── test_*.py               Keyring, local CLI, and shared lifecycle tests
└── typescript_smoke.mjs     Shared MCP interoperability check
```

## Service reference

See the [CLI command reference](src/COMMANDS.md) and [MCP tool reference](src/TOOLS.md) for the complete interfaces. Each service guide includes its command details, examples, and limitations.

## Tests

Personal-data, map, repository, library, faculty, news, and service fixtures are synthetic. Timetable fixtures use fictional course labels and indexes while retaining the HTML structures needed for parser tests. Opt-in live tests print counts and statuses; they do not save academic records or learning materials in the repository.

The offline tests cover keyring storage and failure handling, local credential prompts, session recovery, parsing, scheduling, lossless compaction, output-schema validation, tool calls/errors, and resource discovery. Protocol tests use Python SDK clients and an independent JSON-RPC client over stdio, including protocol versions `2025-06-18` and `2025-11-25`:

```sh
uv run python -m unittest discover -s tests -t . -v
```

An optional check uses the official TypeScript SDK. Node dependencies stay in a temporary directory:

```sh
NTU_MCP_TEST_SDK="$(mktemp -d)"
npm install --prefix "$NTU_MCP_TEST_SDK" --ignore-scripts --no-audit --no-fund @modelcontextprotocol/sdk@1.32.1
uv run node tests/typescript_smoke.mjs "$NTU_MCP_TEST_SDK"
```

These interoperability checks use offline fixtures and never edit saved plans.

Hosted HTTP checks cover public-only registration, rejected personal calls, output schemas, both modern and legacy Python SDK clients, Host/Origin validation, request-size limits, and independent serverless event loops. See the [HTTP test instructions](https://github.com/pitchaya-s/all-abt-ntu-mcp/blob/main/src/shared/README.md#http-tests) for the TypeScript client and opt-in live smoke.

Live checks and service-specific testing instructions: [STARS](https://github.com/pitchaya-s/all-abt-ntu-mcp/blob/main/src/stars/README.md#tests) · [NTULearn](https://github.com/pitchaya-s/all-abt-ntu-mcp/blob/main/src/ntulearn/README.md#tests) · [CareerAxis](https://github.com/pitchaya-s/all-abt-ntu-mcp/blob/main/src/careeraxis/README.md#validation) · [MazeMap](https://github.com/pitchaya-s/all-abt-ntu-mcp/blob/main/src/mazemap/README.md#tests) · [DR-NTU](https://github.com/pitchaya-s/all-abt-ntu-mcp/blob/main/src/drntu/README.md#tests) · [Library](https://github.com/pitchaya-s/all-abt-ntu-mcp/blob/main/src/library/README.md#tests) · [Faculty](https://github.com/pitchaya-s/all-abt-ntu-mcp/blob/main/src/faculty/README.md#tests) · [News](https://github.com/pitchaya-s/all-abt-ntu-mcp/blob/main/src/news/README.md#tests) · [Campus services](https://github.com/pitchaya-s/all-abt-ntu-mcp/blob/main/src/service/README.md#tests) · [NTU Omnibus](https://github.com/pitchaya-s/all-abt-ntu-mcp/blob/main/src/omnibus/README.md#checks) · [One Stop @ SAC](https://github.com/pitchaya-s/all-abt-ntu-mcp/blob/main/src/onestop/README.md#coverage-runtime-and-checks).

## Limitation

- Access depends on service availability and NTU permissions.
- Timetables are published schedules; vacancies are snapshots.
- NTULearn may restrict content, and large collections can return partial results. Inline document reading extracts text without OCR.
- MazeMap directions are estimates. Map data does not establish room availability or current physical access.
- NTU Omnibus positions and arrivals are live snapshots that can be empty or stale; route path geometry is outside the tool outputs.
- DR-NTU file metadata does not establish download permission. The dataset service may interrupt requests with CAPTCHA.
- Room searches cover published undergraduate teaching only, excluding occupancy, graduate classes, exams, other bookings, and access permissions. Unplaced lesson venues remain outside room-specific coverage.
- Library records and access labels do not establish subscription entitlement, anonymous full-text access, or a loanable copy.
- Facility booking statuses do not establish occupancy. MFA stops library login; no borrowing or facility bookings are submitted.

## Disclaimer

This is an independent project and is not affiliated with, sponsored by, or endorsed by Nanyang Technological University (NTU), Singapore.

Your NTU credentials are retrieved locally from your OS keyring and submitted over HTTPS to NTU or its Microsoft sign-in service. They are never returned through MCP. Academic data returned by tools is visible to the AI client. Keyring storage protects credentials at rest; it does not isolate them from other programs or agents allowed to access your unlocked keyring or the server process.

Use this software only to access accounts and materials you are authorized to access. Do not download, copy, store, or redistribute course recordings, lecture files, library resources, research data, or other restricted or copyrighted material unless you have permission. Follow NTU policies, copyright and license notices, source-service terms, and applicable law. Do not bypass authentication, CAPTCHA, DRM, paywalls, or other access restrictions. **You are responsible for ensuring your access, downloads, retention, and reuse are authorized.**
