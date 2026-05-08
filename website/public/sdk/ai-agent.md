# AI Agent & Assistants

This page covers two related AI namespaces:

- **`chatAi` / `chat_ai`** â€” create and manage AI assistants, run completions, manage knowledge bases.
- **`aiAgent` / `ai_agent`** â€” streaming chat (SSE), embedding management, Parquet data, distributed tracing, and the Chat Client sub-API.

The AI Agent resource connects to a dedicated service that runs on a separate base URL from the main API gateway.

For an end-to-end example that ties these together, see [Full Flow Guide Â§1](/sdk/full-flow-guide/#1-create-an-ai-assistant-and-start-chatting).

```typescript
import { ImbraceClient } from "@imbrace/sdk"

const client = new ImbraceClient({
  accessToken: "your-access-token",
  baseUrl: "https://app-gatewayv2.imbrace.co",
})
```
```python
from imbrace import ImbraceClient

client = ImbraceClient(access_token="your-access-token")
```

```typescript
import { ImbraceClient } from "@imbrace/sdk"

const client = new ImbraceClient({
  apiKey: "your-api-key",
  baseUrl: "https://app-gatewayv2.imbrace.co",
})
```
```python
from imbrace import ImbraceClient

client = ImbraceClient(api_key="your-api-key")
```

Both sync (`ImbraceClient`) and async (`AsyncImbraceClient`) clients expose the same surface â€” async methods are awaited and the client uses `AsyncAiAgentResource` under the hood.

---

## Assistants â€” `chatAi` / `chat_ai`

Manages AI assistants (CRUD), runs OpenAI-compatible completions, and handles document/file processing. The same namespace also covers Knowledge Hub folders and knowledge bases.

### Assistant CRUD

```typescript
// List all assistants in your account
const assistants = await client.chatAi.listAssistants();
// Each assistant has an `id` (UUID) and `_id` (MongoDB ObjectId).
// Use the `id` field for all subsequent calls.

// Get a single assistant
const assistant = await client.chatAi.getAssistant("9f77692f-33d0-436a-8138-2efb268838e6");

// Create â€” provider_id and model_id are required
const created = await client.chatAi.createAssistant({
  name: "Support Bot",
  workflow_name: "support_bot_v1",
  provider_id: "system",
  model_id: "gpt-4o",
  description: "Handles tier-1 support queries",
});

// Update â€” workflow_name is required on update too
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

# Create â€” provider_id and model_id are required
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

### Completions (via `client.ai`)

OpenAI-compatible chat completions are available on the `client.ai` namespace for both TypeScript and Python. See the [OpenAI-compatible AI service](#openai-compatible-ai-service--clientai) section below for details.

```typescript
const response = await client.ai.complete({
  model: "gpt-4o",
  messages: [
    { role: "system", content: "You are a helpful CRM assistant." },
    { role: "user", content: "Summarize this customer note: ..." },
  ],
});
console.log(response.choices[0].message.content);
```
```python
response = client.ai.complete(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful CRM assistant."},
        {"role": "user",   "content": "Summarize this customer note: ..."},
    ],
)
print(response["choices"][0]["message"]["content"])
```

### Document AI models

```typescript
const models = await client.chatAi.listDocumentModels();
```
```python
models = client.chat_ai.list_document_models()
```

### Document processing (vision model)

Extract structured data from PDFs and images using a vision model.

```typescript
const result = await client.chatAi.processDocument({
  modelName: "gpt-4o",
  url: "https://example.com/invoice.pdf",
  organizationId: "org_xxx",
});
console.log(result.data);
// { invoice_number: "INV-001", total: 1200, vendor: "Acme Corp", ... }
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

### File extraction (agent file upload)

Upload a file and extract its raw content.

```typescript
// Upload an agent-specific file
const formData = new FormData();
formData.append("file", fileBuffer, "report.pdf");
const uploaded = await client.chatAi.uploadAgentFile(formData);

// Extract content from an uploaded file
const extracted = await client.chatAi.extractFile(formData);
```
```python
# Upload an agent-specific file
uploaded = client.chat_ai.upload_agent_file(files={"file": open("report.pdf", "rb")}, agent_id="asst_abc")

# Extract content from an uploaded file
extracted = client.chat_ai.extract_file(files={"file": open("report.pdf", "rb")})
```

