/**
 * AiAgent resource test — runs against prodv2 gateway.
 * Usage: node test-ai-agent.mjs
 */

import { ImbraceClient } from '@imbrace/sdk'

const ACCESS_TOKEN = process.env.IMBRACE_ACCESS_TOKEN || 'acc_c8c27f3b-e147-4735-b641-61e8d3706692'
const GATEWAY      = process.env.IMBRACE_GATEWAY_URL  || 'https://app-gatewayv2.imbrace.co'
const ORG_ID       = process.env.IMBRACE_ORG_ID       || 'org_8d2a2d53-20ef-4c54-8aa9-aadec5963b5c'

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
// System
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
// Chat v1
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
// Prompt suggestions
// ─────────────────────────────────────────────────────────────────────────────

console.log('\n[3] Prompt suggestions')

// pick first assistant from listChats or use known id from api_reference.md
const ASSISTANT_ID = process.env.IMBRACE_ASSISTANT_ID || 'b64b4dfd-7f02-4f8d-962e-c3f48569af20'
try {
  const res = await aiAgent.getAgentPromptSuggestion(ASSISTANT_ID)
  const suggestions = res?.data ?? res
  ok('getAgentPromptSuggestion()', `${Array.isArray(suggestions) ? suggestions.length : '?'} suggestions`)
} catch (e) { fail('getAgentPromptSuggestion()', e) }

// ─────────────────────────────────────────────────────────────────────────────
// Embeddings / files
// ─────────────────────────────────────────────────────────────────────────────

console.log('\n[4] Embeddings')

try {
  const res = await aiAgent.listEmbeddingFiles()
  const files = Array.isArray(res) ? res : res?.files ?? res?.data ?? []
  ok('listEmbeddingFiles()', `${Array.isArray(files) ? files.length : '?'} files`)
} catch (e) { fail('listEmbeddingFiles()', e) }

try {
  const res = await aiAgent.getEmbeddingStatistics()
  ok('getEmbeddingStatistics()', JSON.stringify(res).slice(0, 100))
} catch (e) { fail('getEmbeddingStatistics()', e) }

// ─────────────────────────────────────────────────────────────────────────────
// Parquet
// ─────────────────────────────────────────────────────────────────────────────

console.log('\n[5] Parquet')

try {
  const res = await aiAgent.listParquetFiles()
  ok('listParquetFiles()', JSON.stringify(res).slice(0, 100))
} catch (e) { fail('listParquetFiles()', e) }

// ─────────────────────────────────────────────────────────────────────────────
// Admin Guides
// ─────────────────────────────────────────────────────────────────────────────

console.log('\n[6] Admin guides')

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
// Chat Client — list chats
// ─────────────────────────────────────────────────────────────────────────────

console.log('\n[7] Chat Client')

try {
  const res = await aiAgent.listClientChats({ organization_id: ORG_ID, limit: 5 })
  const chats = res?.chats ?? res?.data ?? res
  ok('listClientChats()', `count=${Array.isArray(chats) ? chats.length : '?'}`)
} catch (e) { fail('listClientChats()', e) }

// ─────────────────────────────────────────────────────────────────────────────

console.log(`\n${'─'.repeat(55)}`)
console.log(`  ${passed} passed  |  ${failed} failed  |  ${skipped} skipped`)
if (failed > 0) process.exit(1)
