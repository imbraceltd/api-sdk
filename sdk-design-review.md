# SDK Design Review — Issues for Junior Dev

Work through these in priority order. Each issue includes the bad code, where it lives, and exactly how to fix it.

---

## 🔴 Issue 1 — Vietnamese docstrings and comments

Public SDK docstrings must be in English. Any developer who installs this package cannot read Vietnamese.

**Reference code:**

`py/src/imbrace/client.py` lines 161, 169, 177:
```python
def login(self, email: str, password: str) -> dict:
    """Login bằng email/password, tự lưu access token vào client."""

def login_with_otp(self, email: str, otp: str) -> dict:
    """Login bằng OTP (sau khi gọi request_otp), tự lưu access token."""

def request_otp(self, email: str) -> None:
    """Gửi OTP về email. Dùng trước login_with_otp()."""
```

`py/src/imbrace/http.py` lines 106, 113, 204:
```python
def iterate_paged(...) -> Iterator[T]:
    """Tự động duyệt qua tất cả các trang của một API phân trang."""
    ...
    # Giả định cấu hình PagedResponse: { data: [...], pagination: { has_next: bool } }

async def iterate_paged(...) -> AsyncIterator[T]:
    """Tự động duyệt qua tất cả các trang (bất đồng bộ)."""
```

`ts/src/client.ts` lines 42–54 (JSDoc fields) and lines 113, 149, 168, 176 (inline comments):
```typescript
/** Login bằng email/password, tự lưu access token vào client. */
accessToken?: string
/** Gửi kèm header x-organization-id trên mọi request */
organizationId?: string
/** Ping /global/health khi gọi init(). Default: false */
checkHealth?: boolean

// Ưu tiên: code opts > process.env > default 'stable'
// ── Wire resources với per-service base URL ──────────────────
// Workflows cần cả channel-service và platform (n8n)
// Marketplace cần cả marketplaces service và platform/v2/marketplaces
```

Also in `py/src/imbrace/async_client.py` lines 140, 148, 156 — same Vietnamese docstrings as sync client.

**Fix:** Replace all with English.

```python
# py/src/imbrace/client.py
def login(self, email: str, password: str) -> dict:
    """Sign in with email and password. Stores the returned access token on the client."""

def login_with_otp(self, email: str, otp: str) -> dict:
    """Sign in with an OTP code (call request_otp() first). Stores the returned access token."""

def request_otp(self, email: str) -> None:
    """Send a one-time password to the given email address."""

# py/src/imbrace/http.py
def iterate_paged(...) -> Iterator[T]:
    """Iterate over all pages of a paginated endpoint, yielding one item at a time."""
    ...
    # Expected response shape: { data: [...], pagination: { has_next: bool } }
```

```typescript
// ts/src/client.ts
/** User access token (client-side OAuth/JWT). */
accessToken?: string
/** Sent as x-organization-id on every request. */
organizationId?: string
/** Ping /global/health on init(). Default: false */
checkHealth?: boolean

// Priority: explicit opts > default 'stable'
// Wire each resource to its per-service base URL
// Workflows need both channel-service (automations) and platform (n8n)
// Marketplace needs both marketplace service and platform/v2/marketplaces
```

---

## 🔴 Issue 2 — Silent env var fallback for credentials

Both clients fall back to reading credentials from environment variables when none are passed. This is wrong for a public SDK — the user who installs the package should never have their app behave differently based on what env vars happen to be set.

**Reference code:**

`py/src/imbrace/client.py` lines 66–84 (identical in `async_client.py` lines 59–77):
```python
if api_key is not None:
    resolved_key = api_key
elif access_token is None:
    resolved_key = os.environ.get("IMBRACE_API_KEY")   # ← reads secret from env
else:
    resolved_key = None
resolved_env = env or os.environ.get("IMBRACE_ENV") or "stable"
resolved_gateway = base_url or gateway or os.environ.get("IMBRACE_GATEWAY_URL")

env_services = {}
service_keys = ["platform", "channel_service", "ips", "data_board", "ai", "marketplaces"]
for key in service_keys:
    env_val = os.environ.get(f"IMBRACE_{key.upper()}_URL")   # ← reads URLs from env
    if env_val:
        env_services[key] = env_val
```

