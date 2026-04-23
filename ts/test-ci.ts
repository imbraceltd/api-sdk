import { ImbraceClient } from "./src/index.js";
import { randomUUID } from "crypto";
import dotenv from "dotenv";

dotenv.config();

/**
 * COMPREHENSIVE CI TEST SUITE
 * Trọng tâm: Các method nâng cao còn thiếu trong các bản test cơ bản.
 */
async function runCiTest() {
  const apiKey =
    process.env.IMBRACE_API_KEY || "api_bf3be272-1bd1-4944-b167-5dd997f9302f";
  const baseUrl =
    process.env.IMBRACE_GATEWAY_URL || "https://app-gatewayv2.imbrace.co";
  const organizationId =
    process.env.IMBRACE_ORGANIZATION_ID ||
    "org_8d2a2d53-20ef-4c54-8aa9-aadec5963b5c";

  if (!apiKey) {
    console.error("❌ IMBRACE_API_KEY is required in environment variables.");
    process.exit(1);
  }

  const client = new ImbraceClient({ apiKey, baseUrl });
  const ts = Date.now();
  const state = {
    assistantId: null as string | null,
    chatId: null as string | null,
    msgId: null as string | null,
    docId: null as string | null,
    boardId: null as string | null,
    contactId: null as string | null,
    convId: null as string | null,
  };

  console.log("====================================================");
  console.log("🚀 IMBRACE SDK CI - ADVANCED METHODS TEST");
  console.log(`Target: ${baseUrl}`);
  console.log("====================================================");

  async function step(label: string, fn: () => Promise<any>) {
    try {
      const res = await fn();
      console.log(`✅ [PASS] ${label}`);
      return res;
    } catch (e: any) {
      console.error(`❌ [FAIL] ${label}: ${e.message}`);
      if (e.response?.data)
        console.error("   Detail:", JSON.stringify(e.response.data));
      return null;
    }
  }

  // 1. AI Agent - System & Config
  console.log("\n[1] AI Agent System & Config");
  await step("aiAgent.getConfig", () => client.aiAgent.getConfig());
  await step("aiAgent.getHealth", () => client.aiAgent.getHealth(true));
  await step("aiAgent.getVersion", () => client.aiAgent.getVersion());

  // 2. AI Agent - Parquet & Field Suggestions
  console.log("\n[2] Data Analytics (Parquet)");
  await step("aiAgent.generateParquet", () =>
    client.aiAgent.generateParquet({
      data: [{ id: 1, name: "Test" }],
      fileName: `ci_test_${ts}`,
      folderName: "ci_test",
    }),
  );
  await step("aiAgent.listParquetFiles", () =>
    client.aiAgent.listParquetFiles(),
  );
  await step("aiAgent.suggestFieldTypes", () =>
    client.aiAgent.suggestFieldTypes({
      fields: [{ name: "price", samples: ["100", "200", "300"] }],
    }),
  );

  // 3. AI Agent - Tracing (Tempo)
  console.log("\n[3] Observability (Tracing)");
  await step("aiAgent.getTraceServices", () =>
    client.aiAgent.getTraceServices(),
  );
  await step("aiAgent.getTraceTags", () => client.aiAgent.getTraceTags());
  await step("aiAgent.getTraces", () => client.aiAgent.getTraces({ limit: 1 }));

  // 4. Chat Client Sub-API (Frontend style)
  console.log("\n[4] Chat Client Sub-API");
  await step("aiAgent.listClientChats", () =>
    client.aiAgent.listClientChats({
      organization_id: organizationId,
      limit: 1,
    }),
  );

  // Create a client chat for further testing
  const clientChat = await step("aiAgent.createClientChat", () => {
    state.chatId = randomUUID();
    return client.aiAgent.createClientChat({
      id: state.chatId,
      assistantId: "default", // or placeholder
      organizationId: organizationId,
      message: {
        id: randomUUID(),
        role: "user",
        parts: [{ type: "text", text: "CI Test Chat" }],
      },
    });
  });

  if (state.chatId) {
    await step("aiAgent.getClientChat", () =>
      client.aiAgent.getClientChat(state.chatId!),
    );
    await step("aiAgent.updateClientChat", () =>
      client.aiAgent.updateClientChat(state.chatId!, { visibility: "private" }),
    );
    await step("aiAgent.listClientMessages", () =>
      client.aiAgent.listClientMessages(state.chatId!),
    );
    await step("aiAgent.generateClientChatTitle", () =>
      client.aiAgent.generateClientChatTitle(state.chatId!),
    );

    // Document/Artifact creation
    const doc = await step("aiAgent.createDocument", () =>
      client.aiAgent.createDocument({
        kind: "text",
        content: "CI Test Document Content",
      }),
    );
    if (doc) {
      state.docId = doc.id || doc._id;
      await step("aiAgent.getDocument", () =>
        client.aiAgent.getDocument(state.docId!),
      );
      await step("aiAgent.getDocumentLatest", () =>
        client.aiAgent.getDocumentLatest(state.docId!),
      );
      await step("aiAgent.deleteDocument", () =>
        client.aiAgent.deleteDocument(state.docId!),
      );
    }

    await step("aiAgent.deleteClientChat", () =>
      client.aiAgent.deleteClientChat(state.chatId!),
    );
  }

  // 5. Assistant & Knowledge (chatAi)
  console.log("\n[5] Assistant & Knowledge (chatAi)");
  await step("chatAi.listModels", () => client.chatAi.listModels());
  await step("chatAi.listKnowledge", () => client.chatAi.listKnowledge());
  await step("chatAi.listFolders", () => client.chatAi.listFolders());

  // 6. CRM & Messaging (Conversations, Contacts)
  console.log("\n[6] CRM & Messaging");
  const contacts = await step("contacts.list", () =>
    client.contacts.list({ limit: 1 }),
  );
  if (contacts?.data?.length > 0) {
    state.contactId = contacts.data[0].id;
    await step("contacts.getActivity", () =>
      client.contacts.getActivity(state.contactId!),
    );
    await step("contacts.getComments", () =>
      client.contacts.getComments(state.contactId!),
    );
  }

  const convs = await step("conversations.getOutstanding", () =>
    client.conversations.getOutstanding({ limit: 1 }),
  );
  if (convs?.data?.length > 0) {
    state.convId = convs.data[0].id || convs.data[0]._id;
    // Skip destructive/assign calls to avoid messing with live data
    await step("messages.list", () => client.messages.list(state.convId!));
  }

  await step("channel.list", () => client.channel.list());

  // 7. Boards Advanced
  console.log("\n[7] Boards Advanced");
  const boards = await step("boards.list", () =>
    client.boards.list({ limit: 1 }),
  );
  if (boards?.data?.length > 0) {
    state.boardId = boards.data[0].id || boards.data[0]._id;
    await step("boards.listSegments", () =>
      client.boards.listSegments(state.boardId!),
    );
  }

  console.log("\n====================================================");
  console.log("✅ CI TEST SUITE FINISHED");
  console.log("====================================================");
}

runCiTest().catch(console.error);
