# Testing Guide

> Comprehensive guide for running unit tests, integration tests, lint, and type checks for the Imbrace SDK.

**Updated:** 2026-04-10

## Environment Setup

### Python SDK

```bash
cd py

# Install dependencies + dev tools (pytest, ruff, mypy, pytest-httpx)
pip install -e ".[dev]"
```

Create `py/.env` (required only for integration tests):

```env
IMBRACE_API_KEY=api_xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
IMBRACE_BASE_URL=https://app-gatewayv2.imbrace.co
IMBRACE_ORG_ID=org_xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

### TypeScript SDK

```bash
cd ts
npm install
```

---

## Python — Running & Testing

### Unit Tests (No API key needed)

```bash
cd py

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

### Integration Tests (Requires real API key)

Integration tests perform real calls to the API Gateway.

```bash
cd py

# Option 1: Set key directly in command
IMBRACE_API_KEY=api_xxx pytest tests/integration -v -m integration

# Option 2: Use .env (SDK reads it automatically)
pytest tests/integration -v -m integration
```

### Run All (Unit + Integration)

```bash
pytest tests/ -v
```

### Coverage Report

```bash
pytest tests/unit --cov=src/imbrace --cov-report=term-missing
```

---

## TypeScript — Running & Testing

### Build

```bash
cd ts

# Single build
npm run build

# Build in watch mode (auto-rebuild on change)
npm run dev

# Clean dist/
npm run clean
```

### Unit Tests (No API key needed)

```bash
cd ts

# Run all unit tests
npm test

# Run a specific file
npx vitest run tests/unit/http.test.ts
npx vitest run tests/unit/resources/contacts.test.ts

# Watch mode (auto-run on code changes)
npm run test:watch
```

### Integration Tests (Requires real API key)

```bash
cd ts

IMBRACE_API_KEY=api_xxx npm run test:integration
```

### Run All (Unit + Integration)

```bash
npm run test:all
```

---

## Detailed Test Case Breakdown

### Python — Unit Tests

#### `tests/unit/test_auth.py` — TokenManager

Verifies thread-safe token storage and deletion.

| Test case                 | Verification                                          |
| ------------------------- | ----------------------------------------------------- |
| `test_initial_token_none` | Initial token is `None`                               |
| `test_initial_token_set`  | Token is stored correctly from constructor            |
| `test_set_token`          | Token updates successfully                            |
| `test_clear_token`        | Token is deleted, `get_token()` returns `None`        |
| `test_thread_safety`      | 2 concurrent threads — no crashes, no race conditions |

#### `tests/unit/test_exceptions.py` — Error classes

| Error Type     | Occurrence Scenario           |
| -------------- | ----------------------------- |
| `AuthError`    | Server returns 401, 403       |
| `ApiError`     | Server returns other 4xx, 5xx |
| `NetworkError` | Connection lost, timeout      |

| Test case                                       | Verification                                              |
| ----------------------------------------------- | --------------------------------------------------------- |
| `test_hierarchy`                                | All 3 are subclasses of `ImbraceError`                    |
| `test_api_error_message`                        | `status_code` and message follow format `[404] Not Found` |
| `test_auth_error_is_catchable_as_imbrace_error` | Catchable using `except ImbraceError`                     |

#### `tests/unit/test_http.py` — HttpTransport

Uses `pytest-httpx` to simulate server — no real requests made.

| Test case                                | Scenario                         | Verification                                         |
| ---------------------------------------- | -------------------------------- | ---------------------------------------------------- |
| `test_get_success`                       | Server returns 200               | Response parsed correctly                            |
| `test_sets_api_key_header`               | Request with `api_key`           | Header `x-api-key` is present                        |
| `test_sets_bearer_token_header`          | Request with access token        | Token overrides api_key                              |
| `test_401_raises_auth_error`             | Server returns 401               | Raises `AuthError`, no retry                         |
| `test_403_raises_auth_error`             | Server returns 403               | Raises `AuthError`, no retry                         |
| `test_404_raises_api_error`              | Server returns 404               | Raises `ApiError(status_code=404)`                   |
| `test_500_retries_then_raises`           | Server returns 500 consecutively | Retries twice → total 3 requests → raises `ApiError` |
| `test_network_error_retries_then_raises` | Network interrupted              | Retries twice → raises `NetworkError`                |

#### `tests/unit/test_client.py` — ImbraceClient

| Test case                             | Verification                               |
| ------------------------------------- | ------------------------------------------ |
| `test_default_base_url`               | Default URL is correct                     |
| `test_custom_base_url`                | Trailing slash is stripped                 |
| `test_reads_api_key_from_env`         | Reads `IMBRACE_API_KEY` from env           |
| `test_explicit_api_key_overrides_env` | Direct parameter takes priority over env   |
| `test_all_resources_initialized`      | All resources are initialized              |
| `test_set_access_token`               | Token is updated correctly                 |
| `test_context_manager`                | `with` block automatically calls `close()` |

#### `tests/unit/resources/` — Resource tests

| File                        | Endpoint Verified                                          |
| --------------------------- | ---------------------------------------------------------- |
| `test_account.py`           | `GET /v1/backend/account`                                  |
| `test_agent.py`             | `GET/POST/PATCH/DELETE /v2/backend/templates`              |
| `test_ai.py`                | AI completion, embedding, streaming                        |
| `test_auth.py`              | OTP signin, verify, signout                                |
| `test_boards.py`            | Board CRUD, items, search, export CSV                      |
| `test_campaigns.py`         | Campaign CRUD, touchpoints list/get/create/update/delete/validate |
| `test_channel.py`           | Channel list, get, delete, conv count                      |
| `test_contacts.py`          | Contacts list, search, update, notifications               |
| `test_conversations.py`     | Views count, create, search                                |
| `test_messages.py`          | List, send (text/image)                                    |
| `test_message_suggestion.py`| `POST /v1/message-suggestion` — AI reply suggestions       |
| `test_organizations.py`     | List, pagination, auth header                              |
| `test_predict.py`           | `POST /predict/` — ML-based scoring                        |
| `test_sessions.py`          | List sessions, directory filter                            |
| `test_settings.py`          | Message templates, users, bulk invite                      |
| `test_teams.py`             | List, my teams, add/remove users                           |
| `test_workflows.py`         | List, tag filter, channel automation, create/update        |

---

## Lint & Type Check

### Python

```bash
cd py

# Check code style
ruff check src/ tests/

# Automatically fix fixable ruff errors
ruff check src/ tests/ --fix

# Check type annotations
mypy src/imbrace
```

### TypeScript

```bash
cd ts

# Type check
npm run typecheck

# Lint
npm run lint

# Build (compile to JS)
npm run build
```
