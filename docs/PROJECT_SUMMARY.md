# Imbrace SDK — Project Summary

**Last Updated:** 2026-04-10
**Version:** 2.0.0
**Gateways:**
- App Gateway: `https://app-gatewayv2.imbrace.co`
- Server Gateway: `https://app-gatewayv2.imbrace.co/3rd/`
- Journey API: `https://app-gatewayv2.imbrace.co/journeys/`

---

## Purpose

The Imbrace SDK Monorepo provides **official client libraries** for interfacing with the **Imbrace Platform** — a customer engagement / omnichannel communication platform. The SDK abstracts authentication, HTTP transport, retry logic, and resource-based API calls so developers can integrate Imbrace without dealing with raw HTTP.

Target consumers:
- **Backend developers** building server-side integrations (Python, Node.js)
- **Frontend / fullstack developers** consuming Imbrace APIs from browser/Next.js apps (TypeScript)

---

## Repository Structure

```
sdk/
├── ts/                              # @imbrace/sdk — TypeScript/JavaScript SDK
│   ├── src/
│   │   ├── core/                    # Shared transport layer
│   │   │   ├── http.ts              # HttpTransport (fetch, retry, timeout, auth headers)
│   │   │   ├── errors.ts            # ImbraceError, AuthError, ApiError, NetworkError
│   │   │   └── auth/
│   │   │       └── token-manager.ts # Stateful session token
│   │   ├── app/                     # App Gateway (OTP auth → access_token)
│   │   │   ├── client.ts            # AppGatewayClient
│   │   │   └── resources/           # auth, account, agent, ai, boards, channel,
│   │   │                            # contacts, conversations, health, ips,
│   │   │                            # messages, organizations, sessions,
│   │   │                            # settings, teams, workflows  (15 files)
│   │   ├── server/                  # Server Gateway (API Key auth)
│   │   │   ├── client.ts            # ServerGatewayClient
│   │   │   └── resources/           # ai-agent, boards, categories, marketplace,
│   │   │                            # platform, schedule  (6 files)
│   │   ├── journey/                 # Journey API (temp_token auth)
│   │   │   ├── client.ts            # JourneyClient
│   │   │   └── resources/           # ai-assistant, apps, boards, workflow  (4 files)
│   │   ├── types/                   # Shared TypeScript type definitions
│   │   │   └── index.ts             # (common, account, agent, ai, auth, board,
│   │   │                            #  channel, contact, conversation, ips,
│   │   │                            #  marketplace, message, notification,
│   │   │                            #  organization, platform, team)
│   │   ├── client.ts                # ImbraceClient — unified entry point
│   │   └── index.ts                 # Public exports barrel
│   └── tests/
│       ├── unit/                    # vitest, fetch mocked globally
│       │   ├── auth.test.ts
│       │   ├── client.test.ts
│       │   ├── errors.test.ts
│       │   ├── http.test.ts
│       │   └── resources/           # 19 test files (one per resource)
│       └── integration/
│           └── integration.test.ts  # Live calls, auto-skips without API key
│
├── py/                              # imbrace — Python SDK
│   ├── src/imbrace/
│   │   ├── core/                    # Shared transport layer
│   │   │   ├── http.py              # HttpTransport + AsyncHttpTransport (httpx)
│   │   │   ├── exceptions.py        # ImbraceError, AuthError, ApiError, NetworkError
│   │   │   ├── api_key.py           # ImbraceApiKey, extract_api_key helper
│   │   │   └── auth/
│   │   │       └── token_manager.py # Thread-safe session token
│   │   ├── app/                     # App Gateway (OTP auth → access_token)
│   │   │   ├── client.py            # AppGatewayClient + AsyncAppGatewayClient
│   │   │   └── resources/           # auth, account, agent, ai, boards, channel,
│   │   │                            # contacts, conversations, health, ips,
│   │   │                            # messages, organizations, sessions,
│   │   │                            # settings, teams, workflows  (15 files)
│   │   ├── server/                  # Server Gateway (API Key auth)
│   │   │   ├── client.py            # ServerGatewayClient + AsyncServerGatewayClient
│   │   │   └── resources/           # ai_agent, boards, categories, marketplace,
│   │   │                            # platform, schedule  (6 files)
│   │   ├── journey/                 # Journey API (temp_token auth)
│   │   │   ├── client.py            # JourneyClient + AsyncJourneyClient
│   │   │   └── resources/           # ai_assistant, apps, boards, workflow  (4 files)
│   │   ├── types/                   # Shared Python type definitions
│   │   │   └── __init__.py          # (common, agent, ai, channel, ips,
│   │   │                            #  marketplace, platform, session)
│   │   ├── __init__.py              # Public exports
│   │   ├── client.py                # ImbraceClient + AsyncImbraceClient
│   │   └── async_client.py          # Re-export AsyncImbraceClient
│   └── tests/
│       ├── unit/                    # pytest + pytest-httpx (~96 tests)
│       │   ├── test_auth.py
│       │   ├── test_client.py
│       │   ├── test_exceptions.py
│       │   ├── test_http.py
│       │   └── resources/           # 15 test files (one per resource)
│       └── integration/
│           └── test_integration.py  # Live calls, auto-skips without API key
│
└── docs/
    ├── PROJECT_SUMMARY.md           # This file
    ├── document_vn.md               # Run & test guide (Vietnamese)
    ├── document_en.md               # Run & test guide (English)
    └── API document/                # Raw API docs per gateway
        ├── AppGeteway/
        ├── ServerGateway/
        └── JourneyAPI/
```

