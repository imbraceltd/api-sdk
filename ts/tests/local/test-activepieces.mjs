/**
 * Full ActivePieces resource test — runs against prodv2 gateway.
 * Usage: node test-activepieces.mjs
 */

import { ImbraceClient } from '@imbrace/sdk'

const client = new ImbraceClient({
  accessToken: process.env.IMBRACE_ACCESS_TOKEN || 'acc_c8c27f3b-e147-4735-b641-61e8d3706692',
  gateway: process.env.IMBRACE_GATEWAY_URL || 'https://app-gatewayv2.imbrace.co',
})

const ap = client.activepieces

let passed = 0
let failed = 0
let skipped = 0

// track created resources for cleanup
const created = { flowId: null, folderId: null, connectionId: null, invitationId: null }

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

// ── Flows ────────────────────────────────────────────────────────────────────

console.log('\n[1] Flows')
try {
  const res = await ap.listFlows({ limit: 3 })
  ok('listFlows()', `${res.data.length} flows, next=${res.next}`)

  if (res.data.length > 0) {
    const flow = await ap.getFlow(res.data[0].id)
    ok('getFlow()', `id=${flow.id} status=${flow.status}`)
  } else {
    skip('getFlow()', 'no flows available')
  }
} catch (e) { fail('Flows', e) }

// ── Create Flow ──────────────────────────────────────────────────────────────

console.log('\n[2] Create Flow')
try {
  // Need a projectId — get it from existing flow
  const flows = await ap.listFlows({ limit: 1 })
  const projectId = flows.data[0]?.projectId
  if (!projectId) throw new Error('No projectId available from existing flows')

  const flow = await ap.createFlow({ displayName: 'SDK Test Flow', projectId })
  created.flowId = flow.id
  ok('createFlow()', `id=${flow.id} name=${flow.version?.displayName}`)
} catch (e) { fail('createFlow()', e) }

// ── Trigger Flow ──────────────────────────────────────────────────────────────

console.log('\n[3] Trigger Flow (webhook)')
try {
  const flows = await ap.listFlows({ limit: 3 })
  const enabledFlow = flows.data.find(f => f.status === 'ENABLED')
  if (!enabledFlow) {
    skip('triggerFlow()', 'no ENABLED flow found')
  } else {
    const res = await ap.triggerFlow(enabledFlow.id, { test: true, source: 'sdk-test' })
    ok('triggerFlow()', `response=${JSON.stringify(res).slice(0, 60)}`)
  }
} catch (e) { fail('triggerFlow()', e) }

// ── Flow Runs ────────────────────────────────────────────────────────────────

console.log('\n[4] Flow Runs')
try {
  const res = await ap.listRuns({ limit: 3 })
  ok('listRuns()', `${res.data.length} runs`)

  if (res.data.length > 0) {
    const run = await ap.getRun(res.data[0].id)
    ok('getRun()', `id=${run.id} status=${run.status}`)
  } else {
    skip('getRun()', 'no runs available')
  }
} catch (e) { fail('Flow Runs', e) }

// ── Folders ───────────────────────────────────────────────────────────────────

console.log('\n[5] Folders')
try {
  const flows = await ap.listFlows({ limit: 1 })
  const projectId = flows.data[0]?.projectId
  if (!projectId) throw new Error('No projectId available')

  const list = await ap.listFolders({ limit: 3 })
  ok('listFolders()', `${list.data.length} folders`)

  const folder = await ap.createFolder({ displayName: 'SDK Test Folder', projectId })
  created.folderId = folder.id
  ok('createFolder()', `id=${folder.id}`)

  const updated = await ap.updateFolder(folder.id, { displayName: 'SDK Test Folder Updated' })
  ok('updateFolder()', `name=${updated.displayName}`)

  const fetched = await ap.getFolder(folder.id)
  ok('getFolder()', `id=${fetched.id}`)
} catch (e) { fail('Folders', e) }

