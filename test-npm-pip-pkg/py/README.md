# Imbrace SDK — PIP Integration Test Suite (Python)

Bộ công cụ kiểm thử tích hợp (Integration Test) dành cho Imbrace Python SDK, xác thực gói cài đặt từ registry PyPI trên môi trường người dùng cuối.

---

## 1. Mục tiêu

- Xác thực toàn bộ logic SDK sau khi cài đặt qua PIP.
- Đảm bảo tính ổn định của các luồng nghiệp vụ quan trọng (Full Flow) trên môi trường production.

---

## 2. Thiết lập môi trường

### Prerequisites
- Python 3.10+
- pip

### Cấu hình `.env`
Tạo file `.env` tại thư mục này (copy từ `.env.example`):

```env
IMBRACE_API_KEY=your_api_key_here
# hoặc dùng Access Token:
IMBRACE_ACCESS_TOKEN=your_access_token_here

IMBRACE_ORGANIZATION_ID=your_org_id_here
IMBRACE_GATEWAY_URL=https://app-gatewayv2.imbrace.co
IMBRACE_TIMEOUT=30
```

### Cài đặt

```bash
pip install -r requirements.txt
```

> `requirements.txt` đã bao gồm `imbrace` từ PyPI và các dependencies cần thiết.

---

## 3. Chạy toàn bộ Test Suite

```bash
# Windows (fix encoding emoji)
$env:PYTHONIOENCODING="utf-8"; python -m pytest tests/test_all.py -s -v

# Linux / macOS
PYTHONIOENCODING=utf-8 python -m pytest tests/test_all.py -s -v
```

---

## 4. Chạy từng Module đơn lẻ

> **Lưu ý:** Luôn set `PYTHONIOENCODING=utf-8` trên Windows để tránh lỗi emoji encoding.

### Cú pháp chuẩn (pytest — khuyên dùng)

```bash
$env:PYTHONIOENCODING="utf-8"; python -m pytest tests/<tên_file>.py -s -v
```

### Danh sách đầy đủ tất cả test modules

| Lệnh | Mô tả |
|------|-------|
| `python -m pytest tests/test_auth.py -s -v` | Auth: OTP, login, token management |
| `python -m pytest tests/test_platform.py -s -v` | Platform: get_me, users, orgs, teams |
| `python -m pytest tests/test_marketplace.py -s -v` | Marketplace: products, orders |
| `python -m pytest tests/test_crm.py -s -v` | CRM: contacts, conversations, messages, workflows |
| `python -m pytest tests/test_crm_advanced.py -s -v` | CRM nâng cao: activities, comments, board relations |
| `python -m pytest tests/test_boards.py -s -v` | Boards: CRUD, fields, items, segments, folders |
| `python -m pytest tests/test_chat_ai.py -s -v` | Chat AI: assistants, sessions, models, document AI |
| `python -m pytest tests/test_ai_raw.py -s -v` | AI raw: completions, streaming, embeddings, guardrails |
| `python -m pytest tests/test_ai_agent.py -s -v` | AI Agent: health, chat v1/v2, embeddings, parquet, tracing |
| `python -m pytest tests/test_frontend_sdk.py -s -v` | Frontend SDK: chat client auth, chats, messages, votes, documents |
| `python -m pytest tests/test_multi_agent.py -s -v` | Multi-Agent / Sub-agent chat |
| `python -m pytest tests/test_agent.py -s -v` | Agent templates và runs |
| `python -m pytest tests/test_activepieces.py -s -v` | Activepieces: flows, triggers, runs |
| `python -m pytest tests/test_file_service.py -s -v` | File service: upload, list, delete |
| `python -m pytest tests/test_settings.py -s -v` | Settings: message templates, WA templates, users |
| `python -m pytest tests/test_campaign.py -s -v` | Campaigns và touchpoints |
| `python -m pytest tests/test_misc.py -s -v` | Misc: predict, message suggestion, IPS, license |
| `python -m pytest tests/test_multimedia_ai.py -s -v` | Multimedia AI (vision, audio) |
| `python -m pytest tests/test_error_paths.py -s -v` | Error handling: AuthError, ApiError, NetworkError |
| `python -m pytest tests/test_async.py -s -v` | Async client (AsyncImbraceClient) |
| `python -m pytest tests/test_full_flow_guide.py -s -v` | Full Flow: Assistant → RAG → Board → Chat (E2E) |

---

## 5. Chạy nhóm test (nhanh / đầy đủ)

```bash
# Chỉ Auth + Platform + Marketplace (nhanh ~5s)
$env:PYTHONIOENCODING="utf-8"; python -m pytest tests/test_auth.py tests/test_platform.py tests/test_marketplace.py -s -v

# CRM group
$env:PYTHONIOENCODING="utf-8"; python -m pytest tests/test_crm.py tests/test_crm_advanced.py tests/test_boards.py -s -v

# AI group
$env:PYTHONIOENCODING="utf-8"; python -m pytest tests/test_ai_raw.py tests/test_chat_ai.py tests/test_ai_agent.py -s -v

# Frontend / Agent group
$env:PYTHONIOENCODING="utf-8"; python -m pytest tests/test_frontend_sdk.py tests/test_multi_agent.py tests/test_agent.py -s -v
```

---

## 6. Cách chạy thay thế (không dùng pytest)

```bash
# Chạy trực tiếp từng file
python tests/test_auth.py
python tests/test_crm.py
python tests/test_all.py
```

---

## 7. Cấu trúc thư mục

```
test-npm-pip-pkg/py/
├── .env                  # Config (API key, org ID, gateway URL)
├── .env.example          # Template
├── requirements.txt      # Dependencies (imbrace từ PyPI + pytest + dotenv)
├── utils/
│   └── utils.py          # Client init, run_test_section, log_result helpers
└── tests/
    ├── test_all.py               # Runner tổng hợp toàn bộ modules
    ├── test_auth.py              # Auth methods
    ├── test_platform.py          # Platform & teams
    ├── test_marketplace.py       # Marketplace
    ├── test_crm.py               # CRM core
    ├── test_crm_advanced.py      # CRM nâng cao
    ├── test_boards.py            # Data Boards
    ├── test_chat_ai.py           # Chat AI (aiv2)
    ├── test_ai_raw.py            # AI raw completions
    ├── test_ai_agent.py          # AI Agent service
    ├── test_frontend_sdk.py      # Chat Client sub-API
    ├── test_multi_agent.py       # Multi/Sub-agent
    ├── test_agent.py             # Agent templates
    ├── test_activepieces.py      # Activepieces
    ├── test_file_service.py      # File uploads
    ├── test_settings.py          # Org settings
    ├── test_campaign.py          # Campaigns
    ├── test_misc.py              # Misc resources
    ├── test_multimedia_ai.py     # Multimedia AI
    ├── test_error_paths.py       # Error handling
    ├── test_async.py             # Async client
    └── test_full_flow_guide.py   # E2E full flow
```
