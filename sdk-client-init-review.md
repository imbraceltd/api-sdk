# SDK Client Initialization — Code Review Notes

## Context

The SDK is a **public package** that external users download and install. The client currently falls back to environment variables when the user doesn't provide config. This is fine for internal services, but wrong for a public SDK — users should be in full control of what they pass in.

---

## Rule of Thumb

> If it's a **credential or a URL override**, the user must pass it explicitly. The SDK must never silently read it from the environment.

---

## What to Change

### ❌ Remove these env var fallbacks

| Python (`client.py`) | TypeScript (`client.ts`) | Reason |
|---|---|---|
| `os.environ.get("IMBRACE_API_KEY")` | `env.IMBRACE_API_KEY` | Credential — must be explicit |
| `os.environ.get("IMBRACE_ACCESS_TOKEN")` | `env.IMBRACE_ACCESS_TOKEN` | Credential — must be explicit |
| `os.environ.get("IMBRACE_ENV")` | `env.IMBRACE_ENV` | Use hardcoded default `"stable"` instead |
| `os.environ.get("IMBRACE_GATEWAY_URL")` | `env.IMBRACE_GATEWAY_URL` | URL override — must be explicit |
| `os.environ.get("IMBRACE_PLATFORM_URL")` etc. | `env.IMBRACE_*_URL` | Per-service overrides — must be explicit via `services=` |

### ✅ Keep these

| Config | Why |
|---|---|
| `env = "stable"` as hardcoded default | Structural default, not a secret. User gets a working client without knowing internal env names. |
| `services=` / `gateway=` as explicit params | Already correct — user passes these intentionally. |
| `api_key=`, `access_token=`, `organization_id=` as explicit params | Already correct. |

---

## Expected Client Usage After Fix

**Python:**
```python
# ✅ Correct — user passes everything explicitly
client = ImbraceClient(
    api_key="sk-...",
    gateway="https://app-gateway.mycompany.com",
    organization_id="org_123",
)

# ✅ Also fine — user accepts "stable" default
client = ImbraceClient(api_key="sk-...")

# ❌ Should NOT silently work by reading IMBRACE_API_KEY from env
client = ImbraceClient()  # after fix: should warn and fail, not silently pull from env
```

**TypeScript:**
```typescript
// ✅ Correct
const client = new ImbraceClient({
  apiKey: "sk-...",
  gateway: "https://app-gateway.mycompany.com",
  organizationId: "org_123",
})

// ❌ Should NOT silently read process.env.IMBRACE_API_KEY
const client = new ImbraceClient()
```

---

## Specific Code Locations to Fix

### Python — `py/src/imbrace/client.py`

```python
# REMOVE these lines (lines ~69–84):
resolved_key = os.environ.get("IMBRACE_API_KEY")
resolved_env = env or os.environ.get("IMBRACE_ENV") or "stable"
resolved_gateway = base_url or gateway or os.environ.get("IMBRACE_GATEWAY_URL")

env_services = {}
for key in service_keys:
    env_val = os.environ.get(f"IMBRACE_{key.upper()}_URL")
    ...

# REPLACE with:
resolved_key = api_key  # None if not provided — that's fine, warn the user
resolved_env = env or "stable"
resolved_gateway = base_url or gateway  # None if not provided
merged_services = services or {}
```

Also remove the `import os` if it's no longer used elsewhere.

### TypeScript — `ts/src/client.ts`

```typescript
// REMOVE these lines (lines ~94–130):
const env = (globalThis as any).process?.env ?? {}
// ... all reads of env.IMBRACE_* variables

// REPLACE env resolution with:
const envName = opts?.env ?? 'stable'
const gatewayOverride = opts?.gateway
const resolvedApiKey = opts?.apiKey
const mergedServices = opts?.services ?? {}
```

---

## What the Warning Should Look Like After Fix

The "no credentials" warning is good — keep it. Just remove the env var fallback before it:

```
[ImbraceClient] No credentials provided. Pass accessToken= (user login) or apiKey= (server-to-server).
```

---

## Why This Matters

- A public SDK that silently reads `process.env` can **surprise users** — their app behaves differently depending on what env vars happen to be set on the machine.
- It makes the SDK **harder to test** — you need to manage env vars in addition to constructor args.
- Credentials in env vars are an internal deployment pattern, not something a public package should depend on.
