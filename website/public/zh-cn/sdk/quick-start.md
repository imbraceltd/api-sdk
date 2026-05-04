# 快速入门

> 在一分钟内完成你的第一次 Imbrace API 调用。

### 1. 初始化客户端

  
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
  

> 切换 header 中的 **Auth** 下拉菜单以全站切换 API Key 和 Access Token 示例。参见[身份验证](/zh-cn/sdk/authentication/)了解如何选择。

---

### 2. 获取看板列表

看板是 CRM pipeline — leads、deals、tasks 或任何结构化数据。这个调用只需要你的凭证。

  
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
  

如果你看到看板列表，说明 SDK 已连接并通过身份验证。

---

### 3. 后续步骤

[完整流程指南](/zh-cn/sdk/full-flow-guide/)端到端演练四个主要工作流。直接跳转到你需要的部分：

- **AI 助手 + streamChat** → [完整流程指南 §1](/zh-cn/sdk/full-flow-guide/#1-创建-ai-助手并开始聊天)
- **Activepieces 工作流** → [完整流程指南 §2](/zh-cn/sdk/full-flow-guide/#2-使用-activepieces-创建工作流并与助手关联)
- **Knowledge Hub（文件夹、RAG）** → [完整流程指南 §3](/zh-cn/sdk/full-flow-guide/#3-管理-knowledge-hub-并绑定到助手)
- **看板 & 条目（CRM）** → [完整流程指南 §4](/zh-cn/sdk/full-flow-guide/#4-管理数据看板和条目crm-pipelines)

如需按命名空间查看 API 参考，参阅[资源参考](/zh-cn/sdk/resources/)。
