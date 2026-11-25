# Interfaces, resources and lifecycle

[Architecture overview](index.md) · [Security boundaries](security.md)

## From a command or tool to a service

The CLI and MCP expose different interfaces to the same service clients and operations:

1. A CLI command parses terminal arguments, calls the relevant service operation and renders the result. It does not connect to an MCP server.
2. An MCP client calls a registered tool. The server validates its inputs, applies the tool's policy and passes the call to the same service logic.
3. Service clients and workflows handle the upstream request, parsing, models and any applicable cache. Both synchronous and asynchronous operations are supported.

## Resource ownership

The CLI closes connections when the command finishes. A local MCP server can reuse connections while it runs and closes them when it stops. See the [service guides](../services/index.md) for session and cache behavior.

## Temporary workflow state

One Stop forms, appointment slots and checkout previews can contain process-local state. MCP clients can use the related tools while the same server process remains alive. The CLI instead provides standalone interactive commands for request applications, appointment bookings and cart checkout, keeping preparation and submission within one invocation. Temporary IDs should not be assumed to survive a restart.

## Configuration

Direct CLI commands and local MCP share saved service settings. Process environment values take precedence. The MCP profile and tool selection apply to the local MCP server. Credentials are stored in the native OS keyring. See [MCP configuration](../mcp/configuration.md) and [Credentials and keyring access](credentials.md).
