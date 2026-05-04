# Tham Chiếu Resources

> Tham chiếu theo namespace cho Imbrace SDKs — assistants, AI agent, workflows, boards, contacts, và nhiều hơn.

Trang này liệt kê mọi resource namespace được SDK expose với các call phổ biến nhất trong mỗi namespace. Khởi tạo client trước (xem [Cài Đặt](/vi/sdk/installation/) hoặc [Bắt Đầu Nhanh](/vi/sdk/quick-start/)). Tất cả snippets bên dưới giả định `client` là instance đã khởi tạo.

Để xem hướng dẫn end-to-end sử dụng các resources này cùng nhau, xem [Hướng Dẫn Luồng Đầy Đủ](/vi/sdk/full-flow-guide/).

---

## Assistants — `chatAi` / `chat_ai`

Quản lý AI assistants (CRUD), chạy OpenAI-compatible completions, và xử lý document/file. Namespace này cũng bao gồm Knowledge Hub folders và knowledge bases.

### Assistant CRUD

```typescript
// Liệt kê tất cả assistants trong tài khoản
const assistants = await client.chatAi.listAssistants();

// Lấy một assistant
const assistant = await client.chatAi.getAssistant("9f77692f-33d0-436a-8138-2efb268838e6");

// Tạo — provider_id và model_id là bắt buộc
const created = await client.chatAi.createAssistant({
  name: "Support Bot",
  workflow_name: "support_bot_v1",
  provider_id: "system",
  model_id: "gpt-4o",
  description: "Xử lý các câu hỏi hỗ trợ cấp 1",
});

// Cập nhật — workflow_name cũng bắt buộc khi update
const updated = await client.chatAi.updateAssistant(created.id, {
  name: "Support Bot v2",
  workflow_name: "support_bot_v1",
});

// Cập nhật chỉ system instructions
await client.chatAi.updateAssistantInstructions(
  created.id,
  "Bạn là trợ lý hỗ trợ hữu ích.",
);

await client.chatAi.deleteAssistant(created.id);
```

```python
# Liệt kê tất cả assistants
assistants = client.chat_ai.list_assistants()

# Lấy một assistant
assistant = client.chat_ai.get_assistant("9f77692f-33d0-436a-8138-2efb268838e6")

# Tạo — provider_id và model_id là bắt buộc
created = client.chat_ai.create_assistant({
    "name":          "Support Bot",
    "workflow_name": "support_bot_v1",
    "provider_id":   "system",
    "model_id":      "gpt-4o",
    "description":   "Xử lý các câu hỏi hỗ trợ cấp 1",
})

# Cập nhật
updated = client.chat_ai.update_assistant(created["id"], {
    "name":          "Support Bot v2",
    "workflow_name": "support_bot_v1",
})

# Cập nhật chỉ system instructions
client.chat_ai.update_assistant_instructions(
    created["id"],
    "Bạn là trợ lý hỗ trợ hữu ích.",
)

client.chat_ai.delete_assistant(created["id"])
```

### Completions

```typescript
const response = await client.chatAi.chat({
  model: "gpt-4o",
  messages: [
    { role: "system", content: "Bạn là trợ lý CRM hữu ích." },
    { role: "user", content: "Tóm tắt ghi chú khách hàng này: ..." },
  ],
});
console.log(response.choices[0].message.content);
```

```python
response = client.chat_ai.chat({
    "model": "gpt-4o",
    "messages": [
        {"role": "system", "content": "Bạn là trợ lý CRM hữu ích."},
        {"role": "user",   "content": "Tóm tắt ghi chú khách hàng này: ..."},
    ],
})
print(response["choices"][0]["message"]["content"])
```

### Models

```typescript
const models = await client.chatAi.listModels();
```

```python
models = client.chat_ai.list_models()
```

### File Processing

```typescript
// Trích xuất dữ liệu có cấu trúc từ PDF hoặc image
const result = await client.chatAi.extractFile({
  modelName: "gpt-4o",
  url: "https://example.com/invoice.pdf",
  organizationId: "org_xxx",
});
```

```python
result = client.chat_ai.process_document(
    model_name="gpt-4o",
    url="https://example.com/invoice.pdf",
    organization_id="org_xxx",
)
print(result["data"])
# {"invoice_number": "INV-001", "total": 1200, "vendor": "Acme Corp", ...}
```

### Persistent Chat Sessions (Python)

```python
chat    = client.chat_ai.create_chat({"title": "Support Chat"})
history = client.chat_ai.list_chats()
client.chat_ai.delete_chat(chat["id"])
```

### Knowledge Hub — Folders & Knowledge Bases

