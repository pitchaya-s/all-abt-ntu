# MCP management commands

[Back to command catalog](commands.md)

- [`ntu mcp`](#cmd-mcp)
- [`ntu mcp setup`](#cmd-mcp-setup)
- [`ntu mcp tools list`](#cmd-mcp-tools-list)
- [`ntu mcp tools enable`](#cmd-mcp-tools-enable)
- [`ntu mcp tools disable`](#cmd-mcp-tools-disable)

## Command details

<a id="cmd-mcp"></a>
### `ntu mcp`

Start the local MCP server over stdio. It runs until its client disconnects.

#### Usage

```sh
ntu mcp --profile public
```

#### Arguments and options

- `--profile`: Select `public` or `personal`. Omit it to use the saved profile.
- `--help`, `-h`: Show server options.

#### Notes

The server communicates over stdin and stdout. The hosted server is configured separately and exposes public, read-only tools.

<a id="cmd-mcp-setup"></a>
### `ntu mcp setup`

Choose a profile, enabled tool families and clients to configure.

#### Usage

```sh
ntu mcp setup
```

#### Arguments and options

- `--help`, `-h`: Show setup help.

#### Notes

Setup requires an interactive terminal. It may offer Chromium installation and keyring authentication for personal tools. Existing client configuration is handled as described in [MCP setup](../mcp/index.md).

<a id="cmd-mcp-tools-list"></a>
### `ntu mcp tools list`

List tool families and their enabled status.

#### Usage

```sh
ntu mcp tools list --all
```

#### Arguments and options

- `--all`: Show individual tools rather than only families.
- `--help`, `-h`: Show help.

#### Notes

The command uses the saved profile unless a profile is selected before `tools`.

<a id="cmd-mcp-tools-enable"></a>
### `ntu mcp tools enable`

Enable named tool families or individual tools for the active profile.

#### Usage

```sh
ntu mcp tools enable stars
```

#### Arguments and options

- `NAMES...`: One or more family or tool names.
- `--help`, `-h`: Show help.

#### Notes

Enabling an entire family can enable its actions and downloads. Use `ntu mcp tools list --all` to inspect individual tools.

<a id="cmd-mcp-tools-disable"></a>
### `ntu mcp tools disable`

Disable named tool families or individual tools for the active profile.

#### Usage

```sh
ntu mcp tools disable news
```

#### Arguments and options

- `NAMES...`: One or more family or tool names.
- `--help`, `-h`: Show help.

#### Notes

Restart the MCP server after changing tool selections.
