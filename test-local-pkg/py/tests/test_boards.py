import time
from utils.utils import client, run_test_section, log_result, organization_id

def test_boards():
    print("\n🚀 Testing Boards Resource...")

    state = {"board_id": None, "field_id": None, "item_id": None, "folder_id": None}

    # 1. Boards CRUD
    def board_crud():
        res = client.boards.list(limit=5)
        log_result("Boards", res.get("data", []))

        board = client.boards.create(
            name=f"SDK_PY_BOARD_TEST_{int(time.time())}",
            description="Temp board"
        )
        state["board_id"] = board.get("id") or board.get("_id")
        log_result("Created Board", state["board_id"])

        if state["board_id"]:
            fetched = client.boards.get(state["board_id"])
            log_result("Fetched Board", fetched)

            updated = client.boards.update(state["board_id"], {"name": f"SDK_PY_BOARD_UPDATED_{int(time.time())}"})
            log_result("Updated Board", updated)

    run_test_section("Boards CRUD", board_crud)

    # 2. Fields
    def field_lifecycle():
        if not state["board_id"]: return
        res = client.boards.create_field(state["board_id"], {
            "name": "Test Field",
            "type": "ShortText"
        })
        fields = res.get("fields", [])
        field = next((f for f in fields if f["name"] == "Test Field"), None)
        state["field_id"] = field.get("_id") if field else None
        log_result("Created Field", state["field_id"])

        if state["field_id"]:
            client.boards.update_field(state["board_id"], state["field_id"], {"name": "Test Field Updated"})
            log_result("Updated Field", True)

            board_data = client.boards.get(state["board_id"])
            all_fields = board_data.get("fields", [])
            # For reorder, we just pass the same array back (maybe swap first two to test reordering)
            if len(all_fields) > 1:
                all_fields[0], all_fields[1] = all_fields[1], all_fields[0]
            field_ids = [f["_id"] for f in all_fields if "_id" in f]
            
            client.boards.reorder_fields(state["board_id"], {"fields": field_ids})
            log_result("Reordered Fields", True)

            client.boards.bulk_update_fields(state["board_id"], {
                "fields": [{"_id": state["field_id"], "name": "Test Field Bulk", "type": "ShortText"}]
            })
            log_result("Bulk Updated Fields", True)

    run_test_section("Field Lifecycle", field_lifecycle)

    # 3. Items
    def item_lifecycle():
        if not state["board_id"]: return
        board = client.boards.get(state["board_id"])
        id_field = next((f for f in board.get("fields", []) if f.get("is_identifier")), None)
        if id_field:
            item = client.boards.create_item(state["board_id"], {
                "fields": [{"board_field_id": id_field["_id"], "value": "SDK Test Item"}]
            })
            state["item_id"] = item.get("_id") or item.get("id")
            log_result("Created Item", state["item_id"])

            client.boards.list_items(state["board_id"], limit=5)
            client.boards.get_item(state["board_id"], state["item_id"])
            client.boards.update_item(state["board_id"], state["item_id"], {
                "data": [{"key": id_field["_id"], "value": "SDK Test Item Updated"}]
            })
            log_result("Item Ops Verified", True)

            client.boards.bulk_delete_items(state["board_id"], {"ids": [state["item_id"]]})
            log_result("Bulk Deleted Items", True)

    run_test_section("Item Lifecycle", item_lifecycle)

    # 4. Segments
    def segment_lifecycle():
        if not state["board_id"]: return
        segment = client.boards.create_segment(state["board_id"], {
            "name": "Test Segment",
            "filter": {}
        })
        segment_id = segment.get("_id") or segment.get("id")
        log_result("Created Segment", segment_id)

        if segment_id:
            client.boards.list_segments(state["board_id"])
            client.boards.update_segment(state["board_id"], segment_id, {"name": "Test Segment Updated"})
            client.boards.delete_segment(state["board_id"], segment_id)
            log_result("Segment Ops Verified", True)
    
    run_test_section("Segments Lifecycle", segment_lifecycle)

    # 5. Cleanup & Board Reorder
    def cleanup_and_reorder():
        if state["board_id"]:
            client.boards.reorder({"order": [state["board_id"]]})
            log_result("Reordered Boards", True)

            client.boards.delete(state["board_id"])
            print("   Board deleted.")
    run_test_section("Board Cleanup & Reorder", cleanup_and_reorder)

    # 6. Misc Board functions
    def misc_board_ops():
        try:
            preview = client.boards.get_link_preview("https://google.com")
            log_result("Link Preview", preview.get("url"))
        except:
            print("   [Skip] get_link_preview failed")

        try:
            # Need a folder_id for search_files in PY
            folders = client.boards.search_folders()
            if folders:
                files = client.boards.search_files(folders[0]["_id"])
                log_result("Search Files", len(files))
        except:
            print("   [Skip] search_files failed")

        try:
            res = client.boards.check_conflict("dummy", "dummy", {"organization_id": organization_id})
            log_result("Conflict Check", res)
        except:
            print("   [Skip] check_conflict failed")
    
    run_test_section("Misc Board Ops", misc_board_ops)

    # 7. Folders
    def folder_ops():
        folders = client.boards.search_folders()
        log_result("Folders", folders)

        folder = client.boards.create_folder({
            "name": f"SDK_PY_FOLDER_TEST_{int(time.time())}",
            "organization_id": organization_id,
            "parent_id": "root",
            "source_type": "upload"
        })
        state["folder_id"] = folder.get("_id") or folder.get("id")
        log_result("Created Folder", state["folder_id"])

        if state["folder_id"]:
            client.boards.delete_folders(ids=[state["folder_id"]])
            print("   Folder deleted.")
    run_test_section("Folder Ops", folder_ops)

    print("\n✅ Boards Resource Testing Completed.")

if __name__ == "__main__":
    test_boards()
