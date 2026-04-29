## Full Flow Guide.

This guide walks through the four major workflows in the Imbrace SDK from start to finish. Each section is self-contained — follow them in order or jump to the one you need. Toggle the language tabs once and the rest of the page remembers your choice.

---

## 1. Create an AI Assistant and Start Chatting.

### 1. Initialize the client.

**With Access Token (user-facing apps):**
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

**With API Key (server-to-server):**
```typescript
import { ImbraceClient } from "@imbrace/sdk"

const client = new ImbraceClient({
  apiKey: "api_your_key",
  baseUrl: "https://app-gatewayv2.imbrace.co",
})
```

```python
from imbrace import ImbraceClient

client = ImbraceClient(
    api_key="api_your_key",
    base_url="https://app-gatewayv2.imbrace.co",
)
```

The header dropdown swaps these snippets between **access token** (user-facing apps where Imbrace is your backend) and **api key** (service-to-service where Imbrace is a feature inside your stack). See [Authentication → which credential to use](/sdk/authentication/#which-credential-should-i-use) for the full decision tree.

### 2. Create an assistant.

`workflow_name` must be unique within your organization.

```typescript
const assistant = await client.chatAi.createAssistant({
  name: "Support Bot",
  workflow_name: "support_bot_v1",
  description: "Handles tier-1 customer support queries",
  instructions: "You are a helpful support agent. Be concise and friendly.",
  provider_id: "system",   // use the org's default LLM provider
  model_id: "gpt-4o",      // any model name the system provider exposes
})
const assistantId = assistant.id  // UUID — use this for all subsequent calls
console.log("Assistant created:", assistantId)
```

```python
assistant = client.chat_ai.create_assistant({
    "name": "Support Bot",
    "workflow_name": "support_bot_v1",
    "description": "Handles tier-1 customer support queries",
    "instructions": "You are a helpful support agent. Be concise and friendly.",
    "provider_id": "system",   # use the org's default LLM provider
    "model_id": "gpt-4o",      # any model name the system provider exposes
})
assistant_id = assistant["id"]
print("Assistant created:", assistant_id)
```

`provider_id` and `model_id` are required. Pass `provider_id: "system"` to delegate to the org's default LLM provider, or pass a custom provider's UUID. With `provider_id: "system"`, `model_id` accepts a model name like `"gpt-4o"`, or the literal `"Default"` to fall back to the system default model.

### 3. Stream a chat response using the assistant.

```typescript
const response = await client.aiAgent.streamChat({
  assistant_id: assistantId,
  organization_id: "org_your_org_id",
  messages: [{ role: "user", content: "How do I reset my password?" }],
  // id is the session UUID — reuse it to maintain conversation history
  // If omitted, a new UUID is auto-generated each call
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
    "messages": [{"role": "user", "content": "How do I reset my password?"}],
    # id is the session UUID — reuse it to maintain conversation history
})

for line in response.iter_lines():
    if line:
        try:
            chunk = json.loads(line.replace("data: ", "").strip())
            print(chunk.get("delta") or chunk.get("content", ""), end="")
        except:
            pass
```

---

## 2. Create a Workflow with Activepieces and Bind it to an Assistant.

### 1. Initialize the client (API Key recommended for automation).

```typescript
const client = new ImbraceClient({
  apiKey: "api_your_key",
  baseUrl: "https://app-gatewayv2.imbrace.co",
})
```

```python
client = ImbraceClient(api_key="api_your_key")
```

### 2. Create a new flow.

```typescript
const { data: flows } = await client.activepieces.listFlows({ limit: 5 })
const projectId = flows[0]?.projectId

const flow = await client.activepieces.createFlow({
  displayName: "CRM Update on New Lead",
  projectId,
})
```

```python
res = client.activepieces.list_flows(limit=5)
flows = res.get("data", [])
flow = client.activepieces.create_flow(
    display_name="CRM Update on New Lead",
    project_id=flows[0]["projectId"],
)
```

### 3. Add a trigger and publish.

**Important:** A newly created flow is in DRAFT state with no trigger. Add a trigger and publish before calling `triggerFlow`, otherwise you'll get 404.

```typescript
// Set Webhook trigger
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

// Publish — DRAFT → ENABLED; webhook URL becomes live
await client.activepieces.applyFlowOperation(flow.id, {
  type: "LOCK_AND_PUBLISH",
  request: {},
})
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

### 4. Trigger the flow.

```typescript
// Fire and forget
await client.activepieces.triggerFlow(flow.id, { contact_name: "Jane Smith", email: "jane@example.com" })

// Synchronous — flow must have a "Return Response" action, else times out after 30s
const result = await client.activepieces.triggerFlowSync(flow.id, { contact_name: "Jane Smith" })
```

```python
client.activepieces.trigger_flow(flow["id"], {"contact_name": "Jane Smith", "email": "jane@example.com"})
result = client.activepieces.trigger_flow_sync(flow["id"], {"contact_name": "Jane Smith"})
```

### 5. Bind the flow to your assistant.

```typescript
await client.chatAi.updateAssistant(assistantId, {
  name: "Support Bot v2",
  workflow_name: "support_bot_v1",
  // Attach Activepieces workflow:
  workflow_function_call: [{ flow_id: flow.id, description: "Update CRM on new lead" }],
})
```

```python
client.chat_ai.update_assistant(assistant_id, {
    "name": "Support Bot v2",
    "workflow_name": "support_bot_v1",
    "workflow_function_call": [{"flow_id": flow["id"], "description": "Update CRM on new lead"}],
})
```

---

## 3. Manage Knowledge Hubs and Attach to an Assistant.

### 1. Create a Knowledge Hub folder.

```typescript
const folder = await client.boards.createFolder({
  name: "Product Documentation",
  organization_id: "org_your_org_id",
  parent_folder_id: "root",
  source_type: "upload",
})
```

```python
folder = client.boards.create_folder({
    "name": "Product Documentation",
    "organization_id": "org_your_org_id",
    "parent_folder_id": "root",
    "source_type": "upload",
})
folder_id = folder["_id"]
```

### 2. Upload files to the folder.

```typescript
import { readFileSync } from "fs"

const fileBuffer = readFileSync("./docs/faq.pdf")
const formData = new FormData()
formData.append("file", new Blob([fileBuffer], { type: "application/pdf" }), "faq.pdf")
formData.append("folder_id", folder._id)
formData.append("organization_id", "org_your_org_id")

const uploaded = await client.boards.uploadFile(formData)
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
file_id = uploaded.get("file_id") or uploaded.get("_id")
```

### 3. Trigger embedding processing.

```typescript
await client.aiAgent.processEmbedding({ fileId: file_id })
// or with options:
await client.aiAgent.processEmbedding({ fileId: file_id, options: { chunk_size: 512 } })
```

```python
client.ai_agent.process_embedding(file_id)
# or with options:
client.ai_agent.process_embedding(file_id, options={"chunk_size": 512})
```

### 4. List embeddings and verify.

```typescript
const files = await client.aiAgent.listEmbeddingFiles({ page: 1, limit: 20 })
const file = await client.aiAgent.getEmbeddingFile(file_id)
const preview = await client.aiAgent.previewEmbeddingFile({ file_id })
```

```python
files = client.ai_agent.list_embedding_files(page=1, limit=20)
file = client.ai_agent.get_embedding_file(file_id)
preview = client.ai_agent.preview_embedding_file(file_id=file_id)
```

### 5. Attach the folder to your assistant.

```typescript
await client.chatAi.updateAssistant(assistantId, {
  name: "Support Bot v2",
  workflow_name: "support_bot_v1",
  folder_ids: [folder._id],   // Attach Knowledge Hub folder
})
```

```python
client.chat_ai.update_assistant(assistant_id, {
    "name": "Support Bot v2",
    "workflow_name": "support_bot_v1",
    "folder_ids": [folder["_id"]],   # Attach Knowledge Hub folder
})
```

---

## 4. Manage Data Boards and Items (CRM Pipelines).

### 1. Create a board.

```typescript
const { data: boards } = await client.boards.list()
const board = await client.boards.create({
  name: "Sales Pipeline",
  description: "Track all active deals",
})
const boardId = board._id
```

```python
boards = client.boards.list().get("data", [])
board = client.boards.create(name="Sales Pipeline", description="Track all active deals")
board_id = board["_id"]
```

### 2. Create fields.

Field types: `ShortText`, `LongText`, `Number`, `Dropdown`, `Date`, `Checkbox`, etc. `createField` returns the updated board with all fields.

```typescript
const updated = await client.boards.createField(boardId, { name: "Company", type: "ShortText" })
const identifierField = updated.fields.find(f => f.is_identifier)  // auto-created with every board
```

```python
updated = client.boards.create_field(board_id, {"name": "Company", "type": "ShortText"})
identifier_field = next(f for f in updated["fields"] if f.get("is_identifier"))
```

### 3. Create items (records).

Items use `{ fields: [{ board_field_id, value }] }` format for creation. Update uses `{ data: [{ key: fieldId, value }] }` format.

```typescript
const item = await client.boards.createItem(boardId, {
  fields: [{ board_field_id: identifierField._id, value: "Acme Corp" }],
})

const { data: items } = await client.boards.listItems(boardId, { limit: 20, skip: 0 })
const singleItem = await client.boards.getItem(boardId, item._id)

await client.boards.updateItem(boardId, item._id, {
  data: [{ key: identifierField._id, value: "Acme Corp — Closed Won" }],
})

await client.boards.deleteItem(boardId, item._id)
await client.boards.bulkDeleteItems(boardId, [item._id])
```

```python
item = client.boards.create_item(board_id, {
    "fields": [{"board_field_id": identifier_field["_id"], "value": "Acme Corp"}],
})

items = client.boards.list_items(board_id, limit=20, skip=0)
single_item = client.boards.get_item(board_id, item["_id"])

client.boards.update_item(board_id, item["_id"], {
    "data": [{"key": identifier_field["_id"], "value": "Acme Corp — Closed Won"}],
})
client.boards.delete_item(board_id, item["_id"])
client.boards.bulk_delete_items(board_id, [item["_id"]])
```

### 4. Search and segments.

```typescript
const { data: results } = await client.boards.search(boardId, { q: "Acme", limit: 10 })

const { data: segments } = await client.boards.listSegments(boardId)
const segment = await client.boards.createSegment(boardId, {
  name: "High Value Leads",
  filters: [{ field: "value", op: "gt", value: 10000 }],
})
```

```python
results = client.boards.search(board_id, {"q": "Acme", "limit": 10}).get("data", [])

segments = client.boards.list_segments(board_id).get("data", [])
segment = client.boards.create_segment(board_id, {
    "name": "High Value Leads",
    "filters": [{"field": "value", "op": "gt", "value": 10000}],
})
```

### 5. Export to CSV.

```typescript
const csv = await client.boards.exportCsv(boardId)
// csv is a string
```

```python
csv = client.boards.export_csv(board_id)
```
