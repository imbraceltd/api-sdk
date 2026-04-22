/**
 * Document AI test — runs against prodv2 gateway.
 * Usage: node test-document-ai.mjs
 */

import { ImbraceClient } from '@imbrace/sdk'

const ACCESS_TOKEN = process.env.IMBRACE_ACCESS_TOKEN || 'acc_c8c27f3b-e147-4735-b641-61e8d3706692'
const GATEWAY      = process.env.IMBRACE_GATEWAY_URL  || 'https://app-gatewayv2.imbrace.co'
const ORG_ID       = process.env.IMBRACE_ORG_ID       || 'org_8d2a2d53-20ef-4c54-8aa9-aadec5963b5c'

// Small Chinese VAT invoice image — publicly accessible on prodv2
const TEST_IMAGE_URL = 'https://app-gatewayv2.imbrace.co/files/download/118615471-5b33f600-b7f3-11eb-94a1-78e635e66558.png'

const client = new ImbraceClient({ accessToken: ACCESS_TOKEN, baseUrl: GATEWAY, organizationId: ORG_ID })
const chatAi = client.chatAi

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
// List providers (document AI model source)
// ─────────────────────────────────────────────────────────────────────────────

console.log('\n[1] List document AI providers')
let visionModel = null
try {
  const providers = await chatAi.listDocumentModels()
  const list = Array.isArray(providers) ? providers : []
  const allModels = list.flatMap(p => (p.models ?? []).map(m => ({ ...m, providerName: p.name })))
  const visionModels = allModels.filter(m => m.is_vision_available && !m.name.includes('image'))
  // prefer gpt-4o for document reading
  visionModel = visionModels.find(m => m.name === 'gpt-4o')?.name
    ?? visionModels.find(m => m.name.startsWith('gpt-4'))?.name
    ?? visionModels[0]?.name
    ?? null
  ok('listDocumentModels()', `${list.length} providers, ${allModels.length} models, ${visionModels.length} vision-capable`)
} catch (e) { fail('listDocumentModels()', e) }

// ─────────────────────────────────────────────────────────────────────────────
// Process document — vision model from provider
// ─────────────────────────────────────────────────────────────────────────────

console.log('\n[2] Process document with vision model from provider')
if (!visionModel) {
  skip('processDocument()', 'no vision-capable model found in configured providers')
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

// ─────────────────────────────────────────────────────────────────────────────

console.log(`\n${'─'.repeat(55)}`)
console.log(`  ${passed} passed  |  ${failed} failed  |  ${skipped} skipped`)
if (failed > 0) process.exit(1)
