# Profiles, confirmation and security boundaries

[Architecture overview](index.md) · [Credentials and keyring access](credentials.md)

## Local profiles

The local MCP server supports a **public** profile and a **personal** profile. The personal profile adds authenticated operations. Tool-family and individual-tool settings can further restrict what the server exposes; personal actions and downloads start disabled unless explicitly enabled. These MCP settings do not restrict direct CLI commands.

The hosted HTTP server registers only public, read-only tools. It does not accept NTU credentials or register personal operations. See [Hosted public MCP server](../mcp/hosting.md) for deployment boundaries and request limits.

## Confirmation and uncertain outcomes

CLI actions and downloads request confirmation locally and refuse to proceed if interactive confirmation cannot be obtained. MCP operations that require confirmation ask the MCP client through the server's confirmation mechanism. The user must trust the client to present those requests appropriately.

Some upstream actions can fail after the remote service has received a request. When the outcome is uncertain, inspect the current state before retrying rather than assuming the action failed. One Stop workflows and STARS plan saving document their own verification behavior in the relevant service guides.

## Credentials and external data

Credentials are opt-in and stored in the native OS keyring. Passwords are not accepted through tool arguments or the configuration file. Authentication challenges, MFA and CAPTCHA remain part of the upstream login flow; the application does not bypass them.

An AI client can see personal information returned by tools it is allowed to call. Published pages, article text and other upstream content are data supplied by external services, not instructions to the client. The public HTTP client applies host restrictions and bounded request handling described in [Public HTTP reads](public-http.md).

On POSIX systems, NTULearn and One Stop create new download files with owner-only permissions. The files inherit applicable directory access and local filesystem rules. Use a private directory for downloaded personal data.
