/**
 * Regression tests for the 9 bug fixes in SDK v1.0.5 (commit ffb3708).
 * Auth: Access Token.
 *
 * Each section pins one fix from `fix/sdk-bugs-v1.0.5`. If a regression
 * sneaks back in, the corresponding step fails with a concrete reason
 * (not just "backend 400") so it's easy to map back to the offending fix.
 *
 *   1. documentAi.createFull  — board type "General" (not "DocumentAI"),
 *                                schemaFields added one-by-one,
 *                                workflow_name default present.
 *   2. documentAi.updateAgent — partial body auto-merges with existing.
 *   3. aiAgent.suggestFieldTypes — wire body uses `file_urls`, not `fields`.
 *   4. workflows.listMcpServers — projectId arg is optional (auto-resolves).
 *   5. boards.createField — returns BoardField (not the full Board).
 *   6. boards.updateItem — caller can pass createItem-shape `fields:[...]`.
 *   7. boards.createFolder — defaults source_type + parent_folder_id.
 *   8. workflows.listInvitations — type hint check skipped on TS
 *                                  (compile-time-enforced; runtime smoke only).
 *   9. documentAi.createFull (TS workflow_name) — sibling assertion in #1.
 *
 * Creates real resources on the org and cleans up after itself.
 */
import "dotenv/config"
import { ImbraceClient } from "@imbrace/sdk"

const accessToken    = process.env.IMBRACE_ACCESS_TOKEN
const organizationId = process.env.IMBRACE_ORGANIZATION_ID
const baseUrl        = process.env.IMBRACE_GATEWAY_URL ?? "https://app-gatewayv2.imbrace.co"
const sampleDocUrl   = process.env.IMBRACE_SAMPLE_DOC_URL ?? ""
const modelId        = process.env.IMBRACE_DOC_MODEL_ID    ?? "qwen3.5-27b"
const providerId     = process.env.IMBRACE_DOC_PROVIDER_ID ?? "c95e63ad-3c48-4b6a-8ed1-49cf8408088d"

if (!accessToken || !organizationId) {
  console.error("Missing IMBRACE_ACCESS_TOKEN or IMBRACE_ORGANIZATION_ID")
  process.exit(1)
}

const client = new ImbraceClient({ accessToken, organizationId, baseUrl, timeout: 60_000 })

let pass = 0, fail = 0, skip = 0
const fails: string[] = []
const cleanupBoardIds: string[] = []
const cleanupAgentIds: string[] = []
const cleanupFolderIds: string[] = []

async function step(label: string, fn: () => Promise<any>, expectFail = false) {
  process.stdout.write(`  • ${label} ... `)
  const t0 = Date.now()
  try {
    const result = await fn()
    const dt = Date.now() - t0
    const summary = JSON.stringify(result ?? {}).slice(0, 160)
    if (expectFail) {
      console.log(`unexpected pass [${dt}ms]: ${summary}`); fail++; fails.push(`${label} → unexpected pass`)
    } else {
      console.log(`✓ [${dt}ms] ${summary}`); pass++
    }
  } catch (err: any) {
    const detail = err?.message ?? String(err)
    if (expectFail) { console.log(`✓ (expected fail [${detail.slice(0, 200)}])`); pass++ }
    else { console.log(`✗ ${detail.slice(0, 300)}`); fail++; fails.push(`${label} → ${detail.slice(0, 300)}`) }
  }
}

function skipped(label: string, reason: string) {
  console.log(`  - ${label}  ⏭ ${reason}`); skip++
}

function section(title: string) {
  console.log(`\n══ ${title} ══`)
}

function assert(cond: any, msg: string) {
  if (!cond) throw new Error(`assertion failed: ${msg}`)
}

console.log(`\n━━━ v1.0.5 regression — auth: ACCESS TOKEN (npm @imbrace/sdk) ━━━`)
console.log(`gateway=${baseUrl}`)
console.log(`org=${organizationId}`)

const stamp = Date.now()

