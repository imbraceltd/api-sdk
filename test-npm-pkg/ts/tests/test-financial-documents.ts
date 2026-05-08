import { pathToFileURL } from 'url';
import { client, runTestSection, logResult } from "../utils/utils.js";

let notDeployedCount = 0;

function reportError(label: string, e: any) {
  if (e?.name === "FinancialDocumentsNotDeployedError" || e?.message?.includes("not deployed on this gateway")) {
    notDeployedCount++;
    logResult(`${label} [NOT DEPLOYED]`, "Financial Management module unavailable on this gateway");
  } else {
    logResult(`${label} error`, e?.message?.slice(0, 100));
  }
}

async function testFinancialDocuments() {
  console.log("\n🚀 Testing Document AI Workflow (chatAi.processDocument + financialDocuments)...");

  // ─── Preflight: chatAi.processDocument — production-ready extraction ────────
  await runTestSection("PREFLIGHT chatAi.processDocument (real image)", async () => {
    const res = await client.chatAi.processDocument({
      url: "https://app-gatewayv2.imbrace.co/files/download/118615471-5b33f600-b7f3-11eb-94a1-78e635e66558.png",
      modelName: "gpt-4o",
      organizationId: process.env.IMBRACE_ORGANIZATION_ID || "",
    });
    logResult("success", res.success);
    logResult("data keys", Object.keys(res.data || {}).join(", "));
  });

  console.log("\n   ⚠️  Financial workflow methods are EXPERIMENTAL.");
  console.log("       If your gateway doesn't host the Financial Management module,");
  console.log("       calls throw FinancialDocumentsNotDeployedError.\n");

  const dummyFileId = "041b3f82-041a-44b5-bfa8-714389688d5e";
  const dummyReportId = "041b3f82-041a-44b5-bfa8-714389688d5e";

  await runTestSection("financialDocuments.getFile", async () => {
    try { await client.financialDocuments.getFile(dummyFileId); }
    catch (e) { reportError("getFile", e); }
  });
  await runTestSection("financialDocuments.getReport", async () => {
    try { await client.financialDocuments.getReport(dummyReportId); }
    catch (e) { reportError("getReport", e); }
  });
  await runTestSection("financialDocuments.listErrors", async () => {
    try { await client.financialDocuments.listErrors(dummyFileId); }
    catch (e) { reportError("listErrors", e); }
  });
  await runTestSection("financialDocuments.suggest", async () => {
    try { await client.financialDocuments.suggest({ file_id: dummyFileId }); }
    catch (e) { reportError("suggest", e); }
  });
  await runTestSection("financialDocuments.fix", async () => {
    try { await client.financialDocuments.fix({ file_id: dummyFileId }); }
    catch (e) { reportError("fix", e); }
  });
  await runTestSection("financialDocuments.reset", async () => {
    try { await client.financialDocuments.reset(); }
    catch (e) { reportError("reset", e); }
  });
  await runTestSection("financialDocuments.updateFile", async () => {
    try { await client.financialDocuments.updateFile(dummyFileId, { name: "x" }); }
    catch (e) { reportError("updateFile", e); }
  });
  await runTestSection("financialDocuments.updateReport", async () => {
    try { await client.financialDocuments.updateReport(dummyReportId, { status: "x" }); }
    catch (e) { reportError("updateReport", e); }
  });
  await runTestSection("financialDocuments.deleteFile", async () => {
    try { await client.financialDocuments.deleteFile(dummyFileId); }
    catch (e) { reportError("deleteFile", e); }
  });
  await runTestSection("financialDocuments.deleteReport", async () => {
    try { await client.financialDocuments.deleteReport(dummyReportId); }
    catch (e) { reportError("deleteReport", e); }
  });

  console.log("\n✅ Financial Documents Resource Testing Completed.");
  if (notDeployedCount > 0) {
    console.log(`   ℹ️  ${notDeployedCount}/10 financial workflow endpoints not deployed on this gateway.`);
    console.log(`       Methods throw FinancialDocumentsNotDeployedError — user can catch and handle gracefully.`);
  }
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  testFinancialDocuments().catch(console.error);
}

export { testFinancialDocuments };