`ts/src/client.ts` lines 94–129:
```typescript
const env = (globalThis as any).process?.env ?? {}
// ... then reads env.IMBRACE_API_KEY, env.IMBRACE_ENV,
//     env.IMBRACE_GATEWAY_URL, env.IMBRACE_*_URL throughout
const resolvedApiKey = opts?.apiKey !== undefined
  ? opts.apiKey
  : opts?.accessToken !== undefined
    ? undefined
    : (env.IMBRACE_API_KEY as string | undefined)   // ← reads secret from env
```

**Fix:** Remove all `os.environ.get` / `process.env` reads. Only use what the user explicitly passes. Keep `"stable"` as a hardcoded default for `env` since it's structural (not a secret).

```python
# py/src/imbrace/client.py — replace the resolution block with:
resolved_key = api_key          # None if not provided — warning handles it below
resolved_env = env or "stable"  # hardcoded default only, no env var
resolved_gateway = base_url or gateway  # None if not provided
merged_services = services or {}

# remove import os if no longer used elsewhere
```

```typescript
// ts/src/client.ts — replace the env resolution block with:
const envName = opts?.env ?? 'stable'
const gatewayOverride = opts?.gateway
const resolvedApiKey = opts?.apiKey
const mergedServices = opts?.services ?? {}

// remove: const env = (globalThis as any).process?.env ?? {}
// remove: all env.IMBRACE_* reads
```

---

## 🔴 Issue 3 — TokenManager exported publicly

`TokenManager` is an internal implementation detail. It should never appear in the public API surface.

**Reference code:**

`ts/src/index.ts` line 6:
```typescript
export * from "./auth/token-manager.js"   // ← exposes internal class
```

**Fix:** Remove that line. Users interact with tokens via `client.setAccessToken()` and `client.clearAccessToken()` — they never need to touch `TokenManager` directly.

```typescript
// ts/src/index.ts — remove:
export * from "./auth/token-manager.js"
```

---

## 🔴 Issue 4 — Backend typo leaked into public API

The backend endpoint has a typo (`thrid` instead of `third`). The URL path is internal and hidden from users, but the comment calls it out explicitly and preserves it — that's fine. The risk is the comment itself misleads future developers into thinking the SDK intentionally has a typo.

**Reference code:**

`py/src/imbrace/resources/auth.py` lines 26–31:
```python
def get_third_party_token(self, expiration_days: int = 10) -> Dict[str, Any]:
    # Requires active access token. "thrid" is a backend typo — preserved intentionally.
    return self._http.request(
        "POST",
        f"{self._gateway}/private/backend/v1/thrid_party_token",   # ← typo in URL
        json={"expirationDays": expiration_days},
    ).json()
```

`ts/src/resources/auth.ts` lines 28–38:
```typescript
async getThirdPartyToken(expirationDays: number = 10): Promise<ThirdPartyTokenResponse> {
  // Requires active access token. "thrid" is a backend typo — preserved intentionally.
  const gatewayBase = this.base.replace(/\/platform$/, "")   // ← derives gateway from platform URL (separate issue)
  return this.http
    .getFetch()(`${gatewayBase}/private/backend/v1/thrid_party_token`, { ... })
```

**Fix:** The URL must stay as-is (backend owns it). Clean up the comment to be a one-liner that doesn't draw attention to internal paths.

```python
def get_third_party_token(self, expiration_days: int = 10) -> Dict[str, Any]:
    # Path typo is in the backend and intentionally preserved.
    return self._http.request(
        "POST",
        f"{self._gateway}/private/backend/v1/thrid_party_token",
        json={"expirationDays": expiration_days},
    ).json()
```

