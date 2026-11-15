# Interfaces, resources and lifecycle

[Architecture overview](index.md) · [Security boundaries](security.md)

## From a command or tool to a service

The CLI and MCP expose different interfaces to the same service clients and operations:

1. A CLI command parses terminal arguments, calls the relevant service operation and renders the result. It does not connect to an MCP server.
2. An MCP client calls a registered tool. The server validates its inputs, applies the tool's policy and passes the call to the same service logic.
3. Service clients and workflows handle the upstream request, parsing, models and any applicable cache. Both synchronous and asynchronous operations are supported.

Service-specific MCP registrations live with their services. Public registrations and personal registrations are collected in `src/shared/catalog.py`; MCP policy, dependency binding and error translation live in `src/shared/mcp.py`.

## Resource ownership

`Application` in `src/application.py` owns service clients and sessions. Resources are created lazily on first use, so running a public operation does not require opening every personal session. The owner closes resources it created, including asynchronous sessions.

A direct CLI invocation normally creates one application and event loop, then closes them after the command. A local MCP server keeps its application for the server lifetime and closes it when the server stops. Individual services may have additional session and cache rules; their [service guides](../services/index.md) describe those details.

## Temporary workflow state

One Stop forms, appointment slots and checkout previews can contain process-local state. MCP clients can use the related tools while the same server process remains alive. The CLI instead provides standalone interactive commands for request applications, appointment bookings and cart checkout, keeping preparation and submission within one invocation. Temporary IDs should not be assumed to survive a restart.

## Configuration

Direct CLI commands use service defaults and environment variables. MCP profile, tool selection and saved MCP settings apply to the server. Credentials are shared through the native OS keyring rather than stored in the MCP configuration file. See [MCP configuration](../mcp/configuration.md) and [Credentials and keyring access](credentials.md).
