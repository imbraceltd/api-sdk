# 快速入門

> 在一分鐘內完成你的第一次 Imbrace API 呼叫。

### 1. 初始化客戶端

  
    ```typescript
    import { ImbraceClient } from "@imbrace/sdk"

    const client = new ImbraceClient({
      accessToken: "your-access-token",
      baseUrl: "https://app-gatewayv2.imbrace.co",
    })
    ```
  
  
    ```python
    import os
    from dotenv import load_dotenv
    from imbrace import ImbraceClient

    load_dotenv()

    client = ImbraceClient(
        access_token=os.environ["IMBRACE_ACCESS_TOKEN"],
        base_url="https://app-gatewayv2.imbrace.co",
    )
    ```
  

> 切換 header 中的 **Auth** 下拉選單以全站切換 API Key 和 Access Token 範例。參見[身份驗證](/zh-tw/sdk/authentication/)了解如何選擇。

---

### 2. 取得看板列表

看板是 CRM pipeline — leads、deals、tasks 或任何結構化資料。這個呼叫只需要你的憑證。

  
    ```typescript
    const { data: boards } = await client.boards.list()

    for (const board of boards) {
      console.log(board._id, board.doc_name)
    }
    ```
  
  
    ```python
    boards = client.boards.list()

    for board in boards.get("data", []):
        print(board["_id"], board.get("doc_name"))
    ```
  

如果你看到看板列表，說明 SDK 已連接並通過身份驗證。

---

### 3. 後續步驟

[完整流程指南](/zh-tw/sdk/full-flow-guide/)端到端演示四個主要工作流程。直接跳至你需要的部分：

- **AI 助手 + streamChat** → [完整流程指南 §1](/zh-tw/sdk/full-flow-guide/#1-建立-ai-助手並開始聊天)
- **Activepieces 工作流程** → [完整流程指南 §2](/zh-tw/sdk/full-flow-guide/#2-使用-activepieces-建立工作流並與助手關聯)
- **Knowledge Hub（資料夾、RAG）** → [完整流程指南 §3](/zh-tw/sdk/full-flow-guide/#3-管理-knowledge-hub-並綁定到助手)
- **看板 & 項目（CRM）** → [完整流程指南 §4](/zh-tw/sdk/full-flow-guide/#4-管理資料看板和項目crm-pipeline)

如需按命名空間查看 API 參考，參閱[資源參考](/zh-tw/sdk/resources/)。