---

## 🔴 Issue 5 — No return types on most resource methods

Almost every resource method returns `Dict[str, Any]` (Python) or an implicit `Promise<unknown>` (TypeScript). This means users get zero IDE autocomplete and have no idea what fields a response contains.

**Reference code:**

`py/src/imbrace/resources/auth.py` — every method:
```python
def sign_in(self, email: str, password: str) -> Dict[str, Any]:   # ← unknown shape
def get_login_providers(self) -> Dict[str, Any]:                   # ← unknown shape
def get_azure_groups(self) -> Dict[str, Any]:                      # ← unknown shape
```

`ts/src/resources/auth.ts` — most methods have no return type at all:
```typescript
async signIn(body: { email: string; password: string }) {         // ← no return type
async getLoginProviders() {                                        // ← no return type
async getAzureGroups() {                                          // ← no return type
```

Compare to the one method that's done correctly in `ts/src/resources/auth.ts` line 50:
```typescript
async signinWithEmail(...): Promise<{ token: string; email: string; expired_at: string }>
```

**Fix:** Define typed response interfaces for every method. Use `ThirdPartyTokenResponse` already in `auth.ts` as the template — it's the correct pattern.

```python
# py — define TypedDict or dataclass for each response
from typing import TypedDict

class SignInResponse(TypedDict):
    accessToken: str
    token: str

def sign_in(self, email: str, password: str) -> SignInResponse:
    return self._http.request("POST", ...).json()
```

```typescript
// ts — add return type to every method
interface SignInResponse { accessToken: string; userId: string }

async signIn(body: { email: string; password: string }): Promise<SignInResponse> {
  return this.http.getFetch()(...).then(r => r.json())
}
```

---

## 🔴 Issue 6 — TypeScript request bodies use `Record<string, unknown>`

Many TypeScript methods accept `body: Record<string, unknown>`, which means any object passes — no compile-time safety, no IDE hint about what fields are required.

**Reference code:**

`ts/src/resources/auth.ts`:
```typescript
async signUp(body: Record<string, unknown>) { ... }           // line 66
async signinSSO(body: Record<string, unknown>) { ... }        // line 92
async exchangeAccessTokenWithToken(body: Record<string, unknown>) { ... }  // line 113
async signinWithIdentity(body: Record<string, unknown>) { ... }            // line 121
async createOidcRoleMapping(body: Record<string, unknown>) { ... }         // line 162
async bulkUpdateOidcRoleMappings(body: Record<string, unknown>) { ... }    // line 170
async signupWithGoogle(body: Record<string, unknown>) { ... } // line 180
async signinWithGoogle(body: Record<string, unknown>) { ... } // line 188
// ...and more
```

**Fix:** Replace each `Record<string, unknown>` with a typed interface.

```typescript
// Instead of:
async signUp(body: Record<string, unknown>)

// Do:
interface SignUpInput {
  email: string
  password: string
  name: string
  organizationName?: string
}
async signUp(body: SignUpInput): Promise<SignUpResponse>
```

---

## 🟡 Issue 7 — Auth resource derives the gateway URL by string-stripping the platform URL

`AuthResource` needs to call one endpoint on the gateway (not platform). Instead of receiving the gateway URL directly, it strips `/platform` from the platform URL. This is fragile — if the URL structure ever changes, it silently breaks.

**Reference code:**

`py/src/imbrace/resources/auth.py` lines 19–22:
```python
@property
def _gateway(self) -> str:
    # Derive gateway from platform base: "gateway/platform" → "gateway"
    return self._base.removesuffix("/platform")
```

`ts/src/resources/auth.ts` line 30:
```typescript
const gatewayBase = this.base.replace(/\/platform$/, "")
```

**Fix:** Pass the gateway URL directly to `AuthResource` as a second base URL, the same way `SettingsResource` already receives two URLs.

