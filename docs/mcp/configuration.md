# MCP configuration

## Configuration file


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

For a PyPI install, use the same `uvx --from 'all-abt-ntu-mcp[cli,mcp,personal]@latest'` prefix as in [local setup](index.md#local-setup) instead of `uv run`. The supported settings under `env` are:


| Group         | Settings                                                                                                                 |
| ------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `stars`       | `cache_ttl_seconds`, `personal_cache_ttl_seconds`                                                                        |
| `ntulearn`    | `cache_ttl_seconds`, `headless`, `browser_cookies`, `request_concurrency`, `request_interval_seconds`, `timeout_seconds` |
| `careeraxis`  | `cache_ttl_seconds`, `headless`                                                                                          |
| `onestop`     | `upload_dir`                                                                                                             |
| `public_http` | `concurrency`, `interval_seconds`, `timeout_seconds`, `max_retry_delay_seconds`                                          |
| `browser`     | `browsers_path` for Playwright                                                                                           |


Use JSON booleans for switches, numbers for durations and limits, and strings for paths. Other environment variables can be stored under `env.other`, for example with `config set other.CUSTOM_SETTING value`. Configuration-location variables such as `XDG_CONFIG_HOME` must be set outside the file. Process environment variables take precedence over saved settings. Restart the server after changing settings. This file is plain text; use the keyring for credentials.