Folders tổ chức knowledge bases. Truyền folder IDs như `folder_ids` khi tạo assistant — xem [Hướng Dẫn Luồng Đầy Đủ §3](/vi/sdk/full-flow-guide/#3-quản-lý-knowledge-hub-và-gắn-vào-assistant).

```typescript
// Folders
const folders = await client.chatAi.listFolders();
const folder  = await client.chatAi.createFolder({ name: "Báo Cáo Q1" });
await client.chatAi.updateFolder(folder.id, { name: "Báo Cáo Q1 2025" });
await client.chatAi.deleteFolder(folder.id);

// Knowledge bases
const all = await client.chatAi.listKnowledge();
const kb  = await client.chatAi.getKnowledge("kb_id");
const created = await client.chatAi.createKnowledge({
  name: "Tài Liệu Hỗ Trợ",
  folderId: folder.id,
});
await client.chatAi.deleteKnowledge(created.id);
```

```python
# Folders được expose qua client.chat_ai (giống TypeScript)
knowledge_bases = client.chat_ai.list_knowledge()
```

---

## OpenAI-compatible AI Service — `client.ai` (Python)

Raw OpenAI-style completions, streaming, và embeddings. TypeScript SDK hiện không expose namespace này — dùng [Assistants → Completions](#completions) thay thế.

```python
# Single completion
response = client.ai.complete(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "Bạn là trợ lý CRM hữu ích."},
        {"role": "user",   "content": "Tóm tắt ghi chú khách hàng này: ..."},
    ],
    temperature=0.7,
)
print(response["choices"][0]["message"]["content"])

# Streaming
for chunk in client.ai.stream(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Soạn email follow-up cho lead này."}],
):
    print(chunk["choices"][0]["delta"].get("content", ""), end="", flush=True)

# Embeddings
result = client.ai.embed(
    model="text-embedding-ada-002",
    input=["khách hàng khiếu nại về billing", "vấn đề billing leo thang"],
)
```

---

## AI Agent — `aiAgent` / `ai_agent`

Streaming chat với assistants, quản lý embedding knowledge-base, parquet data, và end-user chat sessions. Xem [AI Agent](/vi/sdk/ai-agent/) để biết tham chiếu method đầy đủ. Entry point phổ biến nhất là `streamChat`.

### Stream Chat (SSE)

```typescript
const sessionId = crypto.randomUUID();

const response = await client.aiAgent.streamChat({
  id: sessionId,
  assistant_id: "asst_xxx",
  organization_id: "org_xxx",
  messages: [{ role: "user", content: "Deals nào đã chốt quý này?" }],
});

const reader = response.body!.getReader();
const decoder = new TextDecoder();

while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  const text = decoder.decode(value);
  for (const line of text.split("\n")) {
    if (!line.startsWith("data: ")) continue;
    const raw = line.slice(6).trim();
    if (raw === "[DONE]") break;
    try {
      const event = JSON.parse(raw);
      if (event.type === "text-delta") process.stdout.write(event.textDelta);
    } catch {}
  }
}
```

```python

session_id = str(uuid.uuid4())

resp = client.ai_agent.stream_chat({
    "id": session_id,
    "assistant_id": "asst_xxx",
    "organization_id": "org_xxx",
    "messages": [{"role": "user", "content": "Deals nào đã chốt quý này?"}],
})

for line in resp.iter_lines():
    if line:
        print(line)
```

### Prompt Suggestions

```typescript
const suggestions = await client.aiAgent.getAgentPromptSuggestion("asst_xxx");
```

```python
suggestions = client.ai_agent.get_agent_prompt_suggestion("assistant_id")
```

### Embedding Files (Knowledge Base)

```typescript
const files = await client.aiAgent.listEmbeddingFiles();
const file  = await client.aiAgent.getEmbeddingFile("file_id");

const classified = await client.aiAgent.classifyFile({
  url: "https://example.com/product-catalog.pdf",
  mime_type: "application/pdf",
});

await client.aiAgent.updateEmbeddingFileStatus("file_id", { status: "active" });
await client.aiAgent.deleteEmbeddingFile("file_id");
```

```python
files      = client.ai_agent.list_embedding_files()
classified = client.ai_agent.classify_file(
    url="https://example.com/product-catalog.pdf",
    mime_type="application/pdf",
)
```

### Parquet Data

```typescript
const job = await client.aiAgent.generateParquet({
  assistant_id: "asst_xxx",
  data: [{ id: "1", name: "Acme Corp", revenue: 120000 }],
});

const parquetFiles = await client.aiAgent.listParquetFiles();
await client.aiAgent.deleteParquetFile("file_id");
```

```python
result = client.ai_agent.generate_parquet(
    data=[{"id": "1", "name": "Acme Corp", "revenue": 120000}],
    file_name="users",
    folder_name="exports",
)
files = client.ai_agent.list_parquet_files()
client.ai_agent.delete_parquet_file("exports/users.parquet")
```

### End-user Chat Client

```typescript
const chat = await client.aiAgent.createClientChat({
  id: crypto.randomUUID(),
  assistantId: "asst_xxx",
  organizationId: "org_xxx",
  userId: "user_xxx",
  selectedVisibilityType: "private",
  message: {
    id: crypto.randomUUID(),
    role: "user",
    content: "Xin chào, tôi cần hỗ trợ về đơn hàng.",
    createdAt: new Date().toISOString(),
    parts: [{ type: "text", text: "Xin chào, tôi cần hỗ trợ về đơn hàng." }],
  },
});

const clientChats = await client.aiAgent.listClientChats();
const messages    = await client.aiAgent.listClientMessages(chat.id);
await client.aiAgent.deleteClientChat(chat.id);
```

```python
from datetime import datetime, timezone

chat = client.ai_agent.create_client_chat({
    "id":              str(uuid.uuid4()),
    "assistantId":     "assistant_id",
    "organizationId":  "org_xxx",
    "userId":          "user_id",
    "selectedVisibilityType": "private",
    "message": {
        "id":        str(uuid.uuid4()),
        "role":      "user",
        "content":   "Xin chào",
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "parts":     [{"type": "text", "text": "Xin chào"}],
    },
})

messages = client.ai_agent.list_client_messages(chat["id"])
client.ai_agent.delete_client_chat(chat["id"])
```

---

## Workflows — Activepieces (`client.activepieces`, TypeScript)

Activepieces là visual workflow builder. Để xem toàn bộ lifecycle (create → publish → trigger), xem [Hướng Dẫn Luồng Đầy Đủ §2](/vi/sdk/full-flow-guide/#2-tạo-workflow-với-activepieces-và-liên-kết-với-assistant).

### Flows

```typescript
const { data: flows } = await client.activepieces.listFlows();

const flow = await client.activepieces.getFlow("flow_id");

const newFlow = await client.activepieces.createFlow({
  displayName: "Thông Báo Lead Mới",
  folderId: "folder_id",
});

await client.activepieces.deleteFlow("flow_id");
```

### Trigger a Flow

```typescript
// Fire and forget
await client.activepieces.triggerFlow("flow_id", {
  contactId: "contact_xxx",
  event: "lead_qualified",
});

// Đợi kết quả
const result = await client.activepieces.triggerFlowSync("flow_id", {
  contactId: "contact_xxx",
  event: "lead_qualified",
});
```

### Runs, Folders, Connections, Tables

```typescript
const { data: runs }     = await client.activepieces.listRuns({ flowId: "flow_id", limit: 20 });
const run                = await client.activepieces.getRun("run_id");

const { data: folders }  = await client.activepieces.listFolders();
const folder             = await client.activepieces.createFolder({ displayName: "CRM Automations" });

const { data: connections } = await client.activepieces.listConnections();
await client.activepieces.upsertConnection({
  name: "slack-integration",
  type: "OAUTH2",
  value: { access_token: "xoxb-xxx" },
});

const { data: tables }   = await client.activepieces.listTables();
const { data: records }  = await client.activepieces.listRecords({ tableId: "table_id" });
```

---

## Boards & Items — `client.boards`

Boards là core data store cho CRM pipelines — leads, deals, tasks, hoặc bất kỳ dữ liệu có cấu trúc nào. Xem [Hướng Dẫn Luồng Đầy Đủ §4](/vi/sdk/full-flow-guide/#4-quản-lý-data-boards-và-items-crm-pipeline).

### Board CRUD

```typescript
const { data: boards } = await client.boards.list();
const board = await client.boards.get("board_id");

const newBoard = await client.boards.create({ name: "Enterprise Leads" });
await client.boards.update("board_id", { name: "Enterprise Leads 2025" });
await client.boards.delete("board_id");
```

```python
boards = client.boards.list().get("data", [])
```

### Items

```typescript
const { data: items } = await client.boards.listItems("board_id", { limit: 100 });
const item = await client.boards.getItem("board_id", "item_id");

const lead = await client.boards.createItem("board_id", {
  fields: { name: "Acme Corp", status: "new", value: 50000 },
});

await client.boards.updateItem("board_id", lead.id, {
  fields: { status: "qualified" },
});

await client.boards.deleteItem("board_id", "item_id");
await client.boards.bulkDeleteItems("board_id", ["item_1", "item_2", "item_3"]);
```

```python
leads = client.boards.list_items("board_id", limit=100).get("data", [])

lead = client.boards.create_item("board_id", {
    "fields": {"name": "Acme Corp", "status": "new", "value": 50000}
})

client.boards.update_item("board_id", lead["id"], {
    "fields": {"status": "qualified"}
})
```

### Search

```typescript
const results = await client.boards.search("board_id", { q: "enterprise" });
```

```python
results = client.boards.search("board_id", {"query": "enterprise"})
```

### Fields, Segments, Export

```typescript
// Fields
const field = await client.boards.createField("board_id", {
  name: "Giá Trị Deal",
  type: "number",
});
await client.boards.updateField("board_id", field.id, { name: "Giá Trị Hợp Đồng" });
await client.boards.deleteField("board_id", field.id);

// Segments
const { data: segments } = await client.boards.listSegments("board_id");
const segment = await client.boards.createSegment("board_id", {
  name: "Leads Giá Trị Cao",
  filters: [{ field: "value", op: "gt", value: 10000 }],
});

// Xuất CSV
const csv = await client.boards.exportCsv("board_id");
```

```python
csv = client.boards.export_csv("board_id")
```

---

## Contacts — `client.contacts`

```typescript
const { data: contacts } = await client.contacts.list({ limit: 50 });
const contact = await client.contacts.get("contact_id");

await client.contacts.update("contact_id", {
  name: "Alice B.",
  email: "alice@example.com",
  phone: "+84901234567",
});

const activity = await client.contacts.getActivity("contact_id");
const comments = await client.contacts.getComments("contact_id");
const files    = await client.contacts.getFiles("contact_id");
```

```python
result   = client.contacts.list(limit=50)
contacts = result.get("data", [])

contact = client.contacts.get("contact_id")

client.contacts.update("contact_id", {
    "name":  "Alice B.",
    "email": "alice@example.com",
    "phone": "+84901234567",
})

activity  = client.contacts.get_activities("conversation_id")
comments  = client.contacts.get_comments("contact_id")
files     = client.contacts.get_files("contact_id")
```

---

## Conversations — `client.conversations`

```typescript
// Tìm kiếm
const { data: convs } = await client.conversations.search({
  businessUnitId: "bu_xxx",
  q: "support",
  limit: 20,
});

// Chưa xử lý
const { data: open } = await client.conversations.getOutstanding({
  businessUnitId: "bu_xxx",
  limit: 50,
});

// Phân công
await client.conversations.assignTeamMember({
  conversation_id: "conv_xxx",
  user_id: "user_xxx",
});

// Cập nhật trạng thái
await client.conversations.updateStatus({
  conversation_id: "conv_xxx",
  status: "resolved",
});
```

```python
result = client.conversations.search(
    business_unit_id="bu_xxx",
    q="support",
    limit=20,
)
convs = result.get("data", [])

all_convs = client.conversations.list(limit=50).get("data", [])

client.conversations.update_status({
    "conversation_id": "conv_xxx",
    "status": "resolved",
})
```

---

## Messaging — `client.channel`, `client.messages`

```typescript
const channels = await client.channel.list();

await client.messages.send("conversation_id", {
  parts: [{ type: "text", text: "Xin chào, tôi có thể giúp gì cho bạn hôm nay?" }],
});

const msgs = await client.messages.list("conversation_id");
await client.channel.markRead("conversation_id");
```

```python
channels = client.channel.list()

client.messages.send(
    type="text",
    text="Xin chào, tôi có thể giúp gì cho bạn hôm nay?",
)

msgs = client.messages.list(limit=20)
```

---

## Channel Automation Workflows — `client.workflows` (Python)

```python
automations    = client.workflows.list_channel_automation().get("data", [])
whatsapp_flows = client.workflows.list_channel_automation(channel_type="whatsapp")
```

---

## Campaigns & Touchpoints — `client.campaign` (Python)

```python
# Campaign CRUD
campaigns = client.campaign.list().get("data", [])
campaign  = client.campaign.get("campaign_id")
new_camp  = client.campaign.create({"name": "Q2 Outreach", "type": "email"})
client.campaign.delete("campaign_id")

# Touchpoints
touchpoints = client.campaign.list_touchpoints().get("data", [])
tp = client.campaign.get_touchpoint("touchpoint_id")

client.campaign.create_touchpoint({
    "campaign_id": "campaign_id",
    "type":        "email",
    "delay_days":  3,
})
client.campaign.update_touchpoint("touchpoint_id", {"delay_days": 5})
client.campaign.delete_touchpoint("touchpoint_id")

# Kiểm tra cấu hình touchpoint trước khi lưu
result = client.campaign.validate_touchpoint({"type": "email", "template_id": "tpl_xxx"})
```

---

## Message Suggestion — `client.message_suggestion` (Python)

```python
suggestions = client.message_suggestion.get_suggestions({
    "conversation_id": "conv_xxx",
    "limit": 3,
})
```

---

## Predict — `client.predict` (Python)

```python
result = client.predict.predict({
    "model": "lead_score_v1",
    "input": {"company_size": 200, "industry": "saas", "mrr": 5000},
})
print(result["score"])   # 0.87
```
