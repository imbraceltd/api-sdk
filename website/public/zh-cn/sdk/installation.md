# 安装

> 安装适用于 TypeScript 或 Python 的 Imbrace SDK。

### 安装

  
    ```bash
    npm install @imbrace/sdk
    # 或
    yarn add @imbrace/sdk
    # 或
    pnpm add @imbrace/sdk
    ```

    需要 Node.js 18+（或任何支持原生 `fetch` 和 `ReadableStream` 的浏览器）。
  
  
    ```bash
    pip install imbrace
    # 或
    uv add imbrace
    ```

    需要 Python 3.9+。
  

### 初始化客户端

  
    ```typescript
    import { ImbraceClient } from "@imbrace/sdk"

    // 在 Imbrace 之上开发 — Imbrace 就是你的后端，终端用户通过 OTP 登录
    const client = new ImbraceClient({
      accessToken: "acc_your_token",
      baseUrl: "https://app-gatewayv2.imbrace.co",
    })
    ```

    客户端是有状态的 — 创建一次并在整个应用中复用。
  
  
    ```python
    from imbrace import ImbraceClient

    # 在 Imbrace 之上开发 — Imbrace 就是你的后端，终端用户通过 OTP 登录
    with ImbraceClient(access_token="acc_your_token") as client:
        ...
    ```

    Python 也导出 `AsyncImbraceClient`（`async with ...`），用于 FastAPI 等异步框架。

    上下文管理器自动关闭底层 HTTP 连接池。
  

如需了解何时使用哪种凭证，参阅[身份验证](/zh-cn/sdk/authentication/)。分步骤设置凭证（env vars、dotenv、secrets），参阅[安装指南](/zh-cn/getting-started/setup/#configure-credentials)。

### 验证

  
    ```typescript
    import { ImbraceClient } from "@imbrace/sdk"
    console.log("SDK loaded:", typeof ImbraceClient) // "function"
    ```
  
  
    ```python
    from imbrace import ImbraceClient
    print("SDK ready:", ImbraceClient)
    ```
  

### 环境变量

SDK **不会**自动读取环境变量。将凭证直接传给构造函数，如果将凭证保存在 `.env` 中，请使用加载器（`dotenv` / 框架的 env 处理）。

| 变量 | 用途 |
|---|---|
| `IMBRACE_API_KEY` | 你的 API key（org 级别凭证） |
| `IMBRACE_ACCESS_TOKEN` | 用户的 access token（per-session 凭证） |
| `IMBRACE_BASE_URL` | 覆盖 gateway URL（默认：`https://app-gatewayv2.imbrace.co`） |

org id 已编码在 API key 和 access token 中 — 你永远不需要向 SDK 传递 `organizationId`/`organization_id`。参阅[身份验证](/zh-cn/sdk/authentication/)了解详情。
