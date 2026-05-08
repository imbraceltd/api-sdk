# Workflows

The SDK exposes two workflow systems: **Activepieces** (`client.activepieces` / `client.workflows`) for visual workflow automation, and **channel automation** (`client.workflows`) for messaging channel flows such as WhatsApp.

Initialize the client first (see [Installation](/sdk/installation/) or [Quick Start](/sdk/quick-start/)). For an end-to-end walkthrough that wires a workflow to an assistant, see [Full Flow Guide Â§2](/sdk/full-flow-guide/#2-create-a-workflow-with-activepieces-and-bind-it-to-an-assistant).

---

## Activepieces â€” `client.activepieces` / `client.workflows`

Activepieces is the visual workflow builder. Available for both TypeScript and Python.

### Flows

```typescript
const { data: flows } = await client.activepieces.listFlows();

const flow = await client.activepieces.getFlow("flow_id");

const newFlow = await client.activepieces.createFlow({
  displayName: "New Lead Notification",
  projectId: "project_id",
});

await client.activepieces.deleteFlow("flow_id");
```
```python
flows = client.workflows.list_flows().get("data", [])

flow = client.workflows.get_flow("flow_id")

new_flow = client.workflows.create_flow(
    display_name="New Lead Notification",
    project_id="project_id",
)

client.workflows.delete_flow("flow_id")
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
```python
# Fire and forget
client.workflows.trigger_flow("flow_id", {"contactId": "contact_xxx", "event": "lead_qualified"})

# Wait for result
result = client.workflows.trigger_flow_sync("flow_id", {"contactId": "contact_xxx", "event": "lead_qualified"})
```

### Runs, folders, connections, tables

```typescript
const { data: runs }     = await client.activepieces.listRuns({ flowId: "flow_id", limit: 20 });
const run                = await client.activepieces.getRun("run_id");

const { data: folders }  = await client.activepieces.listFolders();
const folder             = await client.activepieces.createFolder({ displayName: "CRM Automations", projectId: "project_id" });

const { data: connections } = await client.activepieces.listConnections();
await client.activepieces.upsertConnection({
  name: "slack-integration",
  type: "OAUTH2",
  value: { access_token: "xoxb-xxx" },
});

const { data: tables }   = await client.activepieces.listTables();
const { data: records }  = await client.activepieces.listRecords({ tableId: "table_id" });
```
```python
runs   = client.workflows.list_runs(flow_id="flow_id", limit=20).get("data", [])
run    = client.workflows.get_run("run_id")

folders = client.workflows.list_folders().get("data", [])
folder  = client.workflows.create_folder(display_name="CRM Automations", project_id="project_id")

connections = client.workflows.list_connections().get("data", [])
client.workflows.upsert_connection({"name": "slack-integration", "type": "OAUTH2", "value": {"access_token": "xoxb-xxx"}})

tables  = client.workflows.list_tables().get("data", [])
records = client.workflows.list_records(table_id="table_id").get("data", [])
```

---

## Channel Automation â€” `client.workflows`

```typescript
const { data: automations }    = await client.workflows.listChannelAutomation();
const { data: whatsappFlows }  = await client.workflows.listChannelAutomation({ channelType: "whatsapp" });
```
```python
automations    = client.workflows.list_channel_automation().get("data", [])
whatsapp_flows = client.workflows.list_channel_automation(channel_type="whatsapp")
```