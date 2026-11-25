# Credentials and keyring access

## Credential storage

Storage is opt-in. Run `ntu auth save` yourself in a local terminal; the username is visible and the password is hidden while typing. Piped input and terminals that cannot hide password input are refused. Credentials are stored encrypted in the native OS keyring and never included in MCP responses sent to the LLM. Running the command again replaces the saved account/password. `auth status` reports whether an account is stored, and `auth delete` removes it. With uvx, use a package specification containing the `cli` extra for authentication commands; no standalone CLI installation is needed. No credential management commands are exposed as MCP tools.

The keyring entry uses service `all-abt-ntu-mcp`, account `ntu-account`. The username, password, and an opaque revision identifier are stored together as the keyring secret. Neither credential is stored in application files, environment variables, or logs, or returned through MCP. Configuration from older versions is not imported automatically; remove any old credentials from `.env` and client settings yourself. A network username is expanded to a student email address for NTULearn; a full NTU email is used as supplied.

Storage uses Python's [keyring library](https://keyring.readthedocs.io/en/latest/) with an allowlist of native Secret Service/KWallet, macOS Keychain, and Windows Credential Manager backends. Plaintext, custom, null, and non-native backends are rejected. A chained backend is used only through its selected native member, without fallback to other members after failure. Unlock the wallet/keychain through its normal OS interface. Locked or unavailable stores return a sanitized error; public tools remain available.

Authenticated services check saved credentials before keyring-based login and personal reads. Replacing the entry clears an affected service's old session and cache on its next personal operation. Deleting it or losing access to the keyring prevents the next keyring-based login. NTULearn can also authenticate without the keyring by using a browser cookie or a cookie in the process environment. See the [NTULearn sign-in order](../services/ntulearn/index.md#sessions).

Academic data returned through MCP is visible to the AI client. Credentials and session cookies are excluded from responses. Python/browser memory is not guaranteed to be zeroized. OS keyring permissions govern access by other local processes; keyring storage does not isolate secrets from an agent that can execute arbitrary code as your user.

## Linux keyring access

Linux requires a running Secret Service or KWallet service. Keyring's direct KWallet backend additionally needs `dbus-python` in the same Python environment; KWallet can also provide a Secret Service interface. Some Linux installations need a keyring provider installed and configured first.

If terminal `auth status` works but the MCP does not, forward `DBUS_SESSION_BUS_ADDRESS` and `XDG_RUNTIME_DIR` through the client's MCP configuration and restart the client from that same terminal. Codex setup configures forwarding on Linux; see the [MCP setup guide](../mcp/index.md#codex) for manual configuration. Do not hardcode another user's bus address or start a separate D-Bus session for the MCP.

If `busctl --user list` cannot connect, point the current shell at its desktop session bus before checking credentials or launching the MCP client:

```sh
export XDG_RUNTIME_DIR="/run/user/$(id -u)"
export DBUS_SESSION_BUS_ADDRESS="unix:path=$XDG_RUNTIME_DIR/bus"
busctl --user list
uv run ntu auth status
```

The keyring service must appear in the bus listing, and `auth status` must report the account as stored. Restart the MCP client from this corrected session so it inherits the same bus address.

In authentication tool results, `credentials_configured` is `true` when the account is readable, `false` when the keyring is readable but has no account, and `null` when storage cannot be read. A keyring error does not establish that credentials are missing.
