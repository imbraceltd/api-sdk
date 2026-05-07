import { pathToFileURL } from 'url';
import { client, runTestSection, logResult } from "../utils/utils.js";

async function testDocumentAI() {
  console.log("\n🚀 Testing Document AI Resource...");

  // 1. URL routing smoke — fake ID, expect 404 from FastAPI
  await runTestSection("documentAi.getFile (fake ID — 404 expected)", async () => {
    try {
      await client.documentAi.getFile("FAKE_DOCUMENT_ID_FOR_ROUTING_CHECK");
      logResult("Status", "200 (unexpected — backend should return 404)");
    } catch (e: any) {
      const msg = e?.message ?? "";
      if (msg.includes("404") || msg.includes("Not Found") || msg.includes("not found")) {
        logResult("Routing", "404 — endpoint reachable, ID not found ✓");
      } else if (msg.includes("401") || msg.includes("403")) {
        logResult("Routing", `auth error: ${msg.slice(0, 80)}`);
        throw e;
      } else {
        throw e;
      }
    }
  });

  // 2. URL routing — getReport
  await runTestSection("documentAi.getReport (fake ID)", async () => {
    try {
      await client.documentAi.getReport("FAKE_REPORT_ID");
      logResult("Status", "200 (unexpected)");
    } catch (e: any) {
      const msg = e?.message ?? "";
      if (msg.includes("404")) {
        logResult("Routing", "404 — endpoint reachable ✓");
      } else {
        throw e;
      }
    }
  });

  // 3. listErrors with fake ID
  await runTestSection("documentAi.listErrors (fake ID)", async () => {
    try {
      await client.documentAi.listErrors("FAKE_FILE_ID");
      logResult("Status", "ok");
    } catch (e: any) {
      const msg = e?.message ?? "";
      if (msg.includes("404")) {
        logResult("Routing", "404 — endpoint reachable ✓");
      } else {
        throw e;
      }
    }
  });

  // 4. CRUD on real data — only if env IDs provided
  const fileId = process.env.IMBRACE_FIN_FILE_ID;
  const reportId = process.env.IMBRACE_FIN_REPORT_ID;

  if (fileId) {
    await runTestSection("documentAi.getFile (real ID)", async () => {
      const res = await client.documentAi.getFile(fileId, { page: 1, limit: 5 });
      logResult("Pagination", res?.importedFile?.pagination ?? res?.report?.pagination ?? "n/a");
    });

    await runTestSection("documentAi.listErrors (real)", async () => {
      const res = await client.documentAi.listErrors(fileId, { limit: 10 });
      const list = Array.isArray(res) ? res : (res?.data ?? []);
      logResult("Error count", list.length);
    });
  } else {
    console.log("  ℹ Set IMBRACE_FIN_FILE_ID env to test real CRUD on getFile / listErrors");
  }

  if (reportId) {
    await runTestSection("documentAi.getReport (real ID)", async () => {
      const res = await client.documentAi.getReport(reportId, { page: 1, limit: 5 });
      logResult("Rows", res?.data?.length ?? "n/a");
    });
  } else {
    console.log("  ℹ Set IMBRACE_FIN_REPORT_ID env to test real CRUD on getReport");
  }

  console.log("\n✅ Document AI Resource Testing Completed.");
}


if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  testDocumentAI().catch(console.error);
}

export { testDocumentAI };
