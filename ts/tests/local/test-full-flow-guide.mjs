/**
 * Full Flow Guide — end-to-end test
 * Usage: node test-full-flow-guide.mjs <accessToken> [gateway]
 *
 * Runs all 4 guide flows in sequence and reports pass/fail for each step.
 */

import { ImbraceClient } from "../../dist/client.js"
import { readFileSync } from "fs"

const [, , accessToken, orgId = "", gateway = "https://app-gatewayv2.imbrace.co"] = process.argv
if (!accessToken) {
  console.error("Usage: node test-full-flow-guide.mjs <accessToken> [orgId] [gateway]")
  process.exit(1)
}

const client = new ImbraceClient({ gateway, accessToken })

let passed = 0
let failed = 0

async function step(label, fn) {
  try {
    const result = await fn()
    console.log(`  ✓ ${label}`)
    passed++
    return result
  } catch (e) {
    console.error(`  ✗ ${label}: ${e.message}`)
    failed++
    return null
  }
}

function section(title) {
  const dashes = Math.max(2, 50 - title.length)
  console.log(`\n── ${title} ${"─".repeat(dashes)}`)
}

// ─── Flow 1: Create Assistant and Chat ────────────────────────────────────────

section("Flow 1: Create Assistant → Stream Chat")

const ts = Date.now()
let assistantId = null

const assistant = await step("createAssistant", () =>
  client.chatAi.createAssistant({
    name: `SDK Test Assistant ${ts}`,
    workflow_name: `sdk_guide_test_${ts}`,
    description: "Created by full-flow-guide test",
    instructions: "You are a concise test assistant. Reply in one sentence.",
  })
)
if (assistant) assistantId = assistant.id

await step("getAssistant", () =>
  client.chatAi.getAssistant(assistantId)
)

await step("listAssistants (contains new)", async () => {
  const list = await client.chatAi.listAssistants()
  const found = list.find(a => a.id === assistantId)
  if (!found) throw new Error("New assistant not in list")
  return found
})

await step("updateAssistantInstructions", () =>
  client.chatAi.updateAssistantInstructions(assistantId, "You are a helpful test agent. Reply in one sentence.")
)

await step("updateAssistant (rename)", () =>
  client.chatAi.updateAssistant(assistantId, {
    name: `SDK Test Assistant ${ts} (updated)`,
    workflow_name: `sdk_guide_test_${ts}`,
  })
)

// Use an existing (fully configured) assistant for chat — newly created ones have no model
const allAssistants = await client.chatAi.listAssistants().catch(() => [])
const chatAssistant = allAssistants.find(a => a.id !== assistantId && a.model_id) ?? null
const chatAssistantId = chatAssistant?.id ?? null

// Session ID must be a valid UUID — omit to let SDK auto-generate, or store the one it generated
let sessionId = null
await step("streamChat (first message)", async () => {
  if (!chatAssistantId) throw new Error("No configured assistant found for chat test")
  const res = await client.aiAgent.streamChat({
    assistant_id: chatAssistantId,
    organization_id: orgId || undefined,
    messages: [{ role: "user", content: "Say hello in exactly 5 words." }],
  })
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  const text = await res.text()
  if (!text) throw new Error("Empty response body")
  return text.slice(0, 100)
})

await step("streamChat (follow-up, same session)", async () => {
  if (!chatAssistantId) throw new Error("No configured assistant found for chat test")
  const res = await client.aiAgent.streamChat({
    assistant_id: chatAssistantId,
    organization_id: orgId || undefined,
    messages: [{ role: "user", content: "Say that again." }],
  })
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return await res.text().then(t => t.slice(0, 100))
})

// ─── Flow 2: Activepieces Workflow ────────────────────────────────────────────

section("Flow 2: Activepieces — List Flows + Trigger")

let flowId = null

const flows = await step("listFlows", () =>
  client.activepieces.listFlows({ limit: 5 })
)

if (flows?.data?.length > 0) {
  flowId = flows.data[0].id
  console.log(`    (using existing flow: ${flowId})`)

  await step("getFlow", () =>
    client.activepieces.getFlow(flowId)
  )

  await step("triggerFlow (async)", () =>
    client.activepieces.triggerFlow(flowId, { source: "sdk-test", timestamp: ts })
  )

  await step("listRuns", () =>
    client.activepieces.listRuns({ flowId, limit: 3 })
  )
} else {
  console.log("  ℹ No flows found — skipping trigger/run steps")
}

// ─── Flow 3: Knowledge Hub ────────────────────────────────────────────────────

section("Flow 3: Knowledge Hub — Folder + File + Attach to Assistant")

let kbFolderId = null
let orgId2 = null

// get org_id from existing folders
const existingFolders = await client.boards.searchFolders({}).catch(() => [])
orgId2 = existingFolders[0]?.organization_id ?? orgId ?? null