// ── Fix #1 + #9 — documentAi.createFull ─────────────────────────────────────
// Pre-fix: board type "DocumentAI" was rejected by backend enum + adding
// schemaFields at create-time conflicted with auto-Name field's is_identifier
// + TS was missing workflow_name default. Any of those would 400 the call.
section("Fix #1+#9: documentAi.createFull (General board, fields one-by-one, workflow_name default)")
let fullResult: any = null
await step("createFull succeeds end-to-end with 2 schemaFields", async () => {
  fullResult = await client.documentAi.createFull({
    name: `sdk-regress-docfull-${stamp}`,
    description: "regression v1.0.5 — auto-cleanup",
    instructions: "Extract invoice fields. Return JSON.",
    schemaFields: [
      { name: "invoice_number", label: "Invoice Number", type: "ShortText" },
      { name: "total",          label: "Total",          type: "Number" },
    ],
    modelId,
    providerId,
    extraAiAgent: { agent_type: "agent" } as any,
  } as any)
  if (fullResult?.board_id)    cleanupBoardIds.push(fullResult.board_id)
  if (fullResult?.ai_agent_id) cleanupAgentIds.push(fullResult.ai_agent_id)
  return { board_id: fullResult?.board_id, ai_agent_id: fullResult?.ai_agent_id, usecase_id: fullResult?.usecase_id }
})

if (fullResult?.board_id) {
  await step("created board has type='General' (not 'DocumentAI')", async () => {
    const board: any = await client.boards.get(fullResult.board_id)
    assert(board.type === "General", `expected type 'General', got '${board.type}'`)
    return { type: board.type }
  })

  await step("created board contains both schemaFields", async () => {
    const board: any = await client.boards.get(fullResult.board_id)
    const names = new Set((board.fields ?? []).map((f: any) => f.name))
    assert(names.has("invoice_number"), "missing field 'invoice_number'")
    assert(names.has("total"),          "missing field 'total'")
    return { fieldNames: [...names] }
  })
} else {
  skipped("created board has type='General'",   "createFull did not return a board_id")
  skipped("created board contains schemaFields", "createFull did not return a board_id")
}

// ── Fix #2 — documentAi.updateAgent (auto-merge partial body) ───────────────
// Pre-fix: PUT /assistant_apps/{id} is full-replacement at the backend,
// so partial body would 400 for missing required fields (name, workflow_name).
// Post-fix: SDK auto-fetches existing agent + merges body before PUT.
section("Fix #2: documentAi.updateAgent (partial body auto-merges with existing)")
let partialAgentId: string | null = null
const partialAgentName = `sdk-regress-partial-${stamp}`

await step("createAgent fixture", async () => {
  const r: any = await client.documentAi.createAgent({
    name: partialAgentName,
    instructions: "Extract any visible field. Return JSON.",
    model_id: modelId,
    provider_id: providerId,
    schema: { invoice_number: { type: "string" } },
    description: "regression fixture — pre-update",
  } as any)
  partialAgentId = r?._id ?? r?.id ?? null
  if (partialAgentId) cleanupAgentIds.push(partialAgentId)
  return { id: partialAgentId, name: r?.name }
})

if (partialAgentId) {
  await step("updateAgent with ONLY {description} succeeds (auto-merge)", async () => {
    const r: any = await client.documentAi.updateAgent(partialAgentId!, {
      description: "regression fixture — post-update",
    } as any)
    return { id: r?._id ?? r?.id, description: r?.description }
  })

  await step("post-update agent retains original name (merge preserved other fields)", async () => {
    const a: any = await client.documentAi.getAgent(partialAgentId!)
    assert(a.name === partialAgentName, `expected name '${partialAgentName}', got '${a.name}'`)
    assert(a.description === "regression fixture — post-update", `expected new description, got '${a.description}'`)
    return { name: a.name, description: a.description }
  })

  await step("updateAgent mergeMode:'replace' with partial body should fail (opt-out works)",
    () => client.documentAi.updateAgent(
      partialAgentId!,
      { description: "this body is intentionally incomplete" } as any,
      { mergeMode: "replace" },
    ),
    /* expectFail */ true,
  )
} else {
  skipped("updateAgent auto-merge tests", "createAgent fixture did not return an id")
}

