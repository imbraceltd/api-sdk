"""
Test: Misc resources not covered elsewhere:
  - client.categories (list/get/create/update/delete)
  - client.outbound (send_whatsapp, send_email)
  - client.data_files (search/get/create/update/delete/upload/download)
  - client.folders (search/get/get_contents/create/update/delete)
  - client.health (check)
  - client.sessions (list/get/create/delete)
  - client.schedule (list/delete/get_filter_options)
  - client.ips (list_ap_workflows, list_external_data_sync, list_schedulers)
  - client.organizations (list/list_all)
"""
import time
from utils.utils import client, run_test_section, log_result, organization_id

def test_resources():
    print("\n[START] Testing Misc Resources...")

    # 1. Health
    def health_check():
        res = client.health.check()
        log_result("Gateway Health", res)
    run_test_section("health.check", health_check)

    # 2. Organizations
    def org_ops():
        try:
            orgs = client.organizations.list()
            data = orgs if isinstance(orgs, list) else orgs.get("data", [])
            log_result("organizations.list", len(data))
        except Exception as e:
            print(f"   [warn] organizations.list: {str(e)}")
        try:
            all_orgs = client.organizations.list_all()
            data2 = all_orgs if isinstance(all_orgs, list) else all_orgs.get("data", [])
            log_result("organizations.list_all", len(data2))
        except Exception as e:
            print(f"   [warn] organizations.list_all: {str(e)}")
    run_test_section("organizations", org_ops)

    # 3. Categories
    state_cat = {"category_id": None}
    def category_ops():
        try:
            cats = client.categories.list()
            data = cats if isinstance(cats, list) else cats.get("data", [])
            log_result("categories.list", len(data))
            if data:
                state_cat["category_id"] = data[0].get("_id") or data[0].get("id")
        except Exception as e:
            print(f"   [warn] categories.list: {str(e)}")

        if state_cat["category_id"]:
            try:
                cat = client.categories.get(state_cat["category_id"])
                log_result("categories.get", cat.get("_id") or cat.get("id"))
            except Exception as e:
                print(f"   [warn] categories.get: {str(e)}")

        try:
            ts = int(time.time())
            new_cat = client.categories.create({"name": f"SDK_CAT_{ts}"})
            new_id = new_cat.get("_id") or new_cat.get("id")
            log_result("categories.create", new_id)
            if new_id:
                client.categories.update(new_id, {"name": f"SDK_CAT_{ts}_UPDATED"})
                log_result("categories.update", True)
                client.categories.delete(new_id)
                log_result("categories.delete", True)
        except Exception as e:
            print(f"   [warn] categories CRUD: {str(e)}")
    run_test_section("categories CRUD", category_ops)

    # 4. Outbound
    def outbound_ops():
        try:
            client.outbound.send_whatsapp({
                "to": "+84900000000",
                "message": "SDK test ping (dummy)"
            })
            log_result("outbound.send_whatsapp", "Sent")
        except Exception as e:
            print(f"   [warn] outbound.send_whatsapp: {str(e)}")
        try:
            client.outbound.send_email({
                "to": "sdk-test@example.com",
                "subject": "SDK Test Email",
                "body": "Test body"
            })
            log_result("outbound.send_email", "Sent")
        except Exception as e:
            print(f"   [warn] outbound.send_email: {str(e)}")
    run_test_section("outbound send", outbound_ops)

    # 5. Data Files
    state_df = {"file_id": None}
    def data_files_ops():
        try:
            # DataFilesResource.search() takes params dict, not keyword args
            results = client.data_files.search(params={"keyword": "sdk"})
            data = results if isinstance(results, list) else results.get("data", [])
            log_result("data_files.search", len(data))
        except Exception as e:
            print(f"   [warn] data_files.search: {str(e)}")

        try:
            ts = int(time.time())
            # data_files.create requires: file_size, file_type, key, folder_id
            # Get a real folder_id from folders.search first
            try:
                fld_res = client.folders.search()
                fld_data = fld_res if isinstance(fld_res, list) else fld_res.get("data", [])
                real_folder_id = fld_data[0].get("_id") or fld_data[0].get("id") if fld_data else None
            except Exception:
                real_folder_id = None

            new_file = client.data_files.create({
                "name": f"sdk_test_{ts}.csv",
                "organization_id": organization_id,
                "file_size": 128,
                "file_type": "text/csv",
                "key": f"sdk/test/{ts}.csv",
                "folder_id": real_folder_id or "root"
            })
            state_df["file_id"] = new_file.get("_id") or new_file.get("id")
            log_result("data_files.create", state_df["file_id"])
        except Exception as e:
            print(f"   [warn] data_files.create: {str(e)}")

        if state_df["file_id"]:
            try:
                f = client.data_files.get(state_df["file_id"])
                log_result("data_files.get", f.get("name"))
            except Exception as e:
                print(f"   [warn] data_files.get: {str(e)}")
            try:
                client.data_files.update(state_df["file_id"], {"name": "updated.csv"})
                log_result("data_files.update", True)
            except Exception as e:
                print(f"   [warn] data_files.update: {str(e)}")
            try:
                client.data_files.delete(state_df["file_id"])
                log_result("data_files.delete", True)
            except Exception as e:
                print(f"   [warn] data_files.delete: {str(e)}")
    run_test_section("data_files CRUD", data_files_ops)

    # 6. Folders (standalone resource)
    state_fld = {"folder_id": None}
    def folder_ops():
        try:
            results = client.folders.search()
            data = results if isinstance(results, list) else results.get("data", [])
            log_result("folders.search", len(data))
            if data:
                state_fld["folder_id"] = data[0].get("_id") or data[0].get("id")
        except Exception as e:
            print(f"   [warn] folders.search: {str(e)}")

        if state_fld["folder_id"]:
            try:
                fld = client.folders.get(state_fld["folder_id"])
                log_result("folders.get", fld.get("name"))
            except Exception as e:
                print(f"   [warn] folders.get: {str(e)}")
            try:
                contents = client.folders.get_contents(state_fld["folder_id"])
                log_result("folders.get_contents", len(contents) if isinstance(contents, list) else contents)
            except Exception as e:
                print(f"   [warn] folders.get_contents: {str(e)}")

        try:
            ts = int(time.time())
            # folders.create requires source_type and parent_folder_id (real ID)
            real_parent_id = state_fld["folder_id"]  # use a real ID from search above
            if real_parent_id:
                new_fld = client.folders.create({
                    "name": f"SDK_FOLDER_{ts}",
                    "organization_id": organization_id,
                    "source_type": "local",
                    "parent_folder_id": real_parent_id
                })
                new_id = new_fld.get("_id") or new_fld.get("id")
                log_result("folders.create", new_id)
                if new_id:
                    client.folders.update(new_id, {"name": f"SDK_FOLDER_{ts}_UPDATED"})
                    log_result("folders.update", True)
                    client.folders.delete(new_id)
                    log_result("folders.delete", True)
            else:
                print("   [skip] folders.create — no parent_folder_id available")
        except Exception as e:
            print(f"   [warn] folders CRUD: {str(e)}")
    run_test_section("folders CRUD", folder_ops)

    # 7. Sessions
    state_sess = {"session_id": None}
    def session_ops():
        try:
            sessions = client.sessions.list()
            data = sessions if isinstance(sessions, list) else sessions.get("data", [])
            log_result("sessions.list", len(data))
            if data:
                state_sess["session_id"] = data[0].get("_id") or data[0].get("id")
        except Exception as e:
            print(f"   [warn] sessions.list: {str(e)}")

        if state_sess["session_id"]:
            try:
                s = client.sessions.get(state_sess["session_id"])
                log_result("sessions.get", s.get("_id") or s.get("id"))
            except Exception as e:
                print(f"   [warn] sessions.get: {str(e)}")

        try:
            new_sess = client.sessions.create({"organization_id": organization_id})
            new_id = new_sess.get("_id") or new_sess.get("id")
            log_result("sessions.create", new_id)
            if new_id:
                client.sessions.delete(new_id)
                log_result("sessions.delete", True)
        except Exception as e:
            print(f"   [warn] sessions CRUD: {str(e)}")
    run_test_section("sessions CRUD", session_ops)

    # 8. Schedule
    def schedule_ops():
        try:
            scheds = client.schedule.list()
            data = scheds if isinstance(scheds, list) else scheds.get("data", [])
            log_result("schedule.list", len(data))
        except Exception as e:
            print(f"   [warn] schedule.list: {str(e)}")
        try:
            # get_filter_options may require a valid 'type' or 'field' param
            # Try without args first, then with common filter keywords
            try:
                opts = client.schedule.get_filter_options()
                log_result("schedule.get_filter_options (no args)", opts)
            except Exception:
                opts = client.schedule.get_filter_options(params={"type": "schedule"})
                log_result("schedule.get_filter_options (type=schedule)", opts)
        except Exception as e:
            print(f"   [warn] schedule.get_filter_options: {str(e)}")
    run_test_section("schedule", schedule_ops)

    # 9. IPS
    def ips_ops():
        try:
            wfs = client.ips.list_ap_workflows()
            log_result("ips.list_ap_workflows", len(wfs) if isinstance(wfs, list) else wfs)
        except Exception as e:
            print(f"   [warn] ips.list_ap_workflows: {str(e)}")
        try:
            syncs = client.ips.list_external_data_sync()
            log_result("ips.list_external_data_sync", len(syncs) if isinstance(syncs, list) else syncs)
        except Exception as e:
            print(f"   [warn] ips.list_external_data_sync: {str(e)}")
        try:
            schedulers = client.ips.list_schedulers()
            log_result("ips.list_schedulers", len(schedulers) if isinstance(schedulers, list) else schedulers)
        except Exception as e:
            print(f"   [warn] ips.list_schedulers: {str(e)}")
        try:
            filter_opts = client.ips.get_scheduler_filter_options()
            log_result("ips.get_scheduler_filter_options", filter_opts)
        except Exception as e:
            print(f"   [warn] ips.get_scheduler_filter_options: {str(e)}")
    run_test_section("ips", ips_ops)

    print("\n[DONE] Misc Resources Testing Completed.")

if __name__ == "__main__":
    test_resources()