```python
# py/src/imbrace/resources/auth.py
class AuthResource:
    def __init__(self, http: HttpTransport, base: str, gateway: str):
        self._http = http
        self._base = base.rstrip("/")
        self._gateway = gateway.rstrip("/")   # explicit, no string manipulation
```

```python
# py/src/imbrace/client.py — update construction:
self.auth = AuthResource(self.http, urls.platform, urls.gateway)
```

```typescript
// ts/src/resources/auth.ts
constructor(
  private readonly http: HttpTransport,
  private readonly base: string,
  private readonly gateway: string,   // explicit
) {}
```

```typescript
// ts/src/client.ts
this.auth = new AuthResource(this.http, urls.platform, urls.gateway)
```

---

## 🟡 Issue 8 — Internal `.lan` hostnames hardcoded in the `develop` environment preset

`develop` environment has hardcoded `.lan` addresses that are only reachable on the internal network. External developers who use `env="develop"` will get connection errors with no clear explanation.

**Reference code:**

`py/src/imbrace/environments.py` lines 21–27:
```python
ENVIRONMENTS: dict[str, EnvironmentPreset] = {
    "develop": EnvironmentPreset(
        gateway="https://app-gateway.dev.imbrace.co",
        service_hosts=ServiceHosts(
            ips="http://ips.dev.imbrace.lan",          # ← internal only
            data_board="http://data-board.dev.imbrace.lan",  # ← internal only
        ),
    ),
```

`ts/src/environments.ts` has the same values.

**Fix:** Remove `service_hosts` from the `develop` preset so all traffic routes through the gateway, which is publicly reachable. Internal developers who need direct service access can pass `services=` overrides explicitly.

```python
ENVIRONMENTS: dict[str, EnvironmentPreset] = {
    "develop": EnvironmentPreset(
        gateway="https://app-gateway.dev.imbrace.co",
        # no service_hosts — all traffic goes through gateway
    ),
    "sandbox": EnvironmentPreset(
        gateway="https://app-gateway.sandbox.imbrace.co",
    ),
    "stable": EnvironmentPreset(
        gateway="https://app-gateway.imbrace.co",
    ),
}
```

---

## 🟡 Issue 9 — `api_key` is a public mutable attribute on the transport

`set_access_token()` disables API key mode by directly setting `self.http.api_key = None`. This treats an internal transport attribute as a public settable property, which leaks the transport implementation.

**Reference code:**

`py/src/imbrace/client.py` line 182:
```python
def set_access_token(self, token: str) -> None:
    self.token_manager.set_token(token)
    self.http.api_key = None   # ← direct mutation of internal attribute
```

`py/src/imbrace/async_client.py` line 161 — same pattern.

Compare to TypeScript which correctly calls a method (`ts/src/client.ts` line 224):
```typescript
public setAccessToken(token: string): void {
  this.tokenManager.setToken(token)
  this.http.clearApiKey()   // ✅ method call, not property mutation
}
```

**Fix:** Add a `clear_api_key()` method to `HttpTransport` and `AsyncHttpTransport`, then call it instead of direct assignment.

```python
# py/src/imbrace/http.py
class HttpTransport:
    def clear_api_key(self) -> None:
        self.api_key = None

class AsyncHttpTransport:
    def clear_api_key(self) -> None:
        self.api_key = None
```

```python
# py/src/imbrace/client.py and async_client.py
def set_access_token(self, token: str) -> None:
    self.token_manager.set_token(token)
    self.http.clear_api_key()
```

---

## 🟡 Issue 10 — `check_health` on async client doesn't fire on `__init__`, only on `__aenter__`

The sync client calls `self.init()` in `__init__` when `check_health=True`. The async client stores `self._check_health` but only uses it in `__aenter__`. If someone constructs `AsyncImbraceClient(check_health=True)` without using it as a context manager, the health check never runs. The two clients should behave the same way.

**Reference code:**

`py/src/imbrace/client.py` lines 155–156:
```python
if check_health:
    self.init()   # ← fires immediately in __init__
```