const kbFolder = await step("boards.createFolder", () => {
  if (!orgId2) throw new Error("No organization_id available")
  return client.boards.createFolder({
    name: `SDK Test KB Folder ${ts}`,
    organization_id: orgId2,
    parent_folder_id: "root",
    source_type: "upload",
  })
})
if (kbFolder) kbFolderId = kbFolder._id ?? kbFolder.id

await step("boards.searchFolders (contains new)", async () => {
  const list = await client.boards.searchFolders({ q: `SDK Test KB Folder ${ts}` })
  const found = list.find(f => (f._id ?? f.id) === kbFolderId)
  if (!found) throw new Error("Folder not in list")
  return found
})

await step("boards.getFolder", () =>
  client.boards.getFolder(kbFolderId)
)

await step("boards.updateFolder (rename)", () =>
  client.boards.updateFolder(kbFolderId, { name: `SDK Test KB Folder ${ts} (renamed)` })
)

// Upload a tiny test file to the folder
await step("boards.uploadFile", async () => {
  if (!kbFolderId) throw new Error("No folder created")
  const formData = new FormData()
  const content = "SDK test file content for knowledge hub testing."
  formData.append("file", new Blob([content], { type: "text/plain" }), "sdk-test.txt")
  formData.append("folder_id", kbFolderId)
  if (orgId2) formData.append("organization_id", orgId2)
  return client.boards.uploadFile(formData)
})

await step("boards.getFolderContents", async () => {
  const contents = await client.boards.getFolderContents(kbFolderId)
  return contents
})

// Attach folder to assistant as its knowledge base
if (assistantId && kbFolderId) {
  await step("attach knowledge folder to assistant", () =>
    client.chatAi.updateAssistant(assistantId, {
      name: `SDK Test Assistant ${ts} (updated)`,
      workflow_name: `sdk_guide_test_${ts}`,
      knowledge_hubs: [kbFolderId],
    })
  )
}

// ─── Flow 4: Boards & Items ───────────────────────────────────────────────────

section("Flow 4: Boards — Create Board → Fields → Items → Delete")

let boardId = null
let identifierFieldId = null
let itemId = null

const board = await step("boards.create", () =>
  client.boards.create({ name: `SDK Test Board ${ts}`, description: "Created by full-flow-guide test" })
)
if (board) boardId = board._id ?? board.id

// get identifier field auto-created with the board
if (boardId) {
  const b = await client.boards.get(boardId).catch(() => null)
  identifierFieldId = b?.fields?.find(f => f.is_identifier)?._id ?? null
}

await step("boards.createField (ShortText)", async () => {
  const res = await client.boards.createField(boardId, { name: "Company", type: "ShortText" })
  // createField returns the updated board — find the new field
  const f = res?.fields?.find(f => f.name === "Company")
  if (!f) throw new Error("Field not found in response")
  return f
})

const item = await step("boards.createItem", async () => {
  if (!identifierFieldId) throw new Error("No identifier field found")
  return client.boards.createItem(boardId, {
    fields: [{ board_field_id: identifierFieldId, value: "Acme Corp" }],
  })
})
if (item) itemId = item._id ?? item.id

await step("boards.getItem", () =>
  client.boards.getItem(boardId, itemId)
)

await step("boards.listItems", async () => {
  const { data } = await client.boards.listItems(boardId, { limit: 10 })
  if (!data?.length) throw new Error("No items returned")
  return data
})

await step("boards.updateItem", async () => {
  if (!identifierFieldId) throw new Error("No identifier field")
  return client.boards.updateItem(boardId, itemId, {
    data: [{ key: identifierFieldId, value: "Acme Corp Updated" }],
  })
})

await step("boards.search", async () => {
  const { data } = await client.boards.search(boardId, { q: "Acme", limit: 5 })
  return data
})

await step("boards.exportCsv", async () => {
  const csv = await client.boards.exportCsv(boardId)
  if (typeof csv !== "string") throw new Error("Expected string CSV")
  return csv.slice(0, 50)
})

await step("boards.deleteItem", () =>
  client.boards.deleteItem(boardId, itemId)
)

// ─── Cleanup ──────────────────────────────────────────────────────────────────

section("Cleanup")

if (kbFolderId) await step("boards.deleteFolders", () => client.boards.deleteFolders({ ids: [kbFolderId] }))
if (boardId) await step("boards.delete", () => client.boards.delete(boardId))
if (assistantId) await step("deleteAssistant", () => client.chatAi.deleteAssistant(assistantId))

// ─── Summary ──────────────────────────────────────────────────────────────────

console.log(`\n${"─".repeat(52)}`)
console.log(`Results: ${passed} passed, ${failed} failed`)
if (failed > 0) process.exit(1)
