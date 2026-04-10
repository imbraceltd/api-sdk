# Test Execution Guide — iMBRACE SDK

**Updated:** 2026-04-10
**Server Environment:** `https://app-gatewayv2.imbrace.co`

---

## Table of Contents

1. [Test Architecture Overview](#1-test-architecture-overview)
2. [Environment Setup](#2-environment-setup)
3. [Python — Running Tests](#3-python--running-tests)
4. [TypeScript — Running Tests](#4-typescript--running-tests)
5. [Detailed Test File Breakdown](#5-detailed-test-file-breakdown)
6. [Lint & Type Check](#6-lint--type-check)
7. [Common Issues](#7-common-issues)

---

## 1. Test Architecture Overview

The SDK has **2 completely separate test layers**:

```
┌─────────────────────────────────────────────────────────┐
│  UNIT TESTS  (No server required, no API key needed)    │
│  → Mocks all HTTP using pytest-httpx / vitest mock      │
│  → Runs offline, suitable for CI/CD                     │
│  → Verifies: SDK logic, headers, URLs, params, errors   │
├─────────────────────────────────────────────────────────┤
│  INTEGRATION TESTS (Requires real server + valid API key) │
│  → Real calls to app-gatewayv2.imbrace.co               │
│  → Verifies: Server returns data in correct format      │
│  → Automatically skips if IMBRACE_API_KEY is missing    │
└─────────────────────────────────────────────────────────┘
```

**Test Directory Structure:**

```
py/tests/
├── unit/
│   ├── test_auth.py
│   ├── test_client.py
│   ├── test_exceptions.py
│   ├── test_http.py
│   └── resources/
│       ├── test_account.py
│       ├── test_agent.py
│       ├── test_contacts.py
│       └── ... (15 files)
└── integration/
    └── test_integration.py

ts/tests/
├── unit/
│   ├── auth.test.ts
│   ├── client.test.ts
│   ├── errors.test.ts
│   ├── http.test.ts
│   └── resources/
│       ├── account.test.ts
│       ├── contacts.test.ts
│       └── ... (19 files)
└── integration/
    └── integration.test.ts
```

**Important Principles:**

- Unit tests **never** call the internet — all HTTP is simulated.
- Integration tests **only run** with a valid API key.
- If unit tests pass but integration tests fail → the issue is likely on the **server or authentication** side, not the SDK code.

---

## 2. Environment Setup

### Python SDK

```bash
cd D:/HUANGJUNFENG/sdk/py

# Install all dependencies + dev tools (pytest, ruff, mypy, pytest-httpx...)
pip install -e ".[dev]"
```

Create a `py/.env` file (required only for integration tests):

```env
IMBRACE_API_KEY=api_xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
IMBRACE_BASE_URL=https://app-gatewayv2.imbrace.co
IMBRACE_ORG_ID=org_xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

> `https://app-gatewayv2.imbrace.co`

### TypeScript SDK

```bash
cd D:/HUANGJUNFENG/sdk/ts
npm install
```

---

## 3. Python — Running Tests

### 3.1 Unit Tests (No API key needed)

```bash
cd D:/HUANGJUNFENG/sdk/py

# Run all unit tests
pytest tests/unit -v
```

Expected result: **~96 passed**

```bash
# Run a specific test file
pytest tests/unit/test_http.py -v
pytest tests/unit/resources/test_channel.py -v

# Run a specific test case
pytest tests/unit/test_http.py::test_401_raises_auth_error -v

# Run by keyword
pytest tests/unit -k "channel" -v
pytest tests/unit -k "notification" -v
```

### 3.2 Integration Tests (Requires a real API key)

```bash
cd D:/HUANGJUNFENG/sdk/py

# Option 1: Set key directly in the command
IMBRACE_API_KEY=api_xxx pytest tests/integration -v -m integration

# Option 2: Using .env → pytest reads it automatically
# Test log:
# Code sends correct headers, but server rejects because the key expired.
# Unit tests still pass normally because they don't call the real server.

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

## 4. TypeScript — Running Tests

### 4.1 Unit Tests

```bash
cd D:/HUANGJUNFENG/sdk/ts

# Run all unit tests
npm test

# Run a specific file
npx vitest run tests/unit/http.test.ts
npx vitest run tests/unit/resources/contacts.test.ts

# Watch mode (auto-run on code changes)
npm run test:watch
```

### 4.2 Integration Tests

```bash
cd D:/HUANGJUNFENG/sdk/ts

IMBRACE_API_KEY=api_xxx npm run test:integration
```

### 4.3 Run All (Unit + Integration)

```bash
npm run test:all
```

---

## 5. Detailed Test File Breakdown

---

### PYTHON — Unit Tests

---

#### `tests/unit/test_auth.py` — TokenManager Testing

**Purpose:** The TokenManager manages access tokens in memory and provides tokens for each request. This file ensures that token storage/deletion works correctly, even with concurrent thread access (thread-safe).

| Test Case                   | Action                                     | Verification                                                         |
| --------------------------- | ------------------------------------------ | -------------------------------------------------------------------- |
| `test_initial_token_none`   | Create `TokenManager()` with no arguments  | Initial token must be `None`                                         |
| `test_initial_token_set`    | Create `TokenManager("tok_abc")`           | Token is correctly stored from constructor                           |
| `test_set_token`            | Call `tm.set_token("tok_xyz")`             | Token updates successfully                                           |
| `test_clear_token`          | Call `tm.clear()`                          | Token is deleted, `get_token()` returns `None`                       |
| `test_thread_safety`        | 2 threads read/write 100 times concurrently| No crashes, no race conditions, all values are valid                 |

---

#### `tests/unit/test_exceptions.py` — Error System Testing

**Purpose:** The SDK defines 3 distinct error types so users can catch specific errors without parsing messages. This file ensures the error system structure is correct.

| Error Type     | Occurrence Scenario                                 |
| -------------- | --------------------------------------------------- |
| `AuthError`    | Server returns 401, 403 — expired or invalid token  |
| `ApiError`     | Server returns other 4xx, 5xx — logic or server error|
| `NetworkError` | Connection lost, timeout, server unresponsive       |

| Test Case                                         | Action                            | Verification                                                                       |
| ------------------------------------------------- | --------------------------------- | ---------------------------------------------------------------------------------- |
| `test_hierarchy`                                | Check `issubclass`               | All 3 are subclasses of `ImbraceError` → `except ImbraceError` catches all         |
| `test_api_error_message`                        | Create `ApiError(404, "Not Found")`| `status_code == 404`, message contains `[404]` and `Not Found`                    |
| `test_auth_error_is_catchable_as_imbrace_error` | Raise `AuthError`                 | Catchable using `except ImbraceError`                                              |
| `test_network_error`                            | Create `NetworkError("timeout")`  | Message contains "timeout"                                                         |

---

#### `tests/unit/test_http.py` — HTTP Layer Testing (Most Critical)

**Purpose:** `HttpTransport` is the core of the SDK — every request passes through it. This file uses `pytest-httpx` to simulate the server and verify: auth header attachment, retries on failure, timeout handling, and mapping HTTP statuses to correct exceptions.

**How mocking works:**

```python
httpx_mock.add_response(status_code=500, text="Server Error")
# → When SDK initiates a request, it receives a simulated 500 response
# → No actual network request is made
```

| Test Case                                  | Simulated Scenario                          | Verification                                                            |
| ------------------------------------------ | ------------------------------------------- | ----------------------------------------------------------------------- |
| `test_get_success`                       | Server returns 200 + JSON                   | Response is parsed, data is correct                                     |
| `test_sets_api_key_header`               | Request with `api_key="key_test"`           | Header `x-access-token: key_test` must be present                       |
| `test_sets_bearer_token_header`          | Request with access token                   | Header `x-access-token: tok_test` is attached (overrides API key)       |
| `test_no_bearer_when_token_cleared`      | No token provided                           | Header `Authorization` is NOT attached to the request                   |
| `test_401_raises_auth_error`             | Server returns 401                          | SDK raises `AuthError` (no retry)                                       |
| `test_403_raises_auth_error`             | Server returns 403                          | SDK raises `AuthError` (no retry)                                       |
| `test_404_raises_api_error`              | Server returns 404                          | SDK raises `ApiError` with `status_code == 404` (no retry)              |
| `test_500_retries_then_raises`           | Server returns 500 **3 consecutive times**  | SDK retries twice → total 3 requests → then raises `ApiError`           |
| `test_network_error_retries_then_raises` | Network interrupted **3 times**            | SDK retries twice → total 3 times → raises `NetworkError`               |
| `test_close`                             | Call `transport.close()`                    | No crashes, HTTP session closes successfully                            |

---

#### `tests/unit/test_client.py` — Client Initialization Testing

**Purpose:** Ensures `ImbraceClient` and `AsyncImbraceClient` read configurations correctly, initialize all 18+ resources, and handle trailing slashes in URLs.

| Test Case                               | Action                                | Verification                                                                     |
| --------------------------------------- | ------------------------------------- | -------------------------------------------------------------------------------- |
| `test_default_base_url`               | Create client without `baseUrl`       | `base_url == "https://app-gatewayv2.imbrace.co"`                                |
| `test_custom_base_url`                | Provide URL with trailing `/`         | Trailing slash is stripped → `"https://staging.imbrace.co"`                    |
| `test_reads_api_key_from_env`         | Set env `IMBRACE_API_KEY=env_key`     | Client reads key from environment variable                                       |
| `test_explicit_api_key_overrides_env` | Provide key directly when env exists  | Direct parameter takes precedence over env var                                   |
| `test_reads_base_url_from_env`        | Set env `IMBRACE_BASE_URL`            | Client uses URL from environment                                                 |
| `test_all_resources_initialized`      | Create client                         | All resources (`sessions`, `messages`, `health`, `channel`...) are initialized   |
| `test_set_access_token`               | Call `set_access_token("new_token")`  | `token_manager.get_token()` returns the new token                               |
| `test_clear_access_token`             | Call `clear_access_token()`           | Token is deleted, subsequent requests lack Bearer header                          |
| `test_context_manager`                | Use `with ImbraceClient(...) as c:`   | Client automatically calls `close()` when exiting the block                      |
| `test_async_client_*`                 | Same as `AsyncImbraceClient`          | Async client also works correctly                                                |

---

#### `tests/unit/resources/test_account.py`

**Purpose:** Test `GET /v1/backend/account` — retrieves current account info.

| Test Case            | Verification                                             |
| -------------------- | -------------------------------------------------------- |
| `test_get_account`   | Correct `GET /v1/backend/account` call, response parsed  |

---

#### `tests/unit/resources/test_agent.py`

**Purpose:** Test CRUD for AI Agents (Templates) — `GET/POST/PATCH/DELETE /v2/backend/templates`.

| Test Case                  | Verification                                     |
| -------------------------- | ------------------------------------------------ |
| `test_list_agents`       | `GET /v2/backend/templates` returns correct list  |
| `test_get_agent`         | `GET /v2/backend/templates/{id}` with correct ID |
| `test_create_agent`      | `POST /v2/backend/templates/custom` with JSON body|
| `test_update_agent`      | `PATCH /v2/backend/templates/{id}/custom`        |
| `test_delete_agent`      | `DELETE /v2/backend/templates/{id}`              |
| `test_sends_auth_header` | All requests include `x-access-token`            |

---

#### `tests/unit/resources/test_channel.py`

**Purpose:** Test channel management — list, get, create (web), update, delete, conversation count.

| Test Case                        | Verification                                         |
| -------------------------------- | ---------------------------------------------------- |
| `test_list_channels`           | `GET /v1/backend/channels` returns correct data      |
| `test_list_channels_with_type` | URL includes query `?type=web` when `type="web"` passed|
| `test_get_channel`             | `GET /v1/backend/channels/{id}` with correct ID      |
| `test_get_conv_count`          | `GET /v1/backend/channels/_conv_count?view=all`      |
| `test_delete_channel`          | Method is `DELETE`, correct URL                      |

---

#### `tests/unit/resources/test_contacts.py`

**Purpose:** Test contacts and notification management.

| Test Case                          | Verification                                                  |
| ---------------------------------- | ------------------------------------------------------------- |
| `test_list_contacts`             | `GET /v1/backend/contacts?limit=20&skip=0`                    |
| `test_list_contacts_pagination`  | Correct `limit=10&skip=5` params in URL                       |
| `test_search_contacts`           | `GET /contacts/_search?q=alice`                               |
| `test_update_contact`            | `PUT` method, JSON body `{"name": "Bob"}` sent correctly      |
| `test_get_contact_conversations` | `GET /contacts/{id}/conversations`                            |
| `test_list_notifications`        | `GET /v1/backend/notifications?limit=20&skip=0`               |
| `test_mark_notifications_read`   | `DELETE /notifications/dismiss` (correct method per docs)     |

---

#### `tests/unit/resources/test_boards.py`

**Purpose:** Test full Board CRUD — creating boards, adding/editing/deleting items, searching, exporting.

| Test Case                  | Verification                                             |
| -------------------------- | -------------------------------------------------------- |
| `test_list_boards`       | `GET /v1/backend/board?limit=20&skip=0`                  |
| `test_list_board_items`  | `GET /v1/backend/board/{id}/board_items`                 |
| `test_create_board_item` | `POST /v1/backend/board/{id}/board_items` with correct body|
| `test_search_board`      | `POST /v1/backend/meilisearch/{id}/search`               |
| `test_export_csv`        | `GET /v1/backend/board/{id}/export_csv` returns text     |

---

#### `tests/unit/resources/test_conversations.py`

**Purpose:** Test conversation endpoints — view count, creating conversations, searching.

| Test Case                     | Verification                                               |
| ----------------------------- | ---------------------------------------------------------- |
| `test_get_views_count`      | `GET /v2/backend/team_conversations/_views_count`          |
| `test_create_conversation`  | `POST /v1/backend/conversation`                            |
| `test_search_conversations` | `POST /v1/backend/meilisearch/{org}/search` with correct body|

---

#### `tests/unit/resources/test_messages.py`

**Purpose:** Test message listing and sending.

| Test Case                         | Verification                                               |
| --------------------------------- | ---------------------------------------------------------- |
| `test_list_messages`            | `GET /v1/backend/conversation_messages?limit=10&skip=0`    |
| `test_list_messages_pagination` | Correct pagination parameters                              |
| `test_send_message_text`        | `POST /v1/backend/conversation_messages` with `type="text"`|
| `test_send_message_image`       | Body includes `type="image"` and `url`                    |

---

#### `tests/unit/resources/test_teams.py`

**Purpose:** Test team management — listing, listing my teams, adding/removing users.

| Test Case              | Verification                                                        |
| ---------------------- | ------------------------------------------------------------------- |
| `test_list_teams`    | `GET /v2/backend/teams?limit=20&skip=0`                             |
| `test_list_my_teams` | `GET /v2/backend/teams/my`                                          |
| `test_add_users`     | `POST /v2/backend/teams/_add_users` with body `{team_id, user_ids}` |
| `test_remove_users`  | `POST /v2/backend/teams/_remove_users`                              |

---

#### `tests/unit/resources/test_settings.py`

**Purpose:** Test message templates and user management.

| Test Case                                          | Verification                                         |
| -------------------------------------------------- | ---------------------------------------------------- |
| `test_list_message_templates`                    | `GET /v2/backend/message_templates?limit=20&skip=0`  |
| `test_list_message_templates_with_business_unit` | `business_unit_id` query added to URL                |
| `test_list_users`                                | `GET /v1/backend/users?limit=20&skip=0`              |
| `test_list_users_with_search`                    | `search=` query added to URL                         |
| `test_get_roles_count`                           | `GET /v1/backend/users/_roles_count`                 |
| `test_bulk_invite`                               | `POST /v1/backend/users/_bulk_invite` with email body|

---

#### `tests/unit/resources/test_workflows.py`

**Purpose:** Test workflow management and n8n integration.

| Test Case                        | Verification                                 |
| -------------------------------- | -------------------------------------------- |
| `test_list_workflows`          | `GET /v1/backend/workflows` with correct params|
| `test_list_workflows_with_tag` | `tag=` query added to URL                    |
| `test_list_channel_automation` | `GET /v1/backend/workflows/channel_automation`|
| `test_list_n8n_workflows`      | `GET /v1/backend/n8n/workflows`              |

---

#### `tests/unit/resources/test_organizations.py`

| Test Case                                     | Verification                                  |
| --------------------------------------------- | --------------------------------------------- |
| `test_list_organizations`                   | `GET /v2/backend/organizations?limit=20&skip=0`|
| `test_list_organizations_pagination`        | Correct pagination parameters                 |
| `test_list_organizations_sends_auth_header` | Header `x-access-token` is present            |

---

#### `tests/unit/resources/test_sessions.py`

| Test Case                             | Verification               |
| ------------------------------------- | -------------------------- |
| `test_list_sessions`                | `GET /session`             |
| `test_list_sessions_with_directory` | `directory=` query in URL  |

---

### PYTHON — Integration Test

---

#### `tests/integration/test_integration.py` — Real Server Calls

**Purpose:** Confirms that the SDK works end-to-end with a real server. If unit tests pass but integration tests fail, the issue is with the server or authentication, not the SDK.

**Execution Prerequisites:** `IMBRACE_API_KEY` must be set and valid.
**Auto-skip** if `IMBRACE_API_KEY` is empty.

| Test Case                       | Real Endpoint Called                              | Response Verification                        |
| ------------------------------- | ------------------------------------------------- | -------------------------------------------- |
| `test_get_account`            | `GET /v1/backend/account`                         | Response has `id`, `_id`, or `data`          |
| `test_list_channels`          | `GET /v1/backend/channels?type=web`               | Response is a `dict`                         |
| `test_list_agents`            | `GET /v2/backend/templates`                       | Response is a `dict`                         |
| `test_list_teams`             | `GET /v2/backend/teams`                           | Response is a `dict`                         |
| `test_list_my_teams`          | `GET /v2/backend/teams/my`                        | Response is a `dict`                         |
| `test_list_contacts`          | `GET /v1/backend/contacts?limit=5`                | Response is a `dict`                         |
| `test_get_views_count`        | `GET /v2/backend/team_conversations/_views_count` | Response is a `dict`                         |
| `test_list_messages`          | `GET /v1/backend/conversation_messages?limit=5`   | Response is a `dict`                         |
| `test_list_boards`            | `GET /v1/backend/board`                           | Response is a `dict`                         |
| `test_list_users`             | `GET /v1/backend/users?limit=5`                   | Response is a `dict`                         |
| `test_list_message_templates` | `GET /v2/backend/message_templates`               | Response is a `dict`                         |

---

### TYPESCRIPT — Unit Tests

---

#### `tests/unit/errors.test.ts`

Equivalent to `test_exceptions.py` — verifies `AuthError`, `ApiError`, `NetworkError` correctly inherit from `ImbraceError` and format messages properly.

#### `tests/unit/http.test.ts`

Equivalent to `test_http.py` — mocks `globalThis.fetch` instead of using `pytest-httpx`. Verifies:

- `x-access-token` header attachment from `apiKey`
- `authorization: Bearer` header attachment from `accessToken`
- 2 Retries upon 429 or 5xx
- `AbortController` cancellation on timeout
- Correct error class raised for each HTTP status

#### `tests/unit/client.test.ts`

Equivalent to `test_client.py` — verifies initialization, env vars, trailing slash stripping, token management, and `checkHealth`.

#### `tests/unit/auth.test.ts`

Equivalent to `test_auth.py` — verifies set/get/clear token on `TokenManager`.

#### `tests/unit/resources/*.test.ts` (19 files)

Equivalent to `tests/unit/resources/test_*.py` — mocks `globalThis.fetch` to verify URL, method, headers, and body for each API call.

#### `tests/integration/integration.test.ts`

Equivalent to `tests/integration/test_integration.py` — makes real server calls. Auto-skips if `IMBRACE_API_KEY` is not set.

---

## 6. Lint & Type Check

### Python

```bash
cd D:/HUANGJUNFENG/sdk/py

# Check code style and deprecated syntax
ruff check src/ tests/

# Automatically fix fixable ruff errors
ruff check src/ tests/ --fix

# Check type annotations
mypy src/imbrace
```

### TypeScript

```bash
cd D:/HUANGJUNFENG/sdk/ts

# Lint
npm run lint

# Type check (includes tests/)
npm run typecheck

# Build (compile to JS for distribution)
npm run build
```

---

## 7. Common Issues

### `AuthError: Invalid or expired access token.` (HTTP 401)

**Cause:** API key in `.env` has expired.
**Fix:** Contact the backend team for a new key and update `IMBRACE_API_KEY` in `.env`.

---

### `ApiError: [400] {"message":"must have required property 'type'"}`

**Cause:** `channel.list()` called without the mandatory `type` parameter.
**Fix:**

```python
# Incorrect
client.channel.list()

# Correct
client.channel.list(type="web")
```

---

### `ApiError: [404]` with double path in URL

**Error URL Example:** `.../private/backend/v1/thrid_party_token/v1/backend/account`

**Cause:** `IMBRACE_BASE_URL` in `.env` incorrectly set to a full endpoint URL.
**Fix:** Update `.env`:

```env
# Incorrect
IMBRACE_BASE_URL=https://app-gatewayv2.imbrace.co/private/backend/v1/thrid_party_token

# Correct
IMBRACE_BASE_URL=https://app-gatewayv2.imbrace.co
```

---

### `mypy` error: `Pattern matching is only supported in Python 3.10`

**Cause:** mypy is scanning internal pytest files in `site-packages` by mistake.
**Fix:** Already configured in `pyproject.toml`. If error persists:

```bash
mypy src/imbrace --exclude site-packages
```

---

### Integration tests all skipped

**Cause:** `IMBRACE_API_KEY` not set in environment.
**Fix:**

```bash
# Set temporarily
IMBRACE_API_KEY=api_xxx pytest tests/integration -v -m integration

# Or add to .env (SDK reads it automatically)
echo "IMBRACE_API_KEY=api_xxx" >> py/.env
```

---

### `Cannot find module '../../src/client.js'` (TypeScript tests)

**Cause:** Incorrect import path in test file after directory reorganization.
**Path Rules:**

| Test File Location                 | Src File Import                 |
| ---------------------------------- | ------------------------------- |
| `tests/unit/*.test.ts`           | `../../src/x.js`              |
| `tests/unit/resources/*.test.ts` | `../../../src/resources/x.js` |
| `tests/integration/*.test.ts`    | `../../src/x.js`              |
