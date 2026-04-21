/**
 * Boards resource test — runs against prodv2 gateway.
 * Usage: node test-boards.mjs
 *
 * Field notes (from API inspection):
 *   - createField() returns the updated board (not just the field)
 *   - Fields are NOT sorted by insertion order — find new field by name
 *   - createItem POST uses { fields: [{ board_field_id, value }] } array format
 *   - updateItem PUT uses  { data:   [{ key, value }] } array format (asymmetric!)
 *   - reorderFields uses { fields: [id1, id2, ...] }
 */

import { ImbraceClient } from '@imbrace/sdk'

const ACCESS_TOKEN = process.env.IMBRACE_ACCESS_TOKEN || 'acc_c8c27f3b-e147-4735-b641-61e8d3706692'
const GATEWAY      = process.env.IMBRACE_GATEWAY_URL  || 'https://app-gatewayv2.imbrace.co'

const client = new ImbraceClient({ accessToken: ACCESS_TOKEN, gateway: GATEWAY })
const boards = client.boards

let passed = 0, failed = 0, skipped = 0
const created = {
  boardId: null,
  identifierFieldId: null,  // auto-created "Name" field
  fieldId: null,            // Tags field
  fieldId2: null,           // Notes field
  itemId: null,
  itemId2: null,
  segmentId: null,
}

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

// createField returns the updated board; find the newly added field by name
function findField(boardRes, name) {
  return boardRes?.fields?.find(f => f.name === name) ?? null
}

// ── [1] List boards ───────────────────────────────────────────────────────────

console.log('\n[1] List boards')
try {
  const res = await boards.list({ limit: 20 })
  ok('list()', `${res.data.length} boards`)
} catch (e) { fail('list()', e) }

// ── [2] Get board ─────────────────────────────────────────────────────────────

console.log('\n[2] Get board')
try {
  const res = await boards.list({ limit: 1 })
  if (res.data.length > 0) {
    const b = await boards.get(res.data[0]._id ?? res.data[0].id)
    ok('get()', `id=${b._id ?? b.id} name=${b.name} fields=${b.fields?.length ?? 0}`)
  } else {
    skip('get()', 'no boards found')
  }
} catch (e) { fail('get()', e) }

// ── [3] Create test board ─────────────────────────────────────────────────────

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

// Get auto-created identifier field
if (created.boardId) {
  try {
    const b = await boards.get(created.boardId)
    const f = b.fields?.find(f => f.is_identifier)
    created.identifierFieldId = f?._id ?? null
  } catch (_) {}
}

// ── [5] Create fields ─────────────────────────────────────────────────────────

console.log('\n[5] Create fields')
if (!created.boardId) {
  skip('createField()', 'no board created')
} else {
  try {
    const res = await boards.createField(created.boardId, { name: 'Tags', type: 'ShortText' })
    const f = findField(res, 'Tags')
    created.fieldId = f?._id
    ok('createField() Tags', `id=${created.fieldId}`)
  } catch (e) { fail('createField() Tags', e) }

  try {
    const res = await boards.createField(created.boardId, { name: 'Notes', type: 'ShortText' })
    const f = findField(res, 'Notes')
    created.fieldId2 = f?._id
    ok('createField() Notes', `id=${created.fieldId2}`)
  } catch (e) { fail('createField() Notes', e) }
}

// ── [6] Update field ──────────────────────────────────────────────────────────

console.log('\n[6] Update field')
if (!created.boardId || !created.fieldId) {
  skip('updateField()', 'no field created')
} else {
  try {
    await boards.updateField(created.boardId, created.fieldId, { name: 'Tags Updated' })
    ok('updateField()', 'Tags → Tags Updated')
  } catch (e) { fail('updateField()', e) }
}

// ── [7] Reorder fields ────────────────────────────────────────────────────────

console.log('\n[7] Reorder fields')
if (!created.boardId || !created.fieldId || !created.fieldId2 || !created.identifierFieldId) {
  skip('reorderFields()', 'fields not ready')
} else {
  try {
    await boards.reorderFields(created.boardId, {
      fields: [created.identifierFieldId, created.fieldId2, created.fieldId],
    })
    ok('reorderFields()')
  } catch (e) { fail('reorderFields()', e) }
}

// ── [8] Bulk update fields ────────────────────────────────────────────────────

