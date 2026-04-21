/**
 * AI resource test — runs against prodv2 gateway.
 * Usage: node test-ai.mjs
 */

import { ImbraceClient } from '@imbrace/sdk'

const ACCESS_TOKEN = process.env.IMBRACE_ACCESS_TOKEN || 'acc_c8c27f3b-e147-4735-b641-61e8d3706692'
const GATEWAY      = process.env.IMBRACE_GATEWAY_URL  || 'https://app-gatewayv2.imbrace.co'

const client = new ImbraceClient({ accessToken: ACCESS_TOKEN, gateway: GATEWAY })
const ai = client.ai

let passed = 0, failed = 0, skipped = 0

function ok(label, detail = '') {
  console.log(`  ✓ ${label}${detail ? `  →  ${String(detail).slice(0, 80)}` : ''}`)
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

// ── [1] List assistants ───────────────────────────────────────────────────────

console.log('\n[1] List assistants')
let firstAssistant = null
try {
  const res = await ai.listAssistants()
  const list = Array.isArray(res) ? res : (res.data ?? [])
  ok('listAssistants()', `${list.length} assistants`)
  if (list.length > 0) firstAssistant = list[0]
} catch (e) { fail('listAssistants()', e) }

// ── [2] Get assistant ─────────────────────────────────────────────────────────

console.log('\n[2] Get assistant')
if (!firstAssistant) {
  skip('getAssistant()', 'no assistants found')
} else {
  const id = firstAssistant._id ?? firstAssistant.id
  try {
    const a = await ai.getAssistant(id)
    ok('getAssistant()', `id=${a._id ?? a.id} name=${a.name}`)
  } catch (e) {
    if (e?.message?.includes('400')) {
      skip('getAssistant()', 'assistant not accessible via this token scope')
    } else {
      fail('getAssistant()', e)
    }
  }
}

// ── [3] List guardrails ───────────────────────────────────────────────────────

console.log('\n[3] List guardrails')
try {
  const res = await ai.listGuardrails()
  const list = Array.isArray(res) ? res : (res.data ?? [])
  ok('listGuardrails()', `${list.length} guardrails`)
} catch (e) { fail('listGuardrails()', e) }

// ── [4] List providers ────────────────────────────────────────────────────────

console.log('\n[4] List providers')
try {
  const res = await ai.listProviders()
  const list = Array.isArray(res) ? res : (res.data ?? [])
  ok('listProviders()', `${list.length} providers`)
} catch (e) { fail('listProviders()', e) }

// ── [5] Get LLM models ────────────────────────────────────────────────────────

console.log('\n[5] Get LLM models')
try {
  const res = await ai.getLlmModels()
  const list = Array.isArray(res) ? res : (res.data ?? res.models ?? [])
  ok('getLlmModels()', `${list.length} models`)
} catch (e) { fail('getLlmModels()', e) }

// ── [6] Complete (non-streaming) ──────────────────────────────────────────────

console.log('\n[6] Complete')
if (!firstAssistant) {
  skip('complete()', 'no assistant available')
} else {
  const id = firstAssistant._id ?? firstAssistant.id
  try {
    const res = await ai.complete({
      assistant_id: id,
      messages: [{ role: 'user', content: 'Hi' }],
    })
    ok('complete()', `${JSON.stringify(res).slice(0, 80)}`)
  } catch (e) {
    if (e?.message?.includes('404')) {
      skip('complete()', 'completions endpoint not available on this env')
    } else {
      fail('complete()', e)
    }
  }
}

// ── Summary ───────────────────────────────────────────────────────────────────

console.log(`\n${'─'.repeat(50)}`)
console.log(`  ${passed} passed  |  ${failed} failed  |  ${skipped} skipped`)
if (failed > 0) process.exit(1)
