# MCP setup

## Local setup

Run setup in your terminal:

```sh
uvx --from 'all-abt-ntu[cli,mcp,personal]@latest' ntu mcp setup
```

Choose a profile, select tool families, and choose the MCP clients to configure. Setup can register the server with Codex, Claude Code and OpenCode, or you can skip client configuration. Codex and Claude Code must be installed to use their registration commands. On Linux, setup configures Codex to forward the current D-Bus session variables for OS keyring access. OpenCode setup supports JSON and JSONC configurations; if both files exist, configure the server manually to avoid conflicting settings. Setup and tool-management commands require both the `cli` and `mcp` extras; the server itself needs only `mcp`, plus `personal` for authenticated tools.

To start the public stdio server directly without installing the CLI dependencies:

```sh
uvx --from 'all-abt-ntu[mcp]@latest' ntu mcp --profile public
```

## Choose tools

To list or change families and individual tools later, run:

```sh
uvx --from 'all-abt-ntu[cli,mcp,personal]@latest' ntu mcp tools list
uvx --from 'all-abt-ntu[cli,mcp,personal]@latest' ntu mcp tools list --all
uvx --from 'all-abt-ntu[cli,mcp,personal]@latest' ntu mcp tools disable ntulearn
uvx --from 'all-abt-ntu[cli,mcp,personal]@latest' ntu mcp tools enable ntulearn
uvx --from 'all-abt-ntu[cli,mcp,personal]@latest' ntu mcp tools disable mazemap_get_directions
uvx --from 'all-abt-ntu[cli,mcp,personal]@latest' ntu mcp tools enable mazemap_get_directions
```

Run `setup` again to change your profile or family selection. `tools list` shows families; `--all` shows individual tools. `[~]` means a family is partially enabled. Commands manage tools available in the active profile. Disabling a family also disables tools added to it later. Explicitly enabling a family enables all its tools in the active profile, including actions and downloads; individual tools can then be disabled. Restart the MCP server after changes. Settings do not affect the hosted server.

Without saved settings, the server uses the public profile. See [Configuration file](configuration.md#configuration-file) for the file format and service settings.

## Profiles

Profiles limit which tools a local server can offer:

- **public:** public information only.
- **personal:** public and authenticated tools, with action and download tools unchecked until you enable them. Newly added action tools also start unchecked.

Setup saves your choice, so you do not need to pass `--profile` normally. The optional flag overrides the saved profile for a particular invocation; disabled tools remain disabled. Actions and downloads require MCP host confirmation; configure your client to show these requests, since a host may answer automatically.

## Custom MCP for Cloud AI

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

## Codex

Add to `~/.codex/config.toml`:

```toml
[mcp_servers.all-abt-ntu-mcp]
command = "uvx"
args = ["--from", "all-abt-ntu[mcp,personal]@latest", "ntu", "mcp"]
startup_timeout_sec = 120
tool_timeout_sec = 240
```

On Linux, depending on your distribution and Secret Service or KWallet setup, you may need to add this optional line to the same MCP server block for keyring access:

```toml
env_vars = ["DBUS_SESSION_BUS_ADDRESS", "XDG_RUNTIME_DIR"]
```

These variables forward the current desktop session; they contain no NTU credentials. Start Codex from a terminal where `ntu auth status` succeeds. Restart Codex and check `codex mcp list`. Personal tools use your locally saved keyring account.

If an earlier setup stored a fixed D-Bus address, rerun setup and confirm replacement of the Codex entry to switch to forwarding the current session variables.

## Claude Code

Register for your user:

```sh
claude mcp add --scope user all-abt-ntu-mcp \
  -- uvx --from 'all-abt-ntu[mcp,personal]@latest' ntu mcp
claude mcp list
```

Personal tools use your locally saved keyring account. Check `claude mcp list` or `/mcp` inside Claude Code. See [Claude Code's MCP guide](https://code.claude.com/docs/en/mcp) for details.

## OpenCode

Add to `~/.config/opencode/opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "all-abt-ntu-mcp": {
      "type": "local",
      "command": ["uvx", "--from", "all-abt-ntu[mcp,personal]@latest", "ntu", "mcp"],
      "enabled": true,
      "timeout": 240000
    }
  }
}
```

Personal tools use your locally saved keyring account. Check `opencode mcp list`. See [OpenCode's MCP guide](https://docs.opencode.ai/docs/mcp-servers/) for details.

## Manual install

Clone the repository and run the server from a local checkout:

```sh
git clone --branch main https://github.com/pitchaya-s/all-abt-ntu.git
cd all-abt-ntu
uv sync --no-default-groups --extra mcp
uv run --no-sync ntu mcp
```

For setup and personal tools, run `uv sync --no-default-groups --extra cli --extra mcp --extra personal`, then `uv run --no-sync ntu mcp setup` to choose your tools. See [Credentials](../getting-started.md#credentials) to manage your account.

The process uses MCP stdio, so it stays open while its MCP client is connected. Course responses are cached in memory for one hour by default; vacancy snapshots are cached for at most 60 seconds. Set `NTU_CACHE_TTL_SECONDS` to change the cache time or use `0` to disable caching.

## Chromium

Authenticated CLI services that use a browser and the MCP personal profile need Playwright and its matching Chromium build. If you use the PyPI package, install Chromium from the same package environment:

```sh
uvx --from 'all-abt-ntu[personal]@latest' playwright install chromium
```

For a repository checkout, include `--extra personal` in the appropriate `uv sync` command above, then run `uv run --no-sync playwright install chromium`. Playwright versions can require different Chromium builds, so repeat the matching command after upgrading. NTULearn can optionally reuse an existing browser session without launching Chromium, although the shared personal profiles still require Chromium for their other tools.

## Run an HTTP server on localhost

To connect an MCP client using Streamable HTTP, start the public server from the repository root:

```sh
uv run uvicorn api.index:app --host 127.0.0.1 --port 8000
```

Configure the client with `http://127.0.0.1:8000/mcp` and select **Streamable HTTP**. The server listens only on this computer. This HTTP endpoint provides public tools; personal tools require the local stdio command above.

See the [configuration guide](configuration.md#configuration-file) for settings and environment variables.
