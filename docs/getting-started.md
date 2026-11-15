# Getting started

## Quickstart

Install [uv](https://docs.astral.sh/uv/) and Python 3.10 or newer. Install the CLI:

```sh
uv tool install 'all-abt-ntu[cli,personal]@latest'
ntu cli setup
```

Or configure the MCP server:

```sh
uvx --from 'all-abt-ntu[cli,mcp,personal]@latest' ntu mcp setup
```

See [CLI](cli/index.md) and [MCP](mcp/index.md) for installation details and usage.

For a public first command, try `ntu map search "LT1"` or `ntu bus routes`. Run `ntu --help` to explore services and append `--help` to a command for its arguments. Most data commands accept `--json` for scripting.

The CLI runs service operations directly. The MCP server exposes those services to an AI client; its public profile offers public data, while the personal profile also makes authenticated tools available. The hosted MCP server is public and read-only.

## Find a command or tool

- For terminal use, start with the [CLI guide](cli/index.md) or choose a [service](services/index.md), then open its CLI reference. Command help lists the current arguments and options.
- For an AI client, follow [MCP setup](mcp/index.md) and use the [tool reference](mcp/tools.md) or the MCP reference for a particular service. Tool pages describe inputs, outputs and limits.
- Data commands with `--json` write the result to stdout for scripts; diagnostics go to stderr. Use `--refresh` where available to request fresh data instead of a cached result.

Downloads and other changes ask for local confirmation. In MCP, the client must provide the confirmation requested by the server. One Stop applications, appointment bookings and checkout use single-command interactive workflows so their temporary state remains available until the workflow finishes.

## Credentials

Public services need no credentials. `ntu cli setup` can save credentials and install Chromium. If you already saved your credentials during setup, you do not need to save them again. Otherwise, manage your account **yourself in a local terminal**:

```sh
ntu auth save
```

If you only use MCP through `uvx`, run `uvx --from 'all-abt-ntu[cli,personal]@latest' ntu auth save` instead. Browser-based services also need Playwright's [matching Chromium build](mcp/index.md#chromium).

Your password is hidden while typing and stored encrypted locally in your OS keyring. The server never includes it in MCP responses sent to the LLM.

The prompts save one account for STARS, NTULearn, LibFacilities, One Stop and CareerAxis and enable automatic login/session recovery. Run `ntu auth save` again to update it, `ntu auth status` to check storage without revealing credentials, or `ntu auth delete` to remove it. MCP setup can also offer to save credentials when you enable personal tools.

The keyring must be available and unlocked: Secret Service or KWallet on Linux, Keychain on macOS, Credential Manager on Windows. There is no plaintext fallback. Passwords are not accepted through MCP, command arguments, environment variables, `.env`, or client configuration. Remove any credentials left in your old configuration; the server no longer reads them. More details: [shared credential storage](architecture/credentials.md#credential-storage).

Some Linux installations do not include a keyring service. Install a provider such as GNOME Keyring or KWallet using your distribution's package manager, then follow your desktop's setup instructions to start and unlock it before running `ntu auth save`.
