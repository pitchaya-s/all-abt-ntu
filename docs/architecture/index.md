# Architecture

All About NTU has two interfaces over the same NTU service logic. The CLI runs operations directly, while the MCP server registers them as tools for an AI client. Neither interface needs to start the other.

```text
                 NTU service logic
                  /            \
             CLI                 MCP
       terminal commands    local or hosted server
```

The application creates clients and sessions when they are needed. Public and personal access, confirmation, caching and cleanup are handled at their respective boundaries. For the source tree and checks, see [Development](../development.md) and [Testing](../testing.md).

- [Interfaces, resources and lifecycle](interfaces.md)
- [Profiles, confirmation and security boundaries](security.md)
- [Credentials and Linux keyring access](credentials.md)
- [Public HTTP reads, caching and request limits](public-http.md)
- [Hosted public MCP server and HTTP tests](../mcp/hosting.md)
