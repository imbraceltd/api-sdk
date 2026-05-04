# Full Flow Guide

> End-to-end walkthroughs — from client setup to AI agents, workflows, knowledge hubs, and data boards. TypeScript and Python.

This guide walks through the four major workflows in the Imbrace SDK from start to finish. Each section is self-contained — follow them in order or jump to the one you need. Toggle the language tabs once and the rest of the page remembers your choice.

---

## 1. Create an AI Assistant and Start Chatting

1. **Initialize the client**

   
   
     
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
     
   
   

   
   
     
       ```typescript
       import { ImbraceClient } from "@imbrace/sdk"

       const client = new ImbraceClient({
         baseUrl: "https://app-gatewayv2.imbrace.co",
         apiKey: "api_your_key",
       })
       ```
     
     
       ```python
       from imbrace import ImbraceClient

       client = ImbraceClient(
           base_url="https://app-gatewayv2.imbrace.co",
           api_key="api_your_key",
       )
       ```
     
   
   

   The header dropdown swaps these snippets between **access token** (user-facing apps where Imbrace is your backend) and **api key** (service-to-service where Imbrace is a feature inside your stack). See [Authentication → which credential to use](/sdk/authentication/#which-credential-should-i-use) for the full decision tree.

2. **Create an assistant**

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

3. **Stream a chat response using the assistant**

   
     
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
           # id is the session UUID — reuse it to maintain conversation history.
           # If omitted, a new UUID is auto-generated each call.
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
     
   

4. **Maintain conversation history (session ID)**

   Pass the same `id` (must be a UUID) across calls to keep context:

   
     
       ```typescript
       import { randomUUID } from "crypto"

       const sessionId = randomUUID()

       // First message
       await client.aiAgent.streamChat({
         assistant_id: assistantId,
         organization_id: "org_your_org_id",
         id: sessionId,
         messages: [{ role: "user", content: "What's your refund policy?" }],
       })

       // Follow-up — same session, assistant remembers context
       await client.aiAgent.streamChat({
         assistant_id: assistantId,
         organization_id: "org_your_org_id",
         id: sessionId,
         messages: [{ role: "user", content: "How long does it take?" }],
       })
       ```
     
     
       ```python
       import uuid

       session_id = str(uuid.uuid4())

       # First message
       client.ai_agent.stream_chat({
           "assistant_id": assistant_id,
           "organization_id": "org_your_org_id",
           "id": session_id,
           "messages": [{"role": "user", "content": "What's your refund policy?"}],
       })

       # Follow-up — same session, assistant remembers context
       client.ai_agent.stream_chat({
           "assistant_id": assistant_id,
           "organization_id": "org_your_org_id",
           "id": session_id,
           "messages": [{"role": "user", "content": "How long does it take?"}],
       })
       ```
     
   

---

## 2. Create a Workflow with Activepieces and Bind it to an Assistant

1. **List existing flows to find your project ID**

   
     
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
     
   

2. **Create a new flow**

   
     
       ```typescript
       const flow = await client.activepieces.createFlow({
         displayName: "CRM Update on New Lead",
         projectId,
       })
       console.log("Flow created:", flow.id)
       ```
     
     
       ```python
       flow = client.activepieces.create_flow(
           display_name="CRM Update on New Lead",
           project_id=project_id,
       )
       print("Flow created:", flow["id"])
       ```
     
   

3. **Add a Webhook trigger and publish the flow**

   A freshly created flow is in **DRAFT** with no trigger — the webhook URL doesn't exist yet, so `triggerFlow` would 404. Add the Webhook piece as the trigger, then publish:

   
     
       ```typescript
       // Set the Webhook piece as the flow's trigger
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

       // Publish — flow status flips DISABLED → ENABLED and webhook URL becomes live
       await client.activepieces.applyFlowOperation(flow.id, {
         type: "LOCK_AND_PUBLISH",
         request: {},
       })
       ```
     
     
       ```python
       # Set the Webhook piece as the flow's trigger
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

       # Publish — DISABLED → ENABLED, webhook URL becomes live
       client.activepieces.apply_flow_operation(flow["id"], {
           "type": "LOCK_AND_PUBLISH",
           "request": {},
       })
       ```
     
   

4. **Trigger the flow manually with a payload**

   
     
       ```typescript
       // Fire and forget (async)
       await client.activepieces.triggerFlow(flow.id, {
         contact_name: "Jane Smith",
         email: "jane@example.com",
       })

       // Sync trigger — for this to actually return data instead of timing out,
       // the flow needs a "Return Response" action added via applyFlowOperation
       // ADD_ACTION (otherwise the gateway waits 30s for a response and gives up).
       const result = await client.activepieces.triggerFlowSync(flow.id, {
         contact_name: "Jane Smith",
         email: "jane@example.com",
       })
       console.log("Flow result:", result)
       ```
     
     
       ```python
       # Fire and forget (async)
       client.activepieces.trigger_flow(flow["id"], {
           "contact_name": "Jane Smith",
           "email": "jane@example.com",
       })

       # Sync trigger — for this to actually return data instead of timing out,
       # the flow needs a "Return Response" action added via apply_flow_operation
       # ADD_ACTION (otherwise the gateway waits 30s and gives up).
       result = client.activepieces.trigger_flow_sync(flow["id"], {
           "contact_name": "Jane Smith",
           "email": "jane@example.com",
       })
       print("Flow result:", result)
       ```
     
   

5. **Bind the flow to your assistant**

   Open your assistant in the Imbrace dashboard, go to **Tools → Workflows**, and attach the flow. The assistant will be able to trigger it during a conversation when appropriate.

   Alternatively, update the assistant to reference the workflow by name:

   
     
       ```typescript
       await client.chatAi.updateAssistant(assistantId, {
         name: "Support Bot",
         workflow_name: "support_bot_v1",
         workflow_function_call: [{ flow_id: flow.id, description: "Update CRM on new lead" }],
       })
       ```
     
     
       ```python
       client.chat_ai.update_assistant(assistant_id, {
           "name": "Support Bot",
           "workflow_name": "support_bot_v1",
           "workflow_function_call": [
               {"flow_id": flow["id"], "description": "Update CRM on new lead"}
           ],
       })
       ```
     
   

6. **Check run history**

   
     
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

## 3. Manage Knowledge Hubs and Attach to an Assistant

Knowledge Hub files and folders live in the **data-board** service (`client.boards`). The folder's `_id` is what you pass to an assistant as its knowledge source.

1. **Create a folder**

   
     
       ```typescript
       const folder = await client.boards.createFolder({
         name: "Product Documentation",
         organization_id: "org_your_org_id",
         parent_folder_id: "root",
         source_type: "upload",
       })
       console.log("Folder ID:", folder._id)
       ```
     
     
       ```python
       folder = client.boards.create_folder({
           "name": "Product Documentation",
           "organization_id": "org_your_org_id",
           "parent_folder_id": "root",
           "source_type": "upload",
       })
       print("Folder ID:", folder["_id"])
       ```
     
   

2. **Upload a file to the folder**

   
     
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
     
   

3. **Attach the folder to the assistant**

   Pass the folder `_id` in `folder_ids` — the assistant retrieves from every file in that folder. Use `board_ids` to attach a CRM data-board (its items become a knowledge source — see [Resources → Boards & items](/sdk/resources/#boards--items--clientboards)). The legacy `knowledge_hubs` field is deprecated.

   
     
       ```typescript
       await client.chatAi.updateAssistant(assistantId, {
         name: "Support Bot",
         workflow_name: "support_bot_v1",
         folder_ids: [folder._id],
         // board_ids: [boardId],  // optional: attach a CRM data-board too
       })
       ```
     
     
       ```python
       client.chat_ai.update_assistant(assistant_id, {
           "name": "Support Bot",
           "workflow_name": "support_bot_v1",
           "folder_ids": [folder["_id"]],
           # "board_ids": [board_id],  # optional: attach a CRM data-board too
       })
       ```
     
   

4. **Inspect and manage folders and files**

   
     
       ```typescript
       // Search folders
       const folders = await client.boards.searchFolders({ q: "Product" })

       // Get folder with contents
       const contents = await client.boards.getFolderContents(folder._id)
       console.log("Files:", contents.files?.length)

       // Rename a folder
       await client.boards.updateFolder(folder._id, { name: "Product Docs v2" })

       // Search files in a folder
       const files = await client.boards.searchFiles({ folderId: folder._id })

       // Delete folders
       await client.boards.deleteFolders({ ids: [folder._id] })
       ```
     
     
       ```python
       # Search folders
       folders = client.boards.search_folders(q="Product")

       # Get folder with contents
       contents = client.boards.get_folder_contents(folder["_id"])
       print("Files:", len(contents.get("files") or []))

       # Rename a folder
       client.boards.update_folder(folder["_id"], {"name": "Product Docs v2"})

       # Search files in a folder
       files = client.boards.search_files(folder_id=folder["_id"])

       # Delete folders
       client.boards.delete_folders([folder["_id"]])
       ```
     
   

---

## 4. Manage Data Boards and Items (CRM Pipelines)

1. **Create a board**

   A board is a CRM pipeline — leads, deals, tasks, or any structured data.

   
     
       ```typescript
       const board = await client.boards.create({
         name: "Sales Pipeline",
         description: "Track all active deals",
       })
       console.log("Board ID:", board._id)
       ```
     
     
       ```python
       board = client.boards.create(
           name="Sales Pipeline",
           description="Track all active deals",
       )
       print("Board ID:", board["_id"])
       ```
     
   

2. **Add a custom field**

   Field types are `ShortText`, `LongText`, `Number`, `Dropdown`, `Date`, `Checkbox`, etc. `createField` returns the updated board — find your new field inside `board.fields`.

   
     
       ```typescript
       const updated = await client.boards.createField(board._id, {
         name: "Company",
         type: "ShortText",
       })
       // Find the identifier field (auto-created with every board)
       const identifierField = updated.fields.find(f => f.is_identifier)
       ```
     
     
       ```python
       updated = client.boards.create_field(board["_id"], {
           "name": "Company",
           "type": "ShortText",
       })
       identifier_field = next(f for f in updated["fields"] if f.get("is_identifier"))
       ```
     
   

3. **Create board items (records)**

   Items use `{ fields: [{ board_field_id, value }] }` format:

   
     
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
     
   

4. **List and search items**

   
     
       ```typescript
       // Paginate through items
       const { data: items } = await client.boards.listItems(board._id, { limit: 20, skip: 0 })

       // Full-text search
       const { data: results } = await client.boards.search(board._id, {
         q: "Acme",
         limit: 10,
       })
       ```
     
     
       ```python
       # Paginate through items
       items = client.boards.list_items(board["_id"], limit=20, skip=0)

       # Full-text search
       results = client.boards.search(board["_id"], q="Acme", limit=10)
       ```
     
   

5. **Update and delete items**

   `updateItem` uses `{ data: [{ key: fieldId, value }] }` array format:

   
     
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
     
   

6. **Export to CSV**

   
     
       ```typescript
       const csv = await client.boards.exportCsv(board._id)
       // csv is a string — write to a file or send as a download
       ```
     
     
       ```python
       csv = client.boards.export_csv(board["_id"])
       # csv is a str — write to a file or send as a download
       ```
