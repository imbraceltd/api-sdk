# Data Boards

Boards are the core data store for CRM pipelines â€” leads, deals, tasks, or any structured data. Pass board ids in `board_ids` when creating an assistant to give it access to that data â€” see [Full Flow Guide Â§4](/sdk/full-flow-guide/#4-manage-data-boards-and-items-crm-pipelines).

Initialize the client first (see [Installation](/sdk/installation/) or [Quick Start](/sdk/quick-start/)).

---

## Board CRUD

```typescript
const { data: boards } = await client.boards.list();
const board = await client.boards.get("board_id");

const newBoard = await client.boards.create({ name: "Enterprise Leads" });
await client.boards.update("board_id", { name: "Enterprise Leads 2025" });
await client.boards.delete("board_id");
```
```python
boards = client.boards.list().get("data", [])
board = client.boards.get("board_id")

new_board = client.boards.create("Enterprise Leads")
client.boards.update("board_id", {"name": "Enterprise Leads 2025"})
client.boards.delete("board_id")
```

---

## Items

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
await client.boards.bulkDeleteItems("board_id", { ids: ["item_1", "item_2", "item_3"] });
```
```python
leads = client.boards.list_items("board_id", limit=100).get("data", [])

lead = client.boards.create_item("board_id", {
    "fields": {"name": "Acme Corp", "status": "new", "value": 50000}
})

client.boards.update_item("board_id", lead["id"], {
    "fields": {"status": "qualified"}
})

client.boards.delete_item("board_id", "item_id")
client.boards.bulk_delete_items("board_id", {"ids": ["item_1", "item_2", "item_3"]})
```

---

## Search

```typescript
const results = await client.boards.search("board_id", { q: "enterprise" });
```
```python
results = client.boards.search("board_id", q="enterprise")
```

---

## Fields, Segments & Export

```typescript
// Fields
const field = await client.boards.createField("board_id", {
  name: "Deal Value",
  type: "number",
});
await client.boards.updateField("board_id", field._id, { name: "Contract Value" });
await client.boards.deleteField("board_id", field._id);

// Segments
const { data: segments } = await client.boards.listSegments("board_id");
const segment = await client.boards.createSegment("board_id", {
  name: "High Value Leads",
  filter: { field: "value", op: "gt", value: 10000 },
});

// Export to CSV
const csv = await client.boards.exportCsv("board_id");
```
```python
# Fields
field = client.boards.create_field("board_id", {"name": "Deal Value", "type": "number"})
client.boards.update_field("board_id", field["_id"], {"name": "Contract Value"})
client.boards.delete_field("board_id", field["_id"])

# Segments
segments = client.boards.list_segments("board_id")
segment = client.boards.create_segment("board_id", {
    "name": "High Value Leads",
    "filter": {"field": "value", "op": "gt", "value": 10000},
})

# Export to CSV
csv = client.boards.export_csv("board_id")
```