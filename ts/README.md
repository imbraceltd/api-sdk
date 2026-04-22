# Imbrace TypeScript SDK

Official TypeScript/JavaScript client for the Imbrace Gateway.

## Installation

```bash
npm install @imbrace/sdk
```

## Quick Start

### API Key — server-side scripts, cron jobs

```typescript
import { ImbraceClient } from "@imbrace/sdk"

const client = new ImbraceClient({
  apiKey: process.env.IMBRACE_API_KEY,
})

const me = await client.platform.getMe()
```

### Access Token — after user login

```typescript
const client = new ImbraceClient({
  accessToken: "acc_xxxxxxxxxxxxx",
})
```

### OTP Login Flow

```typescript
const client = new ImbraceClient()

await client.requestOtp("user@example.com")
await client.loginWithOtp("user@example.com", "123456")

// all subsequent calls are authenticated
const me = await client.platform.getMe()
```

## Error Handling

```typescript
import { AuthError, ApiError, NetworkError } from "@imbrace/sdk"

try {
  await client.platform.getMe()
} catch (e) {
  if (e instanceof AuthError)    console.error("Invalid credentials")
  if (e instanceof ApiError)     console.error(`[${e.statusCode}] ${e.message}`)
  if (e instanceof NetworkError) console.error("Gateway unreachable")
}
```

## Environment Variables

| Variable | Description |
| --- | --- |
| `IMBRACE_API_KEY` | API key (server-side auth) |
| `IMBRACE_GATEWAY_URL` | Override gateway URL (default: `https://app-gatewayv2.imbrace.co`) |
| `IMBRACE_ENV` | Environment preset: `develop`, `sandbox`, `stable` (default: `stable`) |

## Build

```bash
npm run build      # compile to dist/
npm run typecheck  # type-check only
npm run test       # run unit tests
```

## Resources

Full resource reference: **[sdk.imbrace.co/typescript/resources](https://sdk.imbrace.co/typescript/resources)**
