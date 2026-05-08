/**
 * Document AI test — runs against prodv2 gateway.
 * Usage: node test-document-ai-apikey.mjs
 *
 * Covers:
 *   - chatAi.listDocumentModels / chatAi.processDocument (low-level vision extraction)
 *   - documentAi.listAgents / getAgent / createAgent / updateAgent / deleteAgent
 *   - documentAi.suggestSchema (meta-prompt → JSON schema)
 *   - documentAi.process (agent-driven extraction)
 */

import { ImbraceClient } from '@imbrace/sdk'

const API_KEY = process.env.IMBRACE_API_KEY || 'api_7601650a-96c6-4227-91c0-f00cc258883a'
const GATEWAY      = process.env.IMBRACE_GATEWAY_URL  || 'https://app-gatewayv2.imbrace.co'
const ORG_ID       = process.env.IMBRACE_ORG_ID       || 'org_8d2a2d53-20ef-4c54-8aa9-aadec5963b5c'

// Small Chinese VAT invoice image — publicly accessible on prodv2
const TEST_IMAGE_URL = 'https://app-gatewayv2.imbrace.co/files/download/118615471-5b33f600-b7f3-11eb-94a1-78e635e66558.png'

const client = new ImbraceClient({ apiKey: API_KEY, baseUrl: GATEWAY, organizationId: ORG_ID, timeout: 120000 })
const chatAi = client.chatAi
const documentAi = client.documentAi

let passed = 0, failed = 0, skipped = 0
const created = { agentId: null }

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

// ── [1] List providers ───────────────────────────────────────────────────────

console.log('\n[1] List document AI providers')
let visionModel = null
let visionModelId = null
try {
  const providers = await chatAi.listDocumentModels()
  const list = Array.isArray(providers) ? providers : []
  const allModels = list.flatMap(p => (p.models ?? []).map(m => ({ ...m, providerName: p.name })))
  const visionModels = allModels.filter(m => m.is_vision_available && !m.name.includes('image'))
  const picked = visionModels.find(m => m.name === 'gpt-4o')
    ?? visionModels.find(m => m.name.startsWith('gpt-4'))
    ?? visionModels[0]
    ?? null
  visionModel = picked?.name ?? null
  visionModelId = picked?._id ?? picked?.id ?? null
  ok('listDocumentModels()', `${list.length} providers, ${allModels.length} models, ${visionModels.length} vision-capable`)
} catch (e) { fail('listDocumentModels()', e) }

// ── [2] chatAi.processDocument (low-level URL → structured data) ─────────────

console.log('\n[2] chatAi.processDocument with vision model')
if (!visionModel) {
  skip('processDocument()', 'no vision-capable model found')
} else {
  try {
    const res = await chatAi.processDocument({
      modelName: visionModel,
      url: TEST_IMAGE_URL,
      organizationId: ORG_ID,
    })
    if (!res.success) throw new Error(JSON.stringify(res))
    const keys = Object.keys(res.data ?? {})
    ok(`processDocument() ${visionModel}`, `extracted keys: ${keys.join(', ')}`)
  } catch (e) { fail(`processDocument() ${visionModel}`, e) }
}

// ── [3] documentAi.listAgents ────────────────────────────────────────────────

console.log('\n[3] documentAi.listAgents')
try {
  const res = await documentAi.listAgents()
  const list = Array.isArray(res) ? res : (res?.data ?? [])
  ok('listAgents()', `${list.length} agents`)
} catch (e) { fail('listAgents()', e) }

try {
  const res = await documentAi.listAgents({ documentAiOnly: true })
  const list = Array.isArray(res) ? res : (res?.data ?? [])
  ok('listAgents({documentAiOnly:true})', `${list.length} agents`)
} catch (e) { fail('listAgents({documentAiOnly:true})', e) }

// ── [4] documentAi.suggestSchema ─────────────────────────────────────────────

console.log('\n[4] documentAi.suggestSchema')
if (!visionModel) {
  skip('suggestSchema()', 'no vision-capable model found')
} else {
  try {
    const res = await documentAi.suggestSchema({
      url: TEST_IMAGE_URL,
      organizationId: ORG_ID,
      modelName: visionModel,
    })
    const fieldCount = Object.keys(res?.data?.properties ?? res?.properties ?? {}).length
    ok('suggestSchema()', `${fieldCount} suggested fields`)
  } catch (e) { fail('suggestSchema()', e) }
}

// ── [5] documentAi.createAgent + updateAgent + deleteAgent ───────────────────

console.log('\n[5] documentAi.createAgent / updateAgent / deleteAgent')
if (!visionModelId) {
  skip('createAgent()', 'no vision model id available')
} else {
  try {
    const agent = await documentAi.createAgent({
      name: `SDK Test Agent ${Date.now()}`,
      instructions: 'Extract text content from documents.',
      model_id: visionModelId,
      schema: {
        type: 'object',
        properties: { text: { type: 'string' } },
      },
    })
    created.agentId = agent?._id ?? agent?.id ?? null
    ok('createAgent()', `id=${created.agentId}`)
  } catch (e) { fail('createAgent()', e) }

  if (created.agentId) {
    try {
      const agent = await documentAi.getAgent(created.agentId)
      ok('getAgent()', `id=${agent?._id ?? agent?.id} name=${agent?.name}`)
    } catch (e) { fail('getAgent()', e) }

    try {
      const agent = await documentAi.updateAgent(created.agentId, {
        name: `SDK Test Agent Updated ${Date.now()}`,
      })
      ok('updateAgent()', `name=${agent?.name}`)
    } catch (e) { fail('updateAgent()', e) }
  }
}

// ── [6] documentAi.process — agent-driven extraction ─────────────────────────

console.log('\n[6] documentAi.process (agent-driven)')
if (!created.agentId) {
  skip('process(agentId)', 'no agent created')
} else {
  try {
    const res = await documentAi.process({
      agentId: created.agentId,
      url: TEST_IMAGE_URL,
      organizationId: ORG_ID,
    })
    if (!res?.success) throw new Error(JSON.stringify(res).slice(0, 120))
    ok('process(agentId)', `extracted keys: ${Object.keys(res.data ?? {}).join(', ')}`)
  } catch (e) { fail('process(agentId)', e) }
}

// ── [7] Cleanup ──────────────────────────────────────────────────────────────

console.log('\n[7] Cleanup')
if (created.agentId) {
  try {
    await documentAi.deleteAgent(created.agentId)
    ok(`deleteAgent(${created.agentId})`)
  } catch (e) { fail(`deleteAgent(${created.agentId})`, e) }
}

console.log(`\n${'─'.repeat(55)}`)
console.log(`  ${passed} passed  |  ${failed} failed  |  ${skipped} skipped`)
if (failed > 0) process.exit(1)
