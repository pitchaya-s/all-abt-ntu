# Testing

## Tests

Personal-data, map, repository, library, faculty, news, and service fixtures are synthetic. Timetable fixtures use fictional course labels and indexes while retaining the HTML structures needed for parser tests. Opt-in live tests print counts and statuses; they do not save academic records or learning materials in the repository.

The offline tests cover keyring storage and failure handling, local credential prompts, session recovery, parsing, scheduling, lossless compaction, output-schema validation, tool calls/errors, and resource discovery. Protocol tests use Python SDK clients and an independent JSON-RPC client over stdio, including protocol versions `2025-06-18` and `2025-11-25`:

```sh
uv run python -m unittest discover -s tests -t . -v
```

An optional check uses the official TypeScript SDK. Node dependencies stay in a temporary directory:

```sh
NTU_MCP_TEST_SDK="$(mktemp -d)"
npm install --prefix "$NTU_MCP_TEST_SDK" --ignore-scripts --no-audit --no-fund @modelcontextprotocol/sdk@1.32.1
uv run node tests/mcp/typescript_smoke.mjs "$NTU_MCP_TEST_SDK"
```

These interoperability checks use offline fixtures and never edit saved plans.

Hosted HTTP checks cover public-only registration, rejected personal calls, output schemas, both modern and legacy Python SDK clients, Host/Origin validation, request-size limits, and independent serverless event loops. See the [HTTP test instructions](mcp/hosting.md#http-tests) for the TypeScript client and opt-in live smoke.

Live checks and service-specific testing instructions: [STARS](services/stars/index.md#tests) · [NTULearn](services/ntulearn/index.md#tests) · [CareerAxis](services/careeraxis/index.md#validation) · [MazeMap](services/mazemap/index.md#tests) · [DR-NTU](services/drntu/index.md#tests) · [Library](services/library/index.md#tests) · [Faculty](services/faculty/index.md#tests) · [News](services/news/index.md#tests) · [Campus services](services/campus-services/index.md#tests) · [NTU Omnibus](services/omnibus/index.md#checks) · [One Stop @ SAC](services/one-stop/index.md#coverage-runtime-and-checks).

## Read-only authenticated smoke tests

From the repository root, install with `uv sync --locked --extra cli --extra mcp --extra personal` and use your own [configured keyring](architecture/credentials.md). On Linux, launch from the desktop session so the process inherits its D-Bus address. Run one service at a time:

```sh
uv run --no-sync python -m tests.live_personal learn --authenticated
uv run --no-sync python -m tests.live_personal career --authenticated
uv run --no-sync python -m tests.live_personal library --authenticated
uv run --no-sync python -m tests.live_personal onestop --authenticated
uv run --no-sync python -m tests.stars.live_personal_smoke
```

The probes check advertised MCP schemas and sample service data, keep private records in memory, and report statuses or counts. They are outside the deterministic unittest suite and public CI. If sign-in reports an interactive challenge or a rejection, resolve it through the normal NTU sign-in flow before trying again. The longer NTULearn download smoke tests use temporary directories.
