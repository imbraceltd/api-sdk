/**
 * AiAgent resource test — runs against prodv2 gateway.
 * Usage: node test-ai-agent.mjs
 */

import { ImbraceClient } from '@imbrace/sdk'
import { randomUUID } from 'crypto'

const ACCESS_TOKEN  = process.env.IMBRACE_ACCESS_TOKEN  || 'acc_c8c27f3b-e147-4735-b641-61e8d3706692'
const GATEWAY       = process.env.IMBRACE_GATEWAY_URL   || 'https://app-gatewayv2.imbrace.co'
const ORG_ID        = process.env.IMBRACE_ORG_ID        || 'org_8d2a2d53-20ef-4c54-8aa9-aadec5963b5c'
const ASSISTANT_ID  = process.env.IMBRACE_ASSISTANT_ID  || 'b64b4dfd-7f02-4f8d-962e-c3f48569af20'

const client  = new ImbraceClient({ accessToken: ACCESS_TOKEN, gateway: GATEWAY, organizationId: ORG_ID })
const aiAgent = client.aiAgent

let passed = 0, failed = 0, skipped = 0

function ok(label, detail = '') {
  console.log(`  ✓ ${label}${detail ? `  →  ${String(detail).slice(0, 120)}` : ''}`)
  passed++
}
function fail(label, err) {
  console.error(`  ✗ ${label}: ${err?.message ?? JSON.stringify(err).slice(0, 120)}`)
  failed++
}
function skip(label, reason) {
  console.log(`  - ${label}  (skipped: ${reason})`)
  skipped++
}

// ─────────────────────────────────────────────────────────────────────────────
// [1] System
// ─────────────────────────────────────────────────────────────────────────────

console.log('\n[1] System')

try {
  const cfg = await aiAgent.getConfig()
  ok('getConfig()', JSON.stringify(cfg).slice(0, 100))
} catch (e) { fail('getConfig()', e) }

try {
  const h = await aiAgent.getHealth()
  ok('getHealth()', JSON.stringify(h).slice(0, 100))
} catch (e) { fail('getHealth()', e) }

try {
  const v = await aiAgent.getVersion()
  ok('getVersion()', JSON.stringify(v).slice(0, 100))
} catch (e) { fail('getVersion()', e) }

// ─────────────────────────────────────────────────────────────────────────────
// [2] Chat v1
// ─────────────────────────────────────────────────────────────────────────────

console.log('\n[2] Chat v1')

let firstChatId = null
try {
  const res = await aiAgent.listChats({ organization_id: ORG_ID, limit: 5 })
  const chats = res?.chats ?? res
  firstChatId = Array.isArray(chats) ? chats[0]?.id : null
  ok('listChats()', `count=${res?.count ?? (Array.isArray(chats) ? chats.length : '?')}`)
} catch (e) { fail('listChats()', e) }

if (firstChatId) {
  try {
    const chat = await aiAgent.getChat(firstChatId)
    ok('getChat()', `id=${chat?.id}`)
  } catch (e) { fail('getChat()', e) }
} else {
  skip('getChat()', 'no chats found')
}

// ─────────────────────────────────────────────────────────────────────────────
// [3] Prompt suggestions
// ─────────────────────────────────────────────────────────────────────────────

console.log('\n[3] Prompt suggestions')

try {
  const res = await aiAgent.getAgentPromptSuggestion(ASSISTANT_ID)
  const suggestions = res?.data ?? res
  ok('getAgentPromptSuggestion()', `${Array.isArray(suggestions) ? suggestions.length : '?'} suggestions`)
} catch (e) { fail('getAgentPromptSuggestion()', e) }

// ─────────────────────────────────────────────────────────────────────────────
// [4] Embeddings
// ─────────────────────────────────────────────────────────────────────────────

console.log('\n[4] Embeddings')

try {
  const res = await aiAgent.listEmbeddingFiles()
  const files = Array.isArray(res) ? res : res?.files ?? res?.data ?? []
  ok('listEmbeddingFiles()', `${Array.isArray(files) ? files.length : '?'} files`)
} catch (e) { fail('listEmbeddingFiles()', e) }

try {
  const res = await aiAgent.classifyFile({ url: 'https://example.com/test.pdf', mime_type: 'application/pdf' })
  ok('classifyFile()', JSON.stringify(res).slice(0, 100))
} catch (e) { fail('classifyFile()', e) }

// ─────────────────────────────────────────────────────────────────────────────
// [5] Data Board
// ─────────────────────────────────────────────────────────────────────────────

console.log('\n[5] Data Board')

