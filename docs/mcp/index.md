# MCP setup

## Local setup

Run MCP setup on demand with `uvx`.

```sh
uvx --from 'all-abt-ntu[cli,mcp,personal]@latest' ntu mcp setup
```

Choose a profile, tools, and clients. Setup registers `uvx` for on-demand runs or the absolute path to `ntu` for installed runs.

To start the public stdio server directly, run the following command.

```sh
uvx --from 'all-abt-ntu[mcp]@latest' ntu mcp --profile public
```

### Use an installed ntu

Install `ntu` with MCP support if you prefer to run the executable directly.

```sh
uv tool install 'all-abt-ntu[cli,mcp,personal]@latest'
ntu mcp setup
```

If you previously installed `ntu` with fewer extras, add `--force` to the install command. To launch the installed executable from an MCP client, use the alternate command in its configuration example below. If a client cannot find `ntu` on its `PATH`, use the absolute path to the executable.

To start the installed public server directly, run the following command.

```sh
ntu mcp --profile public
```

## Choose tools

Use `uvx` to list tool families or change which tools are enabled.

```sh
uvx --from 'all-abt-ntu[cli,mcp,personal]@latest' ntu mcp tools list
uvx --from 'all-abt-ntu[cli,mcp,personal]@latest' ntu mcp tools list --all
uvx --from 'all-abt-ntu[cli,mcp,personal]@latest' ntu mcp tools disable ntulearn
uvx --from 'all-abt-ntu[cli,mcp,personal]@latest' ntu mcp tools enable mazemap_get_directions
```

Run `setup` again to change your profile or family selection. `tools list` shows families, and `--all` shows individual tools. `[~]` means a family is partially enabled. Commands manage tools available in the active profile. Disabling a family also disables tools added to it later. Explicitly enabling a family enables all its tools in the active profile, including actions and downloads. You can disable individual tools afterward. Restart the MCP server after changes. Settings do not affect the hosted server.

With the installed executable, run the same subcommands directly, such as `ntu mcp tools list --all`.

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

Add this block to `~/.codex/config.toml`.

```toml
[mcp_servers.all-abt-ntu-mcp]
command = "uvx"
args = ["--from", "all-abt-ntu[mcp,personal]@latest", "ntu", "mcp"]
startup_timeout_sec = 120
tool_timeout_sec = 240
```

To launch an installed `ntu`, use these values in the same block.

```toml
command = "ntu"
args = ["mcp"]
```

On Linux, add this line to the same server block if it needs access to your desktop keyring.

```toml
env_vars = ["DBUS_SESSION_BUS_ADDRESS", "XDG_RUNTIME_DIR"]
```

For keyring-based sign-in, start Codex from a terminal where `ntu auth status` succeeds. NTULearn can also authenticate using a [validated cookie session](../services/ntulearn/index.md#sessions). Restart Codex and check `codex mcp list`.

Remove any fixed D-Bus address from the server block so `env_vars` can forward the current session when Codex starts.

## Claude Code

Register the server for your user.

```sh
claude mcp add --scope user all-abt-ntu-mcp \
  -- uvx --from 'all-abt-ntu[mcp,personal]@latest' ntu mcp
```

To use an installed `ntu`, register this command.

```sh
claude mcp add --scope user all-abt-ntu-mcp -- ntu mcp
```

Check `claude mcp list` or `/mcp` inside Claude Code. See [Claude Code's MCP guide](https://code.claude.com/docs/en/mcp) for details.

## OpenCode

Add this configuration to `~/.config/opencode/opencode.json` or `opencode.jsonc`. If both files exist, configure the active file manually.

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

To launch an installed `ntu`, use this `command` array.

```json
["ntu", "mcp"]
```

Check `opencode mcp list`. See [OpenCode's MCP guide](https://docs.opencode.ai/docs/mcp-servers/) for details.

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

Browser-based services need Playwright and its matching Chromium build. You can list personal MCP tools and use public tools before installing Chromium. If your client launches the server through `uvx`, install Chromium through the same package selection.

```sh
uvx --from 'all-abt-ntu[mcp,personal]@latest' playwright install chromium
```

If you installed `ntu` from PyPI, run setup and select Chromium installation.

```sh
ntu cli setup
```

For a repository checkout, include `--extra personal` in the appropriate `uv sync` command above, then run `uv run --no-sync playwright install chromium`. Playwright versions can require different Chromium builds, so repeat the matching command after upgrading. NTULearn can reuse an existing validated browser session for reads without launching Chromium.

## Run an HTTP server on localhost

To connect an MCP client using Streamable HTTP, start the public server from the repository root:

```sh
uv run uvicorn api.index:app --host 127.0.0.1 --port 8000
```

Configure the client with `http://127.0.0.1:8000/mcp` and select **Streamable HTTP**. The server listens only on this computer. This HTTP endpoint provides public tools; personal tools require the local stdio command above.

See the [configuration guide](configuration.md#configuration-file) for settings and environment variables.
