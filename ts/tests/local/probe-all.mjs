/**
 * Comprehensive read-only probe across every SDK module.
 *
 * Usage:
 *   AUTH_MODE=api-key      node probe-all.mjs
 *   AUTH_MODE=access-token node probe-all.mjs
 *
 * Reads tests/local/.env for IMBRACE_GATEWAY_URL, IMBRACE_API_KEY,
 * IMBRACE_ACCESS_TOKEN, IMBRACE_ORGANIZATION_ID.
 */

import { readFileSync, writeFileSync } from "fs";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";

const __dir = dirname(fileURLToPath(import.meta.url));
try {
  const env = readFileSync(resolve(__dir, ".env"), "utf8");
  for (const line of env.split("\n")) {
    const [k, ...v] = line.trim().split("=");
    if (k && !k.startsWith("#") && !(k in process.env)) process.env[k] = v.join("=");
  }
} catch {}

import { ImbraceClient } from "@imbrace/sdk";

const BASE_URL = process.env.IMBRACE_GATEWAY_URL || "https://app-gatewayv2.imbrace.co";
const API_KEY = process.env.IMBRACE_API_KEY || "";
const ACCESS_TOKEN = process.env.IMBRACE_ACCESS_TOKEN || "";
const ORG_ID = process.env.IMBRACE_ORGANIZATION_ID || "";
const MODE = (process.env.AUTH_MODE || "api-key").toLowerCase();

if (MODE !== "api-key" && MODE !== "access-token") {
  console.error(`Invalid AUTH_MODE: ${MODE}. Use api-key or access-token`);
  process.exit(1);
}

const useApiKey = MODE === "api-key";
const client = new ImbraceClient({
  baseUrl: BASE_URL,
  apiKey: useApiKey ? API_KEY : undefined,
  accessToken: useApiKey ? undefined : ACCESS_TOKEN,
  organizationId: ORG_ID,
  timeout: 6000,
});

console.log("════════════════════════════════════════════════════════════");
console.log(`  IMBRACE SDK PROBE — ${MODE.toUpperCase()} mode`);
console.log(`  Target: ${BASE_URL}`);
console.log(`  Org:    ${ORG_ID}`);
console.log("════════════════════════════════════════════════════════════");

const results = []; // { module, method, status, error, code }

async function probe(mod, method, fn) {
  const start = Date.now();
  try {
    const res = await Promise.race([
      fn(),
      new Promise((_, rej) => setTimeout(() => rej(new Error("probe-timeout-4s")), 4000)),
    ]);
    const ms = Date.now() - start;
    results.push({ module: mod, method, status: "PASS", ms });
    console.log(`  \x1b[32m✓\x1b[0m ${mod}.${method}  (${ms}ms)`);
    return res;
  } catch (e) {
    const ms = Date.now() - start;
    const code = e?.statusCode || e?.status || (e?.message?.match(/\b(\d{3})\b/)?.[1]) || "ERR";
    const msg = (e?.message || String(e)).split("\n")[0].slice(0, 200);
    results.push({ module: mod, method, status: "FAIL", code, error: msg, ms });
    console.log(`  \x1b[31m✗\x1b[0m ${mod}.${method}  [${code}]  ${msg}`);
    return null;
  }
}

function section(name) {
  console.log(`\n── ${name} ──`);
}

// ── Health / License / Account ────────────────────────────────────────

section("health");
await probe("health", "check", () => client.health.check());

section("license");
await probe("license", "get", () => client.license.get());

section("account");
await probe("account", "getAccount", () => client.account.getAccount());

// ── Auth ──────────────────────────────────────────────────────────────

section("auth");
await probe("auth", "getLoginProviders", () => client.auth.getLoginProviders());

// ── Categories ────────────────────────────────────────────────────────

section("categories");
await probe("categories", "list", () => client.categories.list(ORG_ID));

// ── Channel-service group ─────────────────────────────────────────────

section("channel");
await probe("channel", "list", () => client.channel.list({}));
await probe("channel", "getCount", () => client.channel.getCount());
await probe("channel", "getConvCount", () => client.channel.getConvCount({}));
await probe("channel", "listAssignableTeams", () => client.channel.listAssignableTeams());

