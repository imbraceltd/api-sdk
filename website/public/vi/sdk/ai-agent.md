# AI Agent

> Tham chiếu cho resource aiAgent / ai_agent — streaming chat, embeddings, parquet, distributed tracing, và Chat Client sub-API.

`client.aiAgent` / `client.ai_agent` kết nối đến AI Agent service riêng biệt, chạy trên một base URL khác so với API gateway chính. Resource này cung cấp streaming chat, quản lý embedding knowledge base, dữ liệu dạng cột (Parquet), distributed tracing (Tempo), và toàn bộ Chat Client sub-API được sử dụng bởi các ứng dụng frontend.

Để xem ví dụ end-to-end của `streamChat` với real assistant, xem [Hướng Dẫn Luồng Đầy Đủ §1](/vi/sdk/full-flow-guide/#1-tạo-ai-assistant-và-bắt-đầu-chat).

```typescript
const client = new ImbraceClient();
```

```python
from imbrace import ImbraceClient
client = ImbraceClient()
```

Cả sync (`ImbraceClient`) và async (`AsyncImbraceClient`) đều expose cùng surface — async methods dùng `await` và sử dụng `AsyncAiAgentResource` bên dưới.

---

## Chat v2 — Streaming (SSE)

Trả về raw response. Consume body dưới dạng Server-Sent Events stream.

```typescript
const response = await client.aiAgent.streamChat({
  id: "chat_id",
  assistant_id: "asst_abc",
  organization_id: "org_abc",
  messages: [{ role: "user", content: "Bạn có thể làm gì?" }],
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
    "messages": [{"role": "user", "content": "Bạn có thể làm gì?"}],
})

for line in response.iter_lines():
    if line:
        print(line)
```

**Async:**

```python
from imbrace import AsyncImbraceClient

async def main():
    async with AsyncImbraceClient() as client:
        response = await client.ai_agent.stream_chat({
            "id": "chat_id",
            "assistant_id": "asst_abc",
            "organization_id": "org_abc",
            "messages": [{"role": "user", "content": "Xin chào"}],
        })
        async for line in response.aiter_lines():
            if line:
                print(line)

asyncio.run(main())
```

---

## Sub-agent Chat v2

Stream phản hồi từ sub-agent và lấy lịch sử hội thoại.

```typescript
const res = await client.aiAgent.streamSubAgentChat({
  assistant_id: "asst_sub",
  organization_id: "org_abc",
  session_id: "sess_xyz",
  chat_id: "chat_id",
  messages: [{ role: "user", content: "Giải thích dữ liệu." }],
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
    "messages": [{"role": "user", "content": "Giải thích dữ liệu."}],
})

history = client.ai_agent.get_sub_agent_history(
    session_id="sess_xyz",
    chat_id="chat_id",
)
```

---

## Prompt Suggestions

Lấy danh sách prompt gợi ý cho một assistant.

```typescript
const suggestions = await client.aiAgent.getAgentPromptSuggestion("asst_abc");
```

```python
suggestions = client.ai_agent.get_agent_prompt_suggestion("asst_abc")
```

---

## Embeddings & Knowledge Base

Quản lý các file được dùng cho Retrieval-Augmented Generation (RAG). Upload files trước qua [`client.boards.uploadFile`](/vi/sdk/full-flow-guide/#3-quản-lý-knowledge-hub-và-gắn-vào-assistant), rồi trigger embedding processing.

```typescript
// Trigger embedding processing cho file đã upload
await client.aiAgent.processEmbedding({ fileId: "file_abc" });

// Liệt kê và kiểm tra embedding files
const files   = await client.aiAgent.listEmbeddingFiles({ page: 1, limit: 20 });
const file    = await client.aiAgent.getEmbeddingFile("file_abc");
const preview = await client.aiAgent.previewEmbeddingFile({ file_id: "file_abc" });

// Cập nhật trạng thái và xóa
await client.aiAgent.updateEmbeddingFileStatus("file_abc", "active");
await client.aiAgent.deleteEmbeddingFile("file_abc");

// Phân loại file cho RAG
const classification = await client.aiAgent.classifyFile({ file_id: "file_abc" });
```

```python
# Trigger embedding processing cho file đã upload
client.ai_agent.process_embedding("file_abc")

# Với tùy chọn xử lý
client.ai_agent.process_embedding("file_abc", options={"chunk_size": 512})

# Liệt kê và kiểm tra embedding files
files   = client.ai_agent.list_embedding_files(page=1, limit=20)
file    = client.ai_agent.get_embedding_file("file_abc")
preview = client.ai_agent.preview_embedding_file(file_id="file_abc")

# Cập nhật trạng thái và xóa
client.ai_agent.update_embedding_file_status("file_abc", "active")
client.ai_agent.delete_embedding_file("file_abc")

# Phân loại file cho RAG
classification = client.ai_agent.classify_file(file_id="file_abc")
```

---

## Data Board

Gợi ý kiểu dữ liệu bằng AI cho các tập dữ liệu có cấu trúc.

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

Tạo và quản lý các file dữ liệu dạng cột Parquet cho analytics pipelines.

```typescript
// Tạo Parquet file từ JSON data
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

## Distributed Tracing (Tempo)

Truy vấn Grafana Tempo traces từ AI Agent service để quan sát và debug.

```typescript
// Liệt kê traces gần đây
const traces = await client.aiAgent.getTraces({
  service:   "ai-agent",
  limit:     50,
  timeRange: 3600,     // giây
  orgId:     "org_abc",
  details:   true,
});

// Xem chi tiết một trace
const trace = await client.aiAgent.getTrace("trace_id_hex");

// Liệt kê services, tags và giá trị tag
const services = await client.aiAgent.getTraceServices();
const tags     = await client.aiAgent.getTraceTags();
const values   = await client.aiAgent.getTraceTagValues("http.status_code");

// Tìm kiếm bằng TraceQL
const results = await client.aiAgent.searchTraceQL(
  `{ .service.name = "ai-agent" && .http.status = 500 }`
);
```

```python
# Liệt kê traces gần đây
traces = client.ai_agent.get_traces(
    service="ai-agent",
    limit=50,
    time_range=3600,     # giây
    org_id="org_abc",
    details=True,
)

# Xem chi tiết một trace
trace = client.ai_agent.get_trace("trace_id_hex")

# Liệt kê services, tags và giá trị tag
services = client.ai_agent.get_trace_services()
tags     = client.ai_agent.get_trace_tags()
values   = client.ai_agent.get_trace_tag_values("http.status_code")

# Tìm kiếm bằng TraceQL
results = client.ai_agent.search_traceql(
    '{ .service.name = "ai-agent" && .http.status = 500 }'
)
```

---

## Chat Client

Chat Client sub-API phục vụ các ứng dụng frontend (ví dụ: embedded chat widget). Để xem framework-level wiring (React singleton, Express auth proxy, ...), xem [Tích Hợp](/vi/sdk/integrations/).

### Auth

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

### Chats

```typescript
// Tạo session chat mới
await client.aiAgent.createClientChat({
  id: "chat_uuid",
  message: {
    id: "msg_uuid",
    role: "user",
    parts: [{ type: "text", text: "Xin chào!" }],
  },
  assistantId:    "asst_abc",
  organizationId: "org_abc",
});

// Liệt kê, đọc, cập nhật, xóa
const chats = await client.aiAgent.listClientChats({
  organization_id: "org_abc",
  limit: 20,
});
const chat = await client.aiAgent.getClientChat("chat_id");
await client.aiAgent.updateClientChat("chat_id", { visibility: "private" });
await client.aiAgent.deleteClientChat("chat_id");
await client.aiAgent.deleteAllClientChats({ organization_id: "org_abc" });

// Tự động tạo tiêu đề cho chat
await client.aiAgent.generateClientChatTitle("chat_id");

// Stream trạng thái chat thời gian thực dưới dạng SSE — trả về raw Response
const statusStream = await client.aiAgent.streamClientChatStatus("chat_id");
```

```python
# Tạo session chat mới
client.ai_agent.create_client_chat({
    "id": "chat_uuid",
    "message": {
        "id": "msg_uuid",
        "role": "user",
        "parts": [{"type": "text", "text": "Xin chào!"}],
    },
    "assistantId":    "asst_abc",
    "organizationId": "org_abc",
})

# Liệt kê, đọc, cập nhật, xóa
chats = client.ai_agent.list_client_chats(organization_id="org_abc", limit=20)
chat  = client.ai_agent.get_client_chat("chat_id")
client.ai_agent.update_client_chat("chat_id", {"visibility": "private"})
client.ai_agent.delete_client_chat("chat_id")
client.ai_agent.delete_all_client_chats("org_abc")

# Tự động tạo tiêu đề cho chat
client.ai_agent.generate_client_chat_title("chat_id")

# Stream trạng thái chat thời gian thực dưới dạng SSE — trả về raw httpx.Response
status_stream = client.ai_agent.stream_client_chat_status("chat_id")
```

### Messages

```typescript
await client.aiAgent.persistClientMessage({ chatId: "chat_id", content: "Xin chào" });
const messages = await client.aiAgent.listClientMessages("chat_id");
await client.aiAgent.deleteTrailingMessages("message_id");
```

```python
client.ai_agent.persist_client_message({"chatId": "chat_id", "content": "Xin chào"})
messages = client.ai_agent.list_client_messages("chat_id")
client.ai_agent.delete_trailing_messages("message_id")
```

### Votes

```typescript
const votes = await client.aiAgent.getVotes("chat_id");
await client.aiAgent.updateVote({ messageId: "msg_id", vote: "up" });
```

```python
votes = client.ai_agent.get_votes("chat_id")
client.ai_agent.update_vote({"messageId": "msg_id", "vote": "up"})
```

### Documents (AI-generated Artifacts)

```typescript
await client.aiAgent.createDocument({ kind: "text", content: "Bản nháp..." });

const doc        = await client.aiAgent.getDocument("doc_id");
const latest     = await client.aiAgent.getDocumentLatest("doc_id");
const pub        = await client.aiAgent.getDocumentPublic("doc_id");
const byKind     = await client.aiAgent.getDocumentLatestByKind({ kind: "text" });
const suggestion = await client.aiAgent.getDocumentSuggestions("doc_id");

await client.aiAgent.deleteDocument("doc_id");
```

```python
client.ai_agent.create_document({"kind": "text", "content": "Bản nháp..."})

doc        = client.ai_agent.get_document("doc_id")
latest     = client.ai_agent.get_document_latest("doc_id")
pub        = client.ai_agent.get_document_public("doc_id")
by_kind    = client.ai_agent.get_document_latest_by_kind(kind="text")
suggestion = client.ai_agent.get_document_suggestions("doc_id")

client.ai_agent.delete_document("doc_id")
```

---

## Admin Guides

Truy cập tài liệu admin được lưu trữ bởi AI Agent service. File guide được trả về dưới dạng raw binary streams (thường là PDF).

```typescript
const guides = await client.aiAgent.listAdminGuides();

// Download một guide — trả về raw Response (PDF stream)
const response = await client.aiAgent.getAdminGuide("onboarding.pdf");
const blob = await response.blob();
```

```python
guides = client.ai_agent.list_admin_guides()

# Download một guide — trả về raw httpx.Response
response = client.ai_agent.get_admin_guide("onboarding.pdf")
with open("onboarding.pdf", "wb") as f:
    f.write(response.content)
```

---

## Legacy v1 Chat

REST chat endpoints gốc lưu lịch sử hội thoại mà không có streaming. Code mới nên dùng [Chat v2 streaming](#chat-v2--streaming-sse) ở trên; v1 giữ lại để tương thích ngược.

```typescript
// Liệt kê chats cho một tổ chức
const chats = await client.aiAgent.listChats({
  organization_id: "org_abc",
  user_id: "user_123",
  limit: 20,
});

// Lấy một chat (truyền true để include messages)
const chat = await client.aiAgent.getChat("chat_id", true);

// Xóa một chat
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
