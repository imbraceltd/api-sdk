# Imbrace Python SDK — Local Integration Test Suite

Bộ kiểm thử tích hợp cho **imbrace** Python SDK, cài đặt từ file wheel cục bộ (`.whl`) trước khi publish lên PyPI.

---

## 1. Thiết lập

### Yêu cầu
- Python 3.10+
- pip

### Cấu hình `.env`
Copy `.env.example` thành `.env`:

```env
IMBRACE_ACCESS_TOKEN=your_access_token_here
# hoặc:
# IMBRACE_API_KEY=your_api_key_here

IMBRACE_ORGANIZATION_ID=your_org_id_here
IMBRACE_GATEWAY_URL=https://app-gatewayv2.imbrace.co
IMBRACE_TIMEOUT=30

# Bật để bỏ qua các endpoint đang bị 502 (tiết kiệm thời gian chờ retry):
# IMBRACE_SKIP_UNSTABLE=1
```

### Cài đặt
**Bước 1** — Build SDK local (từ thư mục gốc SDK):
```bash
cd ../../py
python -m build
```

**Bước 2** — Cài đặt dependencies:
```bash
cd ../test-local-pkg/py
pip install -r requirements.txt
```
> SDK được cài từ file wheel: `../../py/dist/imbrace-*.whl`

---

## 2. Chạy Test

> **Windows:** Thêm `$env:PYTHONIOENCODING="utf-8";` trước lệnh để tránh lỗi hiển thị emoji.
> **Flag `-s -v` đã được tích hợp sẵn** trong `pytest.ini` — không cần gõ lại.

### ⭐ Full Flow Guide (Ưu tiên cao nhất)
```bash
# Windows
$env:PYTHONIOENCODING="utf-8"; pytest tests/test_full_flow_guide.py

# Linux / macOS
pytest tests/test_full_flow_guide.py
```
**Phủ:** Auth → Assistant → Knowledge Hub RAG → Board → Chat AI

---

### 🚀 Chạy toàn bộ Test Suite
```bash
# Windows
$env:PYTHONIOENCODING="utf-8"; pytest tests/test_all.py

# Linux / macOS
pytest tests/test_all.py
```

### 🚀 Chạy toàn bộ (bỏ qua endpoint 502, nhanh hơn ~10x)
```bash
# Windows
$env:PYTHONIOENCODING="utf-8"; $env:IMBRACE_SKIP_UNSTABLE="1"; pytest tests/test_all.py

# Linux / macOS
IMBRACE_SKIP_UNSTABLE=1 pytest tests/test_all.py
```

---

### 🧩 Danh sách đầy đủ các module

| Lệnh | Module | Trạng thái |
|------|--------|-----------|
| `pytest tests/test_auth.py` | Auth: OTP, login, token management | ✅ |
| `pytest tests/test_chat_ai.py` | Chat AI: assistants, models | ✅ |
| `pytest tests/test_chat_ai_extended.py` | Chat AI extended: files, audio, knowledge | ✅ |
| `pytest tests/test_ai_extended.py` | AI: guardrails, RAG, tools | ✅ |
| `pytest tests/test_ai_raw.py` | AI raw: completions, embeddings | ✅ |
| `pytest tests/test_ai_agent.py` | AI Agent: health, chat, embed, parquet, docs | ✅ |
| `pytest tests/test_boards.py` | Boards: CRUD, items, fields, folders | ✅ |
| `pytest tests/test_activepieces.py` | Activepieces: flows, runs, connections | ✅ |
| `pytest tests/test_marketplace.py` | Marketplace: products | ✅ |
| `pytest tests/test_frontend_sdk.py` | Frontend SDK: chat client, votes, documents | ✅ |
| `pytest tests/test_multi_agent.py` | Multi-Agent / Sub-agent | ✅ |
| `pytest tests/test_agent.py` | Agent templates | ✅ |
| `pytest tests/test_file_service.py` | File service: upload, list, delete | ✅ |
| `pytest tests/test_resources.py` | Resources: data_files, folders, schedule, IPS | ✅ |
| `pytest tests/test_crm.py` | CRM: contacts, conversations, messages | ✅ |
| `pytest tests/test_crm_advanced.py` | CRM Advanced: activities, comments | ✅ |
| `pytest tests/test_misc.py` | Misc: predict, suggestions, license | ✅ |
| `pytest tests/test_multimedia_ai.py` | Multimedia AI: vision, audio | ✅ |
| `pytest tests/test_settings.py` | Settings: message templates, users | ✅ |
| `pytest tests/test_error_paths.py` | Error handling: AuthError, ApiError | ✅ |
| `pytest tests/test_async.py` | Async client (AsyncImbraceClient) | ✅ |
| `pytest tests/test_platform.py` | Platform: users, orgs, teams | ⚠️ 502 |
| `pytest tests/test_account.py` | Account: get, update | ⚠️ 502 |
| `pytest tests/test_channel.py` | Channel: list, counts, credentials | ⚠️ 502 |
| `pytest tests/test_campaign.py` | Campaigns & touchpoints | ⚠️ 502 |
| `pytest tests/test_full_flow_guide.py` | ⭐ Full E2E flow | ✅ |

