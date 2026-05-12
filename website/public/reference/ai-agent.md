# AI Agent Reference

`client.aiAgent` (TypeScript) / `client.ai_agent` (Python) provides chat streaming, embedding management, parquet generation, and distributed tracing for AI agents.

For a guided walkthrough, see [AI Agent in the SDK guide](/sdk/ai-agent/).

---

## Schema

### StreamChatBody

Parameters for initiating a streaming chat session.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `assistant_id` | string | Yes | ID of the AI agent to chat with |
| `messages` | array | Yes | Conversation history (role + content pairs) |
| `id` | string | | Existing chat session ID to continue |
| `model_id` | string | | Override the agent's default LLM model |
| `provider_id` | string | | Override the agent's default LLM provider |
| `user_id` | string | | External user identifier |

### StreamSubAgentChatBody

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `assistant_id` | string | Yes | ID of the AI agent |
| `session_id` | string | Yes | Parent session ID |
| `chat_id` | string | Yes | Chat ID within the session |
| `messages` | array | Yes | Conversation messages |

---

## Methods

| Method | TypeScript | Python | Description |
|--------|-----------|--------|-------------|
| Stream chat | `streamChat` | `stream_chat` | Start a streaming chat session with an AI agent |
| Stream sub-agent chat | `streamSubAgentChat` | `stream_sub_agent_chat` | Streaming chat scoped to a sub-agent session |
| Get sub-agent history | `getSubAgentHistory` | `get_sub_agent_history` | Retrieve message history for a sub-agent chat |
| List chats | `listChats` | `list_chats` | List chat sessions for an organization |
| Get chat | `getChat` | `get_chat` | Get a single chat session |
| Delete chat | `deleteChat` | `delete_chat` | Delete a chat session |
| Prompt suggestions | `getAgentPromptSuggestion` | `get_agent_prompt_suggestion` | Get suggested prompts for an agent |
| Classify file | `classifyFile` | `classify_file` | Classify a file into a category |
| Suggest field types | `suggestFieldTypes` | `suggest_field_types` | Suggest JSON schema from sample documents |
| Process embedding | `processEmbedding` | `process_embedding` | Embed a file into the knowledge base |
| List embedding files | `listEmbeddingFiles` | `list_embedding_files` | List all embedded files |
| Get embedding file | `getEmbeddingFile` | `get_embedding_file` | Get a single embedded file |
| Preview embedding file | `previewEmbeddingFile` | `preview_embedding_file` | Preview embedded content |
| Update embedding status | `updateEmbeddingFileStatus` | `update_embedding_file_status` | Update file embedding status |
| Delete embedding file | `deleteEmbeddingFile` | `delete_embedding_file` | Remove a file from the knowledge base |
| Generate parquet | `generateParquet` | `generate_parquet` | Convert data array to a parquet file |
| List parquet files | `listParquetFiles` | `list_parquet_files` | List generated parquet files |
| Delete parquet file | `deleteParquetFile` | `delete_parquet_file` | Delete a parquet file by name |
| Get traces | `getTraces` | `get_traces` | Query distributed traces |
| Get trace | `getTrace` | `get_trace` | Get a single trace by ID |
| Get trace services | `getTraceServices` | `get_trace_services` | List services emitting traces |

---

## streamChat / stream_chat

Start a streaming chat with an AI agent. Returns a raw HTTP response — iterate over the stream to read SSE chunks.

**TypeScript**

```typescript
const response = await client.aiAgent.streamChat({
  assistant_id: "agent_id",
  messages: [{ role: "user", content: "Hello" }],
  user_id: "user_123",
});

const reader = response.body?.getReader();
const decoder = new TextDecoder();
while (reader) {
  const { done, value } = await reader.read();
  if (done) break;
  console.log(decoder.decode(value));
}
```

**Python**

```python
response = client.ai_agent.stream_chat({
    "assistant_id": "agent_id",
    "messages": [{"role": "user", "content": "Hello"}],
    "user_id": "user_123",
})
for chunk in response.iter_lines():
    print(chunk)
```

---

## streamSubAgentChat / stream_sub_agent_chat

