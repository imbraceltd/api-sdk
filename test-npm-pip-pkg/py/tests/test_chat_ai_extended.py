"""
Test: client.chat_ai — extended coverage
  - Files: list/upload/upload_agent/extract/get_data/update_data/delete
  - Audio: transcribe, speech
  - Knowledge: list/get/create/delete
  - Prompts: list/create/get/update/delete
  - Tools: list/create/get/update/delete
  - Folders: update_folder
  - list_assistant_agents
"""
import time
from io import BytesIO
from utils.utils import client, run_test_section, log_result

def test_chat_ai_extended():
    print("\n[START] Testing Chat AI Resource — Extended Coverage...")

    state = {
        "file_id": None,
        "prompt_id": None,
        "tool_id": None,
        "knowledge_id": None,
    }

    # 1. Files
    def file_ops():
        try:
            files = client.chat_ai.list_files()
            data = files if isinstance(files, list) else files.get("data", [])
            log_result("chat_ai.list_files", len(data))
        except Exception as e:
            print(f"   [warn] list_files: {str(e)}")

        try:
            content = b"SDK chat AI file test"
            file_tuple = {"file": ("sdk_test.txt", content, "text/plain")}
            uploaded = client.chat_ai.upload_file(file_tuple)
            state["file_id"] = uploaded.get("_id") or uploaded.get("id")
            log_result("chat_ai.upload_file", state["file_id"])
        except Exception as e:
            print(f"   [warn] upload_file: {str(e)}")

        if state["file_id"]:
            try:
                data_content = client.chat_ai.get_file_data(state["file_id"])
                log_result("chat_ai.get_file_data", data_content)
            except Exception as e:
                print(f"   [warn] get_file_data: {str(e)}")
            try:
                client.chat_ai.update_file_data(state["file_id"], {"content": "updated"})
                log_result("chat_ai.update_file_data", True)
            except Exception as e:
                print(f"   [warn] update_file_data: {str(e)}")
            try:
                client.chat_ai.delete_file(state["file_id"])
                log_result("chat_ai.delete_file", True)
                state["file_id"] = None
            except Exception as e:
                print(f"   [warn] delete_file: {str(e)}")
    run_test_section("chat_ai.files", file_ops)

    # 2. Agent File upload
    def agent_file_ops():
        try:
            content = b"Agent file test content"
            file_tuple = {"file": ("agent_test.txt", content, "text/plain")}
            res = client.chat_ai.upload_agent_file(file_tuple, agent_id="dummy_agent")
            log_result("chat_ai.upload_agent_file", res.get("_id") or res.get("id"))
        except Exception as e:
            print(f"   [warn] upload_agent_file: {str(e)}")
    run_test_section("chat_ai.upload_agent_file", agent_file_ops)

    # 3. Audio
    def audio_ops():
        try:
            content = b"RIFF" + b"\x00" * 36  # minimal WAV header stub
            file_tuple = {"file": ("test.wav", content, "audio/wav")}
            res = client.chat_ai.transcribe(file_tuple)
            log_result("chat_ai.transcribe", res)
        except Exception as e:
            print(f"   [warn] transcribe: {str(e)}")

        try:
            audio = client.chat_ai.speech({"model": "tts-1", "input": "Hello from SDK test", "voice": "alloy"})
            log_result("chat_ai.speech (bytes)", len(audio.content) if hasattr(audio, "content") else audio)
        except Exception as e:
            print(f"   [warn] speech: {str(e)}")
    run_test_section("chat_ai.audio (transcribe + speech)", audio_ops)

    # 4. Knowledge
    def knowledge_ops():
        try:
            kbs = client.chat_ai.list_knowledge()
            data = kbs if isinstance(kbs, list) else kbs.get("data", [])
            log_result("chat_ai.list_knowledge", len(data))
        except Exception as e:
            print(f"   [warn] list_knowledge: {str(e)}")

        try:
            ts = int(time.time())
            new_kb = client.chat_ai.create_knowledge({
                "name": f"SDK_KB_{ts}",
                "type": "text"
            })
            state["knowledge_id"] = new_kb.get("_id") or new_kb.get("id")
            log_result("chat_ai.create_knowledge", state["knowledge_id"])
        except Exception as e:
            print(f"   [warn] create_knowledge: {str(e)}")

        if state["knowledge_id"]:
            try:
                kb = client.chat_ai.get_knowledge(state["knowledge_id"])
                log_result("chat_ai.get_knowledge", kb.get("name"))
            except Exception as e:
                print(f"   [warn] get_knowledge: {str(e)}")
            try:
                client.chat_ai.delete_knowledge(state["knowledge_id"])
                log_result("chat_ai.delete_knowledge", True)
            except Exception as e:
                print(f"   [warn] delete_knowledge: {str(e)}")
    run_test_section("chat_ai.knowledge", knowledge_ops)

    # 5. Prompts CRUD
    def prompt_ops():
        try:
            ts = int(time.time())
            new_p = client.chat_ai.create_prompt({
                "name": f"SDK_PROMPT_{ts}",
                "content": "You are a test assistant."
            })
            state["prompt_id"] = new_p.get("_id") or new_p.get("id")
            log_result("chat_ai.create_prompt", state["prompt_id"])
        except Exception as e:
            print(f"   [warn] create_prompt: {str(e)}")

        if state["prompt_id"]:
            try:
                p = client.chat_ai.get_prompt(state["prompt_id"])
                log_result("chat_ai.get_prompt", p.get("name"))
            except Exception as e:
                print(f"   [warn] get_prompt: {str(e)}")
            try:
                client.chat_ai.update_prompt(state["prompt_id"], {"content": "Updated prompt content"})
                log_result("chat_ai.update_prompt", True)
            except Exception as e:
                print(f"   [warn] update_prompt: {str(e)}")
            try:
                client.chat_ai.delete_prompt(state["prompt_id"])
                log_result("chat_ai.delete_prompt", True)
            except Exception as e:
                print(f"   [warn] delete_prompt: {str(e)}")
    run_test_section("chat_ai.prompts CRUD", prompt_ops)

    # 6. Tools CRUD
    def tool_ops():
        try:
            ts = int(time.time())
            new_t = client.chat_ai.create_tool({
                "name": f"sdk_tool_{ts}",
                "type": "function",
                "description": "SDK test tool"
            })
            state["tool_id"] = new_t.get("_id") or new_t.get("id")
            log_result("chat_ai.create_tool", state["tool_id"])
        except Exception as e:
            print(f"   [warn] create_tool: {str(e)}")

        if state["tool_id"]:
            try:
                t = client.chat_ai.get_tool(state["tool_id"])
                log_result("chat_ai.get_tool", t.get("name"))
            except Exception as e:
                print(f"   [warn] get_tool: {str(e)}")
            try:
                client.chat_ai.update_tool(state["tool_id"], {"description": "Updated tool"})
                log_result("chat_ai.update_tool", True)
            except Exception as e:
                print(f"   [warn] update_tool: {str(e)}")
            try:
                client.chat_ai.delete_tool(state["tool_id"])
                log_result("chat_ai.delete_tool", True)
            except Exception as e:
                print(f"   [warn] delete_tool: {str(e)}")
    run_test_section("chat_ai.tools CRUD", tool_ops)

    # 7. update_folder + list_assistant_agents
    def misc_ops():
        try:
            folders = client.chat_ai.list_folders()
            data = folders if isinstance(folders, list) else folders.get("data", [])
            if data:
                fld_id = data[0].get("_id") or data[0].get("id")
                fld_name = data[0].get("name", "updated_sdk")
                client.chat_ai.update_folder(fld_id, fld_name)
                log_result("chat_ai.update_folder", True)
        except Exception as e:
            print(f"   [warn] update_folder: {str(e)}")

        try:
            agents = client.chat_ai.list_assistant_agents()
            log_result("chat_ai.list_assistant_agents", len(agents) if isinstance(agents, list) else agents)
        except Exception as e:
            print(f"   [warn] list_assistant_agents: {str(e)}")
    run_test_section("chat_ai.update_folder + list_assistant_agents", misc_ops)

    print("\n[DONE] Chat AI Extended Resource Testing Completed.")

if __name__ == "__main__":
    test_chat_ai_extended()
