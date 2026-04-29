## Installation

### Install

**TypeScript:**
```bash
npm install @imbrace/sdk@1.0.2
# or
yarn add @imbrace/sdk@1.0.2
# or
pnpm add @imbrace/sdk@1.0.2
```

Requires Node.js 18+ (or any browser with native `fetch` and `ReadableStream`).

**Python:**
```bash
pip install imbrace==1.0.2
# or
uv add imbrace==1.0.2
```

Requires Python 3.9+.

### Initialize the client

**Build on Imbrace (Access Token) — TypeScript:**
```typescript
import { ImbraceClient } from "@imbrace/sdk"

// Build on Imbrace — Imbrace IS your backend, end-users log in via OTP
const client = new ImbraceClient({
  accessToken: "acc_your_token",
  baseUrl: "https://app-gatewayv2.imbrace.co",
})
```

The client is stateful — create it once and reuse it across your app.

**Build on Imbrace (Access Token) — Python:**
```python
from imbrace import ImbraceClient

# Build on Imbrace — Imbrace IS your backend, end-users log in via OTP
with ImbraceClient(access_token="acc_your_token") as client:
    ...
```

Python also exports `AsyncImbraceClient` (`async with ...`) for async stacks like FastAPI.

The context manager closes the underlying HTTP connection pool automatically.

**Wrap Imbrace (API Key) — TypeScript:**
```typescript
import { ImbraceClient } from "@imbrace/sdk"

// Wrap Imbrace — Imbrace is a feature inside YOUR backend, your users
const client = new ImbraceClient({
  apiKey: "api_xxx...",
  baseUrl: "https://app-gatewayv2.imbrace.co",
})
```

The client is stateful — create it once and reuse it across your app.

**Wrap Imbrace (API Key) — Python:**
```python
from imbrace import ImbraceClient

# Wrap Imbrace — Imbrace is a feature inside YOUR backend, your users
with ImbraceClient(api_key="api_xxx...") as client:
    ...
```

Python also exports `AsyncImbraceClient` (`async with ...`) for async stacks like FastAPI.

The context manager closes the underlying HTTP connection pool automatically.

For when to use each credential, see [Authentication](/sdk/authentication/). For step-by-step credential setup (env vars, dotenv, secrets), see [Setup Guide](/getting-started/setup/#configure-credentials).

### Verify

**TypeScript:**
```typescript
import { ImbraceClient } from "@imbrace/sdk"
console.log("SDK loaded:", typeof ImbraceClient) // "function"
```

**Python:**
```python
from imbrace import ImbraceClient
print("SDK ready:", ImbraceClient)
```

### Environment variables

The SDK does **not** auto-read environment variables. Pass credentials directly to the constructor and use a loader (`dotenv` / your framework's env handling) if you keep them in `.env`.

| Variable | Purpose |
|---|---|
| `IMBRACE_API_KEY` | Your API key (org-level credential) |
| `IMBRACE_ACCESS_TOKEN` | A user's access token (per-session credential) |
| `IMBRACE_BASE_URL` | Override the gateway URL (default: `https://app-gatewayv2.imbrace.co`) |

The org id is encoded inside both API keys and access tokens — you never pass `organizationId`/`organization_id` to the SDK. See [Authentication](/sdk/authentication/) for details.
