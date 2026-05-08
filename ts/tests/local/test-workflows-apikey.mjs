/**
 * Workflows resource test — runs against prodv2 gateway.
 * Usage: node test-workflows.mjs
 *
 * Covers:
 *   - Channel automation (v2/backend/workflows/channel_automation)
 *   - Flow engine (formerly client.activepieces — flows, runs, folders,
 *     connections, pieces, tables, MCP servers, invitations).
 */

import { ImbraceClient } from '@imbrace/sdk'

const API_KEY = process.env.IMBRACE_API_KEY || 'api_7601650a-96c6-4227-91c0-f00cc258883a'
const GATEWAY      = process.env.IMBRACE_GATEWAY_URL  || 'https://app-gatewayv2.imbrace.co'

const client    = new ImbraceClient({ apiKey: API_KEY, baseUrl: GATEWAY })
const workflows = client.workflows

let passed = 0, failed = 0, skipped = 0
const created = { flowId: null, folderId: null }

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

// ── [1] Channel automation ────────────────────────────────────────────────────

console.log('\n[1] Channel automations')
try {
  const res = await workflows.listChannelAutomation()
  const list = Array.isArray(res) ? res : (res.data ?? [])
  ok('listChannelAutomation()', `${list.length} automations`)
} catch (e) { fail('listChannelAutomation()', e) }

try {
  const res = await workflows.listChannelAutomation({ channelType: 'whatsapp' })
  const list = Array.isArray(res) ? res : (res.data ?? [])
  ok('listChannelAutomation(whatsapp)', `${list.length} automations`)
} catch (e) { fail('listChannelAutomation(whatsapp)', e) }

// ── [2] Flows ─────────────────────────────────────────────────────────────────

console.log('\n[2] Flows')
try {
  const res = await workflows.listFlows({ limit: 3 })
  ok('listFlows()', `${res.data.length} flows, next=${res.next}`)

  if (res.data.length > 0) {
    const flow = await workflows.getFlow(res.data[0].id)
    ok('getFlow()', `id=${flow.id} status=${flow.status}`)
  } else {
    skip('getFlow()', 'no flows available')
  }
} catch (e) { fail('Flows', e) }

// ── [3] Create Flow ───────────────────────────────────────────────────────────

console.log('\n[3] Create Flow')
try {
  const flows = await workflows.listFlows({ limit: 1 })
  const projectId = flows.data[0]?.projectId
  if (!projectId) throw new Error('No projectId available from existing flows')

  const flow = await workflows.createFlow({ displayName: 'SDK Test Flow', projectId })
  created.flowId = flow.id
  ok('createFlow()', `id=${flow.id} name=${flow.version?.displayName}`)
} catch (e) { fail('createFlow()', e) }

// ── [4] Trigger Flow (webhook) ────────────────────────────────────────────────

console.log('\n[4] Trigger Flow (webhook)')
try {
  const flows = await workflows.listFlows({ limit: 3 })
  const enabledFlow = flows.data.find(f => f.status === 'ENABLED')
  if (!enabledFlow) {
    skip('triggerFlow()', 'no ENABLED flow found')
  } else {
    const res = await workflows.triggerFlow(enabledFlow.id, { test: true, source: 'sdk-test' })
    ok('triggerFlow()', `response=${JSON.stringify(res).slice(0, 60)}`)
  }
} catch (e) { fail('triggerFlow()', e) }

// ── [5] Flow Runs ─────────────────────────────────────────────────────────────

console.log('\n[5] Flow Runs')
try {
  const res = await workflows.listRuns({ limit: 3 })
  ok('listRuns()', `${res.data.length} runs`)

  if (res.data.length > 0) {
    const run = await workflows.getRun(res.data[0].id)
    ok('getRun()', `id=${run.id} status=${run.status}`)
  } else {
    skip('getRun()', 'no runs available')
  }
} catch (e) { fail('Flow Runs', e) }

// ── [6] Folders ───────────────────────────────────────────────────────────────

