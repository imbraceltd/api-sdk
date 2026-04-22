/**
 * Campaign resource comprehensive test — runs against prodv2 gateway.
 * Usage: node test-campaign.mjs
 */

import { readFileSync } from "fs";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";

const __dir = dirname(fileURLToPath(import.meta.url));

try {
  const env = readFileSync(resolve(__dir, ".env"), "utf8");
  for (const line of env.split("\n")) {
    const [k, ...v] = line.trim().split("=");
    if (k && !k.startsWith("#") && !(k in process.env)) {
      process.env[k] = v.join("=");
    }
  }
} catch (e) {}

import { ImbraceClient } from "@imbrace/sdk";

const ACCESS_TOKEN =
  process.env.IMBRACE_ACCESS_TOKEN ||
  "acc_c8c27f3b-e147-4735-b641-61e8d3706692";
const GATEWAY =
  process.env.IMBRACE_GATEWAY_URL || "https://app-gatewayv2.imbrace.co";
const ORG_ID =
  process.env.IMBRACE_ORGANIZATION_ID ||
  "org_8d2a2d53-20ef-4c54-8aa9-aadec5963b5c";

console.log(`\nStarting Campaign Test (Gateway: ${GATEWAY})`);

const client = new ImbraceClient({
  accessToken: ACCESS_TOKEN,
  gateway: GATEWAY,
});
const campaign = client.campaign;

let passed = 0,
  failed = 0,
  skipped = 0;

function ok(label, detail = "") {
  console.log(
    `  ✓ ${label}${detail ? `  →  ${String(detail).slice(0, 120)}` : ""}`,
  );
  passed++;
}

function fail(label, err) {
  console.error(`  ✗ ${label}: ${err?.message ?? JSON.stringify(err)}`);
  failed++;
}

function skip(label, reason) {
  console.log(`  - ${label}  (skipped: ${reason})`);
  skipped++;
}

let createdCampaignId = null;
let createdTouchpointId = null;

// ─────────────────────────────────────────────────────────────────────────────
// Interaction Chain
// ─────────────────────────────────────────────────────────────────────────────

console.log("\n[1] List campaigns");
try {
  const res = await campaign.list();
  const list = res.data ?? [];
  ok("list()", `${list.length} campaigns`);
} catch (e) {
  fail("list()", e);
}

console.log("\n[2] Create campaign");
try {
  const res = await campaign.create({
    name: "SDK Test Campaign — " + Date.now(),
    channel_type: "whatsapp",
  });
  createdCampaignId = res._id ?? res.id;
  ok("create()", `id=${createdCampaignId}`);
} catch (e) {
  fail("create()", e);
}

console.log("\n[3] Get campaign");
if (!createdCampaignId) {
  skip("get()", "no campaign created");
} else {
  try {
    const res = await campaign.get(createdCampaignId);
    ok("get()", `id=${res._id ?? res.id} name=${res.name}`);
  } catch (e) {
    fail("get()", e);
  }
}

console.log("\n[4] Create touchpoint");
if (!createdCampaignId) {
  skip("createTouchpoint()", "no campaign created");
} else {
  try {
    const res = await campaign.createTouchpoint({
      name: "SDK Test Touchpoint",
      campaign_id: createdCampaignId,
      type: "message",
      message: "Hello from SDK Test",
    });
    createdTouchpointId = res._id ?? res.id;
    ok("createTouchpoint()", `id=${createdTouchpointId}`);
  } catch (e) {
    fail("createTouchpoint()", e);
  }
}

console.log("\n[5] Cleanup");

if (createdTouchpointId) {
  try {
    await campaign.deleteTouchpoint(createdTouchpointId);
    ok("deleteTouchpoint()", createdTouchpointId);
  } catch (e) {
    fail("deleteTouchpoint()", e);
  }
}

if (createdCampaignId) {
  try {
    await campaign.delete(createdCampaignId);
    ok("delete() campaign", createdCampaignId);
  } catch (e) {
    fail("delete()", e);
  }
}

// ─────────────────────────────────────────────────────────────────────────────

console.log(`\n${"─".repeat(55)}`);
console.log(`  ${passed} passed  |  ${failed} failed  |  ${skipped} skipped`);
if (failed > 0) process.exit(1);
