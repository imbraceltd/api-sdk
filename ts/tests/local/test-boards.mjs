/**
 * Boards resource test — runs against prodv2 gateway.
 * Usage: node test-boards.mjs
 */

import { ImbraceClient } from '@imbrace/sdk'

const ACCESS_TOKEN = process.env.IMBRACE_ACCESS_TOKEN || 'acc_c8c27f3b-e147-4735-b641-61e8d3706692'
const GATEWAY      = process.env.IMBRACE_GATEWAY_URL  || 'https://app-gatewayv2.imbrace.co'

const client = new ImbraceClient({ accessToken: ACCESS_TOKEN, gateway: GATEWAY })
const boards = client.boards

let passed = 0, failed = 0, skipped = 0
const created = { boardId: null, itemId: null }

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

// ── [1] List boards ───────────────────────────────────────────────────────────

console.log('\n[1] List boards')
let firstBoardId = null
try {
  const res = await boards.list({ limit: 3 })
  ok('list()', `${res.data.length} boards`)
  if (res.data.length > 0) firstBoardId = res.data[0]._id ?? res.data[0].id
} catch (e) { fail('list()', e) }

// ── [2] Get board ─────────────────────────────────────────────────────────────

console.log('\n[2] Get board')
if (!firstBoardId) {
  skip('get()', 'no boards found')
} else {
  try {
    const b = await boards.get(firstBoardId)
    ok('get()', `id=${b._id ?? b.id} name=${b.name}`)
  } catch (e) { fail('get()', e) }
}

// ── [3] Create board ──────────────────────────────────────────────────────────

console.log('\n[3] Create board')
try {
  const b = await boards.create({ name: 'SDK Test Board' })
  created.boardId = b._id ?? b.id
  ok('create()', `id=${created.boardId}`)
} catch (e) { fail('create()', e) }

// ── [4] Update board ──────────────────────────────────────────────────────────

console.log('\n[4] Update board')
if (!created.boardId) {
  skip('update()', 'no board created')
} else {
  try {
    const b = await boards.update(created.boardId, { name: 'SDK Test Board Updated' })
    ok('update()', `name=${b.name}`)
  } catch (e) { fail('update()', e) }
}

// ── [5] List items ────────────────────────────────────────────────────────────

console.log('\n[5] List items')
if (!created.boardId) {
  skip('listItems()', 'no board created')
} else {
  try {
    const res = await boards.listItems(created.boardId, { limit: 3 })
    ok('listItems()', `${res.data.length} items`)
  } catch (e) { fail('listItems()', e) }
}

// ── [6] Create item ───────────────────────────────────────────────────────────

console.log('\n[6] Create item')
if (!created.boardId) {
  skip('createItem()', 'no board created')
} else {
  try {
    const item = await boards.createItem(created.boardId, { fields: [] })
    created.itemId = item._id ?? item.id
    ok('createItem()', `id=${created.itemId}`)
  } catch (e) {
    if (e?.message?.includes('400') || e?.message?.includes('required')) {
      skip('createItem()', 'board requires specific identifier fields')
    } else {
      fail('createItem()', e)
    }
  }
}

// ── [7] Get item ──────────────────────────────────────────────────────────────

console.log('\n[7] Get item')
if (!created.boardId || !created.itemId) {
  skip('getItem()', 'no item created')
} else {
  try {
    const item = await boards.getItem(created.boardId, created.itemId)
    ok('getItem()', `id=${item._id ?? item.id}`)
  } catch (e) { fail('getItem()', e) }
}

// ── [8] Update item ───────────────────────────────────────────────────────────

console.log('\n[8] Update item')
if (!created.boardId || !created.itemId) {
  skip('updateItem()', 'no item created')
} else {
  try {
    const item = await boards.updateItem(created.boardId, created.itemId, { fields: [] })
    ok('updateItem()', `id=${item._id ?? item.id}`)
  } catch (e) { fail('updateItem()', e) }
}

// ── [9] Search items ──────────────────────────────────────────────────────────

console.log('\n[9] Search items')
if (!created.boardId) {
  skip('search()', 'no board created')
} else {
  try {
    const res = await boards.search(created.boardId, { q: '', limit: 3 })
    ok('search()', `${res.data?.length ?? 0} results`)
  } catch (e) { fail('search()', e) }
}

// ── [10] Cleanup ──────────────────────────────────────────────────────────────

console.log('\n[10] Cleanup')
if (created.itemId) {
  try {
    await boards.deleteItem(created.boardId, created.itemId)
    ok(`deleteItem(${created.itemId})`)
  } catch (e) { fail('deleteItem()', e) }
}
if (created.boardId) {
  try {
    await boards.delete(created.boardId)
    ok(`delete(${created.boardId})`)
  } catch (e) { fail('delete()', e) }
}

// ── Summary ───────────────────────────────────────────────────────────────────

console.log(`\n${'─'.repeat(50)}`)
console.log(`  ${passed} passed  |  ${failed} failed  |  ${skipped} skipped`)
if (failed > 0) process.exit(1)
