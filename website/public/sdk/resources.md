## Resource Reference.

This page lists every resource namespace exposed by the SDK with the most common calls in each. Initialize the client first (see [Installation](/sdk/installation/) or [Quick Start](/sdk/quick-start/)). All snippets below assume `client` is the initialized instance.

For an end-to-end walkthrough that uses these resources together, see [Full Flow Guide](/sdk/full-flow-guide/).

---

## Assistants — `chatAi` / `chat_ai`.

Manages AI assistants (CRUD), runs OpenAI-compatible completions, and handles document/file processing. The same namespace also covers Knowledge Hub folders and knowledge bases.

### Assistant CRUD.

```typescript
// List all assistants
const assistants = await client.chatAi.listAssistants();

// Get a single assistant
const assistant = await client.chatAi.getAssistant("9f77692f-33d0-436a-8138-2efb268838e6");

// Create — provider_id and model_id are required
const created = await client.chatAi.createAssistant({
  name: "Support Bot",
  workflow_name: "support_bot_v1",
  provider_id: "system",    // org's default LLM provider
  model_id: "gpt-4o",    // or "Default" for system default
  description: "Handles tier-1 support queries",
});

const assistantId = created.id;  // Use this for all subsequent calls

// Update — workflow_name is required on update too
await client.chatAi.updateAssistant(created.id, {
  name: "Support Bot v2",
  workflow_name: "support_bot_v1",
  folder_ids: ["folder_id_1"],  // Attach knowledge folders
  workflow_function_call: [{ flow_id: "flow_id", description: "Update CRM" }],
});

// Update only system instructions
await client.chatAi.updateAssistantInstructions(created.id, "New instructions.");

// Delete
await client.chatAi.deleteAssistant(created.id);
```

```python
# List all assistants
assistants = client.chat_ai.list_assistants()

# Get a single assistant
assistant = client.chat_ai.get_assistant("9f77692f-33d0-436a-8138-2efb268838e6")

# Create — provider_id and model_id are required
created = client.chat_ai.create_assistant({
    "name": "Support Bot",
    "workflow_name": "support_bot_v1",
    "provider_id": "system",
    "model_id": "gpt-4o",
    "description": "Handles tier-1 support queries",
})
assistant_id = created["id"]

# Update
client.chat_ai.update_assistant(created["id"], {
    "name": "Support Bot v2",
    "workflow_name": "support_bot_v1",
    "folder_ids": ["folder_id_1"],
})

# Update only instructions
client.chat_ai.update_assistant_instructions(created["id"], "New instructions.")

# Delete
client.chat_ai.delete_assistant(created["id"])
```

### Completions.

```typescript
const response = await client.chatAi.chat({
  model: "gpt-4o",
  messages: [
    { role: "system", content: "You are a helpful CRM assistant." },
    { role: "user", content: "Summarize this customer note: ..." },
  ],
});
console.log(response.choices[0].message.content);

// List available models
const models = await client.chatAi.listModels();
```

```python
response = client.chat_ai.chat({
    "model": "gpt-4o",
    "messages": [
        {"role": "system", "content": "You are a helpful CRM assistant."},
        {"role": "user", "content": "Summarize this customer note: ..."},
    ],
})
print(response["choices"][0]["message"]["content"])

# List models
models = client.chat_ai.list_models()
```

### File Processing.

```typescript
// Extract structured data from PDF or image
const result = await client.chatAi.extractFile({
  modelName: "gpt-4o",
  url: "https://example.com/invoice.pdf",
  organizationId: "org_xxx",
});
// result.data → {"invoice_number": "INV-001", "total": 1200, ...}

// Upload a file
const uploaded = await client.chatAi.uploadFile({
  file: fileBuffer,
  name: "report.pdf",
});
```

