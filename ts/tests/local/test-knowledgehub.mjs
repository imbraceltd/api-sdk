/**
 * KnowledgeHub resource test — runs against prodv2 gateway (data-board service).
 * Usage: node test-knowledgehub.mjs
 *
 * Routes through {gw}/data-board/folders and {gw}/data-board/files
 *
 * Notes:
 *  - data-board wraps all responses in { success, message, data } — SDK unwraps .data
 *  - createFolder requires organization_id, parent_folder_id, source_type (required by DB schema)
 *  - getFolder response is { data: { folder, files } } — SDK unwraps to data.folder
 *  - createFile requires actual file metadata (key, file_size, file_type) — use uploadFile instead
 *  - deleteFolders body uses { ids: [...] }
 */

import { ImbraceClient } from '@imbrace/sdk'

const ACCESS_TOKEN = process.env.IMBRACE_ACCESS_TOKEN || 'acc_c8c27f3b-e147-4735-b641-61e8d3706692'
const GATEWAY      = process.env.IMBRACE_GATEWAY_URL  || 'https://app-gatewayv2.imbrace.co'

const client = new ImbraceClient({ accessToken: ACCESS_TOKEN, baseUrl: GATEWAY })
const boards = client.boards

let passed = 0, failed = 0, skipped = 0
const created = {
  organizationId: null,
  folderId: null,
  subFolderId: null,
  existingFileId: null,   // from searchFiles on existing folder
  existingFolderId: null, // existing folder for file tests
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

// ── [1] Search folders ────────────────────────────────────────────────────────

console.log('\n[1] Search folders')
try {
  const list = await boards.searchFolders({})
  const folders = Array.isArray(list) ? list : (list.data ?? [])
  if (folders.length > 0) {
    created.organizationId = folders[0].organization_id ?? null
    created.existingFolderId = folders[0]._id ?? folders[0].id
  }
  ok('searchFolders()', `${folders.length} folders  org=${created.organizationId}`)
} catch (e) { fail('searchFolders()', e) }

// ── [2] Create folder ─────────────────────────────────────────────────────────

console.log('\n[2] Create folder')
if (!created.organizationId) {
  skip('createFolder()', 'no organization_id from searchFolders')
} else {
  try {
    const folder = await boards.createFolder({
      name: 'SDK Test Folder',
      organization_id: created.organizationId,
      parent_folder_id: 'root',
      source_type: 'upload',
    })
    created.folderId = folder._id ?? folder.id
    ok('createFolder()', `id=${created.folderId}`)
  } catch (e) { fail('createFolder()', e) }
}

// ── [3] Get folder ────────────────────────────────────────────────────────────

console.log('\n[3] Get folder')
if (!created.folderId) {
  skip('getFolder()', 'no folder created')
} else {
  try {
    const folder = await boards.getFolder(created.folderId)
    ok('getFolder()', `id=${folder._id ?? folder.id} name=${folder.name}`)
  } catch (e) { fail('getFolder()', e) }
}

// ── [4] Folder contents ───────────────────────────────────────────────────────

console.log('\n[4] Folder contents')
if (!created.folderId) {
  skip('getFolderContents()', 'no folder created')
} else {
  try {
    const contents = await boards.getFolderContents(created.folderId)
    ok('getFolderContents()', `files=${contents.files?.length ?? 0} subfolders=${contents.subfolders?.length ?? 0}`)
  } catch (e) { fail('getFolderContents()', e) }
}

// ── [5] Update folder ─────────────────────────────────────────────────────────

console.log('\n[5] Update folder')
if (!created.folderId) {
  skip('updateFolder()', 'no folder created')
} else {
  try {
    const folder = await boards.updateFolder(created.folderId, { name: 'SDK Test Folder Updated' })
    ok('updateFolder()', `name=${folder.name}`)
  } catch (e) { fail('updateFolder()', e) }
}

// ── [6] Create sub-folder ─────────────────────────────────────────────────────

console.log('\n[6] Create sub-folder')
if (!created.folderId || !created.organizationId) {
  skip('createFolder() sub', 'no parent folder created')
} else {
  try {
    const sub = await boards.createFolder({
      name: 'SDK Test Sub-Folder',
      organization_id: created.organizationId,
      parent_folder_id: created.folderId,
      source_type: 'upload',
    })
    created.subFolderId = sub._id ?? sub.id
    ok('createFolder() sub', `id=${created.subFolderId}`)
  } catch (e) { fail('createFolder() sub', e) }
}

// ── [7] Search files in existing folder ──────────────────────────────────────

console.log('\n[7] Search files')
if (!created.existingFolderId) {
  skip('searchFiles()', 'no existing folder from search')
} else {
  try {
    const list = await boards.searchFiles({ folderId: created.existingFolderId })
    const files = Array.isArray(list) ? list : (list.data ?? [])
    if (files.length > 0) created.existingFileId = files[0]._id ?? files[0].id
    ok('searchFiles()', `${files.length} files`)
  } catch (e) { fail('searchFiles()', e) }
}

// ── [8] Get file ──────────────────────────────────────────────────────────────

console.log('\n[8] Get file')
if (!created.existingFileId) {
  skip('getFile()', 'no file from searchFiles')
} else {
  try {
    const file = await boards.getFile(created.existingFileId)
    ok('getFile()', `id=${file._id ?? file.id} name=${file.name}`)
  } catch (e) { fail('getFile()', e) }
}

// ── [9] Cleanup folders ───────────────────────────────────────────────────────

console.log('\n[9] Cleanup folders')
const foldersToDelete = [created.subFolderId, created.folderId].filter(Boolean)
if (foldersToDelete.length === 0) {
  skip('deleteFolders()', 'no folders created')
} else {
  try {
    const res = await boards.deleteFolders({ ids: foldersToDelete })
    ok('deleteFolders()', JSON.stringify(res).slice(0, 80))
    created.folderId = null
    created.subFolderId = null
  } catch (e) { fail('deleteFolders()', e) }
}

// ── Summary ───────────────────────────────────────────────────────────────────

console.log(`\n${'─'.repeat(50)}`)
console.log(`  ${passed} passed  |  ${failed} failed  |  ${skipped} skipped`)
if (failed > 0) process.exit(1)
