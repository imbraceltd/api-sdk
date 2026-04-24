import time
from io import BytesIO
from utils.utils import client, run_test_section, log_result, organization_id

def test_multimedia_ai():
    print("\n🚀 STARTING: MULTIMEDIA AI TEST (PY)")

    # 1. OCR (Extract File)
    def ocr_ops():
        files = {"file": ("test.txt", BytesIO(b"Hello from SDK OCR test."), "text/plain")}
        try:
            res = client.chat_ai.extract_file(files)
            log_result("Extracted Content", res)
        except Exception as e:
            print(f"   ⚠️ Extract file failed: {str(e)}")
    run_test_section("OCR (Extract File)", ocr_ops)

    # 2. STT (Transcribe)
    def stt_ops():
        files = {"file": ("test.wav", BytesIO(b"dummy audio"), "audio/wav")}
        try:
            res = client.chat_ai.transcribe(files)
            log_result("Transcribed Text", res.get("text"))
        except Exception as e:
            print(f"   ⚠️ Transcribe failed: {str(e)}")
    run_test_section("STT (Transcribe)", stt_ops)

    # 3. TTS (Speech)
    def tts_ops():
        try:
            res = client.chat_ai.speech({
                "model": "tts-1",
                "input": "Hello from Python SDK",
                "voice": "alloy"
            })
            if res.status_code == 200:
                log_result("Generated Speech", f"Success ({len(res.content)} bytes)")
            else:
                print(f"   ⚠️ Speech failed: {res.status_code}")
        except Exception as e:
            print(f"   ⚠️ Speech failed: {str(e)}")
    run_test_section("TTS (Speech)", tts_ops)

    # 4. Document AI
    def doc_ai_ops():
        models = client.chat_ai.list_document_models()
        log_result("Doc AI Models", len(models))
        if models:
            try:
                res = client.chat_ai.process_document(
                    model_name=models[0].get("name") or models[0].get("id"),
                    url="https://imbrace.co/favicon.png",
                    organization_id=organization_id,
                    additional_instructions="What is this?"
                )
                log_result("Doc AI Result", res.get("success"))
            except Exception as e:
                print(f"   ⚠️ Doc AI failed: {str(e)}")
    run_test_section("Document AI", doc_ai_ops)

    print("\n✅ Multimedia AI Test Completed.")

if __name__ == "__main__":
    test_multimedia_ai()
