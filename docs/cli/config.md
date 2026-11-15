# MCP configuration commands

[Back to command catalog](commands.md)

- [`ntu config list`](#cmd-config-list)
- [`ntu config set`](#cmd-config-set)
- [`ntu config unset`](#cmd-config-unset)

## Command details

<a id="cmd-config-list"></a>
### `ntu config list`

Show the saved MCP environment settings.

#### Usage

```sh
ntu config list
```

#### Arguments and options

- `--help`, `-h`: Show help.

#### Notes

The output is JSON. These settings apply to MCP, not direct service commands.

<a id="cmd-config-set"></a>
### `ntu config set`

Set a supported MCP environment setting.

#### Usage

```sh
ntu config set ntulearn.headless false
```

#### Arguments and options

- `NAME`: **Required.** The dotted setting name, such as `ntulearn.headless`.
- `VALUE`: **Required.** The value to save in the setting’s expected format.
- `--help`, `-h`: Show help.

#### Notes

Restart the MCP server for changes to take effect. The configuration file is plain text and must not contain credentials.

<a id="cmd-config-unset"></a>
### `ntu config unset`

Remove a saved MCP environment setting.

#### Usage

```sh
ntu config unset ntulearn.headless
```

#### Arguments and options

- `NAME`: **Required.** The dotted setting name to remove.
- `--help`, `-h`: Show help.

#### Notes

After removal, the setting uses its default unless an environment variable overrides it. Restart the MCP server to apply the change.
