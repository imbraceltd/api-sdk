import { pathToFileURL } from 'url';
import { client, runTestSection, logResult } from "../utils/utils.js";

async function testActivepieces() {
  console.log("\n🚀 Testing Activepieces Resource...");

  // 1. Flows
  let testProjectId: string | null = null;
  await runTestSection("activepieces.listFlows", async () => {
    const res = await client.activepieces.listFlows({ limit: 5 });
    logResult("Flows", res.data);
    if (res.data.length > 0) {
        testProjectId = res.data[0].projectId;
    }
  });

  // 2. Runs
  await runTestSection("activepieces.listRuns", async () => {
    const res = await client.activepieces.listRuns({ limit: 5 });
    logResult("Runs", res.data);
  });

  // 3. Folders
  await runTestSection("activepieces.listFolders", async () => {
    const res = await client.activepieces.listFolders({ limit: 5 });
    logResult("Folders", res.data);
  });

  // 4. Connections
  await runTestSection("activepieces.listConnections", async () => {
    const res = await client.activepieces.listConnections({ limit: 5 });
    logResult("Connections", res.data);
  });

  // 5. Tables
  await runTestSection("activepieces.listTables", async () => {
    const res = await client.activepieces.listTables();
    logResult("Tables", res.data);
  });

  // 6. Pieces
  await runTestSection("activepieces.listPieces", async () => {
    const pieces = await client.activepieces.listPieces();
    logResult("Pieces Count", pieces.length);
  });

  // 7. MCP Servers
  await runTestSection("activepieces.listMcpServers", async () => {
    if (!testProjectId) { console.log("  ⚠️  Skipped — no projectId from listFlows"); return; }
    const servers = await client.activepieces.listMcpServers(testProjectId);
    logResult("MCP Servers", servers);
  });

  // 8. Invitations
  await runTestSection("activepieces.listInvitations", async () => {
    const invites = await client.activepieces.listInvitations();
    logResult("Invitations", invites);
  });

  console.log("\n✅ Activepieces Resource Testing Completed.");
  }


if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  testActivepieces().catch(console.error);
}

export { testActivepieces };