// ── Fix #3 — aiAgent.suggestFieldTypes ──────────────────────────────────────
// Pre-fix: SDK sent {fields:[...]} body, backend expected {file_urls:[...]} → 400.
// Post-fix: SDK signature is suggestFieldTypes({fileUrls}) and sends file_urls.
// Compile-time the input type is now {fileUrls: string[]} — passing this file
// already proves the signature changed. Runtime check verifies wire shape too.
section("Fix #3: aiAgent.suggestFieldTypes (body uses file_urls)")
if (!sampleDocUrl) {
  skipped("suggestFieldTypes runtime call", "set IMBRACE_SAMPLE_DOC_URL to a public PDF/image to enable")
} else {
  await step("suggestFieldTypes({fileUrls}) is accepted by backend", async () => {
    const r = await client.aiAgent.suggestFieldTypes({ fileUrls: [sampleDocUrl] })
    return { type: typeof r, hasFields: !!(r && typeof r === "object") }
  })
}

// ── Fix #4 — workflows.listMcpServers (projectId optional) ──────────────────
// Pre-fix: signature was listMcpServers(projectId: string) — missing arg = TS
// compile error or backend 400 with undefined query param.
// Post-fix: arg is optional; SDK auto-resolves via resolveProjectId().
section("Fix #4: workflows.listMcpServers (projectId optional, auto-resolved)")
await step("listMcpServers() (no arg) auto-resolves projectId", async () => {
  const r: any = await client.workflows.listMcpServers()
  const data = r?.data ?? r ?? []
  return { count: Array.isArray(data) ? data.length : "non-array", shape: typeof r }
})

await step("listMcpServers() second call uses cached projectId (no error)", async () => {
  const r: any = await client.workflows.listMcpServers()
  return { type: typeof r }
})

// ── Fix #5 — boards.createField returns BoardField (not Board) ──────────────
// Pre-fix: backend returns the whole Board from POST /board/{id}/board_fields,
// SDK returned that verbatim though the type said BoardField. Caller's
// `result.name` was the BOARD name, and `result.type` was "General".
// Post-fix: SDK extracts the just-added field from board.fields[] by name.
section("Fix #5: boards.createField returns BoardField (not full Board)")
const regressBoardName = `sdk-regress-board-${stamp}`
let regressBoardId: string | null = null

await step("create regression board fixture", async () => {
  const r: any = await client.boards.create({
    name: regressBoardName, description: "regression v1.0.5", type: "General", show_id: false,
  } as any)
  regressBoardId = r?._id ?? r?.id ?? null
  if (regressBoardId) cleanupBoardIds.push(regressBoardId)
  return { id: regressBoardId, name: r?.name, type: r?.type }
})

