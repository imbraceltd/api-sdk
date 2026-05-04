# Resource Reference

> Per-namespace reference for the Imbrace SDKs — assistants, AI agent, workflows, boards, contacts, and more.

This page lists every resource namespace exposed by the SDK with the most common calls in each. Initialize the client first (see [Installation](/sdk/installation/) or [Quick Start](/sdk/quick-start/)). All snippets below assume `client` is the initialized instance.

For an end-to-end walkthrough that uses these resources together, see [Full Flow Guide](/sdk/full-flow-guide/).

---

## Assistants — `chatAi` / `chat_ai`

Manages AI assistants (CRUD), runs OpenAI-compatible completions, and handles document/file processing. The same namespace also covers Knowledge Hub folders and knowledge bases.

### Assistant CRUD

```typescript
// List all assistants in your account
const assistants = await client.chatAi.listAssistants();
// Each assistant has an `id` (UUID) and `_id` (MongoDB ObjectId).
// Use the `id` field for all subsequent calls.

// Get a single assistant
const assistant = await client.chatAi.getAssistant("9f77692f-33d0-436a-8138-2efb268838e6");

// Create — provider_id and model_id are required
const created = await client.chatAi.createAssistant({
  name: "Support Bot",
  workflow_name: "support_bot_v1",
  provider_id: "system",
  model_id: "gpt-4o",
  description: "Handles tier-1 support queries",
});

// Update — workflow_name is required on update too
const updated = await client.chatAi.updateAssistant(created.id, {
  name: "Support Bot v2",
  workflow_name: "support_bot_v1",
});

// Update only the system instructions
await client.chatAi.updateAssistantInstructions(
  created.id,
  "You are a helpful support agent.",
);

await client.chatAi.deleteAssistant(created.id);
```

```python
# List all assistants
assistants = client.chat_ai.list_assistants()

# Get a single assistant
assistant = client.chat_ai.get_assistant("9f77692f-33d0-436a-8138-2efb268838e6")

# Create — provider_id and model_id are required
created = client.chat_ai.create_assistant({
    "name":          "Support Bot",
    "workflow_name": "support_bot_v1",
    "provider_id":   "system",
    "model_id":      "gpt-4o",
    "description":   "Handles tier-1 support queries",
})

# Update
updated = client.chat_ai.update_assistant(created["id"], {
    "name":          "Support Bot v2",
    "workflow_name": "support_bot_v1",
})

# Update only the system instructions
client.chat_ai.update_assistant_instructions(
    created["id"],
    "You are a helpful support agent.",
)

client.chat_ai.delete_assistant(created["id"])
```

### Completions

```typescript
const response = await client.chatAi.chat({
  model: "gpt-4o",
  messages: [
    { role: "system", content: "You are a helpful CRM assistant." },
    { role: "user", content: "Summarize this customer note: ..." },
  ],
});
console.log(response.choices[0].message.content);
```

```python
response = client.chat_ai.chat({
    "model": "gpt-4o",
    "messages": [
        {"role": "system", "content": "You are a helpful CRM assistant."},
        {"role": "user",   "content": "Summarize this customer note: ..."},
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

### File processing

```typescript
// Extract structured data from a PDF or image
const result = await client.chatAi.extractFile({
  modelName: "gpt-4o",
  url: "https://example.com/invoice.pdf",
  organizationId: "org_xxx",
});

