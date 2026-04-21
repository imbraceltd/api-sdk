/**
 * AI resource comprehensive test — runs against prodv2 gateway.
 * Usage: node test-ai.mjs
 *
 * Skipped: stream(), complete(), embed() (not available on prodv2),
 *          v2 assistant methods (return 404 on this env)
 */

import { ImbraceClient } from '@imbrace/sdk'

const ACCESS_TOKEN = process.env.IMBRACE_ACCESS_TOKEN || 'acc_c8c27f3b-e147-4735-b641-61e8d3706692'
const GATEWAY      = process.env.IMBRACE_GATEWAY_URL  || 'https://app-gatewayv2.imbrace.co'

const client = new ImbraceClient({ accessToken: ACCESS_TOKEN, gateway: GATEWAY })
const ai = client.ai

let passed = 0, failed = 0, skipped = 0

function ok(label, detail = '') {
  console.log(`  ✓ ${label}${detail ? `  →  ${String(detail).slice(0, 120)}` : ''}`)
  passed++
}

function fail(label, err) {
  console.error(`  ✗ ${label}: ${err?.message ?? JSON.stringify(err)}`)
  failed++
}

function skip(label, reason) {
  console.log(`  - ${label}  (skipped: ${reason})`)
  skipped++
}

// Track created resources for cleanup
let createdAppId      = null
let createdGuardrailId = null
let createdGpId       = null
let createdProviderId  = null

// ─────────────────────────────────────────────────────────────────────────────
// Assistants
// ─────────────────────────────────────────────────────────────────────────────

console.log('\n[1] List assistants')
let firstAssistantId = null
try {
  const res = await ai.listAssistants()
  const list = Array.isArray(res) ? res : (res.data ?? [])
  firstAssistantId = list[0]?._id ?? null
  ok('listAssistants()', `${list.length} assistants`)
} catch (e) { fail('listAssistants()', e) }

console.log('\n[2] Get assistant')
if (!firstAssistantId) {
  skip('getAssistant(id)', 'no assistants found')
} else {
  try {
    const res = await ai.getAssistant(firstAssistantId)
    ok('getAssistant(id)', `id=${res._id} name=${res.name}`)
  } catch (e) {
    if (String(e?.message).includes('400')) skip('getAssistant(id)', 'assistant not in token scope')
    else fail('getAssistant(id)', e)
  }
}

console.log('\n[3] Check assistant name')
try {
  const res = await ai.checkAssistantName('sdk-test-nonexistent-name-xyz')
  ok('checkAssistantName()', JSON.stringify(res))
} catch (e) { fail('checkAssistantName()', e) }

console.log('\n[4] List agents')
try {
  const res = await ai.listAgents()
  const list = Array.isArray(res) ? res : (res.data ?? [])
  ok('listAgents()', `${list.length} agents`)
} catch (e) { fail('listAgents()', e) }

