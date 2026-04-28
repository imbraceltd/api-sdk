import { ImbraceClient } from "@imbrace/sdk";
import * as dotenv from "dotenv";
import { resolve } from "path";

dotenv.config({ path: resolve(process.cwd(), ".env") });

const apiKey = process.env.IMBRACE_API_KEY;
const accessToken = process.env.IMBRACE_ACCESS_TOKEN;
const organizationId = process.env.IMBRACE_ORGANIZATION_ID;
const baseUrl = process.env.IMBRACE_GATEWAY_URL || "https://app-gatewayv2.imbrace.co";

async function runDocTest() {
  console.log("🚀 STARTING NPM DOCUMENTATION AUTH TEST...");

  const client = new ImbraceClient({
    apiKey: apiKey,
    baseUrl: baseUrl,
  });

  try {
    console.log("\nAttempting to call client.boards.list()...");
    const { data: boards } = await client.boards.list({ limit: 1 });
    console.log("✅ Success! Found", boards.length, "boards.");
  } catch (e: any) {
    console.error("❌ Unexpected Error:", e.message);
  }
}

runDocTest().catch(console.error);