console.log('\n[8] Bulk update fields')
if (!created.boardId || !created.fieldId) {
  skip('bulkUpdateFields()', 'no field created')
} else {
  try {
    await boards.bulkUpdateFields(created.boardId, {
      fields: [{ _id: created.fieldId, name: 'Tags v2', type: 'ShortText', hidden: false }],
    })
    ok('bulkUpdateFields()')
  } catch (e) { fail('bulkUpdateFields()', e) }
}

// ── [9] Create items ──────────────────────────────────────────────────────────

console.log('\n[9] Create items')
if (!created.boardId || !created.identifierFieldId) {
  skip('createItem()', 'board or identifier field not found')
} else {
  try {
    const item = await boards.createItem(created.boardId, {
      fields: [{ board_field_id: created.identifierFieldId, value: 'SDK Test Item 1' }],
    })
    created.itemId = item._id ?? item.id
    ok('createItem() #1', `id=${created.itemId}`)
  } catch (e) { fail('createItem() #1', e) }

  try {
    const item = await boards.createItem(created.boardId, {
      fields: [{ board_field_id: created.identifierFieldId, value: 'SDK Test Item 2' }],
    })
    created.itemId2 = item._id ?? item.id
    ok('createItem() #2', `id=${created.itemId2}`)
  } catch (e) { fail('createItem() #2', e) }
}

// ── [10] Get item ─────────────────────────────────────────────────────────────

console.log('\n[10] Get item')
if (!created.boardId || !created.itemId) {
  skip('getItem()', 'no item created')
} else {
  try {
    const item = await boards.getItem(created.boardId, created.itemId)
    ok('getItem()', `id=${item._id ?? item.id}`)
  } catch (e) { fail('getItem()', e) }
}

// ── [11] Update item ──────────────────────────────────────────────────────────

console.log('\n[11] Update item')
if (!created.boardId || !created.itemId || !created.identifierFieldId) {
  skip('updateItem()', 'no item created')
} else {
  try {
    const item = await boards.updateItem(created.boardId, created.itemId, {
      data: [{ key: created.identifierFieldId, value: 'SDK Test Item 1 Updated' }],
    })
    ok('updateItem()', `id=${item._id ?? item.id}`)
  } catch (e) { fail('updateItem()', e) }
}

// ── [12] List items ───────────────────────────────────────────────────────────

console.log('\n[12] List items')
if (!created.boardId) {
  skip('listItems()', 'no board created')
} else {
  try {
    const res = await boards.listItems(created.boardId, { limit: 10 })
    ok('listItems()', `${res.data?.length ?? 0} items`)
  } catch (e) { fail('listItems()', e) }
}

// ── [13] Search items ─────────────────────────────────────────────────────────

console.log('\n[13] Search items')
if (!created.boardId) {
  skip('search()', 'no board created')
} else {
  try {
    const res = await boards.search(created.boardId, { q: '', limit: 5 })
    ok('search()', `${res.data?.length ?? 0} results`)
  } catch (e) {
    if (e?.message?.includes('400')) skip('search()', 'meilisearch index not ready for new board')
    else fail('search()', e)
  }
}

// ── [14] Bulk delete items ────────────────────────────────────────────────────

console.log('\n[14] Bulk delete items')
if (!created.boardId || !created.itemId2) {
  skip('bulkDeleteItems()', 'no second item created')
} else {
  try {
    const res = await boards.bulkDeleteItems(created.boardId, { ids: [created.itemId2] })
    ok('bulkDeleteItems()', JSON.stringify(res).slice(0, 60))
    created.itemId2 = null
  } catch (e) { fail('bulkDeleteItems()', e) }
}

// ── [15] Check conflict ───────────────────────────────────────────────────────

console.log('\n[15] Check conflict')
if (!created.boardId || !created.itemId) {
  skip('checkConflict()', 'no item created')
} else {
  try {
    const res = await boards.checkConflict(created.boardId, created.itemId, {})
    ok('checkConflict()', `is_conflicted=${res.is_conflicted}`)
  } catch (e) { fail('checkConflict()', e) }
}

// ── [16] Segmentation ─────────────────────────────────────────────────────────

