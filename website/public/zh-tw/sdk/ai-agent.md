# AI Agent

> aiAgent / ai_agent 資源參考 — 串流聊天、向量嵌入、Parquet 資料、分散式追蹤以及 Chat Client 子 API。

`client.aiAgent` / `client.ai_agent` 連接到獨立的 AI Agent 服務，運行在與主 API gateway 不同的 base URL 上。該資源提供串流聊天、embedding knowledge base 管理、列式資料（Parquet）、分散式追蹤（Tempo），以及前端應用使用的完整 Chat Client 子 API。

端到端 `streamChat` 範例，參閱[完整流程指南 §1](/zh-tw/sdk/full-flow-guide/#1-建立-ai-助手並開始聊天)。

```typescript
const client = new ImbraceClient();
```

```python
from imbrace import ImbraceClient
client = ImbraceClient()
```

sync（`ImbraceClient`）和 async（`AsyncImbraceClient`）客戶端公開相同的介面 — async 方法需要 await，底層使用 `AsyncAiAgentResource`。

---

## Chat v2 — 串流傳輸（SSE）

回傳原始 response。將 body 作為 Server-Sent Events 串流消費。

```typescript
const response = await client.aiAgent.streamChat({
  id: "chat_id",
  assistant_id: "asst_abc",
  organization_id: "org_abc",
  messages: [{ role: "user", content: "您能做什麼？" }],
});

const reader = response.body!.getReader();
const decoder = new TextDecoder();
while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  process.stdout.write(decoder.decode(value));
}
```

```python
response = client.ai_agent.stream_chat({
    "id": "chat_id",
    "assistant_id": "asst_abc",
    "organization_id": "org_abc",
    "messages": [{"role": "user", "content": "您能做什麼？"}],
})

for line in response.iter_lines():
    if line:
        print(line)
```

**非同步：**

```python
from imbrace import AsyncImbraceClient

async def main():
    async with AsyncImbraceClient() as client:
        response = await client.ai_agent.stream_chat({
            "id": "chat_id",
            "assistant_id": "asst_abc",
            "organization_id": "org_abc",
            "messages": [{"role": "user", "content": "您好"}],
        })
        async for line in response.aiter_lines():
            if line:
                print(line)

asyncio.run(main())
```

---

## 子 Agent 聊天 v2

從子 agent 串流取得回應並取得其對話歷史。

```typescript
const res = await client.aiAgent.streamSubAgentChat({
  assistant_id: "asst_sub",
  organization_id: "org_abc",
  session_id: "sess_xyz",
  chat_id: "chat_id",
  messages: [{ role: "user", content: "解釋這些資料。" }],
});

const history = await client.aiAgent.getSubAgentHistory({
  session_id: "sess_xyz",
  chat_id: "chat_id",
});
```

```python
res = client.ai_agent.stream_sub_agent_chat({
    "assistant_id": "asst_sub",
    "organization_id": "org_abc",
    "session_id": "sess_xyz",
    "chat_id": "chat_id",
    "messages": [{"role": "user", "content": "解釋這些資料。"}],
})

history = client.ai_agent.get_sub_agent_history(
    session_id="sess_xyz",
    chat_id="chat_id",
)
```

---

## 提示建議

取得助手的建議提示列表。

```typescript
const suggestions = await client.aiAgent.getAgentPromptSuggestion("asst_abc");
```

```python
suggestions = client.ai_agent.get_agent_prompt_suggestion("asst_abc")
```

---

## Embeddings & Knowledge Base

管理用於檢索增強生成（RAG）的檔案。先透過 [`client.boards.uploadFile`](/zh-tw/sdk/full-flow-guide/#3-管理-knowledge-hub-並綁定到助手) 上傳檔案，再觸發 embedding 處理。

```typescript
// 觸發已上傳檔案的 embedding 處理
await client.aiAgent.processEmbedding({ fileId: "file_abc" });

// 列出和檢視 embedding 檔案
const files   = await client.aiAgent.listEmbeddingFiles({ page: 1, limit: 20 });
const file    = await client.aiAgent.getEmbeddingFile("file_abc");
const preview = await client.aiAgent.previewEmbeddingFile({ file_id: "file_abc" });

// 更新狀態和刪除
await client.aiAgent.updateEmbeddingFileStatus("file_abc", "active");
await client.aiAgent.deleteEmbeddingFile("file_abc");

// 為 RAG 分類檔案
const classification = await client.aiAgent.classifyFile({ file_id: "file_abc" });
```

```python
# 觸發已上傳檔案的 embedding 處理
client.ai_agent.process_embedding("file_abc")

# 帶處理選項
client.ai_agent.process_embedding("file_abc", options={"chunk_size": 512})

# 列出和檢視 embedding 檔案
files   = client.ai_agent.list_embedding_files(page=1, limit=20)
file    = client.ai_agent.get_embedding_file("file_abc")
preview = client.ai_agent.preview_embedding_file(file_id="file_abc")

# 更新狀態和刪除
client.ai_agent.update_embedding_file_status("file_abc", "active")
client.ai_agent.delete_embedding_file("file_abc")

# 為 RAG 分類檔案
classification = client.ai_agent.classify_file(file_id="file_abc")
```

---

## 資料看板

為結構化資料集使用 AI 建議欄位類型。

```typescript
const result = await client.aiAgent.suggestFieldTypes({
  fields: [
    { name: "created_at", samples: ["2024-01-01", "2024-02-15"] },
    { name: "amount",     samples: [100, 200.5, 999] },
    { name: "is_active",  samples: [true, false, true] },
  ],
});
// result.fields[i].suggestedType → "datetime" | "number" | "boolean" | ...
```

```python
result = client.ai_agent.suggest_field_types(fields=[
    {"name": "created_at", "samples": ["2024-01-01", "2024-02-15"]},
    {"name": "amount",     "samples": [100, 200.5, 999]},
    {"name": "is_active",  "samples": [True, False, True]},
])
# result["fields"][i]["suggestedType"] → "datetime" | "number" | "boolean" | ...
```

---

## Parquet

為分析管道建立和管理列式 Parquet 資料檔案。

```typescript
// 從 JSON 資料建立 Parquet 檔案
const result = await client.aiAgent.generateParquet({
  data: [{ id: 1, name: "Alice" }, { id: 2, name: "Bob" }],
  fileName: "users",
  folderName: "exports",
});

const files = await client.aiAgent.listParquetFiles();
await client.aiAgent.deleteParquetFile("exports/users.parquet");
```

```python
result = client.ai_agent.generate_parquet(
    data=[{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}],
    file_name="users",
    folder_name="exports",
)

files = client.ai_agent.list_parquet_files()
client.ai_agent.delete_parquet_file("exports/users.parquet")
```

---

## 分散式追蹤（Tempo）

從 AI Agent 服務查詢 Grafana Tempo traces 以進行觀測和除錯。

```typescript
// 列出最近的 traces
const traces = await client.aiAgent.getTraces({
  service:   "ai-agent",
  limit:     50,
  timeRange: 3600,     // 秒
  orgId:     "org_abc",
  details:   true,
});

// 檢視單一 trace 詳情
const trace = await client.aiAgent.getTrace("trace_id_hex");

// 列出 services、tags 和 tag 值
const services = await client.aiAgent.getTraceServices();
const tags     = await client.aiAgent.getTraceTags();
const values   = await client.aiAgent.getTraceTagValues("http.status_code");

// 使用 TraceQL 搜尋
const results = await client.aiAgent.searchTraceQL(
  `{ .service.name = "ai-agent" && .http.status = 500 }`
);
```

```python
# 列出最近的 traces
traces = client.ai_agent.get_traces(
    service="ai-agent",
    limit=50,
    time_range=3600,     # 秒
    org_id="org_abc",
    details=True,
)

# 檢視單一 trace 詳情
trace = client.ai_agent.get_trace("trace_id_hex")

# 列出 services、tags 和 tag 值
services = client.ai_agent.get_trace_services()
tags     = client.ai_agent.get_trace_tags()
values   = client.ai_agent.get_trace_tag_values("http.status_code")

# 使用 TraceQL 搜尋
results = client.ai_agent.search_traceql(
    '{ .service.name = "ai-agent" && .http.status = 500 }'
)
```

---

## Chat Client

Chat Client 子 API 為前端應用（如嵌入式聊天 widget）提供服務。框架級接線參閱[整合](/zh-tw/sdk/integrations/)。

### 驗證

```typescript
await client.aiAgent.verifyChatClientCredentials({ token: "tok_xxx" });
await client.aiAgent.registerChatClient({ name: "web-app", secret: "s3cr3t" });
const user = await client.aiAgent.getChatClientUser({ token: "tok_xxx" });
```

```python
client.ai_agent.verify_chat_client_credentials({"token": "tok_xxx"})
client.ai_agent.register_chat_client({"name": "web-app", "secret": "s3cr3t"})
user = client.ai_agent.get_chat_client_user({"token": "tok_xxx"})
```

### 聊天

```typescript
// 建立新聊天工作階段
await client.aiAgent.createClientChat({
  id: "chat_uuid",
  message: {
    id: "msg_uuid",
    role: "user",
    parts: [{ type: "text", text: "您好！" }],
  },
  assistantId:    "asst_abc",
  organizationId: "org_abc",
});

// 列出、讀取、更新、刪除
const chats = await client.aiAgent.listClientChats({
  organization_id: "org_abc",
  limit: 20,
});
const chat = await client.aiAgent.getClientChat("chat_id");
await client.aiAgent.updateClientChat("chat_id", { visibility: "private" });
await client.aiAgent.deleteClientChat("chat_id");
await client.aiAgent.deleteAllClientChats({ organization_id: "org_abc" });

// 自動產生聊天標題
await client.aiAgent.generateClientChatTitle("chat_id");

// 以 SSE 方式串流傳輸即時聊天狀態 — 回傳原始 Response
const statusStream = await client.aiAgent.streamClientChatStatus("chat_id");
```

```python
# 建立新聊天工作階段
client.ai_agent.create_client_chat({
    "id": "chat_uuid",
    "message": {
        "id": "msg_uuid",
        "role": "user",
        "parts": [{"type": "text", "text": "您好！"}],
    },
    "assistantId":    "asst_abc",
    "organizationId": "org_abc",
})

# 列出、讀取、更新、刪除
chats = client.ai_agent.list_client_chats(organization_id="org_abc", limit=20)
chat  = client.ai_agent.get_client_chat("chat_id")
client.ai_agent.update_client_chat("chat_id", {"visibility": "private"})
client.ai_agent.delete_client_chat("chat_id")
client.ai_agent.delete_all_client_chats("org_abc")

# 自動產生聊天標題
client.ai_agent.generate_client_chat_title("chat_id")

# 以 SSE 方式串流傳輸即時聊天狀態 — 回傳原始 httpx.Response
status_stream = client.ai_agent.stream_client_chat_status("chat_id")
```

### 訊息

```typescript
await client.aiAgent.persistClientMessage({ chatId: "chat_id", content: "您好" });
const messages = await client.aiAgent.listClientMessages("chat_id");
await client.aiAgent.deleteTrailingMessages("message_id");
```

```python
client.ai_agent.persist_client_message({"chatId": "chat_id", "content": "您好"})
messages = client.ai_agent.list_client_messages("chat_id")
client.ai_agent.delete_trailing_messages("message_id")
```

### 投票

```typescript
const votes = await client.aiAgent.getVotes("chat_id");
await client.aiAgent.updateVote({ messageId: "msg_id", vote: "up" });
```

```python
votes = client.ai_agent.get_votes("chat_id")
client.ai_agent.update_vote({"messageId": "msg_id", "vote": "up"})
```

### 文件（AI 產生的產物）

```typescript
await client.aiAgent.createDocument({ kind: "text", content: "草稿..." });

const doc        = await client.aiAgent.getDocument("doc_id");
const latest     = await client.aiAgent.getDocumentLatest("doc_id");
const pub        = await client.aiAgent.getDocumentPublic("doc_id");
const byKind     = await client.aiAgent.getDocumentLatestByKind({ kind: "text" });
const suggestion = await client.aiAgent.getDocumentSuggestions("doc_id");

await client.aiAgent.deleteDocument("doc_id");
```

```python
client.ai_agent.create_document({"kind": "text", "content": "草稿..."})

doc        = client.ai_agent.get_document("doc_id")
latest     = client.ai_agent.get_document_latest("doc_id")
pub        = client.ai_agent.get_document_public("doc_id")
by_kind    = client.ai_agent.get_document_latest_by_kind(kind="text")
suggestion = client.ai_agent.get_document_suggestions("doc_id")

client.ai_agent.delete_document("doc_id")
```

---

## 管理員指南

存取由 AI Agent 服務儲存的管理員文件。指南檔案以原始二進位串流形式回傳（通常是 PDF）。

```typescript
const guides = await client.aiAgent.listAdminGuides();

// 下載特定指南 — 回傳原始 Response（PDF 串流）
const response = await client.aiAgent.getAdminGuide("onboarding.pdf");
const blob = await response.blob();
```

```python
guides = client.ai_agent.list_admin_guides()

# 下載特定指南 — 回傳原始 httpx.Response
response = client.ai_agent.get_admin_guide("onboarding.pdf")
with open("onboarding.pdf", "wb") as f:
    f.write(response.content)
```

---

## 舊版 v1 聊天

原始 REST 聊天介面，無需串流即可保留對話歷史。新程式碼應使用上方的 [Chat v2 串流傳輸](#chat-v2--串流傳輸sse)；v1 保留用於向下相容。

```typescript
// 列出某組織的聊天記錄
const chats = await client.aiAgent.listChats({
  organization_id: "org_abc",
  user_id: "user_123",
  limit: 20,
});

// 取得單一聊天（傳 true 以包含訊息）
const chat = await client.aiAgent.getChat("chat_id", true);

// 刪除聊天
await client.aiAgent.deleteChat("chat_id", {
  organization_id: "org_abc",
  user_id: "user_123",
});
```

```python
chats = client.ai_agent.list_chats(
    organization_id="org_abc",
    user_id="user_123",
    limit=20,
)

chat = client.ai_agent.get_chat("chat_id", include_messages=True)

client.ai_agent.delete_chat(
    "chat_id",
    organization_id="org_abc",
    user_id="user_123",
)
```