section("contacts");
await probe("contacts", "list", () => client.contacts.list({ limit: 1 }));
await probe("contacts", "search", () => client.contacts.search({ limit: 1 }));
await probe("contacts", "listNotifications", () => client.contacts.listNotifications({ limit: 1 }));

section("conversations");
await probe("conversations", "list", () => client.conversations.list({ limit: 1 }));
await probe("conversations", "getViewsCount", () => client.conversations.getViewsCount({}));
await probe("conversations", "getOutstanding", () => client.conversations.getOutstanding({ limit: 1 }));

section("messages");
await probe("messages", "list", () => client.messages.list({ limit: 1 }));

section("campaign");
await probe("campaign", "list", () => client.campaign.list({}));
await probe("campaign", "listTouchpoints", () => client.campaign.listTouchpoints({}));

section("settings");
await probe("settings", "listMessageTemplates", () => client.settings.listMessageTemplates({}));
await probe("settings", "listMessageTemplatesV2", () => client.settings.listMessageTemplatesV2({}));
await probe("settings", "listWhatsAppTemplates", () => client.settings.listWhatsAppTemplates({}));
await probe("settings", "listUsers", () => client.settings.listUsers({}));   // platform-routed
await probe("settings", "getUserRolesCount", () => client.settings.getUserRolesCount()); // platform

// ── Platform group (expected fail on prodv2) ──────────────────────────

section("platform");
await probe("platform", "getMe", () => client.platform.getMe());
await probe("platform", "listUsers", () => client.platform.listUsers({}));
await probe("platform", "listOrgs", () => client.platform.listOrgs({}));
await probe("platform", "listTeams", () => client.platform.listTeams({}));
await probe("platform", "getMyTeams", () => client.platform.getMyTeams());
await probe("platform", "listApps", () => client.platform.listApps());
await probe("platform", "listResources", () => client.platform.listResources());
await probe("platform", "getMenuSettings", () => client.platform.getMenuSettings());
await probe("platform", "listBusinessUnits", () => client.platform.listBusinessUnits({}));
await probe("platform", "listRooms", () => client.platform.listRooms({}));
await probe("platform", "listStores", () => client.platform.listStores());
await probe("platform", "listN8nWorkflows", () => client.platform.listN8nWorkflows({}));
await probe("platform", "listKnowledge", () => client.platform.listKnowledge());
await probe("platform", "listCredentials", () => client.platform.listCredentials());

section("organizations");
await probe("organizations", "list", () => client.organizations.list({}));
await probe("organizations", "listAll", () => client.organizations.listAll({}));

section("teams");
await probe("teams", "list", () => client.teams.list({}));
await probe("teams", "listMy", () => client.teams.listMy());

// ── Boards / Workflows ────────────────────────────────────────────────

section("boards");
await probe("boards", "list", () => client.boards.list({}));
await probe("boards", "searchFolders", () => client.boards.searchFolders({}));
await probe("boards", "searchFiles", () => client.boards.searchFiles({}));

section("workflows");
await probe("workflows", "listChannelAutomation", () => client.workflows.listChannelAutomation({}));

// ── IPS / Schedule ────────────────────────────────────────────────────

section("ips");
await probe("ips", "getMyProfile", () => client.ips.getMyProfile());
await probe("ips", "listSchedulers", () => client.ips.listSchedulers({}));
await probe("ips", "listWorkflows", () => client.ips.listWorkflows({}));
await probe("ips", "listApWorkflows", () => client.ips.listApWorkflows({}));
await probe("ips", "listExternalDataSync", () => client.ips.listExternalDataSync());

section("schedule");
await probe("schedule", "list", () => client.schedule.list({}));

// ── AI / Chat-AI / AI-Agent / Activepieces ────────────────────────────

section("ai");
await probe("ai", "listAiAgents", () => client.ai.listAiAgents());
await probe("ai", "listAgents", () => client.ai.listAgents());
await probe("ai", "listProviders", () => client.ai.listProviders());
await probe("ai", "listGuardrails", () => client.ai.listGuardrails());
await probe("ai", "listGuardrailProviders", () => client.ai.listGuardrailProviders());
await probe("ai", "getLlmModels", () => client.ai.getLlmModels());
await probe("ai", "listRagFiles", () => client.ai.listRagFiles());
await probe("ai", "listAiAgentsV2", () => client.ai.listAiAgentsV2());