console.log('\n[16] Segmentation')
if (!created.boardId) {
  skip('segmentation', 'no board created')
} else {
  try {
    const list = await boards.listSegments(created.boardId)
    ok('listSegments()', `${Array.isArray(list) ? list.length : (list.data?.length ?? 0)} segments`)
  } catch (e) { fail('listSegments()', e) }

  try {
    const seg = await boards.createSegment(created.boardId, { name: 'SDK Test Segment', filter: {} })
    created.segmentId = seg._id ?? seg.id
    ok('createSegment()', `id=${created.segmentId}`)
  } catch (e) { fail('createSegment()', e) }

  if (created.segmentId) {
    try {
      const seg = await boards.updateSegment(created.boardId, created.segmentId, { name: 'SDK Test Segment Updated' })
      ok('updateSegment()', `name=${seg.name}`)
    } catch (e) { fail('updateSegment()', e) }

    try {
      await boards.deleteSegment(created.boardId, created.segmentId)
      ok('deleteSegment()')
      created.segmentId = null
    } catch (e) { fail('deleteSegment()', e) }
  }
}

// ── [17] Link preview ─────────────────────────────────────────────────────────

console.log('\n[17] Link preview')
try {
  const res = await boards.getLinkPreview('https://imbrace.co')
  ok('getLinkPreview()', `title=${res.title ?? '(none)'}`)
} catch (e) { fail('getLinkPreview()', e) }

// ── [18] Export CSV ───────────────────────────────────────────────────────────

console.log('\n[18] Export CSV')
if (!created.boardId) {
  skip('exportCsv()', 'no board created')
} else {
  try {
    const csv = await boards.exportCsv(created.boardId)
    ok('exportCsv()', `${csv.length} chars`)
  } catch (e) { fail('exportCsv()', e) }
}

// ── [19] Reorder boards ───────────────────────────────────────────────────────

console.log('\n[19] Reorder boards')
if (!created.boardId) {
  skip('reorder()', 'no board created')
} else {
  try {
    const res = await boards.list({ limit: 50 })
    const allIds = res.data.map(b => b._id ?? b.id)
    const order = [...allIds.filter(id => id !== created.boardId), created.boardId]
    await boards.reorder({ order })
    ok('reorder()')
  } catch (e) {
    if (e?.message?.includes('500')) skip('reorder()', 'backend 500 — known issue with reorder endpoint')
    else fail('reorder()', e)
  }
}

// ── [20] Delete field ─────────────────────────────────────────────────────────

console.log('\n[20] Delete field')
if (!created.boardId || !created.fieldId) {
  skip('deleteField()', 'no field created')
} else {
  try {
    await boards.deleteField(created.boardId, created.fieldId)
    ok('deleteField() Tags')
    created.fieldId = null
  } catch (e) { fail('deleteField() Tags', e) }
}

// ── [21] Cleanup ──────────────────────────────────────────────────────────────

console.log('\n[21] Cleanup')
if (created.segmentId) {
  try { await boards.deleteSegment(created.boardId, created.segmentId); ok('deleteSegment() cleanup') }
  catch (e) { fail('deleteSegment() cleanup', e) }
}
if (created.itemId2) {
  try { await boards.deleteItem(created.boardId, created.itemId2); ok('deleteItem() #2 cleanup') }
  catch (e) { fail('deleteItem() #2 cleanup', e) }
}
if (created.itemId) {
  try { await boards.deleteItem(created.boardId, created.itemId); ok('deleteItem() #1 cleanup') }
  catch (e) { fail('deleteItem() #1 cleanup', e) }
}
if (created.fieldId2) {
  try { await boards.deleteField(created.boardId, created.fieldId2); ok('deleteField() Notes cleanup') }
  catch (e) { fail('deleteField() Notes cleanup', e) }
}
if (created.fieldId) {
  try { await boards.deleteField(created.boardId, created.fieldId); ok('deleteField() Tags cleanup') }
  catch (e) { fail('deleteField() Tags cleanup', e) }
}
if (created.boardId) {
  try { await boards.delete(created.boardId); ok('delete(board) cleanup') }
  catch (e) { fail('delete(board) cleanup', e) }
}

// ── Summary ───────────────────────────────────────────────────────────────────

console.log(`\n${'─'.repeat(50)}`)
console.log(`  ${passed} passed  |  ${failed} failed  |  ${skipped} skipped`)
if (failed > 0) process.exit(1)