Stream a chat scoped to a sub-agent within a parent session.

**TypeScript**

```typescript
const response = await client.aiAgent.streamSubAgentChat({
  assistant_id: "agent_id",
  session_id: "session_id",
  chat_id: "chat_id",
  messages: [{ role: "user", content: "Follow-up question" }],
});
```

**Python**

```python
response = client.ai_agent.stream_sub_agent_chat({
    "assistant_id": "agent_id",
    "session_id": "session_id",
    "chat_id": "chat_id",
    "messages": [{"role": "user", "content": "Follow-up question"}],
})
```

---

## listChats / list_chats

**TypeScript**

```typescript
const { data: chats } = await client.aiAgent.listChats({
  organization_id: "org_id",
  user_id: "user_123",
  limit: 20,
});
```

**Python**

```python
result = client.ai_agent.list_chats(
    organization_id="org_id",
    user_id="user_123",
    limit=20,
)
chats = result.get("data", [])
```

---

## getSubAgentHistory / get_sub_agent_history

**TypeScript**

```typescript
const history = await client.aiAgent.getSubAgentHistory({
  session_id: "session_id",
  chat_id: "chat_id",
});
```

**Python**

```python
history = client.ai_agent.get_sub_agent_history(
    session_id="session_id",
    chat_id="chat_id",
)
```

---

## processEmbedding / process_embedding

Embed a file into the agent's knowledge base.

**TypeScript**

```typescript
const result = await client.aiAgent.processEmbedding({
  fileId: "file_id",
  options: { chunk_size: 512 },
});
```

**Python**

```python
result = client.ai_agent.process_embedding(
    file_id="file_id",
    options={"chunk_size": 512},
)
```

---

## classifyFile / classify_file

Classify a file into a predefined category based on its content.

**TypeScript**

```typescript
const result = await client.aiAgent.classifyFile({ fileId: "file_id" });
console.log(result.category);
```

**Python**

```python
result = client.ai_agent.classify_file(file_id="file_id")
print(result.get("category"))
```

---

## suggestFieldTypes / suggest_field_types

Analyze sample documents and suggest a JSON schema with field types for document extraction.

**TypeScript**

```typescript
const schema = await client.aiAgent.suggestFieldTypes({
  fileUrls: ["https://example.com/invoice.pdf"],
});
console.log(schema);
```

**Python**

```python
schema = client.ai_agent.suggest_field_types(
    file_urls=["https://example.com/invoice.pdf"],
)
print(schema)
```

---

## previewEmbeddingFile / preview_embedding_file

**TypeScript**

```typescript
const preview = await client.aiAgent.previewEmbeddingFile({ fileId: "file_id" });
console.log(preview);
```

**Python**

```python
preview = client.ai_agent.preview_embedding_file(file_id="file_id")
print(preview)
```

---

## updateEmbeddingFileStatus / update_embedding_file_status

**TypeScript**

```typescript
const result = await client.aiAgent.updateEmbeddingFileStatus("file_id", "completed");
console.log(result);
```

**Python**

```python
result = client.ai_agent.update_embedding_file_status("file_id", "completed")
print(result)
```

---

## generateParquet / generate_parquet

Convert an array of records into a parquet file for structured data ingestion.

**TypeScript**

```typescript
const result = await client.aiAgent.generateParquet({
  data: [{ name: "Alice", score: 95 }, { name: "Bob", score: 87 }],
  fileName: "scores",
  folderName: "results",
});
```

**Python**

```python
result = client.ai_agent.generate_parquet(
    data=[{"name": "Alice", "score": 95}, {"name": "Bob", "score": 87}],
    file_name="scores",
    folder_name="results",
)
```

---

## getTraces / get_traces

Query distributed traces for debugging and observability.

**TypeScript**

```typescript
const traces = await client.aiAgent.getTraces({
  service: "ai-agent",
  limit: 50,
  timeRange: 3600,
  orgId: "org_id",
});
```

**Python**

```python
traces = client.ai_agent.get_traces(
    service="ai-agent",
    limit=50,
    time_range=3600,
    org_id="org_id",
)
```
