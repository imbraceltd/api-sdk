/**
 * Marketplace resource test — runs against prodv2 gateway.
 * Usage: node test-marketplace.mjs
 */

import { ImbraceClient } from '@imbrace/sdk'

const ACCESS_TOKEN = process.env.IMBRACE_ACCESS_TOKEN || 'acc_c8c27f3b-e147-4735-b641-61e8d3706692'
const GATEWAY      = process.env.IMBRACE_GATEWAY_URL  || 'https://app-gatewayv2.imbrace.co'

const client = new ImbraceClient({ accessToken: ACCESS_TOKEN, gateway: GATEWAY })
const marketplace = client.marketplace

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

// ── [1] List use case templates ───────────────────────────────────────────────

console.log('\n[1] Use case templates')
try {
  const res = await marketplace.listUseCaseTemplates()
  const list = Array.isArray(res) ? res : (res.data ?? [])
  ok('listUseCaseTemplates()', `${list.length} templates`)
} catch (e) { fail('listUseCaseTemplates()', e) }

// ── [2] List products ─────────────────────────────────────────────────────────

console.log('\n[2] Products')
let firstProductId = null
try {
  const res = await marketplace.listProducts({ limit: 3 })
  const list = Array.isArray(res) ? res : (res.data ?? [])
  ok('listProducts()', `${list.length} products`)
  if (list.length > 0) firstProductId = list[0]._id ?? list[0].id
} catch (e) { fail('listProducts()', e) }

// ── [3] Get product ───────────────────────────────────────────────────────────

console.log('\n[3] Get product')
if (!firstProductId) {
  skip('getProduct()', 'no products found')
} else {
  try {
    const p = await marketplace.getProduct(firstProductId)
    ok('getProduct()', `id=${p._id ?? p.id} name=${p.name}`)
  } catch (e) { fail('getProduct()', e) }
}

// ── [4] List orders ───────────────────────────────────────────────────────────

console.log('\n[4] Orders')
let firstOrderId = null
try {
  const res = await marketplace.listOrders({ limit: 3 })
  const list = Array.isArray(res) ? res : (res.data ?? [])
  ok('listOrders()', `${list.length} orders`)
  if (list.length > 0) firstOrderId = list[0]._id ?? list[0].id
} catch (e) {
  if (e?.message?.includes('404')) skip('listOrders()', 'orders route not available on this env')
  else fail('listOrders()', e)
}

// ── [5] Get order ─────────────────────────────────────────────────────────────

console.log('\n[5] Get order')
if (!firstOrderId) {
  skip('getOrder()', 'no orders found')
} else {
  try {
    const o = await marketplace.getOrder(firstOrderId)
    ok('getOrder()', `id=${o._id ?? o.id}`)
  } catch (e) { fail('getOrder()', e) }
}

// ── [6] List email templates ──────────────────────────────────────────────────

console.log('\n[6] Email templates')
try {
  const res = await marketplace.listEmailTemplates()
  const list = Array.isArray(res) ? res : (res.data ?? [])
  ok('listEmailTemplates()', `${list.length} templates`)
} catch (e) {
  if (e?.message?.includes('400') || e?.message?.includes('404')) skip('listEmailTemplates()', 'requires org context or route unavailable')
  else fail('listEmailTemplates()', e)
}

// ── [7] List categories ───────────────────────────────────────────────────────

console.log('\n[7] Categories')
try {
  const res = await marketplace.listCategories()
  const list = Array.isArray(res) ? res : (res.data ?? [])
  ok('listCategories()', `${list.length} categories`)
} catch (e) {
  if (e?.message?.includes('404')) skip('listCategories()', 'categories route not available on this env')
  else fail('listCategories()', e)
}

// ── Summary ───────────────────────────────────────────────────────────────────

console.log(`\n${'─'.repeat(50)}`)
console.log(`  ${passed} passed  |  ${failed} failed  |  ${skipped} skipped`)
if (failed > 0) process.exit(1)
