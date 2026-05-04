# 错误处理

> 错误类型、自动重试行为，以及使用 Imbrace SDKs 处理错误的最佳实践。

SDK 抛出的所有错误都继承自一个公共基类，因此可以在一处捕获所有 SDK 错误，或在需要不同处理时按具体子类分支。TypeScript 和 Python SDK 的错误层级完全相同。

## 错误层级

```
Error
└── ImbraceError          （基类 — 捕获所有 SDK 错误）
    ├── AuthError          （401、403 — 无效或过期的凭证）
    ├── ApiError           （4xx/5xx — 服务器拒绝请求）
    └── NetworkError       （超时、连接被拒绝、DNS 失败）
```

```
Exception
└── ImbraceError          （基类 — 捕获所有 SDK 错误）
    ├── AuthError          （401、403 — 无效或过期的凭证）
    ├── ApiError           （4xx/5xx — 服务器拒绝请求）
    └── NetworkError       （超时、连接被拒绝、DNS 失败）
```

如需查看特定错误消息和已知修复方法，参阅[问题排查](/zh-cn/guides/troubleshooting/)。

---

## AuthError

当服务器返回 **401** 或 **403** 时抛出 — 凭证无效、过期或已被撤销。

```typescript

try {
  const me = await client.platform.getMe();
} catch (e) {
  if (e instanceof AuthError) {
    console.error("需要重新认证：", e.message);
  }
}
```

```python
from imbrace import AuthError

try:
    me = client.platform.get_me()
except AuthError as e:
    print(f"认证失败: {e}")
    # 需要重新认证后再试
```

> `AuthError` **永远不会被重试**。SDK 在收到 401/403 时立即抛出 — 需要先修复凭证再重试。凭证策略参阅[身份验证](/zh-cn/sdk/authentication/)。

---

## ApiError

对所有其他 **4xx 和 5xx**（429/5xx 重试耗尽后）抛出。

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

| 属性         | 类型     | 说明                     |
| ------------ | -------- | ------------------------ |
| `statusCode` | `number` | HTTP 状态码              |
| `message`    | `string` | 服务器响应中的错误消息   |

```python
from imbrace import ApiError

try:
    client.marketplace.get_product("nonexistent_id")
except ApiError as e:
    print(f"HTTP {e.status_code}: {e}")
    # 例如："HTTP 404: Product not found"
```

| 属性          | 类型  | 说明                     |
| ------------- | ----- | ------------------------ |
| `status_code` | `int` | HTTP 状态码              |
| `message`    | `str` | 服务器响应中的错误消息   |

---

## NetworkError

请求未能到达服务器时抛出 — 超时、DNS 失败或连接被拒绝。

```typescript

try {
  await client.platform.getMe();
} catch (e) {
  if (e instanceof NetworkError) {
    console.error("无法连接 baseUrl：", e.message);
    // 例如："Request timed out after 30000ms"
  }
}
```

```python
from imbrace import NetworkError

try:
    client.platform.get_me()
except NetworkError as e:
    print(f"网络错误: {e}")
    # 例如："Request timed out after 30s"
```

---

## 捕获所有 SDK 错误

导入基类以在单个块中处理任何 SDK 产生的错误：

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
  throw e; // 重新抛出非 SDK 错误
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

## 自动重试行为

两个 SDK 的 HTTP transport 均以指数退避自动重试瞬时故障。重试次数在不同语言间略有差异，但条件相同。

| 条件                        | 行为                                     |
| --------------------------- | ---------------------------------------- |
| HTTP **429**（频率限制）    | 最多重试 2 次                            |
| HTTP **5xx**（服务器错误）  | 最多重试 2 次                            |
| 网络错误 / 超时             | 最多重试 2 次                            |
| HTTP **401 / 403**          | 不重试 — 立即抛出 `AuthError`            |
| HTTP **4xx**（其他）        | 不重试 — 立即抛出 `ApiError`             |

**退避：** 重试间隔 `2^retryCount` 秒（2s → 4s）。最坏情况：3 次尝试。

| 条件                        | 行为                                     |
| --------------------------- | ---------------------------------------- |
| HTTP **429**（频率限制）    | 最多重试 3 次                            |
| HTTP **5xx**（服务器错误）  | 最多重试 3 次                            |
| 网络错误 / 超时             | 最多重试 3 次                            |
| HTTP **401 / 403**          | 不重试 — 立即引发 `AuthError`            |
| HTTP **4xx**（其他）        | 不重试 — 立即引发 `ApiError`             |

**退避：** 重试间隔 `2^retryCount` 秒（2s → 4s → 8s）。最坏情况：4 次尝试。

---

## 取消请求（TypeScript）

传入 `AbortSignal` 取消进行中的请求：

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
    console.log("请求已被取消");
  }
}
```

## 异步错误处理（Python）

async 客户端抛出相同的异常类型：

```python
from imbrace import AsyncImbraceClient, AuthError, ApiError

async with AsyncImbraceClient() as client:
    try:
        me = await client.platform.get_me()
    except AuthError:
        print("需要重新认证")
    except ApiError as e:
        print(f"[{e.status_code}] {e}")
```

---

## 最佳实践

```typescript
// 1. 单独处理 AuthError — 凭证需要刷新
// 2. 记录 ApiError.statusCode — 400=参数错误，404=未找到，409=冲突
// 3. 在顶层入口点用 try/catch 包装
// 4. AuthError 时不要重试 — 在修复凭证之前重试无效

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
# 1. 使用 context manager 确保连接确定性关闭
with ImbraceClient() as client:
    ...

# 2. 单独处理 AuthError — 凭证需要刷新后再重试
def safe_get_me(client):
    try:
        return client.platform.get_me()
    except AuthError:
        refresh_credentials(client)
        return client.platform.get_me()

# 3. 根据 status_code 处理 ApiError
try:
    client.marketplace.create_product(data)
except ApiError as e:
    if e.status_code == 409:
        print("产品已存在")
    elif e.status_code == 400:
        print(f"数据无效: {e}")
```
