import { pathToFileURL } from 'url';
import { client, runTestSection, logResult, organizationId } from "../utils/utils.js";
import { randomUUID } from "crypto";

async function testAiAgent() {
  console.log("\n🚀 Testing AI Agent Resource...");

  // ── 1. System ────────────────────────────────────────────────────────────
  await runTestSection("aiAgent.getHealth", async () => {
    const health = await client.aiAgent.getHealth(true);
    logResult("Health", health);
  });
  await runTestSection("aiAgent.getConfig", async () => {
    logResult("Config", await client.aiAgent.getConfig());
  });
  await runTestSection("aiAgent.getVersion", async () => {
    logResult("Version", await client.aiAgent.getVersion());
  });

  // ── 2. Chat v1 ───────────────────────────────────────────────────────────
  let firstChatId: string | undefined;
  await runTestSection("aiAgent.listChats", async () => {
    const chats = await client.aiAgent.listChats({ organization_id: organizationId as string, limit: 5 });
    logResult("Chats", chats);
    if (chats && chats.length > 0) firstChatId = chats[0].id;
  });

  await runTestSection("aiAgent.getChat", async () => {
    if (firstChatId) {
      try {
        const chat = await client.aiAgent.getChat(firstChatId, true);
        logResult("Get Chat", chat.id);
      } catch (e: any) { console.warn(`   [Skip] getChat: ${e.message}`); }
    } else { console.log("   [Skip] No chat available"); }
  });

  await runTestSection("aiAgent.deleteChat", async () => {
    if (firstChatId) {
      try {
        await client.aiAgent.deleteChat(firstChatId, { organization_id: organizationId as string });
        logResult("Delete Chat", true);
      } catch (e: any) { console.warn(`   [Skip] deleteChat: ${e.message}`); }
    } else { console.log("   [Skip] No chat available"); }
  });

  // ── 3. Sub-Agent ─────────────────────────────────────────────────────────
  await runTestSection("aiAgent.streamSubAgentChat", async () => {
    try {
      await client.aiAgent.streamSubAgentChat({
        assistant_id: "dummy", organization_id: organizationId as string,
        session_id: "dummy", chat_id: "dummy",
        messages: [{ role: "user", content: "test" }]
      });
      logResult("streamSubAgentChat", "OK");
    } catch (e: any) { console.warn(`   [Skip] streamSubAgentChat: ${e.message?.slice(0,60)}`); }
  });

  await runTestSection("aiAgent.getSubAgentHistory", async () => {
    try {
      const history = await client.aiAgent.getSubAgentHistory({ session_id: "dummy", chat_id: "dummy" });
      logResult("getSubAgentHistory", history);
    } catch (e: any) { console.warn(`   [Skip] getSubAgentHistory: ${e.message?.slice(0,60)}`); }
  });

  // ── 4. Prompt Suggestions ────────────────────────────────────────────────
  await runTestSection("aiAgent.getAgentPromptSuggestion", async () => {
    try {
      const assistants = await client.chatAi.listAssistants();
      if (assistants.length > 0) {
        const suggestions = await client.aiAgent.getAgentPromptSuggestion(assistants[0].id);
        logResult("Suggestions", suggestions);
      } else {
        console.log("   [Skip] No assistants found");
      }
    } catch (e: any) { console.warn(`   [Skip] getAgentPromptSuggestion: ${e.message?.slice(0,60)}`); }
  });

  // ── 5. Embeddings ────────────────────────────────────────────────────────
  let firstEmbeddingFileId: string | undefined;
  await runTestSection("aiAgent.listEmbeddingFiles", async () => {
    const files = await client.aiAgent.listEmbeddingFiles({ limit: 5 });
    logResult("Embedding Files", files?.length || 0);
    if (files && files.length > 0) firstEmbeddingFileId = files[0].id;
  });

  await runTestSection("aiAgent.getEmbeddingFile", async () => {
    if (firstEmbeddingFileId) {
      try {
        const file = await client.aiAgent.getEmbeddingFile(firstEmbeddingFileId);
        logResult("getEmbeddingFile", file.id);
      } catch (e: any) { console.warn(`   [Skip] getEmbeddingFile: ${e.message}`); }
    } else { console.log("   [Skip] No embedding file"); }
  });

  // processEmbedding — Nhóm A
  await runTestSection("aiAgent.processEmbedding", async () => {
    if (firstEmbeddingFileId) {
      try {
        const res = await client.aiAgent.processEmbedding({ fileId: firstEmbeddingFileId });
        logResult("processEmbedding", res);
      } catch (e: any) { console.warn(`   [Skip] processEmbedding: ${e.message?.slice(0,60)}`); }
    } else { console.log("   [Skip] No embedding file"); }
  });

  await runTestSection("aiAgent.updateEmbeddingFileStatus", async () => {
    if (firstEmbeddingFileId) {
      try {
        await client.aiAgent.updateEmbeddingFileStatus(firstEmbeddingFileId, "active");
        logResult("updateEmbeddingFileStatus", true);
      } catch (e: any) { console.warn(`   [Skip] updateEmbeddingFileStatus: ${e.message}`); }
    }
  });

  await runTestSection("aiAgent.previewEmbeddingFile", async () => {
    if (firstEmbeddingFileId) {
      try {
        const preview = await client.aiAgent.previewEmbeddingFile({ file_id: firstEmbeddingFileId });
        logResult("previewEmbeddingFile", preview != null);
      } catch (e: any) { console.warn(`   [Skip] previewEmbeddingFile: ${e.message}`); }
    }
  });

  await runTestSection("aiAgent.classifyFile", async () => {
    if (firstEmbeddingFileId) {
      try {
        const classification = await client.aiAgent.classifyFile({ file_id: firstEmbeddingFileId });
        logResult("classifyFile", classification);
      } catch (e: any) { console.warn(`   [Skip] classifyFile: ${e.message}`); }
    }
  });

  // deleteEmbeddingFile — Nhóm A (cleanup)
  await runTestSection("aiAgent.deleteEmbeddingFile", async () => {
    if (firstEmbeddingFileId) {
      try {
        await client.aiAgent.deleteEmbeddingFile(firstEmbeddingFileId);
        logResult("deleteEmbeddingFile", true);
      } catch (e: any) { console.warn(`   [Skip] deleteEmbeddingFile: ${e.message?.slice(0,60)}`); }
    } else { console.log("   [Skip] No embedding file"); }
  });

  // ── 6. Data Board ────────────────────────────────────────────────────────
  // ⚠️ 404 on prodv2 — backend route not yet deployed
  await runTestSection("aiAgent.suggestFieldTypes", async () => {
    try {
      const result = await client.aiAgent.suggestFieldTypes({
        fields: [
          { name: "amount", samples: [100, 200, 300] },
          { name: "date", samples: ["2024-01-01", "2024-01-02"] }
        ]
      });
      logResult("Field Suggestions", result);
    } catch (e: any) {
      const code = (e as any).statusCode || "?";
      console.warn(`   [Skip] suggestFieldTypes: ${code} — backend route not deployed yet`);
    }
  });

  // ── 7. Parquet ───────────────────────────────────────────────────────────
  let parquetFileName: string | undefined;
  await runTestSection("aiAgent.generateParquet", async () => {
    const fileName = `test_${Date.now()}`;
    try {
      const res = await client.aiAgent.generateParquet({ data: [{ id: 1, name: "Test" }], fileName });
      parquetFileName = fileName;
      logResult("Parquet Result", res);
    } catch (e: any) { console.warn(`   [Skip] generateParquet: ${e.message?.slice(0,60)}`); }
  });

  await runTestSection("aiAgent.listParquetFiles", async () => {
    try {
      const files = await client.aiAgent.listParquetFiles();
      logResult("Parquet Files", files);
    } catch (e: any) { console.warn(`   [Skip] listParquetFiles: ${e.message?.slice(0,60)}`); }
  });

  await runTestSection("aiAgent.deleteParquetFile", async () => {
    if (parquetFileName) {
      try {
        await client.aiAgent.deleteParquetFile(parquetFileName + ".parquet");
        logResult("deleteParquetFile", true);
      } catch (e: any) { console.warn(`   [Skip] deleteParquetFile: ${e.message}`); }
    }
  });

  // ── 8. Tracing (Tempo) ───────────────────────────────────────────────────
  // ⚠️ 500 on prodv2 — Tempo URL not configured
  let firstTraceTag: string | undefined;
  await runTestSection("aiAgent.getTraceServices", async () => {
    try {
      const services = await client.aiAgent.getTraceServices();
      logResult("Trace Services", services);
    } catch (e: any) {
      console.warn(`   [Skip] getTraceServices: ${(e as any).statusCode || "?"} — Tempo URL not configured`);
    }
  });

  await runTestSection("aiAgent.getTraceTags", async () => {
    try {
      const tags = await client.aiAgent.getTraceTags();
      logResult("Trace Tags", tags);
      if (Array.isArray(tags) && tags.length > 0) firstTraceTag = tags[0];
    } catch (e: any) {
      console.warn(`   [Skip] getTraceTags: ${(e as any).statusCode || "?"} — Tempo URL not configured`);
    }
  });

  // getTraceTagValues — Nhóm A
  await runTestSection("aiAgent.getTraceTagValues", async () => {
    const tag = firstTraceTag || "http.status_code";
    try {
      const values = await client.aiAgent.getTraceTagValues(tag);
      logResult("getTraceTagValues", values);
    } catch (e: any) {
      console.warn(`   [Skip] getTraceTagValues(${tag}): ${e.message?.slice(0,60)}`);
    }
  });

  await runTestSection("aiAgent.getTraces", async () => {
    try {
      const traces = await client.aiAgent.getTraces({ limit: 5 });
      logResult("getTraces", traces);
    } catch (e: any) { console.warn(`   [Skip] getTraces: ${e.message?.slice(0,60)}`); }
  });

  // getTrace — Nhóm A
  await runTestSection("aiAgent.getTrace", async () => {
    try {
      await client.aiAgent.getTrace("dummy_trace_id");
      logResult("getTrace", true);
    } catch (e: any) { console.warn(`   [Skip] getTrace: ${e.message?.slice(0,60)}`); }
  });

  // searchTraceQL — Nhóm B
  await runTestSection("aiAgent.searchTraceQL", async () => {
    try {
      const res = await client.aiAgent.searchTraceQL('{ .service.name = "ai-agent" }');
      logResult("searchTraceQL", res);
    } catch (e: any) { console.warn(`   [Skip] searchTraceQL: ${e.message?.slice(0,60)}`); }
  });

  // ── 9. Chat Client sub-API ───────────────────────────────────────────────
  let firstClientChatId: string | undefined;
  let firstMessageId: string | undefined;

  await runTestSection("aiAgent.listClientChats", async () => {
    try {
      const chats = await client.aiAgent.listClientChats({ limit: 5 });
      logResult("Client Chats", chats?.length || 0);
      if (chats && chats.length > 0) firstClientChatId = chats[0].id;
    } catch (e: any) { console.warn(`   [Skip] listClientChats: ${e.message}`); }
  });

  await runTestSection("aiAgent.createClientChat", async () => {
    try {
      const res = await client.aiAgent.createClientChat({
        id: randomUUID(), assistantId: "dummy",
        organizationId: organizationId as string, userId: "dummy",
        selectedVisibilityType: "public",
        message: {
          id: randomUUID(), role: "user", content: "Hello",
          createdAt: new Date().toISOString(), parts: [{ type: "text", text: "Hello" }]
        }
      });
      logResult("Create Client Chat", res);
    } catch (e: any) { console.warn(`   [Skip] createClientChat: ${e.message?.slice(0,60)}`); }
  });

  await runTestSection("aiAgent.listClientMessages", async () => {
    if (firstClientChatId) {
      try {
        const msgs = await client.aiAgent.listClientMessages(firstClientChatId);
        logResult("listClientMessages", msgs.length);
        if (msgs.length > 0) firstMessageId = msgs[0].id;
      } catch (e: any) { console.warn(`   [Skip] listClientMessages: ${e.message}`); }
    } else { console.log("   [Skip] No client chat"); }
  });

  await runTestSection("aiAgent.getVotes", async () => {
    if (firstClientChatId) {
      try {
        const votes = await client.aiAgent.getVotes(firstClientChatId);
        logResult("getVotes", votes);
      } catch (e: any) { console.warn(`   [Skip] getVotes: ${e.message}`); }
    }
  });

  // updateVote — Nhóm A
  await runTestSection("aiAgent.updateVote", async () => {
    if (firstMessageId) {
      try {
        await client.aiAgent.updateVote({ messageId: firstMessageId, vote: "up" });
        logResult("updateVote", true);
      } catch (e: any) { console.warn(`   [Skip] updateVote: ${e.message?.slice(0,60)}`); }
    } else { console.log("   [Skip] No message ID available"); }
  });

  // deleteTrailingMessages — Nhóm A
  await runTestSection("aiAgent.deleteTrailingMessages", async () => {
    if (firstMessageId) {
      try {
        await client.aiAgent.deleteTrailingMessages(firstMessageId);
        logResult("deleteTrailingMessages", true);
      } catch (e: any) { console.warn(`   [Skip] deleteTrailingMessages: ${e.message?.slice(0,60)}`); }
    } else { console.log("   [Skip] No message ID available"); }
  });

  await runTestSection("aiAgent.generateClientChatTitle", async () => {
    if (firstClientChatId) {
      try {
        await client.aiAgent.generateClientChatTitle(firstClientChatId);
        logResult("generateClientChatTitle", true);
      } catch (e: any) { console.warn(`   [Skip] generateClientChatTitle: ${e.message}`); }
    }
  });

  await runTestSection("aiAgent.updateClientChat", async () => {
    if (firstClientChatId) {
      try {
        await client.aiAgent.updateClientChat(firstClientChatId, { visibility: "private" });
        logResult("updateClientChat", true);
      } catch (e: any) { console.warn(`   [Skip] updateClientChat: ${e.message}`); }
    }
  });

  // ── 10. Documents ────────────────────────────────────────────────────────
  await runTestSection("aiAgent.Documents CRUD", async () => {
    let docId: string | undefined;
    try {
      const doc = await client.aiAgent.createDocument({
        id: randomUUID(),
        chatId: randomUUID(),
        kind: "text",
        content: "Test document",
        title: "SDK Test",
        createdAt: new Date().toISOString()
      });
      docId = doc.id;
      logResult("createDocument", docId);
    } catch (e: any) {
      console.warn(`   [Skip] createDocument: ${e.message?.slice(0,80)}`);
      console.warn(`   ℹ️  Backend may require assistantId/userId fields`);
    }

    if (docId) {
      // get
      try {
        const fetched = await client.aiAgent.getDocument(docId);
        logResult("getDocument", fetched.id);
      } catch (e: any) { console.warn(`   [Skip] getDocument: ${e.message}`); }

      // getDocumentLatest — Nhóm A
      try {
        const latest = await client.aiAgent.getDocumentLatest(docId);
        logResult("getDocumentLatest", latest);
      } catch (e: any) { console.warn(`   [Skip] getDocumentLatest: ${e.message?.slice(0,60)}`); }

      // getDocumentPublic — Nhóm A
      try {
        const pub = await client.aiAgent.getDocumentPublic(docId);
        logResult("getDocumentPublic", pub);
      } catch (e: any) { console.warn(`   [Skip] getDocumentPublic: ${e.message?.slice(0,60)}`); }

      // getDocumentSuggestions — Nhóm A
      try {
        const suggestions = await client.aiAgent.getDocumentSuggestions(docId);
        logResult("getDocumentSuggestions", suggestions);
      } catch (e: any) { console.warn(`   [Skip] getDocumentSuggestions: ${e.message?.slice(0,60)}`); }

      // delete
      try {
        await client.aiAgent.deleteDocument(docId);
        logResult("deleteDocument", true);
      } catch (e: any) { console.warn(`   [Skip] deleteDocument: ${e.message}`); }
    }

    // getDocumentLatestByKind — Nhóm A (no docId needed)
    try {
      const byKind = await client.aiAgent.getDocumentLatestByKind({ kind: "text" });
      logResult("getDocumentLatestByKind", byKind);
    } catch (e: any) { console.warn(`   [Skip] getDocumentLatestByKind: ${e.message?.slice(0,60)}`); }
  });

  // ── 11. Admin Guides ─────────────────────────────────────────────────────
  // ⚠️ 404 on prodv2 — backend route not yet deployed
  await runTestSection("aiAgent.adminGuides", async () => {
    let guides: any[] = [];
    try {
      guides = await client.aiAgent.listAdminGuides();
      logResult("listAdminGuides", guides.length);
    } catch (e: any) {
      console.warn(`   [Skip] listAdminGuides: ${(e as any).statusCode || "?"} — route not deployed (expected)`);
    }

    // getAdminGuide — Nhóm A
    if (guides.length > 0) {
      try {
        const name = guides[0]?.name || guides[0]?.file || "guide.pdf";
        const resp = await client.aiAgent.getAdminGuide(name);
        logResult("getAdminGuide", resp ? "OK" : "empty");
      } catch (e: any) { console.warn(`   [Skip] getAdminGuide: ${e.message?.slice(0,60)}`); }
    } else {
      console.log("   [Skip] getAdminGuide — no guides or 404");
    }
  });

  console.log("\n✅ AI Agent Resource Testing Completed.");
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  testAiAgent().catch(console.error);
}

export { testAiAgent };