---

## Core Architecture

### 3-Gateway Model

```
ImbraceClient
    │
    ├── .app        AppGatewayClient      OTP → access_token
    │               header: x-access-token: <tok>
    │               paths:  /v1/backend/, /v2/backend/, /v3/backend/
    │
    ├── .server     ServerGatewayClient   API Key (permanent)
    │               header: x-access-token: <api_key>
    │               paths:  /3rd/
    │
    └── .journey    JourneyClient         temp_token
                    header: x-temp-token: <token>
                    paths:  /journeys/api/v1/, /journeys/v1/, /journeys/v2/
```

### Core Layer (`core/`)

Shared across all 3 gateways — không gateway nào tự implement HTTP hay auth riêng.

| File | Vai trò |
|---|---|
| `core/http.py` / `core/http.ts` | HttpTransport — retry, timeout, header injection |
| `core/exceptions.py` / `core/errors.ts` | Error class hierarchy |
| `core/auth/token_manager` | In-memory session token (thread-safe in Python) |
| `core/api_key.py` *(Python only)* | Helper extract API key từ auth response |

### HTTP Transport

- **Python:** `httpx` (sync `HttpTransport` + async `AsyncHttpTransport`)
- **TypeScript:** native `fetch` + `AbortController` cho timeout
- **Retry:** 2 lần khi `5xx` / network error; không retry `4xx` (trừ `429`)
- **Error mapping:**
  - `401` / `403` → `AuthError`
  - `4xx` / `5xx` khác → `ApiError` (có `status_code`)
  - Connection failure / timeout → `NetworkError`

---

## Resource Map

### App Gateway (`client.app.*`)

| Resource | Domain | Endpoints chính |
|---|---|---|
| `auth` | Authentication | OTP signin, verify, token exchange |
| `account` | Account | `GET /v1/backend/account` |
| `organizations` | Multi-tenancy | `GET/POST /v2/backend/organizations` |
| `agent` | AI Agent Templates | CRUD `/v2/backend/templates` |
| `ai` | AI Inference | Completion, embedding, streaming |
| `channel` | Channels | CRUD `/v1/backend/channels`, conv count |
| `conversations` | Conversations | Create, search, view count |
| `messages` | Messages | List, send (text / image) |
| `contacts` | Contacts | CRUD, search, notifications |
| `teams` | Teams | List, my teams, add/remove users |
| `workflows` | Automation | Workflows, channel automation, n8n |
| `boards` | Kanban Boards | CRUD, items, Meilisearch, CSV export |
| `settings` | Settings | Message templates, users, roles |
| `health` | Health | Gateway health check |
| `sessions` | Sessions | Session listing |
| `ips` | IPS Profiles | Profiles, follow/unfollow, identities |

### Server Gateway (`client.server.*`)

| Resource | Domain | Endpoints chính |
|---|---|---|
| `boards` | Boards (bulk) | Search, create/update items at scale |
| `ai_agent` | AI Agent (RAG) | RAG query, knowledge base |
| `categories` | Categories | Category management |
| `marketplace` | Marketplace | Products, orders |
| `schedule` | Scheduling | Scheduled tasks |
| `platform` | Platform Admin | Users, organizations, permissions |

### Journey API (`client.journey.*`)

| Resource | Domain | Endpoints chính |
|---|---|---|
| `workflow` | Workflow | Get workflow, trigger |
| `ai_assistant` | AI Assistant | List, chat |
| `apps` | Apps | Submit, settings |
| `boards` | Boards | Journey-scoped board access |

---

## Test Architecture

```
┌─────────────────────────────────────────────────────────┐
│  UNIT TESTS  (offline, no API key, mocked HTTP)         │
│  Python: pytest + pytest-httpx  (~96 tests)             │
│  TypeScript: vitest + fetch mock  (23 files)            │
├─────────────────────────────────────────────────────────┤
│  INTEGRATION TESTS  (live server, valid API key needed) │
│  Auto-skip nếu IMBRACE_API_KEY không được set           │
│  Validate response shape từ server thật                 │
└─────────────────────────────────────────────────────────┘
```

