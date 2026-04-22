/**
 * Workflows resource test — runs against prodv2 gateway.
 * Usage: node test-workflows.mjs
 *
 * Routes: v2/backend/workflows/channel_automation
 */

import { ImbraceClient } from '@imbrace/sdk'

const ACCESS_TOKEN = process.env.IMBRACE_ACCESS_TOKEN || 'acc_c8c27f3b-e147-4735-b641-61e8d3706692'
const GATEWAY      = process.env.IMBRACE_GATEWAY_URL  || 'https://app-gatewayv2.imbrace.co'

const client = new ImbraceClient({ accessToken: ACCESS_TOKEN, baseUrl: GATEWAY })
const workflows = client.workflows

let passed = 0, failed = 0, skipped = 0

function ok(label, detail = '') {
  console.log(`  ✓ ${label}${detail ? `  →  ${String(detail).slice(0, 100)}` : ''}`)
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

// ── [1] List channel automations ──────────────────────────────────────────────

console.log('\n[1] List channel automations')
try {
  const res = await workflows.listChannelAutomation()
  const list = Array.isArray(res) ? res : (res.data ?? [])
  ok('listChannelAutomation()', `${list.length} automations`)
} catch (e) { fail('listChannelAutomation()', e) }

// ── [2] Filter by channel type ────────────────────────────────────────────────

console.log('\n[2] Filter by channel type')
try {
  const res = await workflows.listChannelAutomation({ channelType: 'whatsapp' })
  const list = Array.isArray(res) ? res : (res.data ?? [])
  ok('listChannelAutomation(whatsapp)', `${list.length} automations`)
} catch (e) { fail('listChannelAutomation(whatsapp)', e) }

// ── Summary ───────────────────────────────────────────────────────────────────

console.log(`\n${'─'.repeat(50)}`)
console.log(`  ${passed} passed  |  ${failed} failed  |  ${skipped} skipped`)
if (failed > 0) process.exit(1)
