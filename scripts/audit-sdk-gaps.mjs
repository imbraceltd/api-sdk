#!/usr/bin/env node
/**
 * SDK Gap Audit Tool — detailed report
 *
 * Compares endpoints used by the new-frontend webapp against endpoints
 * exposed by the iMBRACE TypeScript SDK, and reports gaps per feature area
 * with file:line, export name, and a suggested SDK method name for each gap.
 *
 * Usage:
 *   node scripts/audit-sdk-gaps.mjs                  # default report
 *   node scripts/audit-sdk-gaps.mjs --area=ai        # filter to one area
 *   node scripts/audit-sdk-gaps.mjs --verbose        # also list SDK endpoints
 *   node scripts/audit-sdk-gaps.mjs --md             # markdown export
 *   node scripts/audit-sdk-gaps.mjs --json           # machine-readable
 *   node scripts/audit-sdk-gaps.mjs --md > gaps.md   # save to file
 *
 * Sources:
 *   - Frontend: d:/HUANGJUNFENG/new-frontend/src/services/api/*.ts
 *   - SDK:      d:/HUANGJUNFENG/IMBrace/sdk/ts/src/resources/*.ts
 */
import { readFileSync, existsSync } from "fs"
import { join, basename } from "path"

const FRONTEND_DIR = "d:/HUANGJUNFENG/new-frontend/src/services/api"
const SDK_DIR      = "d:/HUANGJUNFENG/IMBrace/sdk/ts/src/resources"

// ── Feature areas: map UI files → SDK files ─────────────────────────────────
const AREAS = {
  "AI Agent": {
    frontend: ["ai-assistant.ts", "ai.ts", "guard-rail.ts"],
    sdk:      ["ai.ts", "chat-ai.ts", "ai-agent.ts", "document-ai.ts", "financial-documents.ts", "templates.ts"],
    sdkResource: "ai / chatAi / aiAgent / documentAi",
  },
  "Data Board": {
    frontend: ["boardAutomation.ts", "dataAnalytics.ts", "crm.ts"],
    sdk:      ["boards.ts", "data_files.ts"],
    sdkResource: "boards",
  },
  "Workflow": {
    frontend: ["apWorkflow.ts", "workflow.ts"],
    sdk:      ["workflows.ts"],
    sdkResource: "workflows",
  },
  "Knowledge / Files": {
    frontend: ["knowledgeBase.ts", "knowledgeHub.ts"],
    sdk:      ["chat-ai.ts", "ai.ts", "file-service.ts"],
    sdkResource: "chatAi / fileService",
  },
  "Marketplace / Templates": {
    frontend: ["marketplace.ts", "messageTemplates.ts", "app.ts"],
    sdk:      ["marketplace.ts", "templates.ts", "agent.ts"],
    sdkResource: "marketplace / templates / agent",
  },
  "Channel / Messaging": {
    frontend: ["channel.ts", "contact.ts", "messages.ts", "campaign.ts", "outbound.ts"],
    sdk:      ["channel.ts", "contacts.ts", "messages.ts", "campaign.ts", "outbound.ts", "categories.ts"],
    sdkResource: "channel / contacts / messages / campaign / outbound / categories",
  },
}

// ── Path normalization ──────────────────────────────────────────────────────
function normalizePath(p) {
  return p
    .replace(/^\/api\//, "/")
    .replace(/\$\{[^}]+\}/g, "{ID}")
    .replace(/:[a-zA-Z_]+/g, "{ID}")
    .replace(/[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}/g, "{ID}")
    .replace(/[a-f0-9]{24}/g, "{ID}")
    .replace(/(?:org|u|ch|brd|bi|conv|msg|bu|fol|fi|cat|uc|wf)_[a-z0-9_-]{6,}/gi, "{ID}")
    .replace(/\?.*$/, "")
    .replace(/\/+/g, "/")
    .replace(/\/$/, "")
}

function lineOfOffset(src, offset) {
  return src.slice(0, offset).split("\n").length
}

