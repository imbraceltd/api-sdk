# Hướng Dẫn Chạy & Test — iMBRACE SDK

**Cập nhật:** 2026-04-10

---

## Mục Lục

1. [Tổng Quan Kiến Trúc](#1-tổng-quan-kiến-trúc)
2. [Cài Đặt Môi Trường](#2-cài-đặt-môi-trường)
3. [Python — Lệnh Chạy & Test](#3-python--lệnh-chạy--test)
4. [TypeScript — Lệnh Chạy & Test](#4-typescript--lệnh-chạy--test)
5. [Chi Tiết Từng File Test](#5-chi-tiết-từng-file-test)
6. [Lint & Type Check](#6-lint--type-check)
7. [Lỗi Thường Gặp](#7-lỗi-thường-gặp)

---

## 1. Tổng Quan Kiến Trúc

### Phạm vi

- SDK chi gom **App Gateway + Server Gateway**.
- **Journey API** và các path HTTP riêng cho **n8n** không thuộc phạm vi repo này (xem [SDK_OVERVIEW.md](./SDK_OVERVIEW.md)).

### Cấu trúc SDK

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

### App Gateway và Server Gateway (khác nhau nhanh)

- App Gateway: `x-access-token` = access token; path `/v1|v2|v3/backend/...`.
- Server Gateway: `x-access-token` = API key; path `/3rd/...`.

### Tầng Test

```
┌─────────────────────────────────────────────────────────┐
│  UNIT TESTS  (không cần server, không cần API key)      │
│  → Mock toàn bộ HTTP: pytest-httpx (Python) / vitest   │
│  → Chạy offline, chạy trên CI/CD                        │
│  → Kiểm tra: logic SDK, headers, URL, params, errors   │
│  ├─────────────────────────────────────────────────────────┤
│  INTEGRATION TESTS  (cần server thật + API key hợp lệ) │
│  → Gọi thật tới app-gatewayv2.imbrace.co               │
│  → Tự động skip nếu không có IMBRACE_API_KEY            │
└─────────────────────────────────────────────────────────┘
```

---

## 2. Cài Đặt Môi Trường

### Python SDK

```bash
cd D:/HUANGJUNFENG/IMBrace/sdk/py

# Cài dependencies + dev tools (pytest, ruff, mypy, pytest-httpx)
pip install -e ".[dev]"
```

Tạo file `py/.env` (chỉ cần cho integration test):

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

## 3. Python — Lệnh Chạy & Test

### 3.1 Unit Tests (không cần API key)

```bash
cd D:/HUANGJUNFENG/IMBrace/sdk/py

# Chạy toàn bộ unit tests
pytest tests/unit -v

# Chạy một file cụ thể
pytest tests/unit/test_http.py -v
pytest tests/unit/resources/test_channel.py -v

# Chạy một test case cụ thể
pytest tests/unit/test_http.py::test_401_raises_auth_error -v

# Chạy theo keyword
pytest tests/unit -k "channel" -v
pytest tests/unit -k "boards" -v
```

### 3.2 Integration Tests (cần API key thật)

Kiểm thử tích hợp gọi thật tới API Gateway. Xem chi tiết danh sách tất cả các bài test tại:
👉 **[INTEGRATION_TESTS_VN.md](./INTEGRATION_TESTS_VN.md)**

```bash
cd D:/HUANGJUNFENG/IMBrace/sdk/py

# Cách 1: Set key trực tiếp trong lệnh
IMBRACE_API_KEY=api_xxx pytest tests/integration -v -m integration

# Cách 2: Dùng .env (SDK tự đọc)
pytest tests/integration -v -m integration
```

### 3.3 Chạy tất cả (unit + integration)

```bash
pytest tests/ -v
```

### 3.4 Coverage Report

```bash
pytest tests/unit --cov=src/imbrace --cov-report=term-missing
```

---

## 4. TypeScript — Lệnh Chạy & Test

### 4.1 Build

```bash
cd D:/HUANGJUNFENG/IMBrace/sdk/ts

# Build một lần
npm run build

# Build watch mode (tự rebuild khi thay đổi)
npm run dev

# Xóa dist/
npm run clean
```

### 4.2 Unit Tests (không cần API key)

```bash
cd D:/HUANGJUNFENG/IMBrace/sdk/ts

# Chạy toàn bộ unit tests
npm test

# Chạy một file cụ thể
npx vitest run tests/unit/http.test.ts
npx vitest run tests/unit/resources/contacts.test.ts

# Watch mode (tự chạy lại khi code thay đổi)
npm run test:watch
```

### 4.3 Integration Tests (cần API key thật)

Kiểm thử tích hợp gọi thật tới API Gateway. Xem chi tiết danh sách tất cả các bài test tại:
👉 **[INTEGRATION_TESTS_VN.md](./INTEGRATION_TESTS_VN.md)**

```bash
cd D:/HUANGJUNFENG/IMBrace/sdk/ts

IMBRACE_API_KEY=api_xxx npm run test:integration
```

### 4.4 Chạy tất cả (unit + integration)

```bash
npm run test:all
```

---

## 5. Chi Tiết Từng File Test

### Python — Unit Tests

---

#### `tests/unit/test_auth.py` — TokenManager

Kiểm tra lưu/xóa token thread-safe.

| Test case | Kiểm tra |
|---|---|
| `test_initial_token_none` | Token ban đầu là `None` |
| `test_initial_token_set` | Token được lưu từ constructor |
| `test_set_token` | Token thay đổi thành công |
| `test_clear_token` | Token bị xóa, `get_token()` → `None` |
| `test_thread_safety` | 2 thread đọc/ghi đồng thời — không crash, không race condition |

---

#### `tests/unit/test_exceptions.py` — Error classes

| Loại lỗi | Khi nào xảy ra |
|---|---|
| `AuthError` | Server trả 401, 403 |
| `ApiError` | Server trả 4xx, 5xx khác |
| `NetworkError` | Mất kết nối, timeout |

| Test case | Kiểm tra |
|---|---|
| `test_hierarchy` | Cả 3 đều là subclass của `ImbraceError` |
| `test_api_error_message` | `status_code` và message đúng format `[404] Not Found` |
| `test_auth_error_is_catchable_as_imbrace_error` | Bắt được bằng `except ImbraceError` |

---

#### `tests/unit/test_http.py` — HttpTransport (quan trọng nhất)

Dùng `pytest-httpx` để giả lập server — không có request thật.

| Test case | Kịch bản | Kiểm tra |
|---|---|---|
| `test_get_success` | Server trả 200 | Response parse đúng |
| `test_sets_api_key_header` | Request với `api_key` | Header `x-access-token` có trong request |
| `test_sets_bearer_token_header` | Request với access token | Token đè lên api_key |
| `test_401_raises_auth_error` | Server trả 401 | Raise `AuthError`, không retry |
| `test_403_raises_auth_error` | Server trả 403 | Raise `AuthError`, không retry |
| `test_404_raises_api_error` | Server trả 404 | Raise `ApiError(status_code=404)` |
| `test_500_retries_then_raises` | Server trả 500 liên tiếp | Retry 2 lần → tổng 3 request → raise `ApiError` |
| `test_network_error_retries_then_raises` | Mạng bị ngắt | Retry 2 lần → raise `NetworkError` |

---

#### `tests/unit/test_client.py` — ImbraceClient

| Test case | Kiểm tra |
|---|---|
| `test_default_base_url` | URL mặc định đúng |
| `test_custom_base_url` | Trailing slash bị strip |
| `test_reads_api_key_from_env` | Đọc `IMBRACE_API_KEY` từ env |
| `test_explicit_api_key_overrides_env` | Param trực tiếp ưu tiên hơn env |
| `test_all_resources_initialized` | Tất cả resources được khởi tạo |
| `test_set_access_token` | Token được cập nhật |
| `test_context_manager` | `with` block tự gọi `close()` |

---

#### `tests/unit/resources/` — Resource tests (15 files)

| File | Endpoint kiểm tra |
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

# Kiểm tra code style
ruff check src/ tests/

# Tự fix lỗi ruff có thể sửa
ruff check src/ tests/ --fix

# Kiểm tra type annotations
mypy src/imbrace
```

### TypeScript

```bash
cd D:/HUANGJUNFENG/IMBrace/sdk/ts

# Type check
npm run typecheck

# Lint
npm run lint

# Build (compile ra JS)
npm run build
```

---

## 7. Lỗi Thường Gặp

### `AuthError: Invalid or expired access token.` (HTTP 401)

API key trong `.env` đã hết hạn.

```bash
# Cập nhật .env
IMBRACE_API_KEY=api_xxx_moi
```

---

### `ApiError: [400] {"message":"must have required property 'type'"}`

Gọi `channel.list()` thiếu param bắt buộc.

```python
# Sai
client.app.channel.list()

# Đúng
client.app.channel.list(type="web")
```

---

### `ApiError: [404]` với URL có path kép

URL bị double vì `IMBRACE_BASE_URL` được set nhầm thành full endpoint.

```env
# Sai
IMBRACE_BASE_URL=https://app-gatewayv2.imbrace.co/private/backend/v1/thrid_party_token

# Đúng
IMBRACE_BASE_URL=https://app-gatewayv2.imbrace.co
```

---

### Integration test bị skip toàn bộ

`IMBRACE_API_KEY` chưa được set.

```bash
# Set tạm thời khi chạy
IMBRACE_API_KEY=api_xxx pytest tests/integration -v -m integration

# Hoặc thêm vào .env
echo "IMBRACE_API_KEY=api_xxx" >> py/.env
```

---

### `Cannot find module` (TypeScript tests)

Đường dẫn import trong test file cần đúng cấp thư mục:

| Vị trí test file | Import |
|---|---|
| `tests/unit/*.test.ts` | `../../src/client.js` |
| `tests/unit/resources/*.test.ts` | `../../../src/app/resources/x.js` |
| `tests/integration/*.test.ts` | `../../src/client.js` |

---

### `mypy` báo lỗi `Pattern matching is only supported in Python 3.10`

mypy scan nhầm vào `site-packages`. Đã config trong `pyproject.toml`. Nếu vẫn lỗi:

```bash
mypy src/imbrace --exclude site-packages
```
