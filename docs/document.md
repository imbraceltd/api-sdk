# Hướng Dẫn Chạy Test — iMBRACE SDK

**Cập nhật:** 2026-04-10
**Môi trường server:** `https://app-gatewayv2.imbrace.co`

---

## Mục Lục

1. [Tổng Quan Kiến Trúc Test](#1-tổng-quan-kiến-trúc-test)
2. [Cài Đặt Môi Trường](#2-cài-đặt-môi-trường)
3. [Python — Chạy Tests](#3-python--chạy-tests)
4. [TypeScript — Chạy Tests](#4-typescript--chạy-tests)
5. [Chi Tiết Từng File Test](#5-chi-tiết-từng-file-test)
6. [Lint &amp; Type Check](#6-lint--type-check)
7. [Lỗi Thường Gặp](#7-lỗi-thường-gặp)

---

## 1. Tổng Quan Kiến Trúc Test

SDK có **2 tầng test** hoàn toàn tách biệt:

```
┌─────────────────────────────────────────────────────────┐
│  UNIT TESTS  (không cần server, không cần API key)      │
│  → Mock toàn bộ HTTP bằng pytest-httpx / vitest mock    │
│  → Chạy được offline, chạy trên CI/CD                   │
│  → Kiểm tra: logic SDK, headers, URL, params, errors    │
├─────────────────────────────────────────────────────────┤
│  INTEGRATION TESTS  (cần server thật + API key hợp lệ)  │
│  → Gọi thật tới app-gatewayv2.imbrace.co                │
│  → Kiểm tra: server có trả dữ liệu đúng format không   │
│  → Tự động skip nếu không có IMBRACE_API_KEY            │
└─────────────────────────────────────────────────────────┘
```

**Cấu trúc thư mục test:**

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

**Nguyên tắc quan trọng:**

- Unit test **không bao giờ** gọi ra internet — toàn bộ HTTP được giả lập
- Integration test **chỉ chạy** khi có API key hợp lệ
- Unit test pass nhưng integration test fail → vấn đề ở phía **server hoặc auth**, không phải code SDK

---

## 2. Cài Đặt Môi Trường

### Python SDK

```bash
cd D:/HUANGJUNFENG/sdk/py

# Cài tất cả dependencies + dev tools (pytest, ruff, mypy, pytest-httpx...)
pip install -e ".[dev]"
```

Tạo file `py/.env` (chỉ cần cho integration test):

```env
IMBRACE_API_KEY=api_xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
IMBRACE_BASE_URL=https://app-gatewayv2.imbrace.co
IMBRACE_ORG_ID=org_xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

>
>  `https://app-gatewayv2.imbrace.co`

### TypeScript SDK

```bash
cd D:/HUANGJUNFENG/sdk/ts
npm install
```

---

## 3. Python — Chạy Tests

### 3.1 Unit Tests (không cần API key)

```bash
cd D:/HUANGJUNFENG/sdk/py

# Chạy toàn bộ unit tests
pytest tests/unit -v
```

Kết quả mong đợi: **~96 passed**

```bash
# Chạy một file test cụ thể
pytest tests/unit/test_http.py -v
pytest tests/unit/resources/test_channel.py -v

# Chạy một test case cụ thể
pytest tests/unit/test_http.py::test_401_raises_auth_error -v

# Chạy theo keyword
pytest tests/unit -k "channel" -v
pytest tests/unit -k "notification" -v
```

### 3.2 Integration Tests (bắt buộc cần API key thật)

```bash
cd D:/HUANGJUNFENG/sdk/py

# Cách 1: Set key trực tiếp trong lệnh
IMBRACE_API_KEY=api_xxx pytest tests/integration -v -m integration

# Cách 2: Đã có .env → pytest tự đọc
# test log
Code gửi đúng header, nhưng server từ chối vì key hết hạn. Unit tests vẫn   
pass bình thường vì chúng không gọi server thật. 

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

## 4. TypeScript — Chạy Tests

### 4.1 Unit Tests

```bash
cd D:/HUANGJUNFENG/sdk/ts

# Chạy toàn bộ unit tests
npm test

# Chạy một file cụ thể
npx vitest run tests/unit/http.test.ts
npx vitest run tests/unit/resources/contacts.test.ts

# Watch mode (tự chạy lại khi code thay đổi)
npm run test:watch
```

### 4.2 Integration Tests

```bash
cd D:/HUANGJUNFENG/sdk/ts

IMBRACE_API_KEY=api_xxx npm run test:integration
```

### 4.3 Chạy tất cả (unit + integration)

```bash
npm run test:all
```

---

## 5. Chi Tiết Từng File Test

---

### PYTHON — Unit Tests

---

#### `tests/unit/test_auth.py` — Kiểm tra TokenManager

**Mục đích:** TokenManager là bộ phận lưu access token trong bộ nhớ và cấp token cho mỗi request. File này đảm bảo việc lưu/xóa token hoạt động đúng, kể cả khi nhiều thread truy cập đồng thời (thread-safe).

| Test case                   | Làm gì                                   | Kiểm tra điều gì                                                    |
| --------------------------- | ------------------------------------------ | ----------------------------------------------------------------------- |
| `test_initial_token_none` | Tạo `TokenManager()` không truyền gì | Token ban đầu phải là `None`                                      |
| `test_initial_token_set`  | Tạo `TokenManager("tok_abc")`           | Token được lưu đúng từ constructor                               |
| `test_set_token`          | Gọi `tm.set_token("tok_xyz")`           | Token thay đổi thành công                                           |
| `test_clear_token`        | Gọi `tm.clear()`                        | Token bị xóa,`get_token()` trả về `None`                        |
| `test_thread_safety`      | 2 thread đọc/ghi đồng thời 100 lần   | Không crash, không lỗi race condition, mọi giá trị đều hợp lệ |

---

#### `tests/unit/test_exceptions.py` — Kiểm tra hệ thống Error

**Mục đích:** SDK định nghĩa 3 loại lỗi riêng biệt để người dùng có thể bắt đúng loại lỗi mà không cần parse message. File này đảm bảo hệ thống lỗi đúng cấu trúc.

| Loại lỗi       | Khi nào xảy ra                                      |
| ---------------- | ----------------------------------------------------- |
| `AuthError`    | Server trả 401, 403 — token hết hạn hoặc sai     |
| `ApiError`     | Server trả 4xx, 5xx khác — lỗi logic hoặc server |
| `NetworkError` | Mất kết nối, timeout, server không phản hồi     |

| Test case                                         | Làm gì                            | Kiểm tra điều gì                                                                             |
| ------------------------------------------------- | ----------------------------------- | ------------------------------------------------------------------------------------------------ |
| `test_hierarchy`                                | Kiểm tra `issubclass`            | Cả 3 đều là subclass của `ImbraceError` → có thể `except ImbraceError` bắt tất cả |
| `test_api_error_message`                        | Tạo `ApiError(404, "Not Found")` | `status_code == 404`, message chứa `[404]` và `Not Found`                                |
| `test_auth_error_is_catchable_as_imbrace_error` | Raise `AuthError`                 | Bắt được bằng `except ImbraceError`                                                       |
| `test_network_error`                            | Tạo `NetworkError("timeout")`    | Message chứa "timeout"                                                                          |

---

#### `tests/unit/test_http.py` — Kiểm tra lớp HTTP (quan trọng nhất)

**Mục đích:** `HttpTransport` là lõi của SDK — mọi request đều đi qua đây. File này dùng `pytest-httpx` để giả lập server và kiểm tra: gắn header auth, retry khi lỗi, xử lý timeout, chuyển HTTP status thành đúng exception.

**Cách hoạt động của mock:**

```python
httpx_mock.add_response(status_code=500, text="Server Error")
# → Khi SDK gọi request, nhận được response 500 giả lập
# → Không có network request thật nào xảy ra
```

| Test case                                  | Kịch bản giả lập                        | Kiểm tra điều gì                                                       |
| ------------------------------------------ | ------------------------------------------- | -------------------------------------------------------------------------- |
| `test_get_success`                       | Server trả 200 + JSON                      | Response được parse, data đúng                                        |
| `test_sets_api_key_header`               | Request với `api_key="key_test"`         | Header `x-access-token: key_test` phải có trong request                |
| `test_sets_bearer_token_header`          | Request với access token                   | Header `x-access-token: tok_test` được gắn (token đè lên api key) |
| `test_no_bearer_when_token_cleared`      | Không có token                            | Header `Authorization` KHÔNG được gắn vào request                  |
| `test_401_raises_auth_error`             | Server trả 401                             | SDK raise `AuthError` (không retry)                                     |
| `test_403_raises_auth_error`             | Server trả 403                             | SDK raise `AuthError` (không retry)                                     |
| `test_404_raises_api_error`              | Server trả 404                             | SDK raise `ApiError` với `status_code == 404` (không retry)          |
| `test_500_retries_then_raises`           | Server trả 500 liên tiếp**3 lần** | SDK retry 2 lần → tổng 3 request → rồi raise `ApiError`             |
| `test_network_error_retries_then_raises` | Mạng bị ngắt**3 lần**             | SDK retry 2 lần → tổng 3 lần → raise `NetworkError`                 |
| `test_close`                             | Gọi `transport.close()`                  | Không crash, đóng HTTP session thành công                             |

---

#### `tests/unit/test_client.py` — Kiểm tra khởi tạo Client

**Mục đích:** Đảm bảo `ImbraceClient` và `AsyncImbraceClient` đọc config đúng, khởi tạo đủ 18+ resources, xử lý trailing slash trong URL.

| Test case                               | Làm gì                                | Kiểm tra điều gì                                                                                 |
| --------------------------------------- | --------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `test_default_base_url`               | Tạo client không có baseUrl          | `base_url == "https://app-gatewayv2.imbrace.co"`                                                   |
| `test_custom_base_url`                | Truyền URL có dấu `/` ở cuối     | Trailing slash bị strip →`"https://staging.imbrace.co"`                                          |
| `test_reads_api_key_from_env`         | Set env `IMBRACE_API_KEY=env_key`     | Client đọc được key từ environment variable                                                    |
| `test_explicit_api_key_overrides_env` | Truyền key trực tiếp khi có env     | Tham số trực tiếp được ưu tiên hơn env var                                                  |
| `test_reads_base_url_from_env`        | Set env `IMBRACE_BASE_URL`            | Client dùng URL từ environment                                                                     |
| `test_all_resources_initialized`      | Tạo client                             | Tất cả resources (`sessions`, `messages`, `health`, `channel`...) đều được khởi tạo |
| `test_set_access_token`               | Gọi `set_access_token("new_token")`  | `token_manager.get_token()` trả về token mới                                                    |
| `test_clear_access_token`             | Gọi `clear_access_token()`           | Token bị xóa, request tiếp theo không có Bearer header                                          |
| `test_context_manager`                | Dùng `with ImbraceClient(...) as c:` | Client tự gọi `close()` khi ra khỏi block                                                       |
| `test_async_client_*`                 | Tương tự với `AsyncImbraceClient` | Async client cũng hoạt động đúng                                                               |

---

#### `tests/unit/resources/test_account.py`

**Mục đích:** Kiểm tra `GET /v1/backend/account` — lấy thông tin account hiện tại.

| Test case            | Kiểm tra điều gì                                           |
| -------------------- | -------------------------------------------------------------- |
| `test_get_account` | Gọi đúng `GET /v1/backend/account`, response parse đúng |

---

#### `tests/unit/resources/test_agent.py`

**Mục đích:** Kiểm tra CRUD cho AI Agent (Templates) — `GET/POST/PATCH/DELETE /v2/backend/templates`.

| Test case                  | Kiểm tra điều gì                                 |
| -------------------------- | ---------------------------------------------------- |
| `test_list_agents`       | `GET /v2/backend/templates` trả list đúng       |
| `test_get_agent`         | `GET /v2/backend/templates/{id}` với đúng ID    |
| `test_create_agent`      | `POST /v2/backend/templates/custom` với body JSON |
| `test_update_agent`      | `PATCH /v2/backend/templates/{id}/custom`          |
| `test_delete_agent`      | `DELETE /v2/backend/templates/{id}`                |
| `test_sends_auth_header` | Mọi request đều có `x-access-token`            |

---

#### `tests/unit/resources/test_channel.py`

**Mục đích:** Kiểm tra channel management — list, get, create (web), update, delete, conversation count.

| Test case                        | Kiểm tra điều gì                                     |
| -------------------------------- | -------------------------------------------------------- |
| `test_list_channels`           | `GET /v1/backend/channels` trả data đúng            |
| `test_list_channels_with_type` | URL có query `?type=web` khi truyền `type="web"`   |
| `test_get_channel`             | `GET /v1/backend/channels/{id}` với đúng channel ID |
| `test_get_conv_count`          | `GET /v1/backend/channels/_conv_count?view=all`        |
| `test_delete_channel`          | Method là `DELETE`, URL đúng                        |

---

#### `tests/unit/resources/test_contacts.py`

**Mục đích:** Kiểm tra contacts và notification management.

| Test case                          | Kiểm tra điều gì                                              |
| ---------------------------------- | ----------------------------------------------------------------- |
| `test_list_contacts`             | `GET /v1/backend/contacts?limit=20&skip=0`                      |
| `test_list_contacts_pagination`  | Params `limit=10&skip=5` đúng trong URL                       |
| `test_search_contacts`           | `GET /contacts/_search?q=alice`                                 |
| `test_update_contact`            | Method `PUT`, body JSON `{"name": "Bob"}` được gửi đúng |
| `test_get_contact_conversations` | `GET /contacts/{id}/conversations`                              |
| `test_list_notifications`        | `GET /v1/backend/notifications?limit=20&skip=0`                 |
| `test_mark_notifications_read`   | `DELETE /notifications/dismiss` (đúng method theo docs)       |

---

#### `tests/unit/resources/test_boards.py`

**Mục đích:** Kiểm tra toàn bộ Board CRUD — tạo board, thêm/sửa/xóa board items, tìm kiếm, export.

| Test case                  | Kiểm tra điều gì                                         |
| -------------------------- | ------------------------------------------------------------ |
| `test_list_boards`       | `GET /v1/backend/board?limit=20&skip=0`                    |
| `test_list_board_items`  | `GET /v1/backend/board/{id}/board_items`                   |
| `test_create_board_item` | `POST /v1/backend/board/{id}/board_items` với body đúng |
| `test_search_board`      | `POST /v1/backend/meilisearch/{id}/search`                 |
| `test_export_csv`        | `GET /v1/backend/board/{id}/export_csv` trả text          |

---

#### `tests/unit/resources/test_conversations.py`

**Mục đích:** Kiểm tra conversation endpoints — view count, tạo conversation, tìm kiếm.

| Test case                     | Kiểm tra điều gì                                           |
| ----------------------------- | -------------------------------------------------------------- |
| `test_get_views_count`      | `GET /v2/backend/team_conversations/_views_count`            |
| `test_create_conversation`  | `POST /v1/backend/conversation`                              |
| `test_search_conversations` | `POST /v1/backend/meilisearch/{org}/search` với body đúng |

---

#### `tests/unit/resources/test_messages.py`

**Mục đích:** Kiểm tra list và gửi message.

| Test case                         | Kiểm tra điều gì                                            |
| --------------------------------- | --------------------------------------------------------------- |
| `test_list_messages`            | `GET /v1/backend/conversation_messages?limit=10&skip=0`       |
| `test_list_messages_pagination` | Params pagination đúng                                        |
| `test_send_message_text`        | `POST /v1/backend/conversation_messages` với `type="text"` |
| `test_send_message_image`       | Body có `type="image"` và `url`                           |

---

#### `tests/unit/resources/test_teams.py`

**Mục đích:** Kiểm tra team management — list, list my teams, add/remove users.

| Test case              | Kiểm tra điều gì                                                    |
| ---------------------- | ----------------------------------------------------------------------- |
| `test_list_teams`    | `GET /v2/backend/teams?limit=20&skip=0`                               |
| `test_list_my_teams` | `GET /v2/backend/teams/my`                                            |
| `test_add_users`     | `POST /v2/backend/teams/_add_users` với body `{team_id, user_ids}` |
| `test_remove_users`  | `POST /v2/backend/teams/_remove_users`                                |

---

#### `tests/unit/resources/test_settings.py`

**Mục đích:** Kiểm tra message templates và user management.

| Test case                                          | Kiểm tra điều gì                                     |
| -------------------------------------------------- | -------------------------------------------------------- |
| `test_list_message_templates`                    | `GET /v2/backend/message_templates?limit=20&skip=0`    |
| `test_list_message_templates_with_business_unit` | Query `business_unit_id` được thêm vào URL        |
| `test_list_users`                                | `GET /v1/backend/users?limit=20&skip=0`                |
| `test_list_users_with_search`                    | Query `search=` được thêm vào URL                 |
| `test_get_roles_count`                           | `GET /v1/backend/users/_roles_count`                   |
| `test_bulk_invite`                               | `POST /v1/backend/users/_bulk_invite` với body emails |

---

#### `tests/unit/resources/test_workflows.py`

**Mục đích:** Kiểm tra workflow management và n8n integration.

| Test case                        | Kiểm tra điều gì                             |
| -------------------------------- | ------------------------------------------------ |
| `test_list_workflows`          | `GET /v1/backend/workflows` với params đúng |
| `test_list_workflows_with_tag` | Query `tag=` được thêm vào URL            |
| `test_list_channel_automation` | `GET /v1/backend/workflows/channel_automation` |
| `test_list_n8n_workflows`      | `GET /v1/backend/n8n/workflows`                |

---

#### `tests/unit/resources/test_organizations.py`

| Test case                                     | Kiểm tra điều gì                              |
| --------------------------------------------- | ------------------------------------------------- |
| `test_list_organizations`                   | `GET /v2/backend/organizations?limit=20&skip=0` |
| `test_list_organizations_pagination`        | Params pagination đúng                          |
| `test_list_organizations_sends_auth_header` | Header `x-access-token` có trong request       |

---

#### `tests/unit/resources/test_sessions.py`

| Test case                             | Kiểm tra điều gì           |
| ------------------------------------- | ------------------------------ |
| `test_list_sessions`                | `GET /session`               |
| `test_list_sessions_with_directory` | Query `directory=` trong URL |

---

### PYTHON — Integration Test

---

#### `tests/integration/test_integration.py` — Gọi thật vào server

**Mục đích:** Xác nhận SDK hoạt động end-to-end với server thật. Nếu unit test pass mà integration test fail → vấn đề ở server/auth, không phải SDK.

**Điều kiện chạy:** `IMBRACE_API_KEY` phải được set, key còn hạn.
**Tự động skip** nếu `IMBRACE_API_KEY` trống.

| Test case                       | Endpoint gọi thật                                 | Kiểm tra gì ở response                    |
| ------------------------------- | --------------------------------------------------- | -------------------------------------------- |
| `test_get_account`            | `GET /v1/backend/account`                         | Response có `id`, `_id`, hoặc `data` |
| `test_list_channels`          | `GET /v1/backend/channels?type=web`               | Response là `dict`                        |
| `test_list_agents`            | `GET /v2/backend/templates`                       | Response là `dict`                        |
| `test_list_teams`             | `GET /v2/backend/teams`                           | Response là `dict`                        |
| `test_list_my_teams`          | `GET /v2/backend/teams/my`                        | Response là `dict`                        |
| `test_list_contacts`          | `GET /v1/backend/contacts?limit=5`                | Response là `dict`                        |
| `test_get_views_count`        | `GET /v2/backend/team_conversations/_views_count` | Response là `dict`                        |
| `test_list_messages`          | `GET /v1/backend/conversation_messages?limit=5`   | Response là `dict`                        |
| `test_list_boards`            | `GET /v1/backend/board`                           | Response là `dict`                        |
| `test_list_users`             | `GET /v1/backend/users?limit=5`                   | Response là `dict`                        |
| `test_list_message_templates` | `GET /v2/backend/message_templates`               | Response là `dict`                        |

---

### TYPESCRIPT — Unit Tests

---

#### `tests/unit/errors.test.ts`

Tương đương `test_exceptions.py` — kiểm tra `AuthError`, `ApiError`, `NetworkError` kế thừa đúng `ImbraceError` và message đúng format.

#### `tests/unit/http.test.ts`

Tương đương `test_http.py` — mock `globalThis.fetch` thay vì `pytest-httpx`. Kiểm tra:

- Header `x-access-token` được gắn từ `apiKey`
- Header `authorization: Bearer` được gắn từ `accessToken`
- Retry 2 lần khi 429 hoặc 5xx
- `AbortController` hủy request khi timeout
- Raise đúng error class cho từng HTTP status

#### `tests/unit/client.test.ts`

Tương đương `test_client.py` — kiểm tra khởi tạo, env vars, strip trailing slash, set/clear token, `checkHealth`.

#### `tests/unit/auth.test.ts`

Tương đương `test_auth.py` — kiểm tra set/get/clear token trên `TokenManager`.

#### `tests/unit/resources/*.test.ts` (19 files)

Tương đương `tests/unit/resources/test_*.py` — mock `globalThis.fetch` để kiểm tra URL, method, headers, body của từng API call.

#### `tests/integration/integration.test.ts`

Tương đương `tests/integration/test_integration.py` — gọi thật vào server. Tự skip nếu `IMBRACE_API_KEY` không set.

---

## 6. Lint & Type Check

### Python

```bash
cd D:/HUANGJUNFENG/sdk/py

# Kiểm tra code style và deprecated syntax
ruff check src/ tests/

# Tự động fix lỗi ruff có thể sửa
ruff check src/ tests/ --fix

# Kiểm tra type annotations
mypy src/imbrace
```

### TypeScript

```bash
cd D:/HUANGJUNFENG/sdk/ts

# Lint
npm run lint

# Type check (bao gồm cả tests/)
npm run typecheck

# Build (compile ra JS để phân phối)
npm run build
```

---

## 7. Lỗi Thường Gặp

### `AuthError: Invalid or expired access token.` (HTTP 401)

**Nguyên nhân:** API key trong `.env` đã hết hạn.
**Fix:** Liên hệ backend team lấy key mới, cập nhật `IMBRACE_API_KEY` trong `.env`.

---

### `ApiError: [400] {"message":"must have required property 'type'"}`

**Nguyên nhân:** Gọi `channel.list()` không truyền param bắt buộc `type`.
**Fix:**

```python
# Sai
client.channel.list()

# Đúng
client.channel.list(type="web")
```

---

### `ApiError: [404]` với URL có path kép

**Ví dụ URL lỗi:** `.../private/backend/v1/thrid_party_token/v1/backend/account`

**Nguyên nhân:** `IMBRACE_BASE_URL` trong `.env` bị set nhầm thành URL endpoint đầy đủ.
**Fix:** Sửa `.env`:

```env
# Sai
IMBRACE_BASE_URL=https://app-gatewayv2.imbrace.co/private/backend/v1/thrid_party_token

# Đúng
IMBRACE_BASE_URL=https://app-gatewayv2.imbrace.co
```

---

### `mypy` báo lỗi `Pattern matching is only supported in Python 3.10`

**Nguyên nhân:** mypy scan nhầm vào file nội bộ của pytest trong `site-packages`.
**Fix:** Đã được cấu hình trong `pyproject.toml`. Nếu vẫn lỗi:

```bash
mypy src/imbrace --exclude site-packages
```

---

### Integration test bị skip toàn bộ

**Nguyên nhân:** `IMBRACE_API_KEY` chưa được set trong environment.
**Fix:**

```bash
# Set tạm thời
IMBRACE_API_KEY=api_xxx pytest tests/integration -v -m integration

# Hoặc thêm vào .env (SDK tự đọc)
echo "IMBRACE_API_KEY=api_xxx" >> py/.env
```

---

### `Cannot find module '../../src/client.js'` (TypeScript tests)

**Nguyên nhân:** Import path sai trong test file sau khi tổ chức lại thư mục.
**Quy tắc đường dẫn:**

| Vị trí test file                 | Import src file                 |
| ---------------------------------- | ------------------------------- |
| `tests/unit/*.test.ts`           | `../../src/x.js`              |
| `tests/unit/resources/*.test.ts` | `../../../src/resources/x.js` |
| `tests/integration/*.test.ts`    | `../../src/x.js`              |
