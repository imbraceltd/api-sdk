# Xử Lý Lỗi

> Các loại lỗi, hành vi retry tự động, và best practices khi xử lý lỗi với Imbrace SDKs.

Tất cả lỗi do SDK ném ra đều extend từ một base type chung, cho phép bắt mọi SDK error trong một chỗ hoặc phân nhánh theo subclass cụ thể khi cần xử lý khác nhau. Phân cấp lỗi giống nhau trên cả TypeScript và Python SDK.

## Phân Cấp Lỗi

```
Error
└── ImbraceError          (base — catch-all cho SDK errors)
    ├── AuthError          (401, 403 — credentials không hợp lệ hoặc hết hạn)
    ├── ApiError           (4xx/5xx — server từ chối request)
    └── NetworkError       (timeout, connection refused, DNS failure)
```

```
Exception
└── ImbraceError          (base — catch-all cho SDK errors)
    ├── AuthError          (401, 403 — credentials không hợp lệ hoặc hết hạn)
    ├── ApiError           (4xx/5xx — server từ chối request)
    └── NetworkError       (timeout, connection refused, DNS failure)
```

Để xem thông báo lỗi cụ thể và cách sửa, xem [Troubleshooting](/vi/guides/troubleshooting/).

---

## AuthError

Được ném/raise khi server trả về **401** hoặc **403** — credentials không hợp lệ, hết hạn, hoặc bị thu hồi.

```typescript

try {
  const me = await client.platform.getMe();
} catch (e) {
  if (e instanceof AuthError) {
    console.error("Cần xác thực lại:", e.message);
  }
}
```

```python
from imbrace import AuthError

try:
    me = client.platform.get_me()
except AuthError as e:
    print(f"Xác thực thất bại: {e}")
    # Cần xác thực lại trước khi thử tiếp
```

> `AuthError` **không bao giờ được retry**. SDK throw/raise ngay lập tức khi nhận 401/403 — cần fix credentials trước khi thử lại. Xem [Xác Thực](/vi/sdk/authentication/) để biết chiến lược credential.

---

## ApiError

Được ném cho tất cả **4xx và 5xx** khác (sau khi retry đã hết cho 429/5xx).

```typescript

try {
  await client.marketplace.getProduct("nonexistent_id");
} catch (e) {
  if (e instanceof ApiError) {
    console.error(`HTTP ${e.statusCode}: ${e.message}`);
    // Ví dụ: "HTTP 404: Product not found"
  }
}
```

| Property     | Type     | Mô tả                            |
| ------------ | -------- | -------------------------------- |
| `statusCode` | `number` | HTTP status code                 |
| `message`    | `string` | Thông báo lỗi từ server response |

```python
from imbrace import ApiError

try:
    client.marketplace.get_product("nonexistent_id")
except ApiError as e:
    print(f"HTTP {e.status_code}: {e}")
    # Ví dụ: "HTTP 404: Product not found"
```

| Attribute     | Type  | Mô tả                            |
| ------------- | ----- | -------------------------------- |
| `status_code` | `int` | HTTP status code                 |
| `message`    | `str` | Thông báo lỗi từ server response |

---

## NetworkError

Được ném khi request không đến được server — timeout, DNS failure, hoặc connection reset.

```typescript

try {
  await client.platform.getMe();
} catch (e) {
  if (e instanceof NetworkError) {
    console.error("Không thể kết nối baseUrl:", e.message);
    // Ví dụ: "Request timed out after 30000ms"
  }
}
```

```python
from imbrace import NetworkError

try:
    client.platform.get_me()
except NetworkError as e:
    print(f"Lỗi mạng: {e}")
    # Ví dụ: "Request timed out after 30s"
```

---

## Bắt Tất Cả SDK Errors

Import base type để xử lý bất kỳ SDK error nào trong một block:

```typescript
  ImbraceClient,
  ImbraceError,
  AuthError,
  ApiError,
  NetworkError,
} from "@imbrace/sdk";

try {
  await client.platform.getMe();
} catch (e) {
  if (e instanceof AuthError) return xử_lý_auth_error(e);
  if (e instanceof ApiError) return xử_lý_api_error(e);
  if (e instanceof NetworkError) return xử_lý_network_error(e);
  if (e instanceof ImbraceError) return xử_lý_lỗi_không_xác_định(e);
  throw e; // re-throw lỗi không phải SDK
}
```