> **Ghi chú ⚠️ 502:** Các module này đang chờ backend team khôi phục dịch vụ trên prodv2.
> Dùng `IMBRACE_SKIP_UNSTABLE=1` để bỏ qua tự động.

---

### 🧩 Chạy theo nhóm

```bash
# Auth + Marketplace (nhanh ~5s)
$env:PYTHONIOENCODING="utf-8"; pytest tests/test_auth.py tests/test_marketplace.py

# AI group
$env:PYTHONIOENCODING="utf-8"; pytest tests/test_ai_raw.py tests/test_chat_ai.py tests/test_ai_agent.py

# CRM + Boards group
$env:PYTHONIOENCODING="utf-8"; pytest tests/test_crm.py tests/test_boards.py

# Frontend / Agent group
$env:PYTHONIOENCODING="utf-8"; pytest tests/test_frontend_sdk.py tests/test_multi_agent.py tests/test_agent.py
```

---

## 3. Tình trạng Backend (prodv2)

| Trạng thái | Dịch vụ |
|-----------|---------|
| ✅ Hoạt động | `auth`, `chat_ai`, `ai`, `ai_agent`, `boards`, `activepieces`, `marketplace`, `crm`, `data_files`, `folders`, `ips`, `schedule` |
| ⚠️ 502 (down) | `account`, `channel`, `campaign`, `organizations`, `categories`, `outbound` |
| 🔴 404 (route missing) | `sessions`, `marketplace.orders`, `chat_ai /v3/` routes |

---

## 4. Flag `IMBRACE_SKIP_UNSTABLE`

Bỏ qua các section đang bị 502 thay vì chờ retry timeout (~60s × 3 lần):

```
# test_all không dùng flag: ~13 phút
# test_all có flag:         ~2 phút
```

Khi backend fix xong, chỉ cần xóa biến này hoặc set về `0`.

---

## 5. Cấu trúc thư mục

```
test-local-pkg/py/
├── .env                        # Config cục bộ (không commit)
├── .env.example                # Template
├── pytest.ini                  # pythonpath=. và addopts=-s -v
├── requirements.txt
├── utils/
│   └── utils.py                # Client init, run_test_section, run_stable_section, log_result
└── tests/
    ├── test_all.py             # ▶ Runner tổng hợp
    ├── test_full_flow_guide.py # ⭐ Full E2E (PRIORITY)
    ├── test_auth.py
    ├── test_chat_ai.py
    ├── test_chat_ai_extended.py
    ├── test_ai_extended.py
    ├── test_ai_raw.py
    ├── test_ai_agent.py
    ├── test_boards.py
    ├── test_activepieces.py
    ├── test_resources.py
    ├── test_crm.py
    ├── test_crm_advanced.py
    ├── test_marketplace.py
    ├── test_frontend_sdk.py
    ├── test_multi_agent.py
    ├── test_agent.py
    ├── test_file_service.py
    ├── test_settings.py
    ├── test_campaign.py        # ⚠️ 502
    ├── test_channel.py         # ⚠️ 502
    ├── test_account.py         # ⚠️ 502
    ├── test_platform.py        # ⚠️ 502
    ├── test_misc.py
    ├── test_multimedia_ai.py
    ├── test_error_paths.py
    └── test_async.py
```

---

## 6. Quy tắc đồng bộ

> **Quan trọng:** Mọi thay đổi phải được áp dụng đồng thời cho cả `test-local-pkg/py` và `test-npm-pip-pkg/py`. **Không sửa trực tiếp** trong `test-npm-pip-pkg/py`.

```powershell
# Sync toàn bộ sau khi sửa
Copy-Item "test-local-pkg\py\tests\*" "test-npm-pip-pkg\py\tests" -Force
Copy-Item "test-local-pkg\py\utils\utils.py" "test-npm-pip-pkg\py\utils\utils.py" -Force
Write-Host "✅ Sync done."
```
