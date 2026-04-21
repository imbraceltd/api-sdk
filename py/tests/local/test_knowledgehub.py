"""
KnowledgeHub resource test — sync + async, runs against prodv2 gateway (data-board service).
Usage:
    pip install -e ".[dev]"
    python tests/local/test_knowledgehub.py

Notes:
  - data-board wraps all responses: { success, message, data } — SDK unwraps .data
  - createFolder requires organization_id, parent_folder_id, source_type (DB schema required)
  - getFolder returns { data: { folder, files } } — SDK unwraps to data["folder"]
  - delete_folders body uses { ids: [...] }
  - createFile needs actual file metadata (key, file_size, file_type) — skip in tests
"""
import os
import asyncio
from imbrace import ImbraceClient
from imbrace.async_client import AsyncImbraceClient

ACCESS_TOKEN = os.environ.get("IMBRACE_ACCESS_TOKEN", "acc_c8c27f3b-e147-4735-b641-61e8d3706692")
GATEWAY = os.environ.get("IMBRACE_GATEWAY_URL", "https://app-gatewayv2.imbrace.co")

passed = 0
failed = 0
skipped = 0


def ok(label, detail=""):
    global passed
    detail_str = f"  →  {str(detail)[:100]}" if detail else ""
    print(f"  ✓ {label}{detail_str}")
    passed += 1


def fail(label, err):
    global failed
    print(f"  ✗ {label}: {err}")
    failed += 1


def skip(label, reason):
    global skipped
    print(f"  - {label}  (skipped: {reason})")
    skipped += 1


# ── Sync Tests ────────────────────────────────────────────────────────────────

def test_sync():
    created = {"org_id": None, "folder_id": None, "sub_folder_id": None, "existing_folder_id": None, "existing_file_id": None}
    client = ImbraceClient(access_token=ACCESS_TOKEN, gateway=GATEWAY)
    boards = client.boards

    print("\n[1] Search folders (sync)")
    try:
        folders = boards.search_folders()
        if folders and isinstance(folders, list) and len(folders) > 0:
            created["org_id"] = folders[0].get("organization_id")
            created["existing_folder_id"] = folders[0].get("_id")
        ok("search_folders()", f"{len(folders)} folders  org={created['org_id']}")
    except Exception as e:
        fail("search_folders()", e)

    print("\n[2] Create folder (sync)")
    if not created["org_id"]:
        skip("create_folder()", "no org_id from search_folders")
    else:
        try:
            folder = boards.create_folder({
                "name": "SDK Python Test Folder",
                "organization_id": created["org_id"],
                "parent_folder_id": "root",
                "source_type": "upload",
            })
            created["folder_id"] = folder.get("_id")
            ok("create_folder()", f"id={created['folder_id']}")
        except Exception as e:
            fail("create_folder()", e)

    print("\n[3] Get folder (sync)")
    if not created["folder_id"]:
        skip("get_folder()", "no folder created")
    else:
        try:
            folder = boards.get_folder(created["folder_id"])
            ok("get_folder()", f"id={folder.get('_id')} name={folder.get('name')}")
        except Exception as e:
            fail("get_folder()", e)

    print("\n[4] Folder contents (sync)")
    if not created["folder_id"]:
        skip("get_folder_contents()", "no folder created")
    else:
        try:
            contents = boards.get_folder_contents(created["folder_id"])
            ok("get_folder_contents()", f"files={len(contents.get('files', []))} subfolders={len(contents.get('subfolders', []))}")
        except Exception as e:
            fail("get_folder_contents()", e)

    print("\n[5] Update folder (sync)")
    if not created["folder_id"]:
        skip("update_folder()", "no folder created")
    else:
        try:
            folder = boards.update_folder(created["folder_id"], {"name": "SDK Python Test Folder Updated"})
            ok("update_folder()", f"name={folder.get('name')}")
        except Exception as e:
            fail("update_folder()", e)

    print("\n[6] Create sub-folder (sync)")
    if not created["folder_id"] or not created["org_id"]:
        skip("create_folder() sub", "no parent folder")
    else:
        try:
            sub = boards.create_folder({
                "name": "SDK Python Test Sub-Folder",
                "organization_id": created["org_id"],
                "parent_folder_id": created["folder_id"],
                "source_type": "upload",
            })
            created["sub_folder_id"] = sub.get("_id")
            ok("create_folder() sub", f"id={created['sub_folder_id']}")
        except Exception as e:
            fail("create_folder() sub", e)

    print("\n[7] Search files (sync)")
    if not created["existing_folder_id"]:
        skip("search_files()", "no existing folder")
    else:
        try:
            files = boards.search_files(created["existing_folder_id"])
            if files and isinstance(files, list) and len(files) > 0:
                created["existing_file_id"] = files[0].get("_id")
            ok("search_files()", f"{len(files)} files")
        except Exception as e:
            fail("search_files()", e)

    print("\n[8] Get file (sync)")
    if not created["existing_file_id"]:
        skip("get_file()", "no file from search_files")
    else:
        try:
            f = boards.get_file(created["existing_file_id"])
            ok("get_file()", f"id={f.get('_id')} name={f.get('name')}")
        except Exception as e:
            fail("get_file()", e)

    print("\n[9] Cleanup folders (sync)")
    ids_to_delete = [x for x in [created["sub_folder_id"], created["folder_id"]] if x]
    if not ids_to_delete:
        skip("delete_folders()", "no folders created")
    else:
        try:
            res = boards.delete_folders(ids_to_delete)
            ok("delete_folders()", str(res)[:80])
            created["folder_id"] = None
            created["sub_folder_id"] = None
        except Exception as e:
            fail("delete_folders()", e)


