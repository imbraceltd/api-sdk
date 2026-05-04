# 身份驗證

> API Key 與 Access Token — 何時使用哪種，以及如何傳遞給 SDK。

SDK 支援兩種憑證類型。將 `apiKey` / `api_key` 或 `accessToken` / `access_token` 傳給客戶端建構函式 — 傳輸層自動處理請求標頭。

### 我該選哪種憑證？

選擇取決於**Imbrace 在你的產品中扮演什麼角色**：

#### 在 Imbrace 之上開發 → 使用 Access Token

Imbrace **就是**你的後端。你的終端使用者登入 Imbrace（透過 OTP 或密碼），他們的 `acc_...` access token 就是 SDK 在每個請求送出的憑證。Imbrace 的身份驗證、資料庫、業務邏輯（assistants、knowledge hubs、workflows、AI agents）全都以該登入使用者的身份執行。

典型產品：chat widget、dashboard 或 mobile app，每位使用者就是 Imbrace 的使用者。Imbrace 自動以該 user 為單位記錄 history、permissions 與審計記錄。

#### 包裝 Imbrace → 使用 API Key

你有自己的後端、自己的使用者、自己的資料庫。Imbrace 只是你服務呼叫的**其中一項能力** —「用 Imbrace 的 AI 回答這個」 — 與你正在做的其他事並列。你的終端使用者完全不知道 Imbrace 存在；你的服務以一組由 Imbrace org 管理員核發的 org 級 `api_...` key 呼叫 Imbrace。Imbrace 只看到一個身份（API key 對應的 service account），per-user attribution 由你自己負責。

典型產品：既有的 CRM、客服系統或內部工具，把 Imbrace 嵌入為一個功能。一組憑證放在 env file 裡服務所有請求。

| | 在 Imbrace 之上開發（Access Token） | 包裝 Imbrace（API Key） |
| --- | --- | --- |
| **由誰執行 auth？** | Imbrace（OTP／密碼登入） | 你（你自己的 auth） |
| **誰的使用者？** | Imbrace 的 user | 你的 user |
| **以誰的 DB 為主？** | Imbrace 的 | 你的 |
| **Imbrace 看到的身份** | 真正的終端使用者 | 一個 service account |
| **上游 per-user 審計** | 內建 | 由你處理 |
| **憑證存活時間** | session 內；按需刷新 | 長期；不會自行過期 |
| **發送的請求標頭** | `x-access-token: acc_...` | `x-api-key: api_...` |

> 兩種憑證皆為一級支援。大部分資源接受兩者。少數依賴使用者上下文的功能（document artifacts、各 user 自己的 chat history）只在 access token 模式下有意義。

### 標頭對照

| 憑證 | 發送的請求標頭 |
| --- | --- |
| `apiKey` / `api_key` | `x-api-key: api_xxx...` |
| `accessToken` / `access_token` | `x-access-token: acc_xxx...` |

Org context **內嵌在憑證本身** — 每個 API key 與每個 access token 都綁定到唯一一個 org。Gateway 從你送出的憑證即可解析 org，**完全不需要**傳 `organizationId` / `organization_id` 給 SDK。

分步驟設定憑證（env vars、dotenv、secrets），參閱[安裝指南](/zh-tw/getting-started/setup/#configure-credentials)。

---

### API Key

  
    ```typescript
    import { ImbraceClient } from "@imbrace/sdk";

    const client = new ImbraceClient({
      apiKey: "api_xxx...",
      baseUrl: "https://app-gatewayv2.imbrace.co",
    });
    ```
  
  
    ```python
    import os
    from imbrace import ImbraceClient

    client = ImbraceClient(
        api_key=os.environ["IMBRACE_API_KEY"],
    )
    ```
  

---

### Access Token

如果你已有 `acc_...` token，直接傳入：

  
    ```typescript
    const client = new ImbraceClient({
      accessToken: "acc_xxxxxxxxxxxxx",
      baseUrl: "https://app-gatewayv2.imbrace.co",
    });
    ```
  
  
    ```python
    client = ImbraceClient(
        access_token="acc_xxxxxxxxxxxxx",
    )
    ```
  

---

### OTP 登入流程

使用此流程透過信箱 OTP 驗證使用者並取得 session token。SDK 在登入成功後自動儲存 token。

  
    ```typescript
    import { ImbraceClient } from "@imbrace/sdk"

    const client = new ImbraceClient({
      baseUrl: "https://app-gatewayv2.imbrace.co",
    })

    // 步驟 1：向使用者信箱發送 OTP
    await client.requestOtp("user@example.com")

    // 步驟 2：使用者提交收到的 OTP
    const loginRes = await client.loginWithOtp("user@example.com", "ABC123")

    // 步驟 3：換取長期有效的 access token
    const { token, refresh_token } = await client.auth.exchangeAccessToken("org_your_org_id")

    // 步驟 4：啟用 token 用於後續所有呼叫
    client.setAccessToken(token)

    // 現在使用任何資源
    const { data: boards } = await client.boards.list()
    ```
  
  
    ```python
    from imbrace import ImbraceClient

    client = ImbraceClient()

    # 步驟 1：向使用者信箱發送 OTP
    client.request_otp("user@example.com")

    # 步驟 2：使用者輸入 OTP — token 自動儲存
    client.login_with_otp("user@example.com", "123456")

    # 步驟 3：後續所有呼叫已完成認證
    me = client.platform.get_me()
    ```

    非同步變體：

    ```python
    from imbrace import AsyncImbraceClient

    async with AsyncImbraceClient() as client:
        await client.request_otp("user@example.com")
        await client.login_with_otp("user@example.com", "123456")
        me = await client.platform.get_me()
    ```
  

---

### 密碼登入

  
    ```typescript
    const client = new ImbraceClient({
      baseUrl: "https://app-gatewayv2.imbrace.co",
    })

    await client.login("user@example.com", "password")

    // Token 自動儲存 — 使用任何資源
    const { data: boards } = await client.boards.list()
    ```
  
  
    ```python
    client = ImbraceClient()
    client.login("user@example.com", "password123")

    # Token 自動儲存
    boards = client.boards.list()
    ```
  

---

### Token 管理

  
    ```typescript
    // 替換 token（例如刷新後）
    client.setAccessToken("acc_new_token...")

    // 清除 token（例如登出時）
    client.clearAccessToken()
    ```
  
  
    ```python
    # 替換 token（例如刷新後）
    client.set_access_token("acc_new_token...")

    # 清除 token（例如登出時）
    client.clear_access_token()
    ```
  

---

### 上下文管理器（僅 Python）

始終將 Python 客戶端包裝在上下文管理器中，以確保底層 `httpx` 連接池被正確關閉：

```python
# 同步
with ImbraceClient(api_key="api_xxx") as client:
    me = client.platform.get_me()

# 非同步
async with AsyncImbraceClient(api_key="api_xxx") as client:
    me = await client.platform.get_me()
```