`py/src/imbrace/async_client.py` lines 99, 172–175:
```python
self._check_health = check_health   # ← stored but...

async def __aenter__(self):
    if self._check_health:           # ← only fires when used as context manager
        await self.init()
    return self
```

**Fix:** Document explicitly that `AsyncImbraceClient` requires `async with` to trigger the health check (since you can't `await` inside `__init__`). Update the docstring and raise a clear error if `check_health=True` but the client is used without `async with`.

```python
class AsyncImbraceClient:
    """Asynchronous Imbrace SDK Client.

    When check_health=True, use as an async context manager so the health
    check can run:

        async with AsyncImbraceClient(api_key="...", check_health=True) as client:
            ...

    Using check_health=True without 'async with' has no effect.
    """
```

---

## 🟡 Issue 11 — AI method signatures differ between Python and TypeScript

The same endpoint has different call signatures across the two SDKs. This creates unnecessary friction when teams work across both languages.

**Reference code:**

`py/src/imbrace/resources/ai.py` — positional args:
```python
def complete(self, model: str, messages: list, temperature: float = None, max_tokens: int = None):
```

`ts/src/resources/ai.ts` — single input object:
```typescript
async complete(input: CompletionInput): Promise<Completion>
```

**Fix:** Align Python to the TypeScript pattern — accept a single dataclass/TypedDict so both SDKs look conceptually the same.

```python
from typing import TypedDict, List, Optional

class CompletionInput(TypedDict):
    model: str
    messages: List[dict]
    temperature: Optional[float]
    max_tokens: Optional[int]

def complete(self, input: CompletionInput) -> Completion:
    return self._http.request("POST", ..., json=input).json()
```

---

## 🟡 Issue 12 — TypeScript README references `baseUrl` which doesn't exist

The README shows an example with `baseUrl` but the actual config interface uses `gateway`.

**Reference code:**

`ts/README.md` line 59:
```typescript
const client = new ImbraceClient({
  baseUrl: "https://app-gatewayv2.imbrace.co",   // ← doesn't exist in ImbraceClientConfig
})
```

**Fix:**
```typescript
const client = new ImbraceClient({
  gateway: "https://app-gateway.imbrace.co",
})
```

---

## Summary Table

| # | Severity | Issue | Files |
|---|---|---|---|
| 1 | 🔴 Critical | Vietnamese docstrings and comments | `client.py`, `async_client.py`, `http.py`, `resources/ai.py`, `ts/client.ts` |
| 2 | 🔴 Critical | Silent env var fallback for credentials | `client.py:66–84`, `async_client.py:59–77`, `ts/client.ts:94–129` |
| 3 | 🔴 High | `TokenManager` exported publicly | `ts/src/index.ts:6` |
| 4 | 🔴 High | Backend typo comment misleads future devs | `resources/auth.py:26`, `ts/resources/auth.ts:29` |
| 5 | 🔴 High | No return types — all `Dict[str, Any]` / `unknown` | All resource files |
| 6 | 🔴 High | Request bodies typed as `Record<string, unknown>` | `ts/resources/auth.ts:66,92,113,121,162,170,180,188` |
| 7 | 🟡 Medium | Gateway URL derived from platform URL by string strip | `resources/auth.py:19–22`, `ts/resources/auth.ts:30` |
| 8 | 🟡 Medium | `.lan` hostnames hardcoded in `develop` preset | `environments.py:24–25`, `ts/environments.ts` |
| 9 | 🟡 Medium | `api_key` mutated directly instead of calling a method | `client.py:182`, `async_client.py:161` |
| 10 | 🟡 Medium | `check_health` async/sync behavior mismatch | `client.py:155–156`, `async_client.py:99,172–175` |
| 11 | 🟡 Medium | AI method signatures differ between Python and TS | `resources/ai.py`, `ts/resources/ai.ts` |
| 12 | 🟡 Low | README uses `baseUrl` instead of `gateway` | `ts/README.md:59` |
