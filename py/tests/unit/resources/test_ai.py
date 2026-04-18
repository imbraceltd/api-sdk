"""Tests for AiResource — AI completion and streaming."""
import json
import pytest
from pytest_httpx import HTTPXMock
from imbrace import ImbraceClient

GW = "https://app-gateway.imbrace.co"
AI = f"{GW}/ai"

@pytest.fixture
def client():
    return ImbraceClient(api_key="test_key")

def test_complete(httpx_mock: HTTPXMock, client):
    # Cập nhật payload với đầy đủ các trường bắt buộc của Pydantic Completion model
    payload = {
        "id": "chat_123",
        "model": "gpt-4o",
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": "Hello!"},
                "finish_reason": "stop"
            }
        ],
        "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15}
    }
    httpx_mock.add_response(url=f"{AI}/v3/completions", json=payload)
    
    result = client.ai.complete(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hi"}]
    )
    # Truy cập qua object property thay vì subscript
    assert result.choices[0].message.content == "Hello!"
    req = httpx_mock.get_requests()[0]
    assert req.method == "POST"

def test_embed(httpx_mock: HTTPXMock, client):
    # Cập nhật payload cho Embedding model
    payload = {
        "model": "text-embedding-3-small",
        "data": [{"index": 0, "embedding": [0.1, 0.2], "object": "embedding"}]
    }
    httpx_mock.add_response(url=f"{AI}/v3/embeddings", json=payload)
    
    result = client.ai.embed(model="text-embedding-3-small", input=["hello"])
    assert result.data[0].embedding == [0.1, 0.2]
