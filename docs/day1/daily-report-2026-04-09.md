# Daily Report — 2026-04-09

**Project:** iMBRACE SDK (TypeScript & Python)
**Người thực hiện:** hoangtuanphong1a

---

## Hôm qua làm gì

- Viết lại toàn bộ SDK đa ngôn ngữ (TypeScript + Python) để mapping đúng với backend thực tế dựa trên 114 API docs
- Cập nhật endpoint cho các resource: Agent, Conversations, Messages, Teams, Boards, Settings
- Viết unit test cho cả 2 SDK:
  - Python: 95 tests (12 file)
  - TypeScript: 98 tests (16 file)
- Viết integration test template sẵn sàng cho cả 2 SDK (tự skip nếu chưa có API key)
- Viết tài liệu: `document.md`, `progress-report.md`, `huong-dan-test-va-chay.md`

---

## Hôm nay làm gì

- Phát hiện và fix 2 bug trong `ts/src/http.ts` — HTTP header bị ghi sai tên:
  - `apiKey` đang set vào `x-access-token` → sửa thành `x-api-key`
  - `accessToken` đang set vào `x-access-token` → sửa thành `authorization: Bearer <token>`
- Fix cascading: test `setAccessToken` bị timeout 5000ms do assert fail không resolve Promise → tự khỏi sau khi fix header
- Cập nhật 3 file test resource (account, agent, messages) đang dùng tên header cũ trong assertion
- Kết quả sau fix: **TypeScript 98/98 tests pass**, không còn unhandled error
- Viết tài liệu phân tích bug: `docs/bug_TS_fix.md`

---

## Khó khăn

**1. API key hết hạn — chưa chạy được integration tests**

Key hiện tại `api_6e2447e0-...` đã hết hạn từ `2025-10-04`. Toàn bộ integration test Python trả về `401 Unauthorized`. Chưa thể xác nhận SDK hoạt động đúng với server thực.

→ Cần backend team cấp API key mới.

**2. Endpoint lấy API key mới chưa xác nhận**

`POST /private/backend/v1/thrid_party_token` trả về "API not found" khi test.

→ Cần xác nhận lại endpoint đúng với backend team.

**3. Hai lỗi nhỏ trong Python integration test (phát hiện hôm nay)**

- `client.channels.list()` → sai tên, phải là `client.channel.list()`
- `client.account.get_account()` → method không tồn tại trong `AccountResource`

→ Sẽ fix sau khi có API key để chạy kiểm tra thực tế.