// ── Frontend extractor with file:line + export name ─────────────────────────
// Strategy: find each `api:` occurrence, then look BEFORE for export/const name
// and look AROUND for `method: fetchMethod.X`.
function extractFrontendEndpoints(filePath) {
  if (!existsSync(filePath)) return []
  const src = readFileSync(filePath, "utf-8")
  const fileName = basename(filePath)
  const out = []

  // Match: api: <value>, ... method: fetchMethod.X
  // Or:    method: fetchMethod.X, ... api: <value>
  // <value> can be string literal OR arrow fn returning template literal.
  // Allow backtick-strings and ${...} interpolations inside the value.
  const order1 = /\bapi:\s*((?:`[^`]*`|[^,])+?)\s*,\s*method:\s*fetchMethod\.(\w+)/gs
  const order2 = /\bmethod:\s*fetchMethod\.(\w+)\s*,\s*api:\s*((?:`[^`]*`|[^,])+?)\s*[,}]/gs

  const collected = new Set()
  for (const re of [order1, order2]) {
    let m
    while ((m = re.exec(src)) !== null) {
      const isOrder1 = re === order1
      const apiExpr = (isOrder1 ? m[1] : m[2]).trim()
      const method  = isOrder1 ? m[2] : m[1]
      const offset  = m.index
      const path = extractPathFromExpr(apiExpr)
      if (!path) continue

      // Look BEFORE for export name
      const before = src.slice(0, offset)
      const exportMatch = [...before.matchAll(/(?:export\s+const|const)\s+(\w+)\s*=\s*\{/g)].pop()
      const exportName = exportMatch ? exportMatch[1] : "<anon>"
      const startOffset = exportMatch ? exportMatch.index : offset

      const key = `${method} ${normalizePath(path)} ${exportName}`
      if (collected.has(key)) continue
      collected.add(key)

      out.push({
        method,
        path: normalizePath(path),
        raw: path,
        file: fileName,
        line: lineOfOffset(src, startOffset),
        exportName,
      })
    }
  }
  return dedupe(out)
}

function extractPathFromExpr(expr) {
  const literal = expr.match(/^['"]([^'"]+)['"]/)
  if (literal) return literal[1]
  const tpl = expr.match(/`([^`]+)`/)
  if (tpl) return tpl[1]
  return null
}

// ── SDK extractor with file:line + method name ──────────────────────────────
const STANDARD_PREFIXES = {
  "this.base":             "",
  "this.aiBase":           "/v3/ai",
  "this.gateway":          "",
  "this.backend":          "/v1/backend",
  "this.platform":         "/platform",
  "this.channelService":   "/channel-service",
  "this.channel_service":  "/channel-service",
  "this.dataBoard":        "/data-board",
  "this.data_board":       "/data-board",
  "this.ips":              "/ips/v1",
  "this.aiAgent":          "/ai-agent",
  "this.ai_agent":         "/ai-agent",
  "this.workflowEngine":   "/activepieces",
  "this.workflow_engine":  "/activepieces",
  "this.apBase":           "/activepieces",
  "this.ap_base":          "/activepieces",
  "this.marketplaces":     "/v2/backend/marketplaces",
  "this.fileService":      "/v1/backend/file-service",
  "this.file_service":     "/v1/backend/file-service",
  "this.messageSuggestion":"/v1/message-suggestion",
  "this.message_suggestion":"/v1/message-suggestion",
  "this.predict":          "/predict",
  "this.ai":               "",
}

function buildSdkSubstitutions(src) {
  const subs = { ...STANDARD_PREFIXES }
  const getterRe = /private\s+get\s+(\w+)\s*\(\)\s*\{\s*return\s+`([^`]+)`/g
  let m
  while ((m = getterRe.exec(src)) !== null) {
    subs[`this.${m[1]}`] = m[2]
  }
  for (let i = 0; i < 3; i++) {
    for (const [k, v] of Object.entries(subs)) {
      subs[k] = v.replace(/\$\{([^}]+)\}/g, (_, ref) => {
        const trimmed = ref.trim().replace(/\.replace\([^)]+\)/g, "")
        return subs[trimmed] !== undefined ? subs[trimmed] : `\${${ref}}`
      })
    }
  }
  return subs
}

function applySubstitutions(tpl, subs) {
  let out = tpl
  for (let i = 0; i < 3; i++) {
    out = out.replace(/\$\{([^}]+)\}/g, (_, ref) => {
      const trimmed = ref.trim().replace(/\.replace\([^)]+\)/g, "")
      if (subs[trimmed] !== undefined) return subs[trimmed]
      return "{ID}"
    })
  }
  return out
}

