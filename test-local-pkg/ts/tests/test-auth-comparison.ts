import { ImbraceClient } from "@imbrace/sdk";
import * as dotenv from "dotenv";
import { resolve } from "path";

dotenv.config({ path: resolve(process.cwd(), ".env") });

const apiKey = process.env.IMBRACE_API_KEY;
const accessToken = process.env.IMBRACE_ACCESS_TOKEN;
const organizationId = process.env.IMBRACE_ORGANIZATION_ID;
const baseUrl = process.env.IMBRACE_GATEWAY_URL;

async function verifyAuth() {
  console.log("--- 🛡️ VERIFYING AUTH MODES ---");

  // 1. Test với CHỈ API KEY
  console.log("\n[Mode 1] Testing with API KEY only...");
  if (!apiKey) {
    console.warn("   Skipped: No API Key in .env");
  } else {
    const clientApiKey = new ImbraceClient({
      apiKey: apiKey,
      baseUrl,
      organizationId: organizationId || undefined
    });

    try {
      const res = await clientApiKey.boards.list({ limit: 1 });
      console.log("✅ API KEY Success! Total boards found:", res.data?.length ?? 0);
    } catch (e: any) {
      console.error("❌ API KEY Failed:", e.message);
    }
  }

  // 2. Test với CHỈ ACCESS TOKEN
  console.log("\n[Mode 2] Testing with ACCESS TOKEN only...");
  if (!accessToken) {
    console.warn("   Skipped: No Access Token in .env");
  } else {
    const clientToken = new ImbraceClient({
      accessToken: accessToken,
      baseUrl,
      organizationId: organizationId || undefined
    });

    try {
      const res = await clientToken.boards.list({ limit: 1 });
      console.log("✅ ACCESS TOKEN Success! Total boards found:", res.data?.length ?? 0);
    } catch (e: any) {
      console.error("❌ ACCESS TOKEN Failed:", e.message);
    }
  }
}

verifyAuth().catch(console.error);