```python
from imbrace import ImbraceError, AuthError, ApiError, NetworkError

try:
    result = client.platform.get_me()
except AuthError as e:
    xử_lý_auth_error(e)
except ApiError as e:
    xử_lý_api_error(e)
except NetworkError as e:
    xử_lý_network_error(e)
except ImbraceError as e:
    xử_lý_lỗi_không_xác_định(e)
```

---

## Hành Vi Retry Tự Động

HTTP transport trong cả hai SDK tự động retry trên các lỗi tạm thời với exponential backoff. Số lần retry khác nhau một chút giữa hai ngôn ngữ nhưng điều kiện giống nhau.

| Điều kiện                   | Hành động                                    |
| --------------------------- | -------------------------------------------- |
| HTTP **429** (rate limit)   | Retry tối đa 2 lần                           |
| HTTP **5xx** (server error) | Retry tối đa 2 lần                           |
| Network error / timeout     | Retry tối đa 2 lần                           |
| HTTP **401 / 403**          | Không retry — throw `AuthError` ngay lập tức |
| HTTP **4xx** (khác)         | Không retry — throw `ApiError` ngay lập tức  |

**Backoff:** `2^retryCount` giây giữa các lần thử (2s → 4s). Tổng tệ nhất: 3 lần thử.

| Điều kiện                   | Hành động                                    |
| --------------------------- | -------------------------------------------- |
| HTTP **429** (rate limit)   | Retry tối đa 3 lần                           |
| HTTP **5xx** (server error) | Retry tối đa 3 lần                           |
| Network error / timeout     | Retry tối đa 3 lần                           |
| HTTP **401 / 403**          | Không retry — raise `AuthError` ngay lập tức |
| HTTP **4xx** (khác)         | Không retry — raise `ApiError` ngay lập tức  |

**Backoff:** `2^retryCount` giây giữa các lần thử (2s → 4s → 8s). Tổng tệ nhất: 4 lần thử.

---

## Hủy Request (TypeScript)

Dùng `AbortSignal` để hủy request đang chạy:

```typescript
const controller = new AbortController();
setTimeout(() => controller.abort(), 5000);

try {
  const result = await client.marketplace.listProducts(
    { page: 1 },
    { signal: controller.signal },
  );
} catch (e) {
  if (e instanceof NetworkError && e.message.includes("aborted")) {
    console.log("Request đã bị hủy");
  }
}
```

## Xử Lý Lỗi Async (Python)

Async client raise các exception type giống hệt:

```python
from imbrace import AsyncImbraceClient, AuthError, ApiError

async with AsyncImbraceClient() as client:
    try:
        me = await client.platform.get_me()
    except AuthError:
        print("Cần xác thực lại")
    except ApiError as e:
        print(f"[{e.status_code}] {e}")
```

---

## Best Practices

```typescript
// 1. Xử lý AuthError riêng biệt — credentials cần được refresh
// 2. Log ApiError.statusCode — 400=params sai, 404=không tìm thấy, 409=conflict
// 3. Wrap entry points bằng try/catch
// 4. Không retry khi AuthError — sẽ không có tác dụng cho đến khi credentials được sửa

async function safeGetMe(client: ImbraceClient) {
  try {
    return await client.platform.getMe();
  } catch (e) {
    if (e instanceof AuthError) {
      await refreshCredentials();
      return await client.platform.getMe();
    }
    throw e;
  }
}
```

```python
# 1. Dùng context manager để đảm bảo connection được đóng
with ImbraceClient() as client:
    ...

# 2. Xử lý AuthError riêng biệt — credentials cần refresh trước khi retry
def safe_get_me(client):
    try:
        return client.platform.get_me()
    except AuthError:
        refresh_credentials(client)
        return client.platform.get_me()

# 3. Log ApiError.status_code để debug
try:
    client.marketplace.create_product(data)
except ApiError as e:
    if e.status_code == 409:
        print("Sản phẩm đã tồn tại")
    elif e.status_code == 400:
        print(f"Dữ liệu không hợp lệ: {e}")
```
