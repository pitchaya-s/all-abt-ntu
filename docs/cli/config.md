# Service configuration commands

[Back to command catalog](commands.md)

- [`ntu config list`](#cmd-config-list)
- [`ntu config set`](#cmd-config-set)
- [`ntu config unset`](#cmd-config-unset)

## Command details

<a id="cmd-config-list"></a>
### `ntu config list`

Show saved service settings as JSON.

#### Usage

```sh
ntu config list
```

#### Arguments and options

- `--help`, `-h`: Show help.

#### Notes

The CLI and local MCP server share [service settings](../mcp/configuration.md). MCP profiles and tool selection are managed separately with `ntu mcp`.

<a id="cmd-config-set"></a>
### `ntu config set`

Set a service setting for the CLI and local MCP server.

#### Usage

```sh
ntu config set ntulearn.headless false
```

#### Arguments and options

- `NAME`: **Required.** The dotted setting name, such as `ntulearn.headless`.
- `VALUE`: **Required.** The value to save in the setting’s expected format.
- `--help`, `-h`: Show help.

#### Notes

Changes apply to the next CLI command. Restart the MCP server to apply them there. An explicit environment variable takes precedence. Keep credentials out of the configuration file.

<a id="cmd-config-unset"></a>
### `ntu config unset`

Remove a saved service setting.

#### Usage

```sh
ntu config unset ntulearn.headless
```

#### Arguments and options

- `NAME`: **Required.** The dotted setting name to remove.
- `--help`, `-h`: Show help.

#### Notes

After removal, the setting uses its default unless an environment variable overrides it. Restart the MCP server to apply the change.