```python
# Extract structured data
result = client.chat_ai.process_document(
    model_name="gpt-4o",
    url="https://example.com/invoice.pdf",
    organization_id="org_xxx",
)
# result["data"] → {"invoice_number": "INV-001", "total": 1200, ...}

# Upload file
from pathlib import Path
path = Path("./docs/faq.pdf")
files = {
    "file": (path.name, path.read_bytes(), "application/pdf"),
    "folder_id": (None, folder_id),
    "organization_id": (None, "org_xxx"),
}
uploaded = client.chat_ai.upload_file(files)
```

### Knowledge Hub — Folders & Knowledge Bases.

```typescript
const folders  = await client.chatAi.listFolders();
const folder   = await client.chatAi.createFolder({ name: "Q1 Reports" });
await client.chatAi.updateFolder(folder.id, { name: "Q1 2025 Reports" });
await client.chatAi.deleteFolder(folder.id);

const all     = await client.chatAi.listKnowledge();
const created = await client.chatAi.createKnowledge({ name: "Support Docs", folderId: folder.id });
await client.chatAi.deleteKnowledge(created.id);
```

```python
knowledge_bases = client.chat_ai.list_knowledge()
```

---

## OpenAI-compatible AI — `client.ai` (Python only).

Raw OpenAI-style completions, streaming, and embeddings. TypeScript uses `client.chatAi.chat()` instead.

```python
# Single completion
response = client.ai.complete(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful CRM assistant."},
        {"role": "user", "content": "Summarize this customer note: ..."},
    ],
    temperature=0.7,
)
print(response["choices"][0]["message"]["content"])

# Streaming
for chunk in client.ai.stream(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Draft a follow-up email."}],
):
    print(chunk["choices"][0]["delta"].get("content", ""), end="", flush=True)

# Embeddings
result = client.ai.embed(
    model="text-embedding-ada-002",
    input=["customer complained about billing", "billing issue escalated"],
)
```

---

## AI Agent — `aiAgent` / `ai_agent`.

Connects to a dedicated AI Agent service. Exposes streaming chat (SSE), knowledge-base embedding management, columnar data (Parquet), distributed tracing (Tempo), and the Chat Client sub-API.

### Stream Chat (SSE) — Primary Entry Point.

Keep the same `id` (session UUID) across turns to maintain conversation history. Omit it on the first message to auto-generate a new session.

```typescript
import { randomUUID } from "crypto";

const sessionId = randomUUID();

const response = await client.aiAgent.streamChat({
  id:              sessionId,
  assistant_id:    "asst_xxx",
  organization_id: "org_xxx",
  messages:        [{ role: "user", content: "What deals closed this quarter?" }],
});

const reader  = response.body!.getReader();
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
import uuid, json

session_id = str(uuid.uuid4())

resp = client.ai_agent.stream_chat({
    "id":              session_id,
    "assistant_id":    "asst_xxx",
    "organization_id": "org_xxx",
    "messages":        [{"role": "user", "content": "What deals closed this quarter?"}],
})

for line in resp.iter_lines():
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

### Sub-agent Chat.

```typescript
const res = await client.aiAgent.streamSubAgentChat({
  assistant_id:    "asst_sub",
  organization_id: "org_abc",
  session_id:      "sess_xyz",
  chat_id:         "chat_id",
  messages:        [{ role: "user", content: "Explain the data." }],
});
const history = await client.aiAgent.getSubAgentHistory({ session_id: "sess_xyz", chat_id: "chat_id" });
```

```python
res     = client.ai_agent.stream_sub_agent_chat({ "assistant_id": "asst_sub", ... })
history = client.ai_agent.get_sub_agent_history(session_id="sess_xyz", chat_id="chat_id")
```

### Prompt Suggestions.

```typescript
const suggestions = await client.aiAgent.getAgentPromptSuggestion("asst_xxx");
```

```python
suggestions = client.ai_agent.get_agent_prompt_suggestion("asst_xxx")
```

### Embeddings & Knowledge Base (RAG).

Upload files first via `client.boards.uploadFile` / `client.boards.upload_file`, then trigger embedding processing.

```typescript
await client.aiAgent.processEmbedding({ fileId: "file_abc" });