**Lệnh chạy test:**

```bash
# Python — unit
cd py && pytest tests/unit -v

# Python — integration
cd py && pytest tests/integration -v -m integration

# TypeScript — unit
cd ts && npm test

# TypeScript — integration
cd ts && npm run test:integration
```

---

## Environment Variables

| Variable | Dùng cho | Default |
|---|---|---|
| `IMBRACE_API_KEY` | Server Gateway auth (server-side) | — |
| `IMBRACE_BASE_URL` | Override URL cho cả 3 gateways | `https://app-gatewayv2.imbrace.co` |
| `IMBRACE_TEMP_TOKEN` | Journey API auth | — |
| `IMBRACE_ORG_ID` | Multi-tenant calls | — |

---

## Quick Reference

```python
# Python
from imbrace import ImbraceClient

with ImbraceClient(
    server_api_key="api_xxx",
    journey_temp_token="tok_yyy",
) as client:
    # App Gateway — OTP auth
    client.app.auth.signin_email_request("user@example.com")
    channels = client.app.channel.list(type="web")
    client.app.messages.send(conversation_id="...", type="text", content="Hello")

    # Server Gateway — API Key auth
    client.server.boards.create_items("brd_xxx", items=[...])
    client.server.categories.list()

    # Journey API — temp token
    workflow = client.journey.workflow.get("wf_xxx", org_id="org_xxx")
    client.journey.ai_assistant.list()
```

```typescript
// TypeScript
import { ImbraceClient } from "@imbrace/sdk";

const client = new ImbraceClient({
  serverApiKey: "api_xxx",
  journeyTempToken: "tok_yyy",
});

// App Gateway
const channels = await client.app.channel.list({ type: "web" });
await client.app.messages.send({ conversationId: "...", type: "text", content: "Hello" });

// Server Gateway
await client.server.boards.createItems("brd_xxx", { items: [...] });

// Journey API
const workflow = await client.journey.workflow.get("wf_xxx", { orgId: "org_xxx" });
```

---

## Future Implementation Roadmap

### Phase 1 — Foundation Hardening

| Item | Mô tả | Priority |
|---|---|---|
| **Response Models / DTOs** | Pydantic models (Python) và Zod schemas (TS) cho tất cả API responses. Hiện tại là raw `dict` / `any`. | High |
| **Pagination Helper** | Auto-paginate list endpoints với generator pattern — `client.app.contacts.list_all()` | High |
| **Rate Limiting + Backoff** | Exponential backoff khi `429 Too Many Requests`. Hiện chỉ retry `5xx`. | High |
| **Request Cancellation (Python)** | `httpx` cancel token cho `AsyncImbraceClient` để match TS `AbortController` | Medium |

### Phase 2 — Developer Experience

| Item | Mô tả | Priority |
|---|---|---|
| **SDK Docs Site** | Auto-generate API reference từ docstrings (Python: `pdoc`/`mkdocs`; TS: `typedoc`) | High |
| **More Examples** | Examples cho từng gateway: boards, workflows, agents, journey | Medium |
| **Error Context Enrichment** | Include request URL + method trong error messages | Medium |
| **Logging / Debug Mode** | `ImbraceClient(debug=True)` — in request/response ra stdout | Medium |

### Phase 3 — New SDK Targets

| Item | Mô tả | Priority |
|---|---|---|
| **OpenAPI Spec** | Generate `openapi.yaml` từ gateway; derive SDKs từ đó | High |
| **Go SDK** | `imbrace-go` — server-side Go package | Medium |
| **Browser Bundle** | UMD/CDN build của TS SDK cho `<script>` tag | Medium |
| **Java/Kotlin SDK** | Android và Spring Boot | Low |

### Phase 4 — Advanced Features

| Item | Mô tả | Priority |
|---|---|---|
| **Webhook Signature Verification** | Helper verify Imbrace webhook payload (HMAC) | High |
| **Realtime / WebSocket Client** | Subscribe conversation/message events | Medium |
| **OAuth 2.0 Flow Helper** | Authorization code flow cho marketplace apps | Medium |
| **Multipart File Upload** | Structured helpers upload attachments | Medium |
| **Middleware / Plugin System** | `client.use(middleware)` — custom interceptors | Low |

### Phase 5 — CI / Release Hardening

| Item | Mô tả | Priority |
|---|---|---|
| **GitHub Actions Pipeline** | Lint → type-check → unit tests → build trên mỗi PR | High |
| **Automated Release** | Auto-publish lên PyPI + npm khi merge vào `main` | High |
| **Coverage Gate** | Enforce ≥ 90% coverage trong CI | Medium |
| **Cross-version Testing** | Python matrix (3.9–3.13), Node matrix (18, 20, 22) | Medium |
