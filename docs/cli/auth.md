# Authentication commands

[Back to command catalog](commands.md)

- [`ntu auth save`](#cmd-auth-save)
- [`ntu auth status`](#cmd-auth-status)
- [`ntu auth delete`](#cmd-auth-delete)

## Command details

<a id="cmd-auth-save"></a>
### `ntu auth save`

Prompt for an NTU account and save it in the native OS keyring.

#### Usage

```sh
ntu auth save
```

#### Arguments and options

- `--help`, `-h`: Show help.

#### Notes

Use an interactive local terminal. The password is hidden while typing and is not accepted as a command argument. Running this again replaces the saved account.

<a id="cmd-auth-status"></a>
### `ntu auth status`

Check whether credentials are stored in the native keyring.

#### Usage

```sh
ntu auth status
```

#### Arguments and options

- `--help`, `-h`: Show help.

#### Notes

This checks credential storage without revealing the account or password; it does not verify a service login.

<a id="cmd-auth-delete"></a>
### `ntu auth delete`

Remove the saved NTU credentials from the native keyring.

#### Usage

```sh
ntu auth delete
```

#### Arguments and options

- `--help`, `-h`: Show help.

#### Notes

The command requires local confirmation.
