import { pathToFileURL } from 'url';
import { client, runTestSection, logResult, organizationId } from "../utils/utils.js";

async function testBoards() {
  console.log("\n🚀 Testing Boards Resource...");

  // 1. Boards CRUD
  let testBoardId: string | null = null;
  await runTestSection("boards.list", async () => {
    const res = await client.board.list({ limit: 5 });
    logResult("Boards", res.data);
  });

  await runTestSection("boards.create", async () => {
    const board = await client.board.create({
      name: `SDK_BOARD_TEST_${Date.now()}`,
      description: "Temporary board for testing"
    });
    testBoardId = board.id;
    logResult("Created Board", board);
  });

  if (testBoardId) {
    await runTestSection("boards.get", async () => {
      const board = await client.board.get(testBoardId!);
      logResult("Fetched Board", board);
    });

    await runTestSection("boards.update", async () => {
        const updated = await client.board.update(testBoardId!, {
            name: `SDK_BOARD_TEST_UPDATED_${Date.now()}`,
        });
        logResult("Updated Board", updated);
    });

    // 2. Fields
    let testFieldId: string | null = null;
    await runTestSection("Field Lifecycle", async () => {
        // Create
        const res: any = await client.board.createField(testBoardId!, {
            name: "Test Field",
            type: "ShortText"
        });
        const field = res.fields?.find((f: any) => f.name === "Test Field");
        testFieldId = field?._id;
        logResult("Created Field", testFieldId);

        // Update
        await client.board.updateField(testBoardId!, testFieldId!, { name: "Test Field Updated" });
        logResult("Updated Field", true);

        // Reorder
        await client.board.reorderFields(testBoardId!, { fields: [testFieldId!] });
        logResult("Reordered Fields", true);

        // Bulk Update
        await client.board.bulkUpdateFields(testBoardId!, { 
            fields: [{ _id: testFieldId!, name: "Test Field Bulk" }] 
        });
        logResult("Bulk Updated Fields", true);
    });

    // 3. Items
    let testItemId: string | null = null;
    await runTestSection("Item Lifecycle", async () => {
        const board: any = await client.board.get(testBoardId!);
        const idField = board.fields?.find((f: any) => f.is_identifier);
        if (idField) {
            const item = await client.board.createItem(testBoardId!, {
                fields: [{ board_field_id: idField._id, value: "SDK Test Item" }]
            });
            testItemId = item._id || item.id;
            logResult("Created Item", testItemId);

            await client.board.listItems(testBoardId!, { limit: 5 });
            await client.board.getItem(testBoardId!, testItemId!);
            await client.board.updateItem(testBoardId!, testItemId!, {
                data: [{ key: idField._id, value: "SDK Test Item Updated" }]
            });
            logResult("Item Operations Verified", true);

            // Bulk Delete
            await client.board.bulkDeleteItems(testBoardId!, { ids: [testItemId!] });
            logResult("Bulk Deleted Items", true);
        }
    });

    // 4. Segments
    await runTestSection("Segments Lifecycle", async () => {
        const segment = await client.board.createSegment(testBoardId!, {
            name: "Test Segment",
            filter: {}
        });
        const segmentId = segment._id || (segment as any).id;
        logResult("Created Segment", segmentId);

        await client.board.listSegments(testBoardId!);
        await client.board.updateSegment(testBoardId!, segmentId, { name: "Test Segment Updated" });
        await client.board.deleteSegment(testBoardId!, segmentId);
        logResult("Segment Operations Verified", true);
    });

    // 5. Cleanup & Board Reorder
    await runTestSection("Board Cleanup & Reorder", async () => {
        await client.board.reorder({ order: [testBoardId!] });
        logResult("Reordered Boards", true);
        
        await client.board.delete(testBoardId!);
        console.log("   Board deleted.");
    });
  }

  // 4. Misc Board functions
  await runTestSection("boards.getLinkPreview", async () => {
    try {
        const preview = await client.board.getLinkPreview("https://google.com");
        logResult("Link Preview", preview);
    } catch (e) {
        console.warn("   [Skip] boards.getLinkPreview failed");
    }
  });

  await runTestSection("boards.searchFiles", async () => {
    const files = await client.board.searchFiles({ q: "test" });
    logResult("Search Files Count", files.length);
  });

  await runTestSection("boards.checkConflict", async () => {
    const res = await client.board.checkConflict({
        ids: ["test"],
        organization_id: organizationId as string
    });
    logResult("Conflict Check", res);
  });

  // 5. Folders (Knowledge Hub)
  let testFolderId: string | null = null;
  await runTestSection("boards.searchFolders", async () => {
    const list = await client.board.searchFolders({});
    logResult("Folders", list);
  });

  await runTestSection("boards.createFolder", async () => {
    const folder = await client.board.createFolder({
      name: `SDK_FOLDER_TEST_${Date.now()}`,
      organization_id: organizationId as string,
      parent_id: "root",
      source_type: "upload"
    });
    testFolderId = folder._id || folder.id;
    logResult("Created Folder", folder);
  });

  if (testFolderId) {
    await runTestSection("boards.deleteFolders", async () => {
      await client.board.deleteFolders({ ids: [testFolderId!] });
      console.log("   Folder deleted.");
    });
  }

  console.log("\n✅ Boards Resource Testing Completed.");
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  testBoards().catch(console.error);
}

export { testBoards };

