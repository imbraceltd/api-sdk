/**
 * Local package test — runs against the built dist via npm link.
 *
 * Prerequisites:
 *   1. cd sdk/ts && npm run build && npm link
 *   2. cd tests/local && npm link @imbrace/sdk
 *   3. Copy .env.example → tests/local/.env and fill in credentials
 *   4. node test-local.mjs
 */

import { readFileSync } from 'fs'
import { resolve, dirname } from 'path'
import { fileURLToPath } from 'url'

const __dir = dirname(fileURLToPath(import.meta.url))

// Manual .env loader (no dotenv dep required here)
try {
  const env = readFileSync(resolve(__dir, '.env'), 'utf8')
  for (const line of env.split('\n')) {
    const [k, ...v] = line.trim().split('=')
    if (k && !k.startsWith('#') && !(k in process.env)) {
      process.env[k] = v.join('=')
    }
  }
} catch {
  // .env optional — rely on shell env
}

import { ImbraceClient } from '@imbrace/sdk'

const API_KEY  = process.env.IMBRACE_API_KEY  ?? ''
const ORG_ID   = process.env.IMBRACE_ORGANIZATION_ID ?? ''
const BASE_URL = process.env.IMBRACE_GATEWAY_URL ?? 'https://app-gateway.dev.imbrace.co'

let passed = 0
let failed = 0

function ok(label) {
  console.log(`  ✓ ${label}`)
  passed++
}

function fail(label, err) {
  console.error(`  ✗ ${label}: ${err?.message ?? err}`)
  failed++
}

// ── 1. Instantiation ─────────────────────────────────────────────────────────

console.log('\n[1] Instantiation')
let client
try {
  client = new ImbraceClient({ apiKey: API_KEY || 'placeholder', gateway: BASE_URL, organizationId: ORG_ID })
  ok('ImbraceClient created')
} catch (e) {
  fail('ImbraceClient created', e)
  process.exit(1)
}

// ── 2. Resource surface ───────────────────────────────────────────────────────

console.log('\n[2] Resource surface')
const expected = [
  'auth', 'account', 'organizations', 'teams', 'settings',
  'channel', 'contacts', 'conversations', 'messages',
  'workflows', 'boards', 'ips', 'ai', 'marketplace',
  'agent', 'campaign', 'outbound', 'license', 'health',
  'sessions', 'schedule', 'platform',
]
for (const r of expected) {
  client[r] ? ok(`client.${r}`) : fail(`client.${r}`, 'undefined')
}

// ── 3. Live API calls (skipped if no key) ────────────────────────────────────

if (!API_KEY) {
  console.log('\n[3] Live API calls — SKIPPED (set IMBRACE_API_KEY in tests/local/.env)')
} else {
  console.log(`\n[3] Live API calls  (gateway: ${BASE_URL})`)

  const checks = [
    ['health.check()',                 () => client.health.check()],
    ['account.getAccount()',           () => client.account.getAccount()],
    ['channel.list()',                 () => client.channel.list()],
    ['contacts.list({ limit: 1 })',    () => client.contacts.list({ limit: 1 })],
    ['teams.list()',                   () => client.teams.list()],
    ['conversations.getViewsCount()',  () => client.conversations.getViewsCount()],
    ['boards.list()',                  () => client.boards.list()],
    ['agent.list()',                   () => client.agent.list()],
  ]

  for (const [label, fn] of checks) {
    try {
      const res = await fn()
      ok(`${label}  →  ${JSON.stringify(res).slice(0, 60)}`)
    } catch (e) {
      fail(label, e)
    }
  }
}

// ── Summary ───────────────────────────────────────────────────────────────────

console.log(`\n${'─'.repeat(50)}`)
console.log(`  ${passed} passed  |  ${failed} failed`)
if (failed > 0) process.exit(1)