### Chat v1 sessions

Legacy REST chat endpoints for persisting conversation history. Available on `client.ai_agent` for both TypeScript and Python. See [Legacy v1 chat](#legacy-v1-chat) below.

### Knowledge Hub â€” folders & knowledge bases

Folders and knowledge bases are managed via `client.boards` (TypeScript) / `client.folders` and `client.boards` (Python). Folders organize knowledge bases â€” a knowledge base is a set of files an assistant can retrieve from. Pass folder IDs as `folder_ids` when creating an assistant â€” see [Full Flow Guide Â§3](/sdk/full-flow-guide/#3-manage-knowledge-hubs-and-attach-to-an-assistant).

```typescript
import { type CreateFolderInput } from "@imbrace/sdk";

// Folders
const folders = await client.boards.searchFolders({ organizationId: "org_xxx" });
const folder  = await client.boards.createFolder({ name: "Q1 Reports" });
await client.boards.updateFolder(folder._id, { name: "Q1 2025 Reports" });
await client.boards.deleteFolders({ ids: [folder._id] });

// Files (knowledge base entries)
const uploaded = await client.boards.uploadFile(formData);
const files    = await client.boards.searchFiles({ folderId: folder._id });
const file     = await client.boards.getFile("file_id");
await client.boards.createFile({ name: "doc.txt", folderId: folder.id });
await client.boards.deleteFiles({ ids: ["file_id"] });
```
```python
# Folders
folder = client.folders.create({"name": "Q1 Reports"})
folders = client.folders.search()
client.folders.update(folder["_id"], {"name": "Q1 2025 Reports"})
client.folders.delete([folder["_id"]])

# Files (knowledge base entries)
file = client.boards.upload_file(files={"file": open("doc.pdf", "rb")})
files = client.boards.search_files(folder_id=folder["_id"])
```

---

## OpenAI-compatible AI service â€” `client.ai`

Raw OpenAI-style completions, streaming, and embeddings against the `aiv2` service. Available for both TypeScript and Python.

```typescript
// Single completion
const response = await client.ai.complete({
  model: "gpt-4o",
  messages: [
    { role: "system", content: "You are a helpful CRM assistant." },
    { role: "user",   content: "Summarize this customer note: ..." },
  ],
  temperature: 0.7,
});
console.log(response.choices[0].message.content);

// Streaming
const stream = client.ai.stream({
  model: "gpt-4o",
  messages: [{ role: "user", content: "Draft a follow-up email for this lead." }],
});
for await (const chunk of stream) {
  process.stdout.write(chunk.choices[0].delta.content ?? "");
}

// Embeddings
const result = await client.ai.embed({
  model: "text-embedding-ada-002",
  input: ["customer complained about billing", "billing issue escalated"],
});
```
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

## Chat v2 â€” Streaming (SSE)

Returns a raw response. Consume the body as a Server-Sent Events stream.

```typescript
const response = await client.aiAgent.streamChat({
  id: "chat_id",
  assistant_id: "asst_abc",
  organization_id: "org_abc",
  messages: [{ role: "user", content: "What can you do?" }],
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
    "messages": [{"role": "user", "content": "What can you do?"}],
})

for line in response.iter_lines():
    if line:
        print(line)
```

**Async:**

```python
import asyncio
from imbrace import AsyncImbraceClient

async def main():
    async with AsyncImbraceClient() as client:
        response = await client.ai_agent.stream_chat({
            "id": "chat_id",
            "assistant_id": "asst_abc",
            "organization_id": "org_abc",
            "messages": [{"role": "user", "content": "Hello"}],
        })
        async for line in response.aiter_lines():
            if line:
                print(line)

asyncio.run(main())
```

---

## Sub-agent Chat v2

Stream responses from a sub-agent and retrieve its conversation history.

```typescript
const res = await client.aiAgent.streamSubAgentChat({
  assistant_id: "asst_sub",
  organization_id: "org_abc",
  session_id: "sess_xyz",
  chat_id: "chat_id",
  messages: [{ role: "user", content: "Explain the data." }],
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
    "messages": [{"role": "user", "content": "Explain the data."}],
})

history = client.ai_agent.get_sub_agent_history(
    session_id="sess_xyz",
    chat_id="chat_id",
)
```

---

## Prompt Suggestions

Fetch pre-built prompt suggestions for a given assistant.

```typescript
const suggestions = await client.aiAgent.getAgentPromptSuggestion("asst_abc");
```
```python
suggestions = client.ai_agent.get_agent_prompt_suggestion("asst_abc")
```

---

## Embeddings & Knowledge Base

Manage files used for Retrieval-Augmented Generation (RAG). Upload files first via [`client.boards.uploadFile`](/sdk/full-flow-guide/#3-manage-knowledge-hubs-and-attach-to-an-assistant) (TypeScript) / `client.boards.upload_file` (Python), then trigger embedding processing.

```typescript
// Trigger embedding processing for an uploaded file
await client.aiAgent.processEmbedding({ fileId: "file_abc" });

// List and inspect embedding files
const files   = await client.aiAgent.listEmbeddingFiles({ page: 1, limit: 20 });
const file    = await client.aiAgent.getEmbeddingFile("file_abc");
const preview = await client.aiAgent.previewEmbeddingFile({ file_id: "file_abc" });

// Update status and delete
await client.aiAgent.updateEmbeddingFileStatus("file_abc", "active");
await client.aiAgent.deleteEmbeddingFile("file_abc");

// Classify a file for RAG categorization
const classification = await client.aiAgent.classifyFile({ file_id: "file_abc" });
```
```python
# Trigger embedding processing for an uploaded file
client.ai_agent.process_embedding("file_abc")

# With optional processing options
client.ai_agent.process_embedding("file_abc", options={"chunk_size": 512})

# List and inspect embedding files
files   = client.ai_agent.list_embedding_files(page=1, limit=20)
file    = client.ai_agent.get_embedding_file("file_abc")
preview = client.ai_agent.preview_embedding_file(file_id="file_abc")

# Update status and delete
client.ai_agent.update_embedding_file_status("file_abc", "active")
client.ai_agent.delete_embedding_file("file_abc")

# Classify a file for RAG categorization
classification = client.ai_agent.classify_file(file_id="file_abc")
```

---

## Data Board

AI-assisted field type suggestion for structured datasets.

```typescript
const result = await client.aiAgent.suggestFieldTypes({
  fields: [
    { name: "created_at", samples: ["2024-01-01", "2024-02-15"] },
    { name: "amount",     samples: [100, 200.5, 999] },
    { name: "is_active",  samples: [true, false, true] },
  ],
});
// result.fields[i].suggestedType â†’ "datetime" | "number" | "boolean" | ...
```
```python
result = client.ai_agent.suggest_field_types(fields=[
    {"name": "created_at", "samples": ["2024-01-01", "2024-02-15"]},
    {"name": "amount",     "samples": [100, 200.5, 999]},
    {"name": "is_active",  "samples": [True, False, True]},
])
# result["fields"][i]["suggestedType"] â†’ "datetime" | "number" | "boolean" | ...
```

---

## Parquet

Generate and manage Parquet columnar data files for analytics pipelines.

```typescript
// Generate a Parquet file from JSON data
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

Query Grafana Tempo traces emitted by the AI Agent service for observability and debugging.

```typescript
// List recent traces
const traces = await client.aiAgent.getTraces({
  service:   "ai-agent",
  limit:     50,
  timeRange: 3600,     // seconds
  orgId:     "org_abc",
  details:   true,
});

// Inspect a single trace
const trace = await client.aiAgent.getTrace("trace_id_hex");

// Enumerate services, tags, and tag values
const services = await client.aiAgent.getTraceServices();
const tags     = await client.aiAgent.getTraceTags();
const values   = await client.aiAgent.getTraceTagValues("http.status_code");

// TraceQL search
const results = await client.aiAgent.searchTraceQL(
  `{ .service.name = "ai-agent" && .http.status = 500 }`
);
```
```python
# List recent traces
traces = client.ai_agent.get_traces(
    service="ai-agent",
    limit=50,
    time_range=3600,     # seconds
    org_id="org_abc",
    details=True,
)

# Inspect a single trace
trace = client.ai_agent.get_trace("trace_id_hex")

# Enumerate services, tags, and tag values
services = client.ai_agent.get_trace_services()
tags     = client.ai_agent.get_trace_tags()
values   = client.ai_agent.get_trace_tag_values("http.status_code")

# TraceQL search
results = client.ai_agent.search_traceql(
    '{ .service.name = "ai-agent" && .http.status = 500 }'
)
```

---

## Chat Client

The Chat Client sub-API powers frontend applications (e.g. the embedded chat widget). For framework-level wiring (React singleton, Express auth proxy, etc.), see [Integrations](/sdk/integrations/).

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
// Create a new chat session
await client.aiAgent.createClientChat({
  id: "chat_uuid",
  message: {
    id: "msg_uuid",
    role: "user",
    parts: [{ type: "text", text: "Hello!" }],
  },
  assistantId:    "asst_abc",
  organizationId: "org_abc",
});

// List, read, update, delete chats
const chats = await client.aiAgent.listClientChats({
  organization_id: "org_abc",
  limit: 20,
});
const chat = await client.aiAgent.getClientChat("chat_id");
await client.aiAgent.updateClientChat("chat_id", { visibility: "private" });
await client.aiAgent.deleteClientChat("chat_id");
await client.aiAgent.deleteAllClientChats({ organization_id: "org_abc" });

// Auto-generate a title for the chat
await client.aiAgent.generateClientChatTitle("chat_id");

// Stream real-time chat status as SSE â€” returns raw Response
const statusStream = await client.aiAgent.streamClientChatStatus("chat_id");
```
```python
# Create a new chat session
client.ai_agent.create_client_chat({
    "id": "chat_uuid",
    "message": {
        "id": "msg_uuid",
        "role": "user",
        "parts": [{"type": "text", "text": "Hello!"}],
    },
    "assistantId":    "asst_abc",
    "organizationId": "org_abc",
})

# List, read, update, delete
chats = client.ai_agent.list_client_chats(organization_id="org_abc", limit=20)
chat  = client.ai_agent.get_client_chat("chat_id")
client.ai_agent.update_client_chat("chat_id", {"visibility": "private"})
client.ai_agent.delete_client_chat("chat_id")
client.ai_agent.delete_all_client_chats("org_abc")

# Auto-generate a title for the chat
client.ai_agent.generate_client_chat_title("chat_id")

# Stream real-time chat status as SSE â€” returns raw httpx.Response
status_stream = client.ai_agent.stream_client_chat_status("chat_id")
```

### Messages

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

### Votes

```typescript
const votes = await client.aiAgent.getVotes("chat_id");
await client.aiAgent.updateVote({ messageId: "msg_id", vote: "up" });
```
```python
votes = client.ai_agent.get_votes("chat_id")
client.ai_agent.update_vote({"messageId": "msg_id", "vote": "up"})
```

### Documents (AI-generated artifacts)

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
pub        = client.ai_agent.get_document_public("doc_id")
by_kind    = client.ai_agent.get_document_latest_by_kind(kind="text")
suggestion = client.ai_agent.get_document_suggestions("doc_id")

client.ai_agent.delete_document("doc_id")
```

---

## Admin Guides

Access admin documentation hosted by the AI Agent service. Guide files are returned as raw binary streams (typically PDF).

```typescript
const guides = await client.aiAgent.listAdminGuides();

// Download a specific guide â€” returns raw Response (PDF stream)
const response = await client.aiAgent.getAdminGuide("onboarding.pdf");
const blob = await response.blob();
```
```python
guides = client.ai_agent.list_admin_guides()

# Download a specific guide â€” returns raw httpx.Response
response = client.ai_agent.get_admin_guide("onboarding.pdf")
with open("onboarding.pdf", "wb") as f:
    f.write(response.content)
```

---

## Legacy v1 chat

The original REST chat endpoints persist conversation history without streaming. New code should use [Chat v2 streaming](#chat-v2--streaming-sse) above; v1 stays for backwards compatibility with existing chats.

```typescript
// List chats for an organization
const chats = await client.aiAgent.listChats({
  organization_id: "org_abc",
  user_id: "user_123",
  limit: 20,
});

// Get a single chat (pass true to include messages)
const chat = await client.aiAgent.getChat("chat_id", true);

// Delete a chat
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