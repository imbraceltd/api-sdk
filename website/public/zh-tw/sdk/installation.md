# 安裝

> 安裝適用於 TypeScript 或 Python 的 Imbrace SDK。

### 安裝

  
    ```bash
    npm install @imbrace/sdk
    # 或
    yarn add @imbrace/sdk
    # 或
    pnpm add @imbrace/sdk
    ```

    需要 Node.js 18+（或任何支援原生 `fetch` 和 `ReadableStream` 的瀏覽器）。
  
  
    ```bash
    pip install imbrace
    # 或
    uv add imbrace
    ```

    需要 Python 3.9+。
  

### 初始化客戶端

  
    ```typescript
    import { ImbraceClient } from "@imbrace/sdk"

    // 在 Imbrace 之上開發 — Imbrace 就是你的後端，終端使用者透過 OTP 登入
    const client = new ImbraceClient({
      accessToken: "acc_your_token",
      baseUrl: "https://app-gatewayv2.imbrace.co",
    })
    ```

    客戶端是有狀態的 — 建立一次並在整個應用中複用。
  
  
    ```python
    from imbrace import ImbraceClient

    # 在 Imbrace 之上開發 — Imbrace 就是你的後端，終端使用者透過 OTP 登入
    with ImbraceClient(access_token="acc_your_token") as client:
        ...
    ```

    Python 也匯出 `AsyncImbraceClient`（`async with ...`），用於 FastAPI 等非同步框架。

    上下文管理器自動關閉底層 HTTP 連接池。
  

如需了解何時使用哪種憑證，參閱[身份驗證](/zh-tw/sdk/authentication/)。分步驟設定憑證（env vars、dotenv、secrets），參閱[安裝指南](/zh-tw/getting-started/setup/#configure-credentials)。

### 驗證

  
    ```typescript
    import { ImbraceClient } from "@imbrace/sdk"
    console.log("SDK loaded:", typeof ImbraceClient) // "function"
    ```
  
  
    ```python
    from imbrace import ImbraceClient
    print("SDK ready:", ImbraceClient)
    ```
  

### 環境變數

SDK **不會**自動讀取環境變數。將憑證直接傳給建構函式，如果將憑證儲存在 `.env` 中，請使用載入器（`dotenv` / 框架的 env 處理）。

| 變數 | 用途 |
|---|---|
| `IMBRACE_API_KEY` | 你的 API key（org 級別憑證） |
| `IMBRACE_ACCESS_TOKEN` | 使用者的 access token（per-session 憑證） |
| `IMBRACE_BASE_URL` | 覆蓋 gateway URL（預設：`https://app-gatewayv2.imbrace.co`） |

org id 已編碼在 API key 和 access token 中 — 你永遠不需要向 SDK 傳遞 `organizationId`/`organization_id`。參閱[身份驗證](/zh-tw/sdk/authentication/)了解詳情。
