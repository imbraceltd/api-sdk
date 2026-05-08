import { readFileSync } from "fs"
const har = JSON.parse(readFileSync("d:/HUANGJUNFENG/IMBrace/sdk/webapp.sandbox.imbrace.co.har", "utf-8"))
const entries = har.log.entries

const skipExt = /\.(js|css|png|jpg|jpeg|svg|woff2?|ttf|map|html|ico|webp|gif)(\?|$)/
const api = entries.filter(e => {
  let u; try { u = new URL(e.request.url) } catch { return false }
  if (skipExt.test(u.pathname)) return false
  if (!u.pathname.startsWith("/api/") && !u.pathname.startsWith("/v") && !u.pathname.startsWith("/data-board")) return false
  return true
})

console.log(`Total entries: ${entries.length}, API: ${api.length}\n`)

// Group by method
const byMethod = {}
for (const e of api) {
  byMethod[e.request.method] = (byMethod[e.request.method] || 0) + 1
}
console.log("By method:", byMethod)

// All MUTATIONS with body
console.log("\n=== ALL MUTATIONS (POST/PUT/PATCH/DELETE) — IN TIME ORDER ===")
const muts = api.filter(e => ["POST", "PUT", "PATCH", "DELETE"].includes(e.request.method))
console.log(`Count: ${muts.length}\n`)

for (const e of muts) {
  const u = new URL(e.request.url)
  const ct = (e.request.headers || []).find(h => h.name.toLowerCase() === "content-type")?.value || ""
  console.log(`\n● ${e.request.method} ${u.pathname}`)
  console.log(`    [${e.response.status}]  content-type: ${ct.slice(0, 80)}`)
  const reqBody = e.request.postData?.text || ""
  if (reqBody) {
    console.log(`    REQ:  ${reqBody.slice(0, 600).replace(/\n/g, " ")}${reqBody.length > 600 ? `  (+${reqBody.length - 600})` : ""}`)
  } else if (ct.includes("multipart")) {
    const params = e.request.postData?.params || []
    console.log(`    MULTIPART: ${params.map(p => `${p.name}(${p.fileName ? "file=" + p.fileName : "text"})`).join(", ")}`)
  }
  const resBody = e.response?.content?.text || ""
  if (resBody && e.response.status >= 200 && e.response.status < 400) {
    console.log(`    RES:  ${resBody.slice(0, 200).replace(/\n/g, " ")}`)
  }
}

// Unique read endpoints (GET)
console.log("\n\n=== UNIQUE GET ENDPOINTS (read-only) ===")
const seen = new Set()
for (const e of api.filter(x => x.request.method === "GET")) {
  const u = new URL(e.request.url)
  const norm = u.pathname
    .replace(/[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}/g, "{uuid}")
    .replace(/[a-f0-9]{24}/g, "{oid}")
    .replace(/(?:org|u|ch|brd|bi|conv|msg|bu|fol|fi|cat|uc|wf)_[a-z0-9_-]{6,}/gi, "{prefixId}")
  if (seen.has(norm)) continue
  seen.add(norm)
  console.log(`  [${e.response.status}] GET    ${norm}`)
}
