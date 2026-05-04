# 錯誤處理

> 錯誤類型、自動重試行為，以及使用 Imbrace SDKs 處理錯誤的最佳實踐。

SDK 拋出的所有錯誤都繼承自一個公共基底類型，因此可以在一處捕獲所有 SDK 錯誤，或在需要不同處理時按具體子類別分支。TypeScript 和 Python SDK 的錯誤層級完全相同。

## 錯誤層級

```
Error
└── ImbraceError          （基底 — 捕獲所有 SDK 錯誤）
    ├── AuthError          （401、403 — 無效或過期的憑證）
    ├── ApiError           （4xx/5xx — 伺服器拒絕請求）
    └── NetworkError       （逾時、連線被拒絕、DNS 失敗）
```

```
Exception
└── ImbraceError          （基底 — 捕獲所有 SDK 錯誤）
    ├── AuthError          （401、403 — 無效或過期的憑證）
    ├── ApiError           （4xx/5xx — 伺服器拒絕請求）
    └── NetworkError       （逾時、連線被拒絕、DNS 失敗）
```

如需查看特定錯誤訊息和已知修復方法，參閱[問題排查](/zh-tw/guides/troubleshooting/)。

---

## AuthError

當伺服器回傳 **401** 或 **403** 時拋出 — 憑證無效、過期或已被撤銷。

```typescript

try {
  const me = await client.platform.getMe();
} catch (e) {
  if (e instanceof AuthError) {
    console.error("需要重新驗證：", e.message);
  }
}
```

```python
from imbrace import AuthError

try:
    me = client.platform.get_me()
except AuthError as e:
    print(f"驗證失敗: {e}")
    # 需要重新驗證後再試
```

> `AuthError` **永遠不會被重試**。SDK 在收到 401/403 時立即拋出 — 需要先修復憑證再重試。憑證策略參閱[身份驗證](/zh-tw/sdk/authentication/)。

---

## ApiError

對所有其他 **4xx 和 5xx**（429/5xx 重試耗盡後）拋出。

```typescript

try {
  await client.marketplace.getProduct("nonexistent_id");
} catch (e) {
  if (e instanceof ApiError) {
    console.error(`HTTP ${e.statusCode}: ${e.message}`);
    // 例如："HTTP 404: Product not found"
  }
}
```

| 屬性         | 類型     | 說明                     |
| ------------ | -------- | ------------------------ |
| `statusCode` | `number` | HTTP 狀態碼              |
| `message`    | `string` | 伺服器回應中的錯誤訊息   |

```python
from imbrace import ApiError

try:
    client.marketplace.get_product("nonexistent_id")
except ApiError as e:
    print(f"HTTP {e.status_code}: {e}")
    # 例如："HTTP 404: Product not found"
```

| 屬性          | 類型  | 說明                     |
| ------------- | ----- | ------------------------ |
| `status_code` | `int` | HTTP 狀態碼              |
| `message`    | `str` | 伺服器回應中的錯誤訊息   |

---

## NetworkError

請求未能到達伺服器時拋出 — 逾時、DNS 失敗或連線被拒絕。

```typescript

try {
  await client.platform.getMe();
} catch (e) {
  if (e instanceof NetworkError) {
    console.error("無法連線 baseUrl：", e.message);
    // 例如："Request timed out after 30000ms"
  }
}
```

```python
from imbrace import NetworkError

try:
    client.platform.get_me()
except NetworkError as e:
    print(f"網路錯誤: {e}")
    # 例如："Request timed out after 30s"
```

---

## 捕獲所有 SDK 錯誤

匯入基底類型以在單一區塊中處理任何 SDK 產生的錯誤：

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
  if (e instanceof AuthError) return handleAuthError(e);
  if (e instanceof ApiError) return handleApiError(e);
  if (e instanceof NetworkError) return handleNetworkError(e);
  if (e instanceof ImbraceError) return handleUnknown(e);
  throw e; // 重新拋出非 SDK 錯誤
}
```

```python
from imbrace import ImbraceError, AuthError, ApiError, NetworkError

try:
    result = client.platform.get_me()
except AuthError as e:
    handle_auth_error(e)
except ApiError as e:
    handle_api_error(e)
except NetworkError as e:
    handle_network_error(e)
except ImbraceError as e:
    handle_unknown_sdk_error(e)
```

---

## 自動重試行為

兩個 SDK 的 HTTP transport 均以指數退避自動重試暫時性故障。重試次數在不同語言間略有差異，但條件相同。

| 條件                        | 行為                                     |
| --------------------------- | ---------------------------------------- |
| HTTP **429**（速率限制）    | 最多重試 2 次                            |
| HTTP **5xx**（伺服器錯誤）  | 最多重試 2 次                            |
| 網路錯誤 / 逾時             | 最多重試 2 次                            |
| HTTP **401 / 403**          | 不重試 — 立即拋出 `AuthError`            |
| HTTP **4xx**（其他）        | 不重試 — 立即拋出 `ApiError`             |

**退避：** 重試間隔 `2^retryCount` 秒（2s → 4s）。最壞情況：3 次嘗試。

| 條件                        | 行為                                     |
| --------------------------- | ---------------------------------------- |
| HTTP **429**（速率限制）    | 最多重試 3 次                            |
| HTTP **5xx**（伺服器錯誤）  | 最多重試 3 次                            |
| 網路錯誤 / 逾時             | 最多重試 3 次                            |
| HTTP **401 / 403**          | 不重試 — 立即引發 `AuthError`            |
| HTTP **4xx**（其他）        | 不重試 — 立即引發 `ApiError`             |

**退避：** 重試間隔 `2^retryCount` 秒（2s → 4s → 8s）。最壞情況：4 次嘗試。

---

## 取消請求（TypeScript）

傳入 `AbortSignal` 取消進行中的請求：

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
    console.log("請求已被取消");
  }
}
```

## 非同步錯誤處理（Python）

async 客戶端拋出相同的例外類型：

```python
from imbrace import AsyncImbraceClient, AuthError, ApiError

async with AsyncImbraceClient() as client:
    try:
        me = await client.platform.get_me()
    except AuthError:
        print("需要重新驗證")
    except ApiError as e:
        print(f"[{e.status_code}] {e}")
```

---

## 最佳實踐

```typescript
// 1. 單獨處理 AuthError — 憑證需要刷新
// 2. 記錄 ApiError.statusCode — 400=參數錯誤，404=未找到，409=衝突
// 3. 在頂層入口點用 try/catch 包裝
// 4. AuthError 時不要重試 — 在修復憑證之前重試無效

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
# 1. 使用 context manager 確保連線確定性關閉
with ImbraceClient() as client:
    ...

# 2. 單獨處理 AuthError — 憑證需要刷新後再重試
def safe_get_me(client):
    try:
        return client.platform.get_me()
    except AuthError:
        refresh_credentials(client)
        return client.platform.get_me()

# 3. 根據 status_code 處理 ApiError
try:
    client.marketplace.create_product(data)
except ApiError as e:
    if e.status_code == 409:
        print("產品已存在")
    elif e.status_code == 400:
        print(f"資料無效: {e}")
```
