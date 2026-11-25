# Hosted public MCP server

## Hosted public server

The Vercel entrypoint is the file-based function `api/index.py`. `vercel.json` selects the **Other** framework preset and rewrites requests to that function, which creates the ASGI app in top-level `public_http_server.py`. Top-level `public_server.py` registers public tool modules, and `server.py` runs local public or personal stdio profiles. The public import path does not load authenticated sessions, personal handlers, or NTULearn.

The HTTP endpoint is `/mcp`, using stateless Streamable HTTP with JSON responses and a 1 MB request limit. Each request manages its own SDK lifecycle, so it works when the host omits ASGI lifespan events or changes event loops between requests. No server session identifier, sticky routing, database, or credentials are required. GET/DELETE on `/mcp` return 405 because there is no persistent event stream or session to delete. `/` and `/health` return public status information.

`vercel.json` selects Singapore and a 300-second function duration. Import the repository root with framework preset **Other**, keeping build/install overrides unset. The default `hosted` dependency group installs the MCP extra when Vercel runs `uv sync --no-dev`, without the CLI extra. No environment variables are needed for the default Vercel domains. The app builds its Host/Origin allowlist from `VERCEL_URL`, `VERCEL_PROJECT_PRODUCTION_URL`, and `VERCEL_BRANCH_URL`. For a custom domain, add its bare hostname to `MCP_ALLOWED_HOSTS` in Vercel, then redeploy. Multiple hostnames can be comma-separated; schemes, paths, ports, and wildcards are rejected. Native MCP clients do not need browser CORS access; cross-origin browser clients are not enabled.

Use a publicly accessible deployment URL. Vercel Deployment Protection can require platform sign-in independently of this app.

`.vercelignore` excludes local secrets, browser artifacts, tests, caches, and build output from uploads. No keyring entry or NTU account should be configured on Vercel. Public source caches and request pacing remain bounded per process; caches may disappear on cold starts and are not a shared rate limit across replicas. Configure platform traffic controls if exposing the endpoint to substantial public traffic.

The hosted process also limits each high-fan-out tool to 10 calls per minute across all callers handled by that process. This is an additional upstream safeguard, not a per-client or deployment-wide limit: cold starts and replicas have independent counters. A gateway rule must provide the deployment-wide per-client limit.

Public HTTP clients log a warning containing the service name when an upstream returns HTTP 429; no request URL or query is included in that warning. Configure a log alert on `upstream returned HTTP 429` and investigate sustained rate limiting.

## HTTP tests

From the repository root:

```sh
uv run python -m unittest tests.hosted.test_http -v
uv run uvicorn api.index:app --host 127.0.0.1 --port 8000
```

In another terminal, the opt-in smoke makes a few public NTU reads:

```sh
uv run python -m tests.hosted.live_smoke http://127.0.0.1:8000/mcp
```

Replace that URL with the Vercel `/mcp` URL to verify a deployment. This repository preparation does not deploy or connect a Vercel project.

For an offline TypeScript SDK check, install the SDK in a temporary npm prefix as described in [Development and testing](../testing.md#tests). Start the synthetic HTTP server instead of the live app:

```sh
uv run uvicorn tests.hosted.protocol_server:app --host 127.0.0.1 --port 8001
```

Then run:

```sh
uv run node tests/hosted/typescript_smoke.mjs "$NTU_MCP_TEST_SDK" http://127.0.0.1:8001/mcp
```

Deployment references: [Vercel file-based Python functions](https://vercel.com/docs/functions/runtimes/python/api-directory) and [MCP HTTP deployment guidance](https://py.sdk.modelcontextprotocol.io/run/deploy/).
