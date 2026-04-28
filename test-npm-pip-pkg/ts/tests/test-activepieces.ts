import { pathToFileURL } from 'url';
import { client, runTestSection, logResult } from "../utils/utils.js";

async function testActivepieces() {
  console.log("\n🚀 Testing Activepieces Resource...");

  let testProjectId: string | undefined;
  let testFlowId: string | undefined;
  let testFolderId: string | undefined;
  let testRunId: string | undefined;

  // 1. Flows
  await runTestSection("activepieces.listFlows", async () => {
    const res = await client.activepieces.listFlows({ limit: 5 });
    logResult("Flows", res.data?.length || 0);
    if (res.data && res.data.length > 0) {
        testProjectId = res.data[0].projectId;
    }
  });

  // Create Flow (Nhóm B)
  await runTestSection("activepieces.createFlow", async () => {
    if (testProjectId) {
      try {
        const ts = Date.now();
        const newFlow = await client.activepieces.createFlow({
          displayName: `SDK Test Flow ${ts}`,
          projectId: testProjectId
        });
        testFlowId = newFlow.id || (newFlow as any)._id;
        logResult("createFlow", testFlowId);
      } catch (e: any) {
        console.warn(`   ⚠️ createFlow failed: ${e.message}`);
      }
    } else {
      console.log("   ⚠️ No projectId — skipping createFlow");
    }
  });

  // Get Flow
  await runTestSection("activepieces.getFlow", async () => {
    if (testFlowId) {
      try {
        const flow = await client.activepieces.getFlow(testFlowId);
        logResult("getFlow", flow.id);
      } catch (e: any) {
        console.warn(`   ⚠️ getFlow failed: ${e.message}`);
      }
    } else {
      console.log("   [skip] getFlow — no flowId");
    }
  });

  // Trigger Flow Async
  await runTestSection("activepieces.triggerFlow", async () => {
    if (testFlowId) {
      try {
        await client.activepieces.triggerFlow(testFlowId, { source: "sdk-test" });
        logResult("triggerFlow (async)", "Sent");
      } catch (e: any) {
        console.warn(`   ⚠️ triggerFlow failed: ${e.message}`);
      }
    } else {
      console.log("   [skip] triggerFlow — no flowId");
    }
  });

  // Trigger Flow Sync (Nhóm B)
  await runTestSection("activepieces.triggerFlowSync", async () => {
    if (testFlowId) {
      try {
        const res = await client.activepieces.triggerFlowSync(testFlowId, { source: "sdk-test-sync" });
        logResult("triggerFlowSync", res ? "OK" : "empty");
      } catch (e: any) {
        console.warn(`   ⚠️ triggerFlowSync failed: ${e.message}`);
      }
    } else {
      console.log("   [skip] triggerFlowSync — no flowId");
    }
  });

  // 2. Runs
  await runTestSection("activepieces.listRuns", async () => {
    const res = await client.activepieces.listRuns({ limit: 5 });
    logResult("Runs", res.data?.length || 0);
    if (res.data && res.data.length > 0) {
      testRunId = res.data[0].id || (res.data[0] as any)._id;
    }
  });

  // Get Run
  await runTestSection("activepieces.getRun", async () => {
    if (testRunId) {
      try {
        const run = await client.activepieces.getRun(testRunId);
        logResult("getRun", run.id);
      } catch (e: any) {
        console.warn(`   ⚠️ getRun failed: ${e.message}`);
      }
    } else {
      console.log("   [skip] getRun — no runId");
    }
  });

  // Delete Flow (cleanup)
  await runTestSection("activepieces.deleteFlow", async () => {
    if (testFlowId) {
      try {
        await client.activepieces.deleteFlow(testFlowId);
        logResult("deleteFlow", true);
        testFlowId = undefined;
      } catch (e: any) {
        console.warn(`   ⚠️ deleteFlow failed: ${e.message}`);
      }
    } else {
      console.log("   [skip] deleteFlow — no flowId");
    }
  });

  // 3. Folders
  await runTestSection("activepieces.listFolders", async () => {
    const res = await client.activepieces.listFolders({ limit: 5 });
    logResult("Folders", res.data?.length || 0);
  });

  // Create Folder
  await runTestSection("activepieces.createFolder", async () => {
    if (testProjectId) {
      try {
        const ts = Date.now();
        const newFolder = await client.activepieces.createFolder({
          displayName: `SDK Folder ${ts}`,
          projectId: testProjectId
        });
        testFolderId = newFolder.id || (newFolder as any)._id;
        logResult("createFolder", testFolderId);
      } catch (e: any) {
        console.warn(`   ⚠️ createFolder failed: ${e.message}`);
      }
    } else {
      console.log("   [skip] createFolder — no projectId");
    }
  });

  // 4. Connections
  await runTestSection("activepieces.listConnections", async () => {
    const res = await client.activepieces.listConnections({ limit: 5 });
    logResult("Connections", res.data?.length || 0);
  });

  // Upsert Connection (Nhóm B)
  await runTestSection("activepieces.upsertConnection", async () => {
    try {
      await client.activepieces.upsertConnection({
        name: `sdk-test-conn-${Date.now()}`,
        type: "APP_CONNECTION",
        projectIds: [testProjectId || "dummy"],
        value: { type: "NO_AUTH" } as any,
        externalId: `sdk-conn-${Date.now()}` // required by backend
      });
      logResult("upsertConnection", true);
    } catch (e: any) {
      console.warn(`   ⚠️ upsertConnection failed: ${e.message}`);
    }
  });

  // 5. Tables
  await runTestSection("activepieces.listTables", async () => {
    const res = await client.activepieces.listTables();
    logResult("Tables", res.data?.length || 0);
  });

  // 6. Pieces
  await runTestSection("activepieces.listPieces", async () => {
    const pieces = await client.activepieces.listPieces();
    logResult("Pieces Count", pieces.length);
  });

  // 7. MCP Servers
  await runTestSection("activepieces.listMcpServers", async () => {
    try {
      const servers = await client.activepieces.listMcpServers(testProjectId || "dummy");
      logResult("MCP Servers", servers);
    } catch (e: any) {
      console.warn(`   ⚠️ listMcpServers failed: ${e.message}`);
    }
  });

  // 8. Invitations
  await runTestSection("activepieces.listInvitations", async () => {
    try {
      // requires 'type' query param. Using 'USER' as placeholder
      const invites = await client.activepieces.listInvitations({ type: "USER" });
      logResult("Invitations", invites);
    } catch (e: any) {
      console.warn(`   ⚠️ listInvitations failed: ${e.message}`);
    }
  });

  console.log("\n✅ Activepieces Resource Testing Completed.");
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  testActivepieces().catch(console.error);
}

export { testActivepieces };
