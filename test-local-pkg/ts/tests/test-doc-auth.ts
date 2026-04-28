import { ImbraceClient } from "@imbrace/sdk";
import * as dotenv from "dotenv";
import { resolve } from "path";

dotenv.config({ path: resolve(process.cwd(), ".env") });

const apiKey = process.env.IMBRACE_API_KEY;
const accessToken = process.env.IMBRACE_ACCESS_TOKEN;
const organizationId = process.env.IMBRACE_ORGANIZATION_ID;
const baseUrl = process.env.IMBRACE_GATEWAY_URL || "https://app-gatewayv2.imbrace.co";

async function runDocTest() {
  console.log("🚀 STARTING DOCUMENTATION AUTH TEST...");

  // 1. Test API Key (Server-Side)
  console.log("\n--- Testing API Key (Server-Side) ---");
  if (apiKey) {
    const client = new ImbraceClient({
      apiKey: apiKey,
      baseUrl: baseUrl,
    });
    try {
      // Test gọi resource (giả định dùng plural 'boards' như tài liệu)
      const { data: boards } = await client.boards.list({ limit: 1 });
      console.log("✅ API Key: Success. Found", boards.length, "boards.");
    } catch (e: any) {
      console.error("❌ API Key: Failed.", e.message);
    }
  }

  // 2. Test Access Token (Client-Side)
  console.log("\n--- Testing Access Token (Client-Side) ---");
  if (accessToken) {
    const client = new ImbraceClient({
      accessToken: accessToken,
      baseUrl: baseUrl,
    });
    try {
      const { data: boards } = await client.boards.list({ limit: 1 });
      console.log("✅ Access Token: Success. Found", boards.length, "boards.");
    } catch (e: any) {
      console.error("❌ Access Token: Failed.", e.message);
    }
  }

  // 3. Test Token Management
  console.log("\n--- Testing Token Management ---");
  const clientMgmt = new ImbraceClient({ baseUrl });
  if (accessToken) {
      clientMgmt.setAccessToken(accessToken);
      try {
        await clientMgmt.boards.list({ limit: 1 });
        console.log("✅ setAccessToken: Success.");
        
        clientMgmt.clearAccessToken();
        console.log("✅ clearAccessToken: Success.");
      } catch (e: any) {
        console.error("❌ Token Management: Failed.", e.message);
      }
  } else {
      console.warn("   Skipped: No Access Token for management test");
  }

  console.log("\n✅ DOCUMENTATION AUTH TEST COMPLETED.");
}

runDocTest().catch(console.error);