const files      = await client.aiAgent.listEmbeddingFiles({ page: 1, limit: 20 });
const file       = await client.aiAgent.getEmbeddingFile("file_abc");
const preview    = await client.aiAgent.previewEmbeddingFile({ file_id: "file_abc" });
const classified = await client.aiAgent.classifyFile({ file_id: "file_abc" });

await client.aiAgent.updateEmbeddingFileStatus("file_abc", "active");
await client.aiAgent.deleteEmbeddingFile("file_abc");
```

```python
client.ai_agent.process_embedding("file_abc")
client.ai_agent.process_embedding("file_abc", options={"chunk_size": 512})

files      = client.ai_agent.list_embedding_files(page=1, limit=20)
file       = client.ai_agent.get_embedding_file("file_abc")
preview    = client.ai_agent.preview_embedding_file(file_id="file_abc")
classified = client.ai_agent.classify_file(file_id="file_abc")

client.ai_agent.update_embedding_file_status("file_abc", "active")
client.ai_agent.delete_embedding_file("file_abc")
```

### Parquet.

```typescript
const result = await client.aiAgent.generateParquet({
  data:       [{ id: 1, name: "Alice" }, { id: 2, name: "Bob" }],
  fileName:   "users",
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

### Distributed Tracing (Grafana Tempo).

```typescript
const traces = await client.aiAgent.getTraces({
  service:   "ai-agent",
  limit:     50,
  timeRange: 3600,
  orgId:     "org_abc",
  details:   true,
});
const trace    = await client.aiAgent.getTrace("trace_id_hex");
const services = await client.aiAgent.getTraceServices();
const tags     = await client.aiAgent.getTraceTags();
const values   = await client.aiAgent.getTraceTagValues("http.status_code");
const results  = await client.aiAgent.searchTraceQL(`{ .service.name = "ai-agent" && .http.status = 500 }`);
```

```python
traces   = client.ai_agent.get_traces(service="ai-agent", limit=50, time_range=3600, org_id="org_abc")
trace    = client.ai_agent.get_trace("trace_id_hex")
services = client.ai_agent.get_trace_services()
tags     = client.ai_agent.get_trace_tags()
values   = client.ai_agent.get_trace_tag_values("http.status_code")
results  = client.ai_agent.search_traceql('{ .service.name = "ai-agent" && .http.status = 500 }')
```

### Chat Client Sub-API (frontend applications).

**Auth:**
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

**Chats:**
```typescript
await client.aiAgent.createClientChat({
  id:             "chat_uuid",
  assistantId:    "asst_abc",
  organizationId: "org_abc",
  message: {
    id:    "msg_uuid",
    role:  "user",
    parts: [{ type: "text", text: "Hello!" }],
  },
});
const chats = await client.aiAgent.listClientChats({ organization_id: "org_abc", limit: 20 });
const chat  = await client.aiAgent.getClientChat("chat_id");
await client.aiAgent.updateClientChat("chat_id", { visibility: "private" });
await client.aiAgent.deleteClientChat("chat_id");
await client.aiAgent.deleteAllClientChats({ organization_id: "org_abc" });
await client.aiAgent.generateClientChatTitle("chat_id");

// Stream real-time chat status as SSE
const statusStream = await client.aiAgent.streamClientChatStatus("chat_id");
```

```python
client.ai_agent.create_client_chat({
    "id": "chat_uuid", "assistantId": "asst_abc", "organizationId": "org_abc",
    "message": {"id": "msg_uuid", "role": "user", "parts": [{"type": "text", "text": "Hello!"}]},
})
chats = client.ai_agent.list_client_chats(organization_id="org_abc", limit=20)
chat  = client.ai_agent.get_client_chat("chat_id")
client.ai_agent.delete_client_chat("chat_id")
client.ai_agent.delete_all_client_chats("org_abc")
client.ai_agent.generate_client_chat_title("chat_id")
status_stream = client.ai_agent.stream_client_chat_status("chat_id")
```

**Messages:**
```typescript
await client.aiAgent.persistClientMessage({ chatId: "chat_id", content: "Hello" });
const messages = await client.aiAgent.listClientMessages("chat_id");
await client.aiAgent.deleteTrailingMessages("message_id");
```

```python
client.ai_agent.persist_client_message({"chatId": "chat_id", "content": "Hello"})
messages = client.ai_agent.list_client_messages("chat_id")
client.ai_agent.delete_trailing_messages("message_id")
```

**Votes:**
```typescript
const votes = await client.aiAgent.getVotes("chat_id");
await client.aiAgent.updateVote({ messageId: "msg_id", vote: "up" });
```

```python
votes = client.ai_agent.get_votes("chat_id")
client.ai_agent.update_vote({"messageId": "msg_id", "vote": "up"})
```

**Documents (AI-generated artifacts):**
```typescript
await client.aiAgent.createDocument({ kind: "text", content: "Draft..." });
const doc        = await client.aiAgent.getDocument("doc_id");
const latest     = await client.aiAgent.getDocumentLatest("doc_id");
const pub        = await client.aiAgent.getDocumentPublic("doc_id");
const byKind     = await client.aiAgent.getDocumentLatestByKind({ kind: "text" });
const suggestion = await client.aiAgent.getDocumentSuggestions("doc_id");
await client.aiAgent.deleteDocument("doc_id");
```

```python
client.ai_agent.create_document({"kind": "text", "content": "Draft..."})
doc        = client.ai_agent.get_document("doc_id")
latest     = client.ai_agent.get_document_latest("doc_id")
suggestion = client.ai_agent.get_document_suggestions("doc_id")
client.ai_agent.delete_document("doc_id")
```

**Admin Guides (PDF streams):**
```typescript
const guides = await client.aiAgent.listAdminGuides();
const response = await client.aiAgent.getAdminGuide("onboarding.pdf");
const blob = await response.blob();
```

```python
guides   = client.ai_agent.list_admin_guides()
response = client.ai_agent.get_admin_guide("onboarding.pdf")
with open("onboarding.pdf", "wb") as f:
    f.write(response.content)
```

### Legacy v1 Chat (non-streaming, backwards compat only).

```typescript
const chats = await client.aiAgent.listChats({ organization_id: "org_abc", user_id: "user_123", limit: 20 });
const chat  = await client.aiAgent.getChat("chat_id", true);  // true = include messages
await client.aiAgent.deleteChat("chat_id", { organization_id: "org_abc", user_id: "user_123" });
```

```python
chats = client.ai_agent.list_chats(organization_id="org_abc", user_id="user_123", limit=20)
chat  = client.ai_agent.get_chat("chat_id", include_messages=True)
client.ai_agent.delete_chat("chat_id", organization_id="org_abc", user_id="user_123")
```

---

## Activepieces Workflows — `activepieces`.

Visual workflow builder. The TypeScript SDK exposes flows, runs, folders, connections, tables, and records.

**Important:** A newly created flow is in DRAFT state with no trigger. Add a trigger and publish before calling `triggerFlow`, otherwise you'll get 404.

### Flows.

```typescript
const { data: flows } = await client.activepieces.listFlows({ limit: 5 });
const projectId = flows[0]?.projectId;

const flow = await client.activepieces.createFlow({
  displayName: "CRM Update on New Lead",
  projectId,
});

await client.activepieces.deleteFlow("flow_id");
```

```python
res     = client.activepieces.list_flows(limit=5)
flows   = res.get("data", [])
flow    = client.activepieces.create_flow(display_name="CRM Update on New Lead", project_id=project_id)
```

### Apply Flow Operations.

Used to add/update triggers and actions to a flow:

```typescript
// Set Webhook trigger
await client.activepieces.applyFlowOperation(flow.id, {
  type:    "UPDATE_TRIGGER",
  request: {
    name:        "trigger",
    type:        "PIECE_TRIGGER",
    valid:       true,
    displayName: "Webhook",
    settings: {
      pieceName:        "@activepieces/piece-webhook",
      pieceVersion:     "0.1.24",
      triggerName:      "catch_webhook",
      input:            { authType: "none" },
      propertySettings: {},
    },
  },
});

// Publish — DRAFT → ENABLED; webhook URL becomes live
await client.activepieces.applyFlowOperation(flow.id, {
  type:    "LOCK_AND_PUBLISH",
  request: {},
});
```

```python
client.activepieces.apply_flow_operation(flow["id"], {
    "type": "UPDATE_TRIGGER",
    "request": {
        "name": "trigger", "type": "PIECE_TRIGGER", "valid": True, "displayName": "Webhook",
        "settings": {
            "pieceName": "@activepieces/piece-webhook", "pieceVersion": "0.1.24",
            "triggerName": "catch_webhook", "input": {"authType": "none"}, "propertySettings": {},
        },
    },
})
client.activepieces.apply_flow_operation(flow["id"], {"type": "LOCK_AND_PUBLISH", "request": {}})
```

### Trigger a Flow.

```typescript
// Fire and forget
await client.activepieces.triggerFlow(flow.id, { contact_name: "Jane Smith", email: "jane@example.com" });

// Synchronous — flow must have a "Return Response" action, else times out after 30s
const result = await client.activepieces.triggerFlowSync(flow.id, { contact_name: "Jane Smith" });
```

```python
client.activepieces.trigger_flow(flow["id"], {"contact_name": "Jane Smith", "email": "jane@example.com"})
result = client.activepieces.trigger_flow_sync(flow["id"], {"contact_name": "Jane Smith"})
```

### Runs, Folders, Connections, Tables.

```typescript
const { data: runs }        = await client.activepieces.listRuns({ flowId: flow.id, limit: 10 });
const run                   = await client.activepieces.getRun("run_id");

const { data: folders }     = await client.activepieces.listFolders();
const folder                = await client.activepieces.createFolder({ displayName: "CRM Automations" });

const { data: connections } = await client.activepieces.listConnections();
await client.activepieces.upsertConnection({
  name:  "slack-integration",
  type:  "OAUTH2",
  value: { access_token: "xoxb-xxx" },
});

const { data: tables }  = await client.activepieces.listTables();
const { data: records } = await client.activepieces.listRecords({ tableId: "table_id" });
```

```python
res  = client.activepieces.list_runs(flow_id=flow["id"], limit=10)
runs = res.get("data", [])

# Folders, connections, tables — refer to Python SDK source for method signatures
```

---

## Boards & Items (CRM) — `boards`.

Boards are the core CRM data store. Also used for Knowledge Hub file management (folders, uploaded files).

### Board CRUD.

```typescript
const { data: boards } = await client.boards.list();
const board = await client.boards.get("board_id");
const newBoard = await client.boards.create({ name: "Sales Pipeline", description: "Track all active deals" });
await client.boards.update("board_id", { name: "Sales Pipeline 2025" });
await client.boards.delete("board_id");
```

```python
boards    = client.boards.list().get("data", [])
board     = client.boards.create(name="Sales Pipeline", description="Track all active deals")
board_id  = board["_id"]
```

### Fields.

Field types: `ShortText`, `LongText`, `Number`, `Dropdown`, `Date`, `Checkbox`, etc. `createField` returns the updated board with all fields.

```typescript
const updated        = await client.boards.createField(board._id, { name: "Company", type: "ShortText" });
const identifierField = updated.fields.find(f => f.is_identifier);  // auto-created with every board

await client.boards.updateField("board_id", field.id, { name: "Contract Value" });
await client.boards.deleteField("board_id", field.id);
```

```python
updated          = client.boards.create_field(board["_id"], {"name": "Company", "type": "ShortText"})
identifier_field = next(f for f in updated["fields"] if f.get("is_identifier"))
```

### Items (Records).

Items use `{ fields: [{ board_field_id, value }] }` format for creation. Update uses `{ data: [{ key: fieldId, value }] }` format.

```typescript
const item = await client.boards.createItem(board._id, {
  fields: [{ board_field_id: identifierField._id, value: "Acme Corp" }],
});

const { data: items } = await client.boards.listItems(board._id, { limit: 20, skip: 0 });
const singleItem = await client.boards.getItem("board_id", "item_id");

await client.boards.updateItem(board._id, item._id, {
  data: [{ key: identifierField._id, value: "Acme Corp — Closed Won" }],
});

await client.boards.deleteItem(board._id, item._id);
await client.boards.bulkDeleteItems("board_id", ["item_1", "item_2"]);
```

```python
item  = client.boards.create_item(board["_id"], {
    "fields": [{"board_field_id": identifier_field["_id"], "value": "Acme Corp"}],
})
items = client.boards.list_items(board["_id"], limit=20, skip=0)

client.boards.update_item(board["_id"], item["_id"], {
    "data": [{"key": identifier_field["_id"], "value": "Acme Corp — Closed Won"}],
})
client.boards.delete_item(board["_id"], item["_id"])
```

### Search & Segments.

```typescript
const { data: results } = await client.boards.search("board_id", { q: "Acme", limit: 10 });

const { data: segments } = await client.boards.listSegments("board_id");
const segment = await client.boards.createSegment("board_id", {
  name:    "High Value Leads",
  filters: [{ field: "value", op: "gt", value: 10000 }],
});
```

```python
results = client.boards.search(board_id, {"q": "Acme", "limit": 10}).get("data", [])

segments = client.boards.list_segments(board_id).get("data", [])
segment  = client.boards.create_segment(board_id, {
    "name": "High Value Leads",
    "filters": [{"field": "value", "op": "gt", "value": 10000}],
})
```

### CSV Export.

```typescript
const csv = await client.boards.exportCsv("board_id");
// csv is a string
```

```python
csv = client.boards.export_csv("board_id")
```

### Knowledge Hub File Management (via client.boards).

```typescript
// Create a folder
const folder = await client.boards.createFolder({
  name:             "Product Documentation",
  organization_id:  "org_your_org_id",
  parent_folder_id: "root",
  source_type:      "upload",
});

// Upload a file
import { readFileSync } from "fs";
const fileBuffer = readFileSync("./docs/faq.pdf");
const formData   = new FormData();
formData.append("file", new Blob([fileBuffer], { type: "application/pdf" }), "faq.pdf");
formData.append("folder_id", folder._id);
formData.append("organization_id", "org_your_org_id");
const uploaded = await client.boards.uploadFile(formData);

// Manage folders
const folders  = await client.boards.searchFolders({ q: "Product" });
const contents = await client.boards.getFolderContents(folder._id);
await client.boards.updateFolder(folder._id, { name: "Product Docs v2" });
const files = await client.boards.searchFiles({ folderId: folder._id });
await client.boards.deleteFolders({ ids: [folder._id] });
```

```python
folder = client.boards.create_folder({
    "name": "Product Documentation",
    "organization_id": "org_your_org_id",
    "parent_folder_id": "root",
    "source_type": "upload",
})

from pathlib import Path
path = Path("./docs/faq.pdf")
files = {
    "file":            (path.name, path.read_bytes(), "application/pdf"),
    "folder_id":       (None, folder["_id"]),
    "organization_id": (None, "org_your_org_id"),
}
uploaded = client.boards.upload_file(files)
file_id  = uploaded.get("file_id") or uploaded.get("_id")

folders  = client.boards.search_folders(q="Product")
contents = client.boards.get_folder_contents(folder["_id"])
client.boards.update_folder(folder["_id"], {"name": "Product Docs v2"})
files    = client.boards.search_files(folder_id=folder["_id"])
client.boards.delete_folders([folder["_id"]])
```

---

## Contacts — `contacts`.

```typescript
const { data: contacts } = await client.contacts.list({ limit: 50 });
const contact = await client.contacts.get("contact_id");

await client.contacts.update("contact_id", {
  name:  "Alice B.",
  email: "alice@example.com",
  phone: "+84901234567",
});

const activity = await client.contacts.getActivity("contact_id");
const comments = await client.contacts.getComments("contact_id");
const files    = await client.contacts.getFiles("contact_id");
```

```python
contacts = client.contacts.list(limit=50).get("data", [])
contact  = client.contacts.get("contact_id")

client.contacts.update("contact_id", {
    "name":  "Alice B.",
    "email": "alice@example.com",
    "phone": "+84901234567",
})

activity = client.contacts.get_activities("conversation_id")
comments = client.contacts.get_comments("contact_id")
files    = client.contacts.get_files("contact_id")
```

---

## Conversations — `conversations`.

```typescript
const { data: convs } = await client.conversations.search({
  businessUnitId: "bu_xxx",
  q:              "support",
  limit:          20,
});

const { data: open } = await client.conversations.getOutstanding({ businessUnitId: "bu_xxx", limit: 50 });

await client.conversations.assignTeamMember({ conversation_id: "conv_xxx", user_id: "user_xxx" });
await client.conversations.updateStatus({ conversation_id: "conv_xxx", status: "resolved" });
```

```python
convs    = client.conversations.search(business_unit_id="bu_xxx", q="support", limit=20).get("data", [])
all_conv = client.conversations.list(limit=50).get("data", [])
client.conversations.update_status({"conversation_id": "conv_xxx", "status": "resolved"})
```

---

## Messaging — `channel` / `messages`.

```typescript
const channels = await client.channel.list();
await client.messages.send("conversation_id", {
  parts: [{ type: "text", text: "Hello, how can I help you today?" }],
});
const msgs = await client.messages.list("conversation_id");
await client.channel.markRead("conversation_id");
```

```python
channels = client.channel.list()
client.messages.send(type="text", text="Hello, how can I help you today?")
msgs = client.messages.list(limit=20)
```

---

## Platform — `platform`.

```typescript
const me = await client.platform.getMe();
```

```python
me = client.platform.get_me()
```

---

## Additional Python-only Resources.

### Channel Automation — `workflows`.

```python
automations    = client.workflows.list_channel_automation().get("data", [])
whatsapp_flows = client.workflows.list_channel_automation(channel_type="whatsapp")
```

### Campaigns & Touchpoints — `campaign`.

```python
campaigns  = client.campaign.list().get("data", [])
campaign   = client.campaign.get("campaign_id")
new_camp   = client.campaign.create({"name": "Q2 Outreach", "type": "email"})
client.campaign.delete("campaign_id")

touchpoints = client.campaign.list_touchpoints().get("data", [])
tp          = client.campaign.get_touchpoint("touchpoint_id")
client.campaign.create_touchpoint({"campaign_id": "campaign_id", "type": "email", "delay_days": 3})
client.campaign.update_touchpoint("touchpoint_id", {"delay_days": 5})
client.campaign.delete_touchpoint("touchpoint_id")

# Validate config before saving
result = client.campaign.validate_touchpoint({"type": "email", "template_id": "tpl_xxx"})
```

### Message Suggestion — `message_suggestion`.

```python
suggestions = client.message_suggestion.get_suggestions({
    "conversation_id": "conv_xxx",
    "limit": 3,
})
```

### ML Prediction — `predict`.

```python
result = client.predict.predict({
    "model": "lead_score_v1",
    "input": {"company_size": 200, "industry": "saas", "mrr": 5000},
})
print(result["score"])  # e.g. 0.87
```