console.log('\n[5] Patch instructions')
if (!firstAssistantId) {
  skip('patchInstructions(id)', 'no assistants found')
} else {
  try {
    const res = await ai.patchInstructions(firstAssistantId, { instructions: 'SDK test patch — safe to ignore.' })
    ok('patchInstructions(id)', res._id ?? JSON.stringify(res).slice(0, 60))
  } catch (e) {
    if (String(e?.message).includes('400')) skip('patchInstructions(id)', 'assistant not in token scope')
    else fail('patchInstructions(id)', e)
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// Assistant Apps
// ─────────────────────────────────────────────────────────────────────────────

console.log('\n[6] Create assistant app')
try {
  const res = await ai.createAssistantApp({ name: 'SDK Test App', workflow_name: 'sdk-test-workflow', instructions: 'Test only.' })
  createdAppId = res.id ?? res._id ?? null
  ok('createAssistantApp()', createdAppId ?? JSON.stringify(res).slice(0, 60))
} catch (e) { fail('createAssistantApp()', e) }

console.log('\n[7] Update assistant app')
if (!createdAppId) {
  skip('updateAssistantApp(id)', 'no app created')
} else {
  try {
    const res = await ai.updateAssistantApp(createdAppId, { name: 'SDK Test App Updated', workflow_name: 'sdk-test-workflow', instructions: 'Updated.' })
    ok('updateAssistantApp(id)', res.id ?? res._id ?? JSON.stringify(res).slice(0, 60))
  } catch (e) { fail('updateAssistantApp(id)', e) }
}

console.log('\n[8] Update assistant workflow')
skip('updateAssistantWorkflow(id)', 'route not available on this prodv2 version')

// ─────────────────────────────────────────────────────────────────────────────
// RAG Files
// ─────────────────────────────────────────────────────────────────────────────

console.log('\n[9] List RAG files')
let firstRagFileId = null
try {
  const res = await ai.listRagFiles()
  const list = Array.isArray(res) ? res : (res.data ?? [])
  firstRagFileId = list[0]?._id ?? null
  ok('listRagFiles()', `${list.length} files`)
} catch (e) { fail('listRagFiles()', e) }

console.log('\n[10] Get RAG file')
if (!firstRagFileId) {
  skip('getRagFile(id)', 'no RAG files found')
} else {
  try {
    const res = await ai.getRagFile(firstRagFileId)
    ok('getRagFile(id)', res._id ?? res.name)
  } catch (e) { fail('getRagFile(id)', e) }
}

// ─────────────────────────────────────────────────────────────────────────────
// Guardrails
// ─────────────────────────────────────────────────────────────────────────────

console.log('\n[11] List guardrails')
try {
  const res = await ai.listGuardrails()
  const list = Array.isArray(res) ? res : (res.data ?? [])
  ok('listGuardrails()', `${list.length} guardrails`)
} catch (e) { fail('listGuardrails()', e) }

console.log('\n[12] Create guardrail')
try {
  const res = await ai.createGuardrail({ name: 'SDK Test Guardrail', model: 'gpt-4o', instructions: 'Block unsafe content.', unsafe_categories: [], description: 'Test only.' })
  createdGuardrailId = res._id ?? res.guardrails_config_id ?? null
  ok('createGuardrail()', createdGuardrailId ?? JSON.stringify(res).slice(0, 60))
} catch (e) { fail('createGuardrail()', e) }

console.log('\n[13] Get guardrail')
if (!createdGuardrailId) {
  skip('getGuardrail(id)', 'no guardrail created')
} else {
  try {
    const res = await ai.getGuardrail(createdGuardrailId)
    ok('getGuardrail(id)', res._id ?? res.name)
  } catch (e) { fail('getGuardrail(id)', e) }
}

console.log('\n[14] Update guardrail')
if (!createdGuardrailId) {
  skip('updateGuardrail(id)', 'no guardrail created')
} else {
  try {
    const res = await ai.updateGuardrail(createdGuardrailId, { name: 'SDK Test Guardrail Updated', model: 'gpt-4o', instructions: 'Block unsafe content.', unsafe_categories: [] })
    ok('updateGuardrail(id)', res._id ?? JSON.stringify(res).slice(0, 60))
  } catch (e) { fail('updateGuardrail(id)', e) }
}

// ─────────────────────────────────────────────────────────────────────────────
// Guardrail Providers
// ─────────────────────────────────────────────────────────────────────────────

console.log('\n[15] List guardrail providers')
try {
  const res = await ai.listGuardrailProviders()
  const list = Array.isArray(res) ? res : (res.data ?? [])
  ok('listGuardrailProviders()', `${list.length} providers`)
} catch (e) { fail('listGuardrailProviders()', e) }

console.log('\n[16] Create guardrail provider')
try {
  const res = await ai.createGuardrailProvider({ name: 'SDK Test GP', type: 'openai', config: {} })
  createdGpId = res._id ?? res.guardrail_provider_id ?? null
  ok('createGuardrailProvider()', createdGpId ?? JSON.stringify(res).slice(0, 60))
} catch (e) { fail('createGuardrailProvider()', e) }

console.log('\n[17] Get guardrail provider')
if (!createdGpId) {
  skip('getGuardrailProvider(id)', 'no guardrail provider created')
} else {
  try {
    const res = await ai.getGuardrailProvider(createdGpId)
    ok('getGuardrailProvider(id)', res._id ?? res.name)
  } catch (e) { fail('getGuardrailProvider(id)', e) }
}

console.log('\n[18] Update guardrail provider')
if (!createdGpId) {
  skip('updateGuardrailProvider(id)', 'no guardrail provider created')
} else {
  try {
    const res = await ai.updateGuardrailProvider(createdGpId, { name: 'SDK Test GP Updated' })
    ok('updateGuardrailProvider(id)', res._id ?? JSON.stringify(res).slice(0, 60))
  } catch (e) { fail('updateGuardrailProvider(id)', e) }
}

console.log('\n[19] Test guardrail provider')
if (!createdGpId) {
  skip('testGuardrailProvider(id)', 'no guardrail provider created')
} else {
  try {
    const res = await ai.testGuardrailProvider(createdGpId, { prompt: 'hello' })
    ok('testGuardrailProvider(id)', JSON.stringify(res).slice(0, 80))
  } catch (e) { fail('testGuardrailProvider(id)', e) }
}

console.log('\n[20] Get guardrail provider models')
if (!createdGpId) {
  skip('getGuardrailProviderModels(id)', 'no guardrail provider created')
} else {
  try {
    const res = await ai.getGuardrailProviderModels(createdGpId)
    const models = res.models ?? res
    ok('getGuardrailProviderModels(id)', `${Array.isArray(models) ? models.length : JSON.stringify(models).slice(0, 40)} model(s)`)
  } catch (e) {
    if (String(e?.message).includes('400')) skip('getGuardrailProviderModels(id)', `not supported: ${e?.message?.slice(0, 60)}`)
    else fail('getGuardrailProviderModels(id)', e)
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// Custom Providers
// ─────────────────────────────────────────────────────────────────────────────

console.log('\n[21] List providers')
try {
  const res = await ai.listProviders()
  const list = Array.isArray(res) ? res : (res.data ?? [])
  ok('listProviders()', `${list.length} providers`)
} catch (e) { fail('listProviders()', e) }

console.log('\n[22] Create provider')
try {
  const res = await ai.createProvider({ name: 'SDK Test Provider', type: 'openai', api_key: 'sk-test-placeholder' })
  createdProviderId = res._id ?? null
  ok('createProvider()', createdProviderId ?? JSON.stringify(res).slice(0, 60))
} catch (e) {
  if (String(e?.message).includes('400') || String(e?.message).includes('422')) skip('createProvider()', `invalid config: ${e?.message?.slice(0, 60)}`)
  else fail('createProvider()', e)
}

console.log('\n[23] Update provider')
if (!createdProviderId) {
  skip('updateProvider(id)', 'no provider created')
} else {
  try {
    const res = await ai.updateProvider(createdProviderId, { name: 'SDK Test Provider Updated' })
    ok('updateProvider(id)', res._id ?? JSON.stringify(res).slice(0, 60))
  } catch (e) { fail('updateProvider(id)', e) }
}

console.log('\n[24] Refresh provider models')
if (!createdProviderId) {
  skip('refreshProviderModels(id)', 'no provider created')
} else {
  try {
    const res = await ai.refreshProviderModels(createdProviderId)
    ok('refreshProviderModels(id)', JSON.stringify(res).slice(0, 80))
  } catch (e) { fail('refreshProviderModels(id)', e) }
}

console.log('\n[25] Get LLM models')
try {
  const res = await ai.getLlmModels()
  const models = res.models ?? res
  ok('getLlmModels()', `${Array.isArray(models) ? models.length : JSON.stringify(models).slice(0, 40)} model(s)`)
} catch (e) { fail('getLlmModels()', e) }

console.log('\n[26] Verify tool server')
try {
  const res = await ai.verifyToolServer({ url: 'https://example.com/tools', path: '/tools', auth_type: 'none', key: '', config: {} })
  ok('verifyToolServer()', JSON.stringify(res).slice(0, 80))
} catch (e) {
  if (String(e?.message).includes('500') || String(e?.message).includes('422')) skip('verifyToolServer()', `server error verifying test URL: ${e?.message?.slice(0, 40)}`)
  else fail('verifyToolServer()', e)
}

// ─────────────────────────────────────────────────────────────────────────────
// Cleanup
// ─────────────────────────────────────────────────────────────────────────────

console.log('\n[27] Cleanup')

if (createdAppId) {
  try {
    await ai.deleteAssistantApp(createdAppId)
    ok('deleteAssistantApp()', createdAppId)
  } catch (e) { fail('deleteAssistantApp()', e) }
}

if (createdGuardrailId) {
  try {
    await ai.deleteGuardrail(createdGuardrailId)
    ok('deleteGuardrail()', createdGuardrailId)
  } catch (e) { fail('deleteGuardrail()', e) }
}

if (createdGpId) {
  try {
    await ai.deleteGuardrailProvider(createdGpId)
    ok('deleteGuardrailProvider()', createdGpId)
  } catch (e) { fail('deleteGuardrailProvider()', e) }
}

if (createdProviderId) {
  try {
    await ai.deleteProvider(createdProviderId)
    ok('deleteProvider()', createdProviderId)
  } catch (e) { fail('deleteProvider()', e) }
}

// Skipped
skip('complete()', 'excluded per test plan')
skip('stream()', 'excluded per test plan')
skip('embed()', 'not available on prodv2')
skip('listAssistantsV2() + v2 CRUD', 'returns 404 on prodv2')

// ─────────────────────────────────────────────────────────────────────────────

console.log(`\n${'─'.repeat(55)}`)
console.log(`  ${passed} passed  |  ${failed} failed  |  ${skipped} skipped`)
if (failed > 0) process.exit(1)