// Find the enclosing async/sync method name for a given offset
function findEnclosingMethod(src, offset) {
  const before = src.slice(0, offset)
  const methodRe = /(?:async\s+)?(\w+)\s*(?:<[^>]*>)?\s*\([^)]*\)[^{]*\{/g
  let lastMatch = null
  let m
  while ((m = methodRe.exec(before)) !== null) {
    if (["if", "for", "while", "switch", "catch", "function", "return", "throw"].includes(m[1])) continue
    lastMatch = m[1]
  }
  return lastMatch || "<unknown>"
}

function extractSdkEndpoints(filePath) {
  if (!existsSync(filePath)) return []
  const src = readFileSync(filePath, "utf-8")
  const subs = buildSdkSubstitutions(src)
  const fileName = basename(filePath)
  const out = []

  function add(rawPath, method, offset) {
    const path = normalizePath(applySubstitutions(rawPath, subs))
    out.push({
      method, path, raw: rawPath,
      file: fileName,
      line: lineOfOffset(src, offset),
      methodName: findEnclosingMethod(src, offset),
    })
  }

  let m

  // getFetch()(`...`, { method: "X" })
  const re = /getFetch\(\)\s*\(\s*(?:`([^`]+)`|([\w.]+))\s*(?:,\s*\{[^}]*?method:\s*["'](\w+)["'][^}]*\})?/g
  while ((m = re.exec(src)) !== null) {
    if (m[1]) add(m[1], m[3] || "GET", m.index)
  }

  // new URL(`...`) … getFetch(url, { method: "X" })
  const urlBlockRe = /new URL\(`([^`]+)`\)[\s\S]{0,400}?getFetch\(\)\s*\([^,]+,\s*\{[^}]*?method:\s*["'](\w+)["']/g
  while ((m = urlBlockRe.exec(src)) !== null) {
    add(m[1], m[2], m.index)
  }

  // new URL(`...`) without explicit method → GET
  const urlOnlyRe = /new URL\(`([^`]+)`\)/g
  while ((m = urlOnlyRe.exec(src)) !== null) {
    const path = normalizePath(applySubstitutions(m[1], subs))
    if (!out.some(e => e.path === path)) {
      add(m[1], "GET", m.index)
    }
  }

  // Python-style: self._http.request("METHOD", f"...")
  const pyRe = /\.request\(\s*["'](\w+)["'],\s*f["']([^"']+)["']/g
  while ((m = pyRe.exec(src)) !== null) {
    add(m[2], m[1], m.index)
  }

  // Helper-wrapped: this.apFetch(this.apUrl('/path'), { method: 'X' })
  const helperRe = /apUrl\(\s*[`'"]([^`'"]+)[`'"][^)]*\)\s*(?:,\s*\{[^}]*?method:\s*["'](\w+)["'][^}]*\})?/g
  while ((m = helperRe.exec(src)) !== null) {
    add(m[1], m[2] || "GET", m.index)
  }

  return dedupe(out)
}

function dedupe(arr) {
  const seen = new Set()
  return arr.filter(e => {
    const k = `${e.method} ${e.path}`
    if (seen.has(k)) return false
    seen.add(k)
    return true
  })
}

// ── Suggest SDK method name from frontend export or path ────────────────────
function suggestMethodName(ep) {
  // Heuristic 1: derive from export name (most reliable)
  if (ep.exportName) {
    // postEmailTemplateCategory → createEmailTemplateCategory
    // getN8nWorkflow → getN8nWorkflow
    // putApWorkflowFlow → updateApWorkflowFlow
    let name = ep.exportName
      .replace(/^post/, "create")
      .replace(/^put/, "update")
      .replace(/^patch/, "update")
      .replace(/^delete/, "delete")
      .replace(/^get/, "get")
    return name
  }
  // Heuristic 2: derive from path + method
  const verb = { GET: "get", POST: "create", PUT: "update", PATCH: "update", DELETE: "delete" }[ep.method] || "call"
  const tail = ep.path.split("/").filter(p => p && p !== "{ID}").pop() || "thing"
  return `${verb}${tail.charAt(0).toUpperCase() + tail.slice(1).replace(/[-_]/g, "")}`
}

// ── Compare ─────────────────────────────────────────────────────────────────
function diffEndpoints(frontend, sdk) {
  const sdkSet = new Set(sdk.map(e => `${e.method} ${e.path}`))
  const missing = []
  const covered = []
  for (const fe of frontend) {
    const k = `${fe.method} ${fe.path}`
    if (sdkSet.has(k)) covered.push(fe)
    else missing.push(fe)
  }
  // For each missing, attach suggested method name
  for (const m of missing) m.suggestedMethod = suggestMethodName(m)
  return { covered, missing }
}

function groupByCategory(endpoints) {
  const groups = {}
  for (const e of endpoints) {
    const parts = e.path.split("/").filter(Boolean)
    const cat = inferCategory(parts)
    if (!groups[cat]) groups[cat] = []
    groups[cat].push(e)
  }
  // Sort each group by method then path
  const order = ["GET", "POST", "PATCH", "PUT", "DELETE"]
  for (const k of Object.keys(groups)) {
    groups[k].sort((a, b) => {
      const d = order.indexOf(a.method) - order.indexOf(b.method)
      return d !== 0 ? d : a.path.localeCompare(b.path)
    })
  }
  return groups
}

function inferCategory(parts) {
  if (parts.includes("n8n")) return "n8n / workflow editor"
  if (parts.includes("credentials") || parts.includes("oauth1-credential") || parts.includes("oauth2-credential")) return "Credentials / OAuth"
  if (parts.includes("crmboard")) return "Board Automation (legacy CRM)"
  if (parts.includes("workflowlist")) return "Board Automation"
  if (parts.includes("templates")) return "Use Case Templates"
  if (parts.includes("analysis")) return "Data Analytics"
  if (parts.includes("files")) return "File Management"
  if (parts.includes("assistants") || parts.includes("assistant_apps")) return "Assistants"
  if (parts.includes("guardrail")) return "Guardrails"
  if (parts.includes("providers")) return "AI Providers"
  if (parts.includes("knowledge")) return "Knowledge Base"
  if (parts.includes("channels")) return "Channels"
  if (parts.includes("contacts") || parts.includes("contact")) return "Contacts"
  if (parts.includes("flows") || parts.includes("flow-runs")) return "Flows / Runs"
  return parts.slice(0, 2).join("/")
}

// ── Output: terminal ────────────────────────────────────────────────────────
function colorize(text, color) {
  const codes = { red: 31, green: 32, yellow: 33, blue: 34, cyan: 36, gray: 90, bold: 1 }
  if (process.env.NO_COLOR) return text
  return `\x1b[${codes[color] || 0}m${text}\x1b[0m`
}

function printAreaReport(area, info, opts) {
  const { frontend, sdk, covered, missing } = info
  const total = frontend.length
  const cov = covered.length
  const miss = missing.length
  const cov_pct = total > 0 ? Math.round((cov / total) * 100) : 100

  const status = miss === 0 ? colorize("✓", "green") : colorize("✗", "red")
  console.log()
  console.log(colorize("─".repeat(72), "gray"))
  console.log(`${status} ${colorize(area, "bold")}  ${cov}/${total} covered (${cov_pct}%)`)
  console.log(colorize(`  SDK resource(s): client.${AREAS[area].sdkResource}`, "gray"))
  console.log(colorize(`  Frontend: ${total} endpoints | SDK: ${sdk.length} endpoints | Missing: ${miss}`, "gray"))

  if (miss > 0) {
    console.log()
    console.log(colorize("  ❌ MISSING — endpoints UI calls but SDK doesn't expose:", "yellow"))
    const grouped = groupByCategory(missing)
    for (const [cat, eps] of Object.entries(grouped)) {
      console.log()
      console.log(colorize(`    ┌─ ${cat} (${eps.length})`, "cyan"))
      for (const e of eps) {
        const where = colorize(`${e.file}:${e.line}`, "gray")
        const exp   = colorize(e.exportName, "blue")
        const suggested = colorize(`→ client.${AREAS[area].sdkResource.split(" / ")[0]}.${e.suggestedMethod}()`, "green")
        console.log(`    │ ${e.method.padEnd(6)} ${e.path.padEnd(50)} ${where}`)
        console.log(`    │   ${colorize("UI:", "gray")} ${exp}  ${suggested}`)
      }
    }
  }

  if (opts.verbose && sdk.length > 0) {
    console.log()
    console.log(colorize("  ✅ SDK exposes:", "green"))
    const sdkGrouped = groupByCategory(sdk)
    for (const [cat, eps] of Object.entries(sdkGrouped)) {
      console.log(colorize(`    [${cat}] ${eps.length}`, "gray"))
      for (const e of eps.slice(0, 5)) {
        console.log(colorize(`      ${e.method.padEnd(6)} ${e.path}  ${e.file}:${e.line}  (${e.methodName})`, "gray"))
      }
      if (eps.length > 5) console.log(colorize(`      ... +${eps.length - 5} more`, "gray"))
    }
  }
}

// ── Output: markdown ────────────────────────────────────────────────────────
function printMarkdown(reports, totals) {
  const lines = []
  lines.push("# SDK Gap Audit Report")
  lines.push("")
  lines.push(`**Generated**: ${new Date().toISOString()}`)
  lines.push("")
  lines.push("## Summary")
  lines.push("")
  lines.push("| Area | Coverage | Frontend | SDK | Missing |")
  lines.push("|---|---|---|---|---|")
  for (const [area, info] of Object.entries(reports)) {
    const total = info.frontend.length
    const cov = info.covered.length
    const pct = total > 0 ? Math.round((cov / total) * 100) : 100
    const emoji = info.missing.length === 0 ? "✅" : pct >= 70 ? "🟡" : "🔴"
    lines.push(`| ${emoji} **${area}** | ${cov}/${total} (${pct}%) | ${total} | ${info.sdk.length} | ${info.missing.length} |`)
  }
  const overall = totals.frontend > 0 ? Math.round((totals.covered / totals.frontend) * 100) : 100
  lines.push(`| | **${totals.covered}/${totals.frontend} (${overall}%)** | **${totals.frontend}** | | **${totals.missing}** |`)
  lines.push("")

  for (const [area, info] of Object.entries(reports)) {
    if (info.missing.length === 0) continue
    lines.push(`## ${area} — ${info.missing.length} missing`)
    lines.push("")
    lines.push(`> SDK resource: \`client.${AREAS[area].sdkResource}\``)
    lines.push("")
    const grouped = groupByCategory(info.missing)
    for (const [cat, eps] of Object.entries(grouped)) {
      lines.push(`### ${cat}`)
      lines.push("")
      lines.push("| Method | Path | UI Source | Suggested SDK Method |")
      lines.push("|---|---|---|---|")
      for (const e of eps) {
        const sugRes = AREAS[area].sdkResource.split(" / ")[0]
        lines.push(`| \`${e.method}\` | \`${e.path}\` | [\`${e.exportName}\`](../new-frontend/src/services/api/${e.file}#L${e.line}) | \`client.${sugRes}.${e.suggestedMethod}()\` |`)
      }
      lines.push("")
    }
  }

  console.log(lines.join("\n"))
}

// ── Main ────────────────────────────────────────────────────────────────────
function main() {
  const args = process.argv.slice(2)
  const filterArea = args.find(a => a.startsWith("--area="))?.split("=")[1]?.toLowerCase()
  const jsonOut = args.includes("--json")
  const mdOut = args.includes("--md")
  const verbose = args.includes("--verbose") || args.includes("-v")

  if (!existsSync(FRONTEND_DIR)) {
    console.error(colorize(`Frontend dir not found: ${FRONTEND_DIR}`, "red"))
    process.exit(1)
  }

  const reports = {}
  const totals = { frontend: 0, sdk: 0, covered: 0, missing: 0 }

  for (const [area, cfg] of Object.entries(AREAS)) {
    if (filterArea && !area.toLowerCase().includes(filterArea)) continue

    const fe = []
    for (const f of cfg.frontend) {
      fe.push(...extractFrontendEndpoints(join(FRONTEND_DIR, f)))
    }
    const sdk = []
    for (const f of cfg.sdk) {
      sdk.push(...extractSdkEndpoints(join(SDK_DIR, f)))
    }
    const dedupedFe = dedupe(fe)
    const dedupedSdk = dedupe(sdk)
    const diff = diffEndpoints(dedupedFe, dedupedSdk)

    reports[area] = { frontend: dedupedFe, sdk: dedupedSdk, ...diff }
    totals.frontend += dedupedFe.length
    totals.sdk      += dedupedSdk.length
    totals.covered  += diff.covered.length
    totals.missing  += diff.missing.length
  }

  if (jsonOut) {
    console.log(JSON.stringify({ reports, totals }, null, 2))
    return
  }

  if (mdOut) {
    printMarkdown(reports, totals)
    return
  }

  // Default terminal output
  console.log()
  console.log(colorize("━".repeat(72), "gray"))
  console.log(colorize("  iMBRACE SDK Gap Audit", "bold"))
  console.log(colorize("━".repeat(72), "gray"))

  for (const [area, info] of Object.entries(reports)) {
    printAreaReport(area, info, { verbose })
  }

  // Footer summary
  console.log()
  console.log(colorize("━".repeat(72), "gray"))
  const overall = totals.frontend > 0 ? Math.round((totals.covered / totals.frontend) * 100) : 100
  console.log(colorize("Overall Summary", "bold"))
  console.log(`  Frontend endpoints: ${totals.frontend}`)
  console.log(`  SDK endpoints:      ${totals.sdk}`)
  console.log(`  Covered:            ${colorize(totals.covered, "green")}`)
  console.log(`  Missing:            ${colorize(totals.missing, totals.missing > 0 ? "red" : "green")}`)
  console.log(`  Coverage:           ${overall}%`)
  console.log()
  console.log(colorize("Flags:", "gray"))
  console.log(colorize("  --area=NAME    Filter to one area (ai, board, workflow, ...)", "gray"))
  console.log(colorize("  --verbose      Also list SDK endpoints", "gray"))
  console.log(colorize("  --md           Output markdown (pipe to file: > gaps.md)", "gray"))
  console.log(colorize("  --json         Machine-readable JSON output", "gray"))
}

main()
