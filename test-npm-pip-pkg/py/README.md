# Imbrace Python SDK — PyPI Package Test Suite

Bộ kiểm thử tích hợp cho **imbrace** Python SDK, cài đặt trực tiếp từ PyPI. Dùng để xác nhận SDK đã publish hoạt động đúng trên môi trường thực.

---

## 1. Thiết lập

### Yêu cầu
- Python 3.10+
- pip

### Cấu hình `.env`
```env
IMBRACE_ACCESS_TOKEN=your_access_token_here
IMBRACE_ORGANIZATION_ID=your_org_id_here
IMBRACE_GATEWAY_URL=https://app-gatewayv2.imbrace.co
IMBRACE_TIMEOUT=30
# IMBRACE_SKIP_UNSTABLE=1
```

### Cài đặt
```bash
pip install -r requirements.txt
```
> SDK được cài từ PyPI: `imbrace` (phiên bản mới nhất)

---

## 2. Chạy Test

> **Windows:** Thêm `$env:PYTHONIOENCODING="utf-8";` trước lệnh để tránh lỗi hiển thị emoji.
> **Flag `-s -v` đã được tích hợp sẵn** trong `pytest.ini`.

### ⭐ Full Flow Guide
```bash
# Windows
$env:PYTHONIOENCODING="utf-8"; pytest tests/test_full_flow_guide.py

# Linux / macOS
pytest tests/test_full_flow_guide.py
```

### 🚀 Toàn bộ Test Suite
```bash
# Windows
$env:PYTHONIOENCODING="utf-8"; pytest tests/test_all.py

# Nhanh hơn (bỏ qua 502):
$env:PYTHONIOENCODING="utf-8"; $env:IMBRACE_SKIP_UNSTABLE="1"; pytest tests/test_all.py

# Linux / macOS
IMBRACE_SKIP_UNSTABLE=1 pytest tests/test_all.py
```

---

## 3. Tình trạng Backend (prodv2)

| Trạng thái | Dịch vụ |
|-----------|---------|
| ✅ Hoạt động | `auth`, `chat_ai`, `ai`, `ai_agent`, `boards`, `activepieces`, `marketplace`, `crm` |
| ⚠️ 502 (down) | `account`, `channel`, `campaign`, `organizations`, `categories`, `outbound` |
| 🔴 404 (route missing) | `sessions`, `marketplace.orders`, `chat_ai /v3/` routes |

---

## 4. Quy tắc đồng bộ

> Bộ test này phải **luôn giống hệt** `test-local-pkg/py`. **Không sửa trực tiếp tại đây.**

```powershell
Copy-Item "test-local-pkg\py\tests\*" "test-npm-pip-pkg\py\tests" -Force
Copy-Item "test-local-pkg\py\utils\utils.py" "test-npm-pip-pkg\py\utils\utils.py" -Force
Write-Host "✅ Sync done."
```

Xem README đầy đủ tại: [`test-local-pkg/py/README.md`](../../test-local-pkg/py/README.md)
