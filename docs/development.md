# Development and testing

## Documentation

Documentation is maintained in `docs/` alongside the code. Preview it locally or check the production build with:

```sh
uvx --from mkdocs==1.6.1 mkdocs serve
uvx --from mkdocs==1.6.1 mkdocs build --strict
```

The GitHub Actions workflow builds the site and deploys it to GitHub Pages when documentation changes reach `main`. To enable publishing, choose **GitHub Actions** under the repository's **Settings → Pages → Build and deployment**. The workflow can also be run manually from the default branch.

## Source layout

```text
src/
├── cli/                    CLI commands, dispatch, and rendering
├── application.py          Lazy service resources and cleanup
├── server.py               Local public/personal stdio server
├── public_server.py        Public tool registry
├── public_http_server.py   Hosted ASGI app and transport security
├── public_http_client.py   Pooled public HTTP client
├── shared/                 Operation catalog, MCP adapter, credentials, and shared helpers
├── stars/
│   ├── tools/               Academic, personal, and teaching-room tool groups
│   ├── schemas/             Course and room tool schemas
│   ├── domain/             Course models, timetable matching and room searches
│   ├── client/             Public NTU requests and caching
│   ├── parser/             Schedule and personal-page parsing
│   └── wish/               WISH login and saved-plan editing
├── ntulearn/
│   ├── mcp.py       Shared NTULearn operations and input schemas
│   ├── models/             Typed responses grouped by domain
│   ├── client/             Login, sessions, and REST requests
│   ├── parser/             Response and document parsing
│   └── services/           Content, files, mailbox, people, and activity
├── careeraxis/
│   ├── mcp.py       Authenticated CareerAxis operations
│   ├── client.py            Section searches and record detail requests
│   ├── browser/             ADFS login, browser session, and page snapshots
│   ├── parser.py            Rendered section and record normalization
│   └── models.py            Search, detail, and auth status responses
├── mazemap/
│   ├── mcp.py       Public map operations and input schemas
│   ├── models.py           Typed place and direction responses
│   ├── client.py           HTTP requests, pacing, and caching
│   └── parser.py           Place and route normalization
├── drntu/
│   ├── mcp.py       Public repository operations and schemas
│   ├── models.py           Shared metadata, snapshots, and errors
│   ├── rest/               DSpace search, files, and Dataverse datasets
│   └── oai/                OAI-PMH client, parser, models, and service
├── library/
│   ├── mcp.py       Public library operations and schemas
│   ├── personal_tools.py    Local authenticated facility tool
│   ├── models.py           Catalogue, access and facility responses
│   ├── client.py           OneSearch requests and pagination
│   ├── facilities/         Directory, map availability, browser, and schedules
│   └── parser.py           Primo record normalization
├── faculty/
│   ├── mcp.py       Public faculty operations and input schemas
│   ├── models.py           Typed profile and research-interest responses
│   ├── client.py           Directory requests, filters, and pagination
│   └── parser.py           Profile cards and interest form parsing
├── news/
│   ├── mcp.py       Public news operations and input schemas
│   ├── models.py           Typed story, category, and article responses
│   ├── client.py           News search and bounded article retrieval
│   └── parser.py           Story cards and article body extraction
├── service/
│   ├── mcp.py       Public campus service operations and input schemas
│   ├── models.py           Typed location and filter responses
│   ├── client.py           Complete directory collection and local search
│   └── parser.py           Contact, hours, and map normalization
├── omnibus/                Public shuttle and LTA stops, positions, arrivals and schedules
└── onestop/                Local ServiceNow reads and native workflows
    ├── services/           Catalog, form, ticket, cart, knowledge, and portal workflows
    └── attachments/        Verified attachment actions and safe local-file handling
tests/
├── cli/                    CLI commands, setup, and authentication
├── mcp/                    MCP profiles, confirmation, and SDK interoperability
├── shared/                 Credentials, caching, HTTP, and application lifecycle
├── hosted/                 Public HTTP protocol, isolation, and deployment checks
├── careeraxis/             CareerAxis tests and synthetic fixtures
├── drntu/                  DR-NTU tests and synthetic fixtures
├── faculty/                Faculty directory tests and synthetic fixtures
├── library/                OneSearch and LibFacilities tests and fixtures
├── mazemap/                MazeMap tests and synthetic fixtures
├── news/                   News search and article tests with synthetic fixtures
├── ntulearn/               NTULearn tests and synthetic fixtures
├── omnibus/                Shuttle tests and synthetic fixtures
├── onestop/                One Stop workflows and upload safety
├── service/                Campus directory tests and synthetic fixtures
└── stars/                  STARS tests and fictionalized fixtures
```

See [Testing](testing.md) for unit, protocol and live-check instructions.
