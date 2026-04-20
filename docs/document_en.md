# Execution & Testing Guide — iMBRACE SDK

**Updated:** 2026-04-10

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Environment Setup](#2-environment-setup)
3. [Python — Running & Testing](#3-python--running--testing)
4. [TypeScript — Running & Testing](#4-typescript--running--testing)
5. [Detailed Test Case Breakdown](#5-detailed-test-case-breakdown)
6. [Lint & Type Check](#6-lint--type-check)
7. [Common Issues](#7-common-issues)

---

## 1. Architecture Overview

### Scope

- The SDK covers **App Gateway + Server Gateway** only.
- **Journey API** and **n8n-specific HTTP paths** are out of scope for this repo (see `SDK_OVERVIEW.md`).

### SDK Structure

```
sdk/
├── py/src/imbrace/
│   ├── core/                  ← transport, auth, errors, api_key
│   │   ├── http.py
│   │   ├── exceptions.py
│   │   ├── api_key.py
│   │   └── auth/token_manager.py
│   ├── app/                   ← App Gateway (OTP auth)
│   │   ├── client.py
│   │   └── resources/         (auth, account, agent, ai, boards, channel,
│   │                            contacts, conversations, health, ips,
│   │                            messages, organizations, sessions,
│   │                            settings, teams, workflows)
│   ├── server/                ← Server Gateway (API Key auth)
│   │   ├── client.py
│   │   └── resources/         (ai_agent, boards, categories, marketplace,
│   │                            platform, schedule)
│   ├── types/                 ← shared type definitions
│   └── client.py              ← ImbraceClient (unified entry point)
│
└── ts/src/
    ├── core/                  ← transport, auth, errors
    │   ├── http.ts
    │   ├── errors.ts
    │   └── auth/token-manager.ts
    ├── app/                   ← App Gateway
    │   ├── client.ts
    │   └── resources/         (auth, account, agent, ai, boards, channel,
    │                            contacts, conversations, health, ips,
    │                            messages, organizations, sessions,
    │                            settings, teams, workflows)
    ├── server/                ← Server Gateway
    │   ├── client.ts
    │   └── resources/         (ai-agent, boards, categories, marketplace,
    │                            platform, schedule)
    ├── types/                 ← shared type definitions
    └── client.ts              ← ImbraceClient (unified entry point)
```

### Gateway Differences (Quick)

- App Gateway uses `x-access-token` with access token and `/v1|v2|v3/backend/...` paths.
- Server Gateway uses `x-access-token` with API key and `/3rd/...` paths.

### Test Layers

```
┌─────────────────────────────────────────────────────────┐
│  UNIT TESTS  (No server required, no API key needed)    │
│  → Mocks all HTTP: pytest-httpx (Python) / vitest (TS)  │
│  → Runs offline, suitable for CI/CD                     │
│  → Verifies: SDK logic, headers, URL, params, errors    │
├─────────────────────────────────────────────────────────┤
│  INTEGRATION TESTS (Requires real server + valid API key)│
│  → Real calls to app-gatewayv2.imbrace.co               │
│  → Automatically skips if IMBRACE_API_KEY is missing    │
└─────────────────────────────────────────────────────────┘
```

---

## 2. Environment Setup

### Python SDK

```bash
cd D:/HUANGJUNFENG/IMBrace/sdk/py

# Install dependencies + dev tools (pytest, ruff, mypy, pytest-httpx)
pip install -e ".[dev]"
```

Create `py/.env` file (required only for integration tests):

```env
IMBRACE_API_KEY=api_xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
IMBRACE_BASE_URL=https://app-gatewayv2.imbrace.co
IMBRACE_ORG_ID=org_xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

### TypeScript SDK

```bash
cd D:/HUANGJUNFENG/IMBrace/sdk/ts

npm install
```

---

## 3. Python — Running & Testing

### 3.1 Unit Tests (No API key needed)

```bash
cd D:/HUANGJUNFENG/IMBrace/sdk/py

# Run all unit tests
pytest tests/unit -v

# Run a specific file
pytest tests/unit/test_http.py -v
pytest tests/unit/resources/test_channel.py -v

# Run a specific test case
pytest tests/unit/test_http.py::test_401_raises_auth_error -v

# Run by keyword
pytest tests/unit -k "channel" -v
pytest tests/unit -k "boards" -v
```

### 3.2 Integration Tests (Requires real API key)

Integration tests perform real calls to the API Gateway. See the full list of test cases at:
👉 **[INTEGRATION_TESTS_EN.md](./INTEGRATION_TESTS_EN.md)**

```bash
cd D:/HUANGJUNFENG/IMBrace/sdk/py

# Option 1: Set key directly in command
IMBRACE_API_KEY=api_xxx pytest tests/integration -v -m integration

# Option 2: Use .env (SDK reads it automatically)
pytest tests/integration -v -m integration
```

### 3.3 Run All (Unit + Integration)

```bash
pytest tests/ -v
```

### 3.4 Coverage Report

```bash
pytest tests/unit --cov=src/imbrace --cov-report=term-missing
```

---

## 4. TypeScript — Running & Testing

### 4.1 Build

```bash
cd D:/HUANGJUNFENG/IMBrace/sdk/ts

# Single build
npm run build

# Build in watch mode (auto-rebuild on change)
npm run dev

# Clean dist/
npm run clean
```

### 4.2 Unit Tests (No API key needed)

```bash
cd D:/HUANGJUNFENG/IMBrace/sdk/ts

# Run all unit tests
npm test

# Run a specific file
npx vitest run tests/unit/http.test.ts
npx vitest run tests/unit/resources/contacts.test.ts

# Watch mode (auto-run on code changes)
npm run test:watch
```

### 4.3 Integration Tests (Requires real API key)

Integration tests perform real calls to the API Gateway. See the full list of test cases at:
👉 **[INTEGRATION_TESTS_EN.md](./INTEGRATION_TESTS_EN.md)**

```bash
cd D:/HUANGJUNFENG/IMBrace/sdk/ts

IMBRACE_API_KEY=api_xxx npm run test:integration
```

### 4.4 Run All (Unit + Integration)

```bash
npm run test:all
```

---

## 5. Detailed Test Case Breakdown

### Python — Unit Tests

---

#### `tests/unit/test_auth.py` — TokenManager

Verifies thread-safe token storage and deletion.

| Test case | Verification |
|---|---|
| `test_initial_token_none` | Initial token is `None` |
| `test_initial_token_set` | Token is stored correctly from constructor |
| `test_set_token` | Token updates successfully |
| `test_clear_token` | Token is deleted, `get_token()` returns `None` |
| `test_thread_safety` | 2 concurrent threads — no crashes, no race conditions |

---

#### `tests/unit/test_exceptions.py` — Error classes

| Error Type | Occurrence Scenario |
|---|---|
| `AuthError` | Server returns 401, 403 |
| `ApiError` | Server returns other 4xx, 5xx |
| `NetworkError` | Connection lost, timeout |

| Test case | Verification |
|---|---|
| `test_hierarchy` | All 3 are subclasses of `ImbraceError` |
| `test_api_error_message` | `status_code` and message follow format `[404] Not Found` |
| `test_auth_error_is_catchable_as_imbrace_error` | Catchable using `except ImbraceError` |

---

#### `tests/unit/test_http.py` — HttpTransport (Most Critical)

Uses `pytest-httpx` to simulate server — no real requests made.

| Test case | Scenario | Verification |
|---|---|---|
| `test_get_success` | Server returns 200 | Response parsed correctly |
| `test_sets_api_key_header` | Request with `api_key` | Header `x-access-token` is present in request |
| `test_sets_bearer_token_header` | Request with access token | Token overrides api_key |
| `test_401_raises_auth_error` | Server returns 401 | Raises `AuthError`, no retry |
| `test_403_raises_auth_error` | Server returns 403 | Raises `AuthError`, no retry |
| `test_404_raises_api_error` | Server returns 404 | Raises `ApiError(status_code=404)` |
| `test_500_retries_then_raises` | Server returns 500 consecutively | Retries twice → total 3 requests → raises `ApiError` |
| `test_network_error_retries_then_raises` | Network interrupted | Retries twice → raises `NetworkError` |

---

#### `tests/unit/test_client.py` — ImbraceClient

| Test case | Verification |
|---|---|
| `test_default_base_url` | Default URL is correct |
| `test_custom_base_url` | Trailing slash is stripped |
| `test_reads_api_key_from_env` | Reads `IMBRACE_API_KEY` from env |
| `test_explicit_api_key_overrides_env` | Direct parameter takes priority over env |
| `test_all_resources_initialized` | All resources are initialized |
| `test_set_access_token` | Token is updated correctly |
| `test_context_manager` | `with` block automatically calls `close()` |

---

#### `tests/unit/resources/` — Resource tests (15 files)

| File | Endpoint Verified |
|---|---|
| `test_account.py` | `GET /v1/backend/account` |
| `test_agent.py` | `GET/POST/PATCH/DELETE /v2/backend/templates` |
| `test_ai.py` | AI completion, embedding, streaming |
| `test_auth.py` | OTP signin, verify, signout |
| `test_boards.py` | Board CRUD, items, search, export CSV |
| `test_channel.py` | Channel list, get, delete, conv count |
| `test_contacts.py` | Contacts list, search, update, notifications |
| `test_conversations.py` | Views count, create, search |
| `test_messages.py` | List, send (text/image) |
| `test_organizations.py` | List, pagination, auth header |
| `test_sessions.py` | List sessions, directory filter |
| `test_settings.py` | Message templates, users, bulk invite |
| `test_teams.py` | List, my teams, add/remove users |
| `test_workflows.py` | List, tag filter, channel automation, create/update |

---

## 6. Lint & Type Check

### Python

```bash
cd D:/HUANGJUNFENG/IMBrace/sdk/py

# Check code style
ruff check src/ tests/

# Automatically fix fixable ruff errors
ruff check src/ tests/ --fix

# Check type annotations
mypy src/imbrace
```

### TypeScript

```bash
cd D:/HUANGJUNFENG/IMBrace/sdk/ts

# Type check
npm run typecheck

# Lint
npm run lint

# Build (compile to JS)
npm run build
```

---

## 7. Common Issues

### `AuthError: Invalid or expired access token.` (HTTP 401)

API key in `.env` has expired.

```bash
# Update .env
IMBRACE_API_KEY=new_api_key
```

---

### `ApiError: [400] {"message":"must have required property 'type'"}`

`channel.list()` called without mandatory parameter.

```python
# Incorrect
client.app.channel.list()

# Correct
client.app.channel.list(type="web")
```

---

### `ApiError: [404]` with double path in URL

URL is doubled because `IMBRACE_BASE_URL` was incorrectly set to a full endpoint.

```env
# Incorrect
IMBRACE_BASE_URL=https://app-gatewayv2.imbrace.co/private/backend/v1/thrid_party_token

# Correct
IMBRACE_BASE_URL=https://app-gatewayv2.imbrace.co
```

---

### Integration tests all skipped

`IMBRACE_API_KEY` is not set.

```bash
# Set temporarily during execution
IMBRACE_API_KEY=api_xxx pytest tests/integration -v -m integration

# Or add to .env
echo "IMBRACE_API_KEY=api_xxx" >> py/.env
```

---

### `Cannot find module` (TypeScript tests)

Import paths in test files must be relative to the directory depth:

| Test file location | Import |
|---|---|
| `tests/unit/*.test.ts` | `../../src/client.js` |
| `tests/unit/resources/*.test.ts` | `../../../src/app/resources/x.js` |
| `tests/integration/*.test.ts` | `../../src/client.js` |

---

### `mypy` error: `Pattern matching is only supported in Python 3.10`

mypy scanning `site-packages` by mistake. Configured in `pyproject.toml`. If it persists:

```bash
mypy src/imbrace --exclude site-packages
```