import time
from io import BytesIO
from utils.utils import client, run_test_section, log_result

def test_file_service():
    print("\n🚀 Testing File Service Resource...")

    state = {"file_id": None}

    # 1. Upload
    def upload_ops():
        content = b"Hello from SDK File Service test."
        res = client.file_service.upload_file(BytesIO(content))
        state["file_id"] = res.get("id") or res.get("_id")
        log_result("File Uploaded", state["file_id"])

        if state["file_id"]:
            fetched = client.file_service.get_file(state["file_id"])
            log_result("Fetched File", fetched.get("filename"))

    run_test_section("Upload Ops", upload_ops)

    # 2. Search & List
    def search_list():
        files = client.file_service.list_files()
        log_result("Files Count", len(files))

        search = client.file_service.search_files(filename="*.txt")
        log_result("Search Results", len(search))
    run_test_section("Search & List", search_list)

    # 3. Content
    def content_ops():
        if state["file_id"]:
            data_content = client.file_service.get_file_data_content(state["file_id"])
            log_result("File Data Content", data_content.get("content"))

            client.file_service.update_file_data_content(state["file_id"], "Updated content from SDK")
            log_result("Updated Content", True)

            url = client.file_service.get_public_download_url(state["file_id"])
            log_result("Public URL", url)
    run_test_section("Content Ops", content_ops)

    # 4. Cleanup
    def cleanup():
        if state["file_id"]:
            client.file_service.delete_file(state["file_id"])
            log_result("File Deleted", True)
    run_test_section("Cleanup", cleanup)

    print("\n✅ File Service Resource Testing Completed.")

if __name__ == "__main__":
    test_file_service()
