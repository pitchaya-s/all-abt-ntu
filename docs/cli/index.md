# CLI guide

## Installation

To make `ntu` available as a command, run:

```sh
uv tool install 'all-abt-ntu[cli,personal]@latest'
ntu cli setup
```

The `cli` extra installs the terminal interface; `personal` adds browser support for authenticated services. Setup offers to save credentials and install Chromium; you can skip either step. For public CLI services only, install `all-abt-ntu[cli]@latest`. The MCP server is a separate extra and is not installed by those commands.

When no credentials are saved, the credential prompt defaults to yes. If credentials are already saved, replacing them defaults to no. Setup skips the Chromium prompt when the matching Playwright browser is already installed.

`ntu auth status` checks the local keyring only. Service commands such as `ntu onestop auth status` attempt a real sign-in to verify that service; they may require a network connection and can report an MFA or CAPTCHA challenge.

The `personal` extra includes NTULearn browser cookie discovery. See the [NTULearn session settings](../services/ntulearn/index.md#sessions) for the sign-in order and how to disable discovery.

## Find the right command

Every service has a command group. Open its reference for examples, arguments and output fields:

| I want to… | Start here |
| --- | --- |
| Search courses, compare indexes or inspect prerequisites | [STARS](../services/stars/cli/index.md) |
| Browse my courses, materials, grades or calendar | [NTULearn](../services/ntulearn/cli/index.md) |
| Find internships, employers or career events | [CareerAxis](../services/careeraxis/cli/index.md) |
| Find a place or get directions | [MazeMap](../services/mazemap/cli/index.md) |
| Search research publications and datasets | [DR-NTU](../services/drntu/cli/index.md) |
| Search library resources or check facilities | [Library](../services/library/cli/index.md) |
| Search faculty profiles or interests | [Faculty](../services/faculty/cli/index.md) |
| Browse university stories | [News](../services/news/cli/index.md) |
| Find food, shops, clinics or services | [Campus Services](../services/campus-services/cli/index.md) |
| Check shuttle stops, arrivals or schedules | [Omnibus](../services/omnibus/cli/index.md) |
| Manage student requests, appointments or the catalog | [One Stop](../services/one-stop/cli/index.md) |

Run `ntu --help` for the service list, `ntu stars --help` for a service, or `ntu stars indexes --help` for a subgroup. Append `--help` to an individual command to see its arguments and options. The [complete command reference](commands.md) also lists the management commands.

## Read a command

In `ntu stars course ZZ0001 --year 2026 --semester 1`, `stars course` selects the operation, `ZZ0001` is a positional course code, and `--year` and `--semester` are options. Reference tables mark required values and defaults. Quotation marks keep a multiword query or URL together in your shell.

Use `--json` when supported to write machine-readable results to stdout. Many list and search commands offer `--limit`, `--offset` or `--page`; follow the pagination fields in the response when available. Use `--refresh` where offered to fetch fresh data. `-h`, `-j`, `-l`, `-p` and `-r` are short forms for help, JSON, limit, page and refresh where the corresponding option is available.

## Examples

Use `ntu --help` to explore all eleven service families. For example:

```sh
# STARS: search courses, inspect a course, and browse its indexes
ntu stars courses search "data structures" --year 2026 --semester 1 --limit 10 --offset 0
ntu stars course ZZ0001 --year 2026 --semester 1
ntu stars indexes ZZ0001 --year 2026 --semester 1 --limit 10 --offset 0
ntu stars prerequisites ZZ0001 --year 2026 --semester 1 --prerequisite-depth 2 --dependent-depth 2

# NTULearn: list courses, browse content, and download materials
ntu learn courses --limit 20 --offset 0
ntu learn content ZZ0001 --limit 20 --offset 0
ntu learn attachments ZZ0001 "_67890_1" --limit 20 --offset 0
ntu learn files download ZZ0001 "_67890_1" "_24680_1" --output "./lecture.pdf" --max-bytes 20000000
ntu learn courses download ZZ0001 --output "./course-materials" --max-files 50 --max-total-mb 200
ntu learn videos download ZZ0001 "_67890_1" --output "./lecture.mp4" --max-mb 500
ntu learn announcements ZZ0001 --limit 20 --offset 0
ntu learn upcoming --since 2026-01-01 --until 2026-12-31

# Other NTU services
ntu career opportunities search "software engineer" --page 1 --limit 10
ntu map search "LT1" --limit 10 --offset 0
ntu research search "machine learning" --entity-type Publication --page 0 --page-size 10
ntu library search "machine learning" --field title --match contains --limit 10 --offset 0
ntu faculty search "Tan" --page 1
ntu news search "artificial intelligence" --sort latest --page 1
ntu services search "coffee" --location "North Spine" --limit 10 --offset 0
ntu bus arrivals --route Blue --stop "Hall 6"
ntu onestop catalog search "transcript" --limit 10 --offset 0
```

`ZZ0001` is a fictional course. For NTULearn, replace it and the example content and attachment IDs with the IDs returned by the preceding commands; NTULearn uses its own course IDs. Downloads require local confirmation; choose new file paths for individual files and videos. NTULearn, CareerAxis, and One Stop commands require an authenticated account.

You can also pass an NTULearn document or lecture launch URL in place of the course and content IDs. The `https://` prefix is optional. Quote the URL so the shell preserves its query string:

```sh
ntu learn attachments 'https://ntulearn.ntu.edu.sg/ultra/courses/_100_1/document/_200_1?view=content&state=view'
ntu learn videos download 'https://ntulearn.ntu.edu.sg/ultra/courses/_100_1/document/_200_1?view=content&state=view' --output './lecture.mp4'
```

For `learn files read` and `learn files download`, the attachment ID is still required: the page URL identifies the content item, not an individual attachment. List attachments first to find it.

Use `-h` for help. Common options also have short forms, including `-r` for refresh, `-l` for limit, `-p` for page, `-j` for JSON, and `-o` for a download destination. See the [complete command reference](commands.md) for all commands and options.

## Manual install

To run the CLI from a local checkout:

```sh
git clone https://github.com/pitchaya-s/all-abt-ntu.git
cd all-abt-ntu
uv sync --no-default-groups --extra cli
source .venv/bin/activate
ntu --help
```

On Windows, use `.venv\Scripts\activate.bat` in Command Prompt or `.venv\Scripts\Activate.ps1` in PowerShell instead. For authenticated services, install the personal dependencies and Chromium, then save your credentials:

```sh
uv sync --no-default-groups --extra cli --extra personal
playwright install chromium
ntu auth save
```

Playwright versions can require different Chromium builds, so repeat the install command after upgrading. NTULearn can optionally reuse an existing browser session without launching Chromium. While the environment is active, run commands directly, for example `ntu map search LT1`.