# ── Async Tests ───────────────────────────────────────────────────────────────

async def test_async():
    created = {"org_id": None, "folder_id": None, "existing_folder_id": None, "existing_file_id": None}
    client = AsyncImbraceClient(access_token=ACCESS_TOKEN, gateway=GATEWAY)
    boards = client.boards

    print("\n[10] Search folders (async)")
    try:
        folders = await boards.search_folders()
        if folders and isinstance(folders, list) and len(folders) > 0:
            created["org_id"] = folders[0].get("organization_id")
            created["existing_folder_id"] = folders[0].get("_id")
        ok("async search_folders()", f"{len(folders)} folders")
    except Exception as e:
        fail("async search_folders()", e)

    print("\n[11] Create + Get + Delete folder (async)")
    if not created["org_id"]:
        skip("async folder CRUD", "no org_id")
    else:
        try:
            folder = await boards.create_folder({
                "name": "SDK Python Async Test Folder",
                "organization_id": created["org_id"],
                "parent_folder_id": "root",
                "source_type": "upload",
            })
            created["folder_id"] = folder.get("_id")
            ok("async create_folder()", f"id={created['folder_id']}")

            fetched = await boards.get_folder(created["folder_id"])
            ok("async get_folder()", f"id={fetched.get('_id')} name={fetched.get('name')}")

            contents = await boards.get_folder_contents(created["folder_id"])
            ok("async get_folder_contents()", f"files={len(contents.get('files', []))}")
        except Exception as e:
            fail("async folder CRUD", e)

    print("\n[12] Search + Get file (async)")
    if not created["existing_folder_id"]:
        skip("async file read", "no existing folder")
    else:
        try:
            files = await boards.search_files(created["existing_folder_id"])
            ok("async search_files()", f"{len(files)} files")
            if files:
                f = await boards.get_file(files[0].get("_id"))
                ok("async get_file()", f"id={f.get('_id')} name={f.get('name')}")
            else:
                skip("async get_file()", "no files in folder")
        except Exception as e:
            fail("async file read", e)

    print("\n[13] Async cleanup")
    if created["folder_id"]:
        try:
            res = await boards.delete_folders([created["folder_id"]])
            ok("async delete_folders()", str(res)[:60])
        except Exception as e:
            fail("async delete_folders()", e)

    await client.close()


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    test_sync()
    asyncio.run(test_async())

    print(f"\n{'─' * 55}")
    print(f"  {passed} passed  |  {failed} failed  |  {skipped} skipped")
    if failed > 0:
        raise SystemExit(1)
