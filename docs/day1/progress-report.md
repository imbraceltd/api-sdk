# Báo Cáo Tiến Độ — iMBRACE SDK

**Ngày:** 2026-04-09
**Môi trường:** `https://app-gatewayv2.imbrace.co` (ServerGateway, dev)
**Organization:** `org_........`

---

## 1. Tổng Quan

SDK đa ngôn ngữ (Python + TypeScript) cho nền tảng iMBRACE đã được viết lại hoàn toàn để mapping đúng với hệ thống backend thực tế. Toàn bộ endpoint đã được cập nhật dựa trên 114 API docs trong `docs/API document/AppGeteway/`.

---

## 2. Thay Đổi Chính

### 2.1 Auth Header

| Trước                                   | Sau                            |
| ----------------------------------------- | ------------------------------ |
| `X-Api-Key` + `Authorization: Bearer` | `x-access-token` (duy nhất) |

### 2.2 Endpoint Mapping

| Resource      | Endpoint cũ (sai)       | Endpoint mới (đúng)                                   |
| ------------- | ------------------------ | -------------------------------------------------------- |
| Agent         | `/agent/agents`        | `/v2/backend/templates`                                |
| Conversations | `/conversations`       | `/v2/backend/team_conversations/_views_count`          |
| Messages      | `/session/:id/message` | `/v1/backend/conversation_messages`                    |
| Teams         | `/teams`               | `/v2/backend/teams`                                    |
| Boards        | `/boards`              | `/v1/backend/board`                                    |
| Settings      | —                       | `/v2/backend/message_templates`, `/v1/backend/users` |

---

## 3. File Đã Tạo / Cập Nhật

### Python (`py/`)

| File                                       | Trạng Thái           |
| ------------------------------------------ | ---------------------- |
| `src/imbrace/http.py`                    | Cập nhật auth header |
| `src/imbrace/client.py`                  | Viết lại toàn bộ   |
| `src/imbrace/async_client.py`            | Viết lại toàn bộ   |
| `src/imbrace/resources/auth.py`          | Mới                   |
| `src/imbrace/resources/account.py`       | Mới                   |
| `src/imbrace/resources/organizations.py` | Mới                   |
| `src/imbrace/resources/agent.py`         | Viết lại             |
| `src/imbrace/resources/channel.py`       | Viết lại             |
| `src/imbrace/resources/conversations.py` | Mới                   |
| `src/imbrace/resources/messages.py`      | Viết lại             |
| `src/imbrace/resources/contacts.py`      | Mới                   |
| `src/imbrace/resources/teams.py`         | Mới                   |
| `src/imbrace/resources/workflows.py`     | Mới                   |
| `src/imbrace/resources/boards.py`        | Mới                   |
| `src/imbrace/resources/settings.py`      | Mới                   |

### TypeScript (`ts/`)

| File                               | Trạng Thái           |
| ---------------------------------- | ---------------------- |
| `src/http.ts`                    | Cập nhật auth header |
| `src/client.ts`                  | Viết lại toàn bộ   |
| `src/types/index.ts`             | Viết lại toàn bộ   |
| `src/resources/auth.ts`          | Mới                   |
| `src/resources/account.ts`       | Mới                   |
| `src/resources/organizations.ts` | Mới                   |
| `src/resources/agent.ts`         | Viết lại             |
| `src/resources/channel.ts`       | Mới                   |
| `src/resources/conversations.ts` | Mới                   |
| `src/resources/messages.ts`      | Viết lại             |
| `src/resources/contacts.ts`      | Mới                   |
| `src/resources/teams.ts`         | Mới                   |
| `src/resources/workflows.ts`     | Mới                   |
| `src/resources/boards.ts`        | Mới                   |
| `src/resources/settings.ts`      | Mới                   |

---

## 4. Unit Tests

### Python — 11 file test

| File                                | Số Test      |
| ----------------------------------- | ------------- |
| `test_resources_agent.py`         | 5             |
| `test_resources_account.py`       | 2             |
| `test_resources_channel.py`       | 4             |
| `test_resources_messages.py`      | 5             |
| `test_resources_conversations.py` | 3             |
| `test_resources_teams.py`         | 4             |
| `test_resources_boards.py`        | 5             |
| `test_resources_contacts.py`      | 7             |
| `test_resources_workflows.py`     | 6             |
| `test_resources_settings.py`      | 8             |
| `test_resources_auth.py`          | 3             |
| `test_resources_organizations.py` | 3             |
| **Total**                     | **~55** |

### TypeScript — 9 file test

| File                      | Số Test      |
| ------------------------- | ------------- |
| `agent.test.ts`         | 6             |
| `account.test.ts`       | 2             |
| `channel.test.ts`       | 6             |
| `conversations.test.ts` | 4             |
| `messages.test.ts`      | 5             |
| `contacts.test.ts`      | 7             |
| `teams.test.ts`         | 4             |
| `boards.test.ts`        | 7             |
| `settings.test.ts`      | 8             |
| **Total**           | **~49** |

---

## 5. Integration Tests

Cả 2 SDK đều có integration test template sẵn sàng:

- **Python:** `py/tests/test_integration.py` — chạy với `pytest -m integration`
- **TypeScript:** `ts/src/__tests__/integration.test.ts` — chạy với `vitest run`

Test sẽ tự động skip nếu `IMBRACE_API_KEY` chưa được set.

---

## 6. Vấn Đề Còn Tồn Tại

| Vấn Đề                                                                           | Mức Độ      | Giải Pháp                            |
| ----------------------------------------------------------------------------------- | -------------- | -------------------------------------- |
| API key hết hạn (`2025-10-04`)                                                  | Cao            | Cần lấy key mới từ backend team    |
| Endpoint `/private/backend/v1/thrid_party_token` không tồn tại trên gatewayv2 | Trung bình    | Hỏi backend team endpoint chính xác |
| Integration tests chưa chạy được                                               | Phụ thuộc #1 | Cần API key mới                      |

---

## 7. Cách Chạy Tests

### Python

```bash
cd py
pip install -e ".[dev]"
pytest tests/ -v                     # unit tests
pytest tests/ -m integration -v      # integration tests (cần API key)
```

### TypeScript

```bash
cd ts
npm install
npm test                                        # unit tests
IMBRACE_API_KEY=api_xxx npx vitest run src/__tests__/integration.test.ts
```

---

## 8. Cách Lấy API Key Mới

```bash
curl -X POST https://app-gatewayv2.imbrace.co/private/backend/v1/thrid_party_token \
  -H "Content-Type: application/json" \
  -H "x-access-token: <current_key>" \
  -d '{"expirationDays": 10}'
```

> **Lưu ý:** Cần xác nhận endpoint chính xác với backend team vì endpoint này trả về "API not found" khi test.