console.log('\n[6] Folders')
try {
  const flows = await workflows.listFlows({ limit: 1 })
  const projectId = flows.data[0]?.projectId
  if (!projectId) throw new Error('No projectId available')

  const list = await workflows.listFolders({ limit: 3 })
  ok('listFolders()', `${list.data.length} folders`)

  const folder = await workflows.createFolder({ displayName: 'SDK Test Folder', projectId })
  created.folderId = folder.id
  ok('createFolder()', `id=${folder.id}`)

  const updated = await workflows.updateFolder(folder.id, { displayName: 'SDK Test Folder Updated' })
  ok('updateFolder()', `name=${updated.displayName}`)

  const fetched = await workflows.getFolder(folder.id)
  ok('getFolder()', `id=${fetched.id}`)
} catch (e) { fail('Folders', e) }

// ── [7] App Connections ───────────────────────────────────────────────────────

console.log('\n[7] App Connections')
try {
  const res = await workflows.listConnections({ limit: 3 })
  ok('listConnections()', `${res.data.length} connections`)

  if (res.data.length > 0) {
    const conn = await workflows.getConnection(res.data[0].id)
    ok('getConnection()', `id=${conn.id} piece=${conn.pieceName}`)
  } else {
    skip('getConnection()', 'no connections available')
  }
} catch (e) { fail('App Connections', e) }

// ── [8] Pieces ────────────────────────────────────────────────────────────────

console.log('\n[8] Pieces')
try {
  const res = await workflows.listPieces({ limit: 5 })
  ok('listPieces()', `${res.length} pieces, first=${res[0]?.displayName}`)
} catch (e) { fail('listPieces()', e) }

// ── [9] Triggers ──────────────────────────────────────────────────────────────

console.log('\n[9] Triggers')
try {
  const res = await workflows.getTriggerRunStatus()
  const pieceCount = Object.keys(res.pieces ?? {}).length
  ok('getTriggerRunStatus()', `${pieceCount} pieces tracked`)
} catch (e) { fail('getTriggerRunStatus()', e) }

// ── [10] Tables & Records ─────────────────────────────────────────────────────

console.log('\n[10] Tables & Records')
try {
  const tables = await workflows.listTables({ limit: 3 })
  ok('listTables()', `${tables.data.length} tables`)

  if (tables.data.length > 0) {
    const table = await workflows.getTable(tables.data[0].id)
    ok('getTable()', `id=${table.id}`)

    const records = await workflows.listRecords({ tableId: table.id, limit: 3 })
    ok('listRecords()', `${records.data.length} records`)
  } else {
    skip('getTable() / listRecords()', 'no tables available')
  }
} catch (e) { fail('Tables & Records', e) }

// ── [11] MCP Servers ──────────────────────────────────────────────────────────

console.log('\n[11] MCP Servers')
try {
  const flows = await workflows.listFlows({ limit: 1 })
  const projectId = flows.data[0]?.projectId
  if (!projectId) throw new Error('No projectId available')

  const res = await workflows.listMcpServers(projectId)
  ok('listMcpServers()', `${res.data.length} MCP servers`)

  if (res.data.length > 0) {
    const server = await workflows.getMcpServer(res.data[0].id)
    ok('getMcpServer()', `id=${server.id}`)
  } else {
    skip('getMcpServer()', 'no MCP servers available')
  }
} catch (e) { fail('MCP Servers', e) }

// ── [12] User Invitations ─────────────────────────────────────────────────────

console.log('\n[12] User Invitations')
try {
  const res = await workflows.listInvitations({ type: 'PLATFORM', limit: 3 })
  ok('listInvitations(type=PLATFORM)', `${res.data.length} invitations`)
} catch (e) { fail('listInvitations(PLATFORM)', e) }

try {
  const res = await workflows.listInvitations({ type: 'PROJECT', limit: 3 })
  ok('listInvitations(type=PROJECT)', `${res.data.length} invitations`)
} catch (e) { fail('listInvitations(PROJECT)', e) }

// ── [13] Cleanup ──────────────────────────────────────────────────────────────

console.log('\n[13] Cleanup')
if (created.folderId) {
  try {
    await workflows.deleteFolder(created.folderId)
    ok(`deleteFolder(${created.folderId})`)
  } catch (e) { fail('deleteFolder()', e) }
}
if (created.flowId) {
  try {
    await workflows.deleteFlow(created.flowId)
    ok(`deleteFlow(${created.flowId})`)
  } catch (e) { fail('deleteFlow()', e) }
}

// ── Summary ───────────────────────────────────────────────────────────────────

console.log(`\n${'─'.repeat(55)}`)
console.log(`  ${passed} passed  |  ${failed} failed  |  ${skipped} skipped`)
if (failed > 0) process.exit(1)
