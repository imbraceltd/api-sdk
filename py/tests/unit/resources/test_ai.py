"""Tests for AiResource — AI completion and streaming."""
import json
import pytest
from pytest_httpx import HTTPXMock
from imbrace import ImbraceClient
from imbrace.types.ai import CompletionInput, EmbeddingInput

GW = "https://app-gatewayv2.imbrace.co"
AI = f"{GW}/v3/ai"

@pytest.fixture
def client():
    return ImbraceClient(api_key="test_key")

def test_complete(httpx_mock: HTTPXMock, client):
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
    httpx_mock.add_response(url=f"{AI}/completions", method="POST", json=payload)
    
    result = client.ai.complete(CompletionInput(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hi"}]
    ))
    assert result.choices[0].message.content == "Hello!"

def test_embed(httpx_mock: HTTPXMock, client):
    payload = {
        "model": "text-embedding-3-small",
        "data": [{"index": 0, "embedding": [0.1, 0.2], "object": "embedding"}]
    }
    httpx_mock.add_response(url=f"{AI}/embeddings", method="POST", json=payload)
    
    result = client.ai.embed(EmbeddingInput(model="text-embedding-3-small", input=["hello"]))
    assert result.data[0].embedding == [0.1, 0.2]
