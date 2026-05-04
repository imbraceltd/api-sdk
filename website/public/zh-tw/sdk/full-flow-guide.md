# 完整流程指南

> 端到端指南 — 從初始化 client 到 AI agents、工作流程、knowledge hubs 和資料看板。TypeScript 和 Python。

本指南從頭到尾演示 Imbrace SDK 的四個主要流程。每個部分相互獨立 — 可以按順序閱讀，也可以直接跳到需要的部分。切換一次語言 Tab，頁面其餘部分將記住你的選擇。

---

## 1. 建立 AI 助手並開始聊天

1. **初始化 client**

   
     
       ```typescript
       import { ImbraceClient } from "@imbrace/sdk"

       const client = new ImbraceClient({
         baseUrl: "https://app-gatewayv2.imbrace.co",
         accessToken: "acc_your_token",
       })
       ```
     
     
       ```python
       from imbrace import ImbraceClient

       client = ImbraceClient(
           base_url="https://app-gatewayv2.imbrace.co",
           access_token="acc_your_token",
       )
       ```
     
   

   參見[身份驗證 → 選哪種憑證](/zh-tw/sdk/authentication/#我該選哪種憑證)了解完整決策樹。

2. **建立助手**

   `workflow_name` 在組織內必須唯一。

   
     
       ```typescript
       const assistant = await client.chatAi.createAssistant({
         name: "Support Bot",
         workflow_name: "support_bot_v1",
         description: "處理一級客戶支援問題",
         instructions: "您是支援助手。請簡潔友好地回答。",
         provider_id: "system",   // 使用組織預設的 LLM 供應商
         model_id: "gpt-4o",      // system 供應商支援的模型名稱
       })

       const assistantId = assistant.id  // UUID — 用於所有後續呼叫
       console.log("Assistant created:", assistantId)
       ```
     
     
       ```python
       assistant = client.chat_ai.create_assistant({
           "name": "Support Bot",
           "workflow_name": "support_bot_v1",
           "description": "處理一級客戶支援問題",
           "instructions": "您是支援助手。請簡潔友好地回答。",
           "provider_id": "system",   # 使用組織預設的 LLM 供應商
           "model_id": "gpt-4o",      # system 供應商支援的模型名稱
       })

       assistant_id = assistant["id"]
       print("Assistant created:", assistant_id)
       ```
     
   

   `provider_id` 與 `model_id` 為必填。傳入 `provider_id: "system"` 使用組織預設的 LLM 供應商，或傳入自訂供應商的 UUID。當 `provider_id: "system"` 時，`model_id` 可填模型名稱（例如 `"gpt-4o"`）或字串 `"Default"` 以使用系統預設模型。

3. **從助手串流取得聊天回應**

   
     
       ```typescript
       const response = await client.aiAgent.streamChat({
         assistant_id: assistantId,
         organization_id: "org_your_org_id",
         messages: [{ role: "user", content: "如何重設密碼？" }],
         // id 是工作階段 UUID — 重複傳入以保留對話歷史
         // 若省略，每次呼叫將自動產生新 UUID
       })

       const reader = response.body!.getReader()
       const decoder = new TextDecoder()

       while (true) {
         const { done, value } = await reader.read()
         if (done) break
         const text = decoder.decode(value)
         for (const line of text.split("\n")) {
           if (line.startsWith("data: ")) {
             const data = line.slice(6).trim()
             if (data && data !== "[DONE]") {
               try {
                 const chunk = JSON.parse(data)
                 process.stdout.write(chunk.delta ?? chunk.content ?? "")
               } catch {}
             }
           }
         }
       }
       ```
     
     
       ```python
       response = client.ai_agent.stream_chat({
           "assistant_id": assistant_id,
           "organization_id": "org_your_org_id",
           "messages": [{"role": "user", "content": "如何重設密碼？"}],
           # id 是工作階段 UUID — 重複傳入以保留對話歷史
           # 若省略，每次呼叫將自動產生新 UUID
       })

       import json
       for line in response.iter_lines():
           if isinstance(line, bytes):
               line = line.decode()
           if not line.startswith("data: "):
               continue
           data = line[6:].strip()
           if data and data != "[DONE]":
               try:
                   chunk = json.loads(data)
                   print(chunk.get("delta") or chunk.get("content") or "", end="")
               except Exception:
                   pass
       ```
     
   

4. **維護對話歷史（session ID）**

   在多次呼叫中傳入相同的 `id`（必須是 UUID）以保留上下文：

   
     
       ```typescript
       import { randomUUID } from "crypto"

       const sessionId = randomUUID()

       // 第一條訊息
       await client.aiAgent.streamChat({
         assistant_id: assistantId,
         organization_id: "org_your_org_id",
         id: sessionId,
         messages: [{ role: "user", content: "您的退款政策是什麼？" }],
       })

       // 下一條訊息 — 同一工作階段，助手記住上下文
       await client.aiAgent.streamChat({
         assistant_id: assistantId,
         organization_id: "org_your_org_id",
         id: sessionId,
         messages: [{ role: "user", content: "需要多長時間處理？" }],
       })
       ```
     
     
       ```python
       import uuid

       session_id = str(uuid.uuid4())

       # 第一條訊息
       client.ai_agent.stream_chat({
           "assistant_id": assistant_id,
           "organization_id": "org_your_org_id",
           "id": session_id,
           "messages": [{"role": "user", "content": "您的退款政策是什麼？"}],
       })

       # 下一條訊息 — 同一工作階段，助手記住上下文
       client.ai_agent.stream_chat({
           "assistant_id": assistant_id,
           "organization_id": "org_your_org_id",
           "id": session_id,
           "messages": [{"role": "user", "content": "需要多長時間處理？"}],
       })
       ```
     
   

---

## 2. 使用 Activepieces 建立工作流並與助手關聯

1. **列出現有 flows 以取得 project ID**

   
     
       ```typescript
       const { data: flows } = await client.activepieces.listFlows({ limit: 5 })
       const projectId = flows[0]?.projectId
       console.log("Project ID:", projectId)
       ```
     
     
       ```python
       res = client.activepieces.list_flows(limit=5)
       flows = res.get("data", [])
       project_id = flows[0]["projectId"] if flows else None
       print("Project ID:", project_id)
       ```
     
   

2. **建立新 flow**

   
     
       ```typescript
       const flow = await client.activepieces.createFlow({
         displayName: "新 Lead 時更新 CRM",
         projectId,
       })
       console.log("Flow created:", flow.id)
       ```
     
     
       ```python
       flow = client.activepieces.create_flow(
           display_name="新 Lead 時更新 CRM",
           project_id=project_id,
       )
       print("Flow created:", flow["id"])
       ```
     
   

3. **新增 Webhook 觸發器並發布 flow**

   剛建立的 flow 處於 **DRAFT** 狀態且沒有觸發器 — webhook URL 尚未存在，因此呼叫 `triggerFlow` 會回傳 404。新增 Webhook piece 作為觸發器，再發布：

   
     
       ```typescript
       // 將 Webhook piece 設為 flow 的觸發器
       await client.activepieces.applyFlowOperation(flow.id, {
         type: "UPDATE_TRIGGER",
         request: {
           name: "trigger",
           type: "PIECE_TRIGGER",
           valid: true,
           displayName: "Webhook",
           settings: {
             pieceName: "@activepieces/piece-webhook",
             pieceVersion: "0.1.24",
             triggerName: "catch_webhook",
             input: { authType: "none" },
             propertySettings: {},
           },
         },
       })

       // 發布 — 狀態從 DISABLED → ENABLED，webhook URL 開始可用
       await client.activepieces.applyFlowOperation(flow.id, {
         type: "LOCK_AND_PUBLISH",
         request: {},
       })
       ```
     
     
       ```python
       # 將 Webhook piece 設為 flow 的觸發器
       client.activepieces.apply_flow_operation(flow["id"], {
           "type": "UPDATE_TRIGGER",
           "request": {
               "name": "trigger",
               "type": "PIECE_TRIGGER",
               "valid": True,
               "displayName": "Webhook",
               "settings": {
                   "pieceName": "@activepieces/piece-webhook",
                   "pieceVersion": "0.1.24",
                   "triggerName": "catch_webhook",
                   "input": {"authType": "none"},
                   "propertySettings": {},
               },
           },
       })

       # 發布 — DISABLED → ENABLED，webhook URL 開始可用
       client.activepieces.apply_flow_operation(flow["id"], {
           "type": "LOCK_AND_PUBLISH",
           "request": {},
       })
       ```
     
   

4. **手動觸發 flow 並傳入 payload**

   
     
       ```typescript
       // 非同步（fire and forget）
       await client.activepieces.triggerFlow(flow.id, {
         contact_name: "張三",
         email: "zhangsan@example.com",
       })

       // 同步觸發 — 若要實際取得回傳值而非逾時，flow 需透過
       // applyFlowOperation ADD_ACTION 加入「Return Response」動作
       const result = await client.activepieces.triggerFlowSync(flow.id, {
         contact_name: "張三",
         email: "zhangsan@example.com",
       })
       console.log("Flow result:", result)
       ```
     
     
       ```python
       # 非同步（fire and forget）
       client.activepieces.trigger_flow(flow["id"], {
           "contact_name": "張三",
           "email": "zhangsan@example.com",
       })

       # 同步觸發 — 若要實際取得回傳值而非逾時，flow 需透過
       # apply_flow_operation ADD_ACTION 加入「Return Response」動作
       result = client.activepieces.trigger_flow_sync(flow["id"], {
           "contact_name": "張三",
           "email": "zhangsan@example.com",
       })
       print("Flow result:", result)
       ```
     
   

5. **將 flow 與助手關聯**

   在 Imbrace dashboard 中開啟助手，進入 **Tools → Workflows** 並綁定 flow。助手在對話中將能夠在適當時機觸發 flow。

   或更新助手以按名稱引用工作流程：

   
     
       ```typescript
       await client.chatAi.updateAssistant(assistantId, {
         name: "Support Bot",
         workflow_name: "support_bot_v1",
         workflow_function_call: [{ flow_id: flow.id, description: "新 lead 時更新 CRM" }],
       })
       ```
     
     
       ```python
       client.chat_ai.update_assistant(assistant_id, {
           "name": "Support Bot",
           "workflow_name": "support_bot_v1",
           "workflow_function_call": [
               {"flow_id": flow["id"], "description": "新 lead 時更新 CRM"}
           ],
       })
       ```
     
   

6. **查看執行歷史**

   
     
       ```typescript
       const { data: runs } = await client.activepieces.listRuns({
         flowId: flow.id,
         limit: 10,
       })
       for (const run of runs) {
         console.log(run.id, run.status, run.startTime)
       }
       ```
     
     
       ```python
       res = client.activepieces.list_runs(flow_id=flow["id"], limit=10)
       for run in res.get("data", []):
           print(run["id"], run.get("status"), run.get("startTime"))
       ```
     
   

---

## 3. 管理 Knowledge Hub 並綁定到助手

Knowledge Hub 在 **data-board** 服務（`client.boards`）中儲存檔案和資料夾。資料夾的 `_id` 是您傳給助手作為知識來源的值。

1. **建立資料夾**

   
     
       ```typescript
       const folder = await client.boards.createFolder({
         name: "產品文件",
         organization_id: "org_your_org_id",
         parent_folder_id: "root",
         source_type: "upload",
       })
       console.log("Folder ID:", folder._id)
       ```
     
     
       ```python
       folder = client.boards.create_folder({
           "name": "產品文件",
           "organization_id": "org_your_org_id",
           "parent_folder_id": "root",
           "source_type": "upload",
       })
       print("Folder ID:", folder["_id"])
       ```
     
   

2. **上傳檔案到資料夾**

   
     
       ```typescript
       import { readFileSync } from "fs"

       const fileBuffer = readFileSync("./docs/faq.pdf")
       const formData = new FormData()
       formData.append("file", new Blob([fileBuffer], { type: "application/pdf" }), "faq.pdf")
       formData.append("folder_id", folder._id)
       formData.append("organization_id", "org_your_org_id")

       const uploaded = await client.boards.uploadFile(formData)
       console.log("File uploaded:", uploaded.file_id)
       ```
     
     
       ```python
       from pathlib import Path

       path = Path("./docs/faq.pdf")
       files = {
           "file": (path.name, path.read_bytes(), "application/pdf"),
           "folder_id": (None, folder["_id"]),
           "organization_id": (None, "org_your_org_id"),
       }
       uploaded = client.boards.upload_file(files)
       print("File uploaded:", uploaded.get("file_id") or uploaded.get("_id"))
       ```
     
   

3. **將資料夾綁定到助手**

   將資料夾的 `_id` 傳入 `folder_ids` — 助手將從該資料夾的所有檔案中檢索。使用 `board_ids` 可額外附加 CRM data-board。舊的 `knowledge_hubs` 欄位已停用。

   
     
       ```typescript
       await client.chatAi.updateAssistant(assistantId, {
         name: "Support Bot",
         workflow_name: "support_bot_v1",
         folder_ids: [folder._id],
         // board_ids: [boardId],  // 可選：同時附加 CRM data-board
       })
       ```
     
     
       ```python
       client.chat_ai.update_assistant(assistant_id, {
           "name": "Support Bot",
           "workflow_name": "support_bot_v1",
           "folder_ids": [folder["_id"]],
           # "board_ids": [board_id],  # 可選：同時附加 CRM data-board
       })
       ```
     
   

4. **查看和管理資料夾/檔案**

   
     
       ```typescript
       // 搜尋資料夾
       const folders = await client.boards.searchFolders({ q: "產品" })

       // 取得資料夾內容
       const contents = await client.boards.getFolderContents(folder._id)
       console.log("Files:", contents.files?.length)

       // 重新命名資料夾
       await client.boards.updateFolder(folder._id, { name: "產品文件 v2" })

       // 搜尋資料夾中的檔案
       const files = await client.boards.searchFiles({ folderId: folder._id })

       // 刪除資料夾
       await client.boards.deleteFolders({ ids: [folder._id] })
       ```
     
     
       ```python
       # 搜尋資料夾
       folders = client.boards.search_folders(q="產品")

       # 取得資料夾內容
       contents = client.boards.get_folder_contents(folder["_id"])
       print("Files:", len(contents.get("files") or []))

       # 重新命名資料夾
       client.boards.update_folder(folder["_id"], {"name": "產品文件 v2"})

       # 搜尋資料夾中的檔案
       files = client.boards.search_files(folder_id=folder["_id"])

       # 刪除資料夾
       client.boards.delete_folders([folder["_id"]])
       ```
     
   

---

## 4. 管理資料看板和項目（CRM Pipeline）

1. **建立看板**

   看板是 CRM pipeline — leads、deals、tasks 或任何結構化資料。

   
     
       ```typescript
       const board = await client.boards.create({
         name: "Sales Pipeline",
         description: "追蹤所有活躍交易",
       })
       console.log("Board ID:", board._id)
       ```
     
     
       ```python
       board = client.boards.create(
           name="Sales Pipeline",
           description="追蹤所有活躍交易",
       )
       print("Board ID:", board["_id"])
       ```
     
   

2. **新增自訂欄位**

   欄位類型：`ShortText`、`LongText`、`Number`、`Dropdown`、`Date`、`Checkbox` 等。`createField` 返回已更新的看板 — 新欄位位於 `board.fields` 中。

   
     
       ```typescript
       const updated = await client.boards.createField(board._id, {
         name: "公司",
         type: "ShortText",
       })
       // 取得識別符欄位（每個看板自動建立）
       const identifierField = updated.fields.find(f => f.is_identifier)
       ```
     
     
       ```python
       updated = client.boards.create_field(board["_id"], {
           "name": "公司",
           "type": "ShortText",
       })
       identifier_field = next(f for f in updated["fields"] if f.get("is_identifier"))
       ```
     
   

3. **建立看板項目（記錄）**

   項目使用格式 `{ fields: [{ board_field_id, value }] }`：

   
     
       ```typescript
       const item = await client.boards.createItem(board._id, {
         fields: [
           { board_field_id: identifierField._id, value: "Acme Corp" },
         ],
       })
       console.log("Item ID:", item._id)
       ```
     
     
       ```python
       item = client.boards.create_item(board["_id"], {
           "fields": [
               {"board_field_id": identifier_field["_id"], "value": "Acme Corp"},
           ],
       })
       print("Item ID:", item["_id"])
       ```
     
   

4. **列出和搜尋項目**

   
     
       ```typescript
       // 分頁項目
       const { data: items } = await client.boards.listItems(board._id, { limit: 20, skip: 0 })

       // 全文搜尋
       const { data: results } = await client.boards.search(board._id, {
         q: "Acme",
         limit: 10,
       })
       ```
     
     
       ```python
       # 分頁項目
       items = client.boards.list_items(board["_id"], limit=20, skip=0)

       # 全文搜尋
       results = client.boards.search(board["_id"], q="Acme", limit=10)
       ```
     
   

5. **更新和刪除項目**

   `updateItem` 使用陣列格式 `{ data: [{ key: fieldId, value }] }`：

   
     
       ```typescript
       await client.boards.updateItem(board._id, item._id, {
         data: [{ key: identifierField._id, value: "Acme Corp — Closed Won" }],
       })

       await client.boards.deleteItem(board._id, item._id)
       ```
     
     
       ```python
       client.boards.update_item(board["_id"], item["_id"], {
           "data": [{"key": identifier_field["_id"], "value": "Acme Corp — Closed Won"}],
       })

       client.boards.delete_item(board["_id"], item["_id"])
       ```
     
   

6. **匯出看板為 CSV**

   
     
       ```typescript
       const csv = await client.boards.exportCsv(board._id)
       // csv 是字串 — 寫入檔案或作為下載發送
       ```
     
     
       ```python
       csv = client.boards.export_csv(board["_id"])
       # csv 是 str — 寫入檔案或作為下載發送
       ```
