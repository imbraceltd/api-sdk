import { ImbraceClient } from "@imbrace/sdk";
import * as dotenv from "dotenv";
import { resolve } from "path";

dotenv.config({ path: resolve(process.cwd(), ".env") });

const apiKey = process.env.IMBRACE_API_KEY;
const accessToken = process.env.IMBRACE_ACCESS_TOKEN;
const baseUrl = process.env.IMBRACE_GATEWAY_URL || "https://app-gatewayv2.imbrace.co";

async function runStepByStepTest() {
  console.log("\n🚀 BẮT ĐẦU KIỂM TRA TOÀN BỘ LUỒNG AUTHENTICATION");

  // --- MỤC 1: API KEY (SERVER-SIDE) ---
  console.log("\n[BƯỚC 1] Kiểm tra API Key (Server-Side)...");
  if (apiKey) {
    const client = new ImbraceClient({ apiKey, baseUrl });
    try {
      const { data } = await client.boards.list({ limit: 1 });
      console.log("   ✅ Thành công! Đã lấy được danh sách Boards bằng API Key.");
    } catch (e: any) {
      console.log("   ❌ Thất bại:", e.message);
    }
  } else {
    console.log("   ⚠️ Bỏ qua: Không có IMBRACE_API_KEY trong .env");
  }

  // --- MỤC 2: ACCESS TOKEN (CLIENT-SIDE) ---
  console.log("\n[BƯỚC 2] Kiểm tra Access Token (Client-Side)...");
  if (accessToken) {
    const client = new ImbraceClient({ accessToken, baseUrl });
    try {
      const { data } = await client.boards.list({ limit: 1 });
      console.log("   ✅ Thành công! Đã lấy được danh sách Boards bằng Access Token.");
    } catch (e: any) {
      console.log("   ❌ Thất bại:", e.message);
    }
  } else {
    console.log("   ⚠️ Bỏ qua: Không có IMBRACE_ACCESS_TOKEN trong .env");
  }

  // --- MỤC 3: QUẢN LÝ TOKEN (TOKEN MANAGEMENT) ---
  console.log("\n[BƯỚC 3] Kiểm tra Quản lý Token (set/clear)...");
  const clientMgmt = new ImbraceClient({ baseUrl });
  
  if (accessToken) {
    console.log("   -> Đang gọi setAccessToken()...");
    clientMgmt.setAccessToken(accessToken);
    try {
      await clientMgmt.boards.list({ limit: 1 });
      console.log("   ✅ Thành công! Token đã được kích hoạt.");
      
      console.log("   -> Đang gọi clearAccessToken()...");
      clientMgmt.clearAccessToken();
      try {
        await clientMgmt.boards.list({ limit: 1 });
      } catch (e: any) {
        console.log("   ✅ Thành công! Token đã bị xóa (Đúng như mong đợi).");
      }
    } catch (e: any) {
      console.log("   ❌ Thất bại trong quản lý token:", e.message);
    }
  }

  // --- MỤC 4: KIỂM TRA Tên Resource (Boards - Plural) ---
  console.log("\n[BƯỚC 4] Kiểm tra tính nhất quán tên Resource (boards)...");
  const clientPlural = new ImbraceClient({ apiKey, baseUrl });
  if (clientPlural.boards) {
    console.log("   ✅ Thành công! 'client.boards' (số nhiều) đã tồn tại.");
  } else {
    console.log("   ❌ Thất bại! 'client.boards' không tồn tại.");
  }

  console.log("\n🏁 KẾT THÚC KIỂM TRA.\n");
}

runStepByStepTest().catch(console.error);