skip('suggestFieldTypes()', 'route not wired in this app-gateway build (POST / path stripped)')

// ─────────────────────────────────────────────────────────────────────────────
// [6] Parquet
// ─────────────────────────────────────────────────────────────────────────────

console.log('\n[6] Parquet')

try {
  const res = await aiAgent.listParquetFiles()
  ok('listParquetFiles()', JSON.stringify(res).slice(0, 100))
} catch (e) { fail('listParquetFiles()', e) }

let generatedFileName = null
try {
  const res = await aiAgent.generateParquet({
    fileName: `sdk_test_${Date.now()}`,
    data: [{ id: 1, name: 'test', value: 42 }],
  })
  generatedFileName = res?.fileName ?? null
  ok('generateParquet()', JSON.stringify(res).slice(0, 100))
} catch (e) { fail('generateParquet()', e) }

if (generatedFileName) {
  try {
    await aiAgent.deleteParquetFile(generatedFileName)
    ok('deleteParquetFile()')
  } catch (e) { fail('deleteParquetFile()', e) }
} else {
  skip('deleteParquetFile()', 'generateParquet failed or returned no fileName')
}

// ─────────────────────────────────────────────────────────────────────────────
// [7] Trace
// ─────────────────────────────────────────────────────────────────────────────

console.log('\n[7] Trace')

skip('getTraceServices()', 'Grafana Tempo URL not configured on this deployment')
skip('getTraceTags()',    'Grafana Tempo URL not configured on this deployment')
skip('getTraces()',       'Grafana Tempo URL not configured on this deployment')

// ─────────────────────────────────────────────────────────────────────────────
// [8] Admin guides
// ─────────────────────────────────────────────────────────────────────────────

console.log('\n[8] Admin guides')

let firstGuide = null
try {
  const res = await aiAgent.listAdminGuides()
  const guides = Array.isArray(res) ? res : res?.guides ?? res?.data ?? []
  firstGuide = Array.isArray(guides) ? guides[0]?.filename ?? guides[0]?.name : null
  ok('listAdminGuides()', `${Array.isArray(guides) ? guides.length : '?'} guides`)
} catch (e) { fail('listAdminGuides()', e) }

if (firstGuide) {
  try {
    const r = await aiAgent.getAdminGuide(firstGuide)
    ok('getAdminGuide()', `status=${r.status}, type=${r.headers.get('content-type')}`)
  } catch (e) { fail('getAdminGuide()', e) }
} else {
  skip('getAdminGuide()', 'no guides listed')
}

// ─────────────────────────────────────────────────────────────────────────────
// [9] Chat Client — CRUD cycle
// ─────────────────────────────────────────────────────────────────────────────

console.log('\n[9] Chat Client')

try {
  const res = await aiAgent.listClientChats({ organization_id: ORG_ID, limit: 5 })
  const chats = res?.chats ?? res?.data ?? res
  ok('listClientChats()', `count=${Array.isArray(chats) ? chats.length : '?'}`)
} catch (e) { fail('listClientChats()', e) }

const newChatId = randomUUID()
let createdChat = null
try {
  createdChat = await aiAgent.createClientChat({
    id: newChatId,
    message: { id: randomUUID(), role: 'user', parts: [{ type: 'text', text: 'SDK test message' }] },
    selectedVisibilityType: 'private',
    assistantId: ASSISTANT_ID,
    organizationId: ORG_ID,
  })
  ok('createClientChat()', `id=${createdChat?.id ?? newChatId}`)
} catch (e) { fail('createClientChat()', e) }

if (createdChat) {
  try {
    const chat = await aiAgent.getClientChat(newChatId)
    ok('getClientChat()', `id=${chat?.id}`)
  } catch (e) { fail('getClientChat()', e) }

  try {
    const msgs = await aiAgent.listClientMessages(newChatId)
    const list = msgs?.messages ?? msgs?.data ?? msgs
    ok('listClientMessages()', `${Array.isArray(list) ? list.length : '?'} messages`)
  } catch (e) { fail('listClientMessages()', e) }

  try {
    await aiAgent.deleteClientChat(newChatId)
    ok('deleteClientChat()')
  } catch (e) { fail('deleteClientChat()', e) }
} else {
  skip('getClientChat()', 'createClientChat failed')
  skip('listClientMessages()', 'createClientChat failed')
  skip('deleteClientChat()', 'createClientChat failed')
}

// ─────────────────────────────────────────────────────────────────────────────

console.log(`\n${'─'.repeat(55)}`)
console.log(`  ${passed} passed  |  ${failed} failed  |  ${skipped} skipped`)
if (failed > 0) process.exit(1)