if (regressBoardId) {
  const fieldName = `regress_field_${stamp}`
  await step("createField returns the new field, not the parent board", async () => {
    const r: any = await client.boards.createField(regressBoardId!, {
      name: fieldName, type: "ShortText",
    } as any)
    // BoardField has the field's own name; Board would have the board's name.
    assert(r?.name === fieldName,
      `expected field name '${fieldName}', got '${r?.name}' (smells like Board not BoardField)`)
    // Board returns `type: 'General'`; a ShortText field has type 'ShortText'.
    assert(r?.type !== "General",
      `result.type='General' suggests Board leaked through; expected field type`)
    // Board has a .fields[] array; a BoardField doesn't.
    assert(!Array.isArray(r?.fields),
      `result has .fields[] array — looks like the whole Board was returned`)
    return { name: r?.name, type: r?.type, id: r?._id ?? r?.id }
  })

  // ── Fix #6 — boards.updateItem auto-translates fields shape ───────────────
  // Pre-fix: SDK forwarded body verbatim. createItem uses
  // {fields:[{board_field_id,value}]} but updateItem wire requires
  // {fields:[], data:[{key,value}]} — caller had to know the asymmetry.
  // Post-fix: SDK accepts createItem-shape and auto-translates.
  section("Fix #6: boards.updateItem accepts createItem-shape fields[]")
  let idFieldId: string | null = null
  let regressItemId: string | null = null

  await step("locate identifier field on regression board", async () => {
    const board: any = await client.boards.get(regressBoardId!)
    const idF = (board.fields ?? []).find((f: any) => f.is_identifier)
    idFieldId = idF?._id ?? null
    return { idFieldId, idFieldName: idF?.name }
  })

  if (idFieldId) {
    await step("createItem fixture", async () => {
      const r: any = await client.boards.createItem(regressBoardId!, {
        fields: [{ board_field_id: idFieldId, value: "regress-initial" }],
      } as any)
      regressItemId = r?._id ?? r?.id ?? null
      return { id: regressItemId }
    })

    if (regressItemId) {
      await step("updateItem({fields:[{board_field_id,value}]}) succeeds (auto-translated to data[])", async () => {
        const r: any = await client.boards.updateItem(regressBoardId!, regressItemId!, {
          fields: [{ board_field_id: idFieldId, value: "regress-updated" }],
        } as any)
        return { id: r?._id ?? r?.id }
      })

      await step("post-update item reflects new value", async () => {
        const it: any = await client.boards.getItem(regressBoardId!, regressItemId!)
        const raw = JSON.stringify(it).toLowerCase()
        assert(raw.includes("regress-updated"),
          `item should contain 'regress-updated' after update; got ${raw.slice(0, 200)}`)
        return { ok: true }
      })

      await step("updateItem raw wire shape {fields:[], data:[...]} still passes through", async () => {
        const r: any = await client.boards.updateItem(regressBoardId!, regressItemId!, {
          fields: [],
          data: [{ key: idFieldId, value: "regress-rewire" }],
        } as any)
        return { id: r?._id ?? r?.id }
      })
    } else {
      skipped("updateItem regression checks", "createItem fixture did not return an id")
    }
  } else {
    skipped("updateItem regression checks", "no identifier field found on regression board")
  }
} else {
  skipped("createField / updateItem regression checks", "regression board fixture create failed")
}

// ── Fix #7 — boards.createFolder defaults source_type + parent_folder_id ────
// Pre-fix: omitting either field 400'd at the backend (enum / null reject).
// Post-fix: SDK auto-fills source_type:"upload" + parent_folder_id:"root".
section("Fix #7: boards.createFolder defaults source_type + parent_folder_id")
await step("createFolder({name}) only — no source_type/parent_folder_id — succeeds", async () => {
  const r: any = await client.boards.createFolder({
    name: `sdk-regress-folder-${stamp}`,
    organization_id: organizationId,
  } as any)
  const folderId = r?._id ?? r?.id ?? null
  if (folderId) cleanupFolderIds.push(folderId)
  return { id: folderId, name: r?.name }
})

// ── Fix #8 — workflows.listInvitations (Py-only Literal hint) ───────────────
// Py-only fix; TS already had the union type at compile time. We do a
// minimal runtime sanity call instead.
section("Fix #8: workflows.listInvitations (runtime smoke, hint is Py-only)")
await step("listInvitations({type:'PLATFORM'}) is accepted", async () => {
  const r: any = await client.workflows.listInvitations({ type: "PLATFORM", limit: 1 } as any)
  return { type: typeof r }
})

// ── Cleanup ─────────────────────────────────────────────────────────────────
section("Cleanup")
for (const aid of cleanupAgentIds) {
  await step(`deleteAgent(${aid})`, async () => {
    await client.documentAi.deleteAgent(aid)
    return { deleted: aid }
  })
}
for (const bid of cleanupBoardIds) {
  await step(`boards.delete(${bid})`, async () => {
    await client.boards.delete(bid)
    return { deleted: bid }
  })
}
for (const fid of cleanupFolderIds) {
  await step(`boards.deleteFolders([${fid}])`, async () => {
    await client.boards.deleteFolders({ ids: [fid] } as any)
    return { deleted: fid }
  })
}

// ── Summary ─────────────────────────────────────────────────────────────────
console.log(`\n━━━ Summary ━━━`)
console.log(`pass=${pass}  fail=${fail}  skip=${skip}`)
if (fails.length) {
  console.log("Failures:")
  for (const f of fails) console.log(`  - ${f}`)
}
process.exit(fail > 0 ? 1 : 0)