// ── App Connections ───────────────────────────────────────────────────────────

console.log('\n[6] App Connections')
try {
  const res = await ap.listConnections({ limit: 3 })
  ok('listConnections()', `${res.data.length} connections`)

  if (res.data.length > 0) {
    const conn = await ap.getConnection(res.data[0].id)
    ok('getConnection()', `id=${conn.id} piece=${conn.pieceName}`)
  } else {
    skip('getConnection()', 'no connections available')
  }
} catch (e) { fail('App Connections', e) }

// ── Pieces ────────────────────────────────────────────────────────────────────

console.log('\n[7] Pieces')
try {
  const res = await ap.listPieces({ limit: 5 })
  ok('listPieces()', `${res.length} pieces, first=${res[0]?.displayName}`)
} catch (e) { fail('listPieces()', e) }

// ── Triggers ──────────────────────────────────────────────────────────────────

console.log('\n[8] Triggers')
try {
  const res = await ap.getTriggerRunStatus()
  const pieceCount = Object.keys(res.pieces ?? {}).length
  ok('getTriggerRunStatus()', `${pieceCount} pieces tracked`)
} catch (e) { fail('getTriggerRunStatus()', e) }

// ── Tables & Records ──────────────────────────────────────────────────────────

console.log('\n[9] Tables & Records')
try {
  const tables = await ap.listTables({ limit: 3 })
  ok('listTables()', `${tables.data.length} tables`)

  if (tables.data.length > 0) {
    const table = await ap.getTable(tables.data[0].id)
    ok('getTable()', `id=${table.id}`)

    const records = await ap.listRecords({ tableId: table.id, limit: 3 })
    ok('listRecords()', `${records.data.length} records`)
  } else {
    skip('getTable() / listRecords()', 'no tables available')
  }
} catch (e) { fail('Tables & Records', e) }

// ── MCP Servers ───────────────────────────────────────────────────────────────

console.log('\n[10] MCP Servers')
try {
  const flows = await ap.listFlows({ limit: 1 })
  const projectId = flows.data[0]?.projectId
  if (!projectId) throw new Error('No projectId available')

  const res = await ap.listMcpServers(projectId)
  ok('listMcpServers()', `${res.data.length} MCP servers`)

  if (res.data.length > 0) {
    const server = await ap.getMcpServer(res.data[0].id)
    ok('getMcpServer()', `id=${server.id}`)
  } else {
    skip('getMcpServer()', 'no MCP servers available')
  }
} catch (e) { fail('MCP Servers', e) }

// ── User Invitations ──────────────────────────────────────────────────────────

console.log('\n[11] User Invitations')
try {
  const res = await ap.listInvitations({ type: 'PLATFORM', limit: 3 })
  ok('listInvitations(type=PLATFORM)', `${res.data.length} invitations`)
} catch (e) { fail('listInvitations()', e) }

try {
  const res = await ap.listInvitations({ type: 'PROJECT', limit: 3 })
  ok('listInvitations(type=PROJECT)', `${res.data.length} invitations`)
} catch (e) { fail('listInvitations(type=PROJECT)', e) }

// ── Cleanup ───────────────────────────────────────────────────────────────────

console.log('\n[12] Cleanup')
if (created.folderId) {
  try {
    await ap.deleteFolder(created.folderId)
    ok(`deleteFolder(${created.folderId})`)
  } catch (e) { fail('deleteFolder()', e) }
}
if (created.flowId) {
  try {
    await ap.deleteFlow(created.flowId)
    ok(`deleteFlow(${created.flowId})`)
  } catch (e) { fail('deleteFlow()', e) }
}

// ── Summary ───────────────────────────────────────────────────────────────────

console.log(`\n${'─'.repeat(55)}`)
console.log(`  ${passed} passed  |  ${failed} failed  |  ${skipped} skipped`)
if (failed > 0) process.exit(1)
