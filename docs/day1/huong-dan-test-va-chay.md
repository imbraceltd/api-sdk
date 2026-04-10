# Hướng Dẫn Chạy & Test — iMBRACE Python SDK

> Thư mục làm việc: `D:\HUANGJUNFENG\sdk\py`

---

## 1. Cài Đặt

```bash
# Di chuyển vào thư mục Python SDK
cd D:/HUANGJUNFENG/sdk/py

# Cài dependencies + dev tools
pip install -e ".[dev]"
```

---

## 2. Cấu Hình Môi Trường

Tạo file `.env` trong `py/`:

```env
IMBRACE_API_KEY=api_xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
IMBRACE_BASE_URL=https://app-gatewayv2.imbrace.co
IMBRACE_ORG_ID=org_xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

> Lấy API key mới:
>
> ```
> POST https://app-gatewayv2.imbrace.co/private/backend/v1/thrid_party_token
> Body: {"expirationDays": 10}
> Header: x-access-token: <key_hien_tai>
> ```

---

## 3. Chạy Tests

### 3.1 Chạy toàn bộ unit tests (không cần mạng)

```bash
pytest tests/ --ignore=tests/test_integration.py -v
```

Kết quả mong đợi: **95 passed**

---

### 3.2 Chạy từng nhóm test

```bash
# Test HTTP transport
pytest tests/test_http.py -v

# Test khởi tạo client
pytest tests/test_client.py -v

# Test từng resource
pytest tests/test_resources_messages.py -v
pytest tests/test_resources_contacts.py -v
pytest tests/test_resources_organizations.py -v
pytest tests/test_resources_teams.py -v
pytest tests/test_resources_boards.py -v
pytest tests/test_resources_settings.py -v
pytest tests/test_resources_sessions.py -v
pytest tests/test_resources_ai.py -v
pytest tests/test_resources_channel.py -v
pytest tests/test_resources_agent.py -v
pytest tests/test_resources_workflows.py -v
pytest tests/test_resources_auth.py -v
pytest tests/test_resources_conversations.py -v
```

---

### 3.3 Chạy integration tests (cần API key hợp lệ)

```bash
# Đặt API key trực tiếp
IMBRACE_API_KEY=api_xxx pytest tests/test_integration.py -v -m integration

# Hoặc dùng .env (đã có python-dotenv)

```

---

### 3.4 Các lệnh hữu ích

```bash
# Chạy nhanh, tắt output chi tiết
pytest tests/ --ignore=tests/test_integration.py -q

# Dừng ngay khi có 1 test fail
pytest tests/ --ignore=tests/test_integration.py -x

# Chỉ chạy test có tên chứa keyword
pytest tests/ -k "list" -v

# Xem coverage
pytest tests/ --ignore=tests/test_integration.py --cov=src/imbrace --cov-report=term-missing
```

---

## 4. Chạy SDK Thực Tế

### 4.1 Sync client

```python
from imbrace import ImbraceClient

client = ImbraceClient(api_key="api_xxx")

# Account
account = client.account.get()

# Channels (type bắt buộc: web, whatsapp, facebook, wechat, ...)
channels = client.channel.list(type="web")

# Teams
teams = client.teams.list(limit=10)
my_teams = client.teams.list_my()

# Contacts
contacts = client.contacts.list(limit=20)
found = client.contacts.search("alice")

# Messages
messages = client.messages.list(limit=5)
client.messages.send(type="text", text="Hello!")

# Boards
boards = client.boards.list()
items = client.boards.list_items("board_id_here")

# Settings
users = client.settings.list_users(limit=10)
templates = client.settings.list_message_templates()

# Sessions
sessions = client.sessions.list()

# AI
result = client.ai.complete(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}]
)

client.close()
```

### 4.2 Async client

```python
import asyncio
from imbrace import AsyncImbraceClient

async def main():
    async with AsyncImbraceClient(api_key="api_xxx") as client:
        account = await client.account.get()
        messages = await client.messages.list(limit=5)
        print(account, messages)

asyncio.run(main())
```

### 4.3 Dùng Access Token (thay cho API key)

```python
client = ImbraceClient()
client.set_access_token("eyJhbGci...")

# Hoặc truyền vào constructor
client = ImbraceClient(access_token="eyJhbGci...")
```

---

## 5. Xử Lý Lỗi

```python
from imbrace import ImbraceClient, AuthError, ApiError, NetworkError

client = ImbraceClient(api_key="api_xxx")

try:
    result = client.teams.list()
except AuthError:
    print("API key hết hạn hoặc không hợp lệ")
except ApiError as e:
    print(f"Lỗi API: {e.status_code} — {e}")
except NetworkError as e:
    print(f"Lỗi mạng/timeout: {e}")
```

---

## 7. Lỗi Thường Gặp khi Chạy Integration Tests

### `AuthError: Invalid or expired access token.` (HTTP 401)

**Nguyên nhân:** API key trong `.env` đã hết hạn.

**Cách fix:** Lấy key mới (xem mục 2), cập nhật `IMBRACE_API_KEY` trong `.env`.

---

### `ApiError: [400] must have required property 'type'` — `test_list_channels`

**Nguyên nhân:** API `GET /v1/backend/channels` bắt buộc phải có query param `type`.

**Cách fix:** Truyền `type` khi gọi `channel.list()`:

```python
# Sai — server trả 400
client.channel.list()

# Đúng — các giá trị hợp lệ: web, whatsapp, facebook, wechat, ...
client.channel.list(type="web")
```

Nếu đang viết integration test, cập nhật lại:

```python
def test_list_channels(client):
    result = client.channel.list(type="web")
    assert isinstance(result, dict)
```

---

## 6. Lint & Type Check

```bash
# Kiểm tra code style
ruff check src/ tests/

# Kiểm tra kiểu dữ liệu
mypy src/imbrace
```