section("chatAi");
await probe("chatAi", "listDocumentModels", () => client.chatAi.listDocumentModels());
await probe("chatAi", "listAiAgents", () => client.chatAi.listAiAgents());
await probe("chatAi", "listAiAgentSubAgents", () => client.chatAi.listAiAgentSubAgents());

section("aiAgent");
await probe("aiAgent", "getHealth", () => client.aiAgent.getHealth());
await probe("aiAgent", "getVersion", () => client.aiAgent.getVersion());
await probe("aiAgent", "getConfig", () => client.aiAgent.getConfig());
await probe("aiAgent", "listChats", () => client.aiAgent.listChats({ organization_id: ORG_ID }));
await probe("aiAgent", "listClientChats", () => client.aiAgent.listClientChats({}));
await probe("aiAgent", "listEmbeddingFiles", () => client.aiAgent.listEmbeddingFiles({}));
await probe("aiAgent", "getTraceServices", () => client.aiAgent.getTraceServices());
await probe("aiAgent", "listAdminGuides", () => client.aiAgent.listAdminGuides());

// documentAi: no list method (only getFile/getReport which require IDs); skipped

// ── Marketplace / Agent ───────────────────────────────────────────────

section("marketplace");
await probe("marketplace", "listProducts", () => client.marketplace.listProducts({}));
await probe("marketplace", "listOrders", () => client.marketplace.listOrders({}));
await probe("marketplace", "listEmailTemplates", () => client.marketplace.listEmailTemplates({}));
await probe("marketplace", "listCategories", () => client.marketplace.listCategories({}));
await probe("marketplace", "listUseCaseTemplates", () => client.marketplace.listUseCaseTemplates());

section("agent");
await probe("agent", "list", () => client.agent.list());
await probe("agent", "listUseCases", () => client.agent.listUseCases());

// ── File-service ──────────────────────────────────────────────────────

section("fileService");
await probe("fileService", "listFiles", () => client.fileService.listFiles());

// ── Sessions ──────────────────────────────────────────────────────────

section("sessions");
await probe("sessions", "list", () => client.sessions.list({ limit: 1 }));

// ── Skipped (POST-only / write-only / dangerous): predict, message-suggestion, outbound

console.log("\n  [skipped] predict, message-suggestion, outbound — POST-only / write-only");

// ── Summary ───────────────────────────────────────────────────────────

const passed = results.filter(r => r.status === "PASS").length;
const failed = results.filter(r => r.status === "FAIL").length;
const total = results.length;

console.log("\n════════════════════════════════════════════════════════════");
console.log(`  RESULT: ${passed}/${total} passed, ${failed} failed (${MODE})`);
console.log("════════════════════════════════════════════════════════════");

const byModule = {};
for (const r of results) {
  if (!byModule[r.module]) byModule[r.module] = { pass: 0, fail: 0 };
  byModule[r.module][r.status === "PASS" ? "pass" : "fail"]++;
}

console.log("\nPer-module:");
for (const [mod, c] of Object.entries(byModule)) {
  const flag = c.fail === 0 ? "\x1b[32m✓\x1b[0m" : c.pass === 0 ? "\x1b[31m✗\x1b[0m" : "\x1b[33m~\x1b[0m";
  console.log(`  ${flag} ${mod.padEnd(20)} ${c.pass} pass / ${c.fail} fail`);
}

if (failed > 0) {
  console.log("\nFailures:");
  for (const r of results.filter(r => r.status === "FAIL")) {
    console.log(`  ✗ ${r.module}.${r.method}  [${r.code}]  ${r.error}`);
  }
}

const reportPath = resolve(__dir, `probe-report-${MODE}.json`);
writeFileSync(reportPath, JSON.stringify({ mode: MODE, baseUrl: BASE_URL, results, summary: { passed, failed, total } }, null, 2));
console.log(`\nFull report: ${reportPath}`);