// Upload a file for processing
const uploaded = await client.chatAi.uploadFile({
  file: fileBuffer,
  name: "report.pdf",
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

### Persistent chat sessions (Python)

```python
chat    = client.chat_ai.create_chat({"title": "Support Chat"})
history = client.chat_ai.list_chats()
client.chat_ai.delete_chat(chat["id"])
```

### Knowledge Hub — folders & knowledge bases

Folders organize knowledge bases. A knowledge base is a set of files an assistant can retrieve from. Pass folder IDs as `folder_ids` when creating an assistant — see [Full Flow Guide §3](/sdk/full-flow-guide/#3-manage-knowledge-hubs-and-attach-to-an-assistant).

```typescript
// Folders
const folders = await client.chatAi.listFolders();
const folder  = await client.chatAi.createFolder({ name: "Q1 Reports" });
await client.chatAi.updateFolder(folder.id, { name: "Q1 2025 Reports" });
await client.chatAi.deleteFolder(folder.id);

// Knowledge bases
const all = await client.chatAi.listKnowledge();
const kb  = await client.chatAi.getKnowledge("kb_id");
const created = await client.chatAi.createKnowledge({
  name: "Support Docs",
  folderId: folder.id,
});
await client.chatAi.deleteKnowledge(created.id);
```

```python
# Folders are exposed via client.chat_ai (same as TypeScript)
# Refer to the SDK source for the exact method signatures.
knowledge_bases = client.chat_ai.list_knowledge()
```

---

## OpenAI-compatible AI service — `client.ai` (Python)

Raw OpenAI-style completions, streaming, and embeddings against the `aiv2` service. The TypeScript SDK does not currently expose this namespace — use [Assistants → Completions](#completions) instead.

```python
# Single completion
response = client.ai.complete(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful CRM assistant."},
        {"role": "user",   "content": "Summarize this customer note: ..."},
    ],
    temperature=0.7,
)
print(response["choices"][0]["message"]["content"])

# Streaming
for chunk in client.ai.stream(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Draft a follow-up email for this lead."}],
):
    print(chunk["choices"][0]["delta"].get("content", ""), end="", flush=True)

# Embeddings
result = client.ai.embed(
    model="text-embedding-ada-002",
    input=["customer complained about billing", "billing issue escalated"],
)
```

---

## AI Agent — `aiAgent` / `ai_agent`

Streaming chat with assistants, knowledge-base embedding management, parquet data, and end-user chat sessions. For the full method-by-method reference, see [AI Agent](/sdk/ai-agent/). The most common entry point is `streamChat`.

### Stream chat (SSE)

Keep the `id` (session id) across turns to maintain conversation history. Omit it on the first message to let the SDK generate one. `user_id` is also optional — resolved from the auth context.

```typescript
const sessionId = crypto.randomUUID();

const response = await client.aiAgent.streamChat({
  id: sessionId,
  assistant_id: "asst_xxx",
  organization_id: "org_xxx",
  messages: [{ role: "user", content: "What deals closed this quarter?" }],
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
import uuid

session_id = str(uuid.uuid4())  # persist for the conversation lifetime

resp = client.ai_agent.stream_chat({
    "id": session_id,
    "assistant_id": "asst_xxx",
    "organization_id": "org_xxx",
    "messages": [{"role": "user", "content": "What deals closed this quarter?"}],
})

for line in resp.iter_lines():
    if line:
        print(line)
```

### Prompt suggestions

```typescript
const suggestions = await client.aiAgent.getAgentPromptSuggestion("asst_xxx");
```

```python
suggestions = client.ai_agent.get_agent_prompt_suggestion("assistant_id")
```

### Embedding files (knowledge base)

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

### Parquet data

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

### End-user chat client

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
    content: "Hello, I need help with my order.",
    createdAt: new Date().toISOString(),
    parts: [{ type: "text", text: "Hello, I need help with my order." }],
  },
});

const clientChats = await client.aiAgent.listClientChats();
const messages    = await client.aiAgent.listClientMessages(chat.id);
await client.aiAgent.deleteClientChat(chat.id);
```

```python
import uuid
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
        "content":   "Hello",
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "parts":     [{"type": "text", "text": "Hello"}],
    },
})

messages = client.ai_agent.list_client_messages(chat["id"])
client.ai_agent.delete_client_chat(chat["id"])
```

---

## Workflows — Activepieces (`client.activepieces`, TypeScript)

Activepieces is the visual workflow builder. The TypeScript SDK exposes flows, runs, folders, connections, tables, and records. For the full lifecycle (create → publish → trigger), see [Full Flow Guide §2](/sdk/full-flow-guide/#2-create-a-workflow-with-activepieces-and-bind-it-to-an-assistant).

### Flows

```typescript
const { data: flows } = await client.activepieces.listFlows();

const flow = await client.activepieces.getFlow("flow_id");

const newFlow = await client.activepieces.createFlow({
  displayName: "New Lead Notification",
  folderId: "folder_id",
});

await client.activepieces.deleteFlow("flow_id");
```

### Trigger a flow

```typescript
// Fire and forget
await client.activepieces.triggerFlow("flow_id", {
  contactId: "contact_xxx",
  event: "lead_qualified",
});

// Wait for result
const result = await client.activepieces.triggerFlowSync("flow_id", {
  contactId: "contact_xxx",
  event: "lead_qualified",
});
```

### Runs, folders, connections, tables

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

## Boards & items — `client.boards`

Boards are the core data store for CRM pipelines — leads, deals, tasks, or any structured data. Pass board ids in `board_ids` when creating an assistant to give it access to that data — see [Full Flow Guide §4](/sdk/full-flow-guide/#4-manage-data-boards-and-items-crm-pipelines).

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

### Fields, segments, export

```typescript
// Fields
const field = await client.boards.createField("board_id", {
  name: "Deal Value",
  type: "number",
});
await client.boards.updateField("board_id", field.id, { name: "Contract Value" });
await client.boards.deleteField("board_id", field.id);

// Segments
const { data: segments } = await client.boards.listSegments("board_id");
const segment = await client.boards.createSegment("board_id", {
  name: "High Value Leads",
  filters: [{ field: "value", op: "gt", value: 10000 }],
});

// Export to CSV
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
// Search
const { data: convs } = await client.conversations.search({
  businessUnitId: "bu_xxx",
  q: "support",
  limit: 20,
});

// Outstanding (unresolved)
const { data: open } = await client.conversations.getOutstanding({
  businessUnitId: "bu_xxx",
  limit: 50,
});

// Assign
await client.conversations.assignTeamMember({
  conversation_id: "conv_xxx",
  user_id: "user_xxx",
});

// Update status
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
  parts: [{ type: "text", text: "Hello, how can I help you today?" }],
});

const msgs = await client.messages.list("conversation_id");
await client.channel.markRead("conversation_id");
```

```python
channels = client.channel.list()

client.messages.send(
    type="text",
    text="Hello, how can I help you today?",
)

msgs = client.messages.list(limit=20)
```

---

## Channel automation workflows — `client.workflows` (Python)

```python
automations    = client.workflows.list_channel_automation().get("data", [])
whatsapp_flows = client.workflows.list_channel_automation(channel_type="whatsapp")
```

---

## Campaigns & touchpoints — `client.campaign` (Python)

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

# Validate touchpoint config before saving
result = client.campaign.validate_touchpoint({"type": "email", "template_id": "tpl_xxx"})
```

---

## Message suggestion — `client.message_suggestion` (Python)

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
