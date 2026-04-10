"""Tests for AiResource (sync)."""
import json
import pytest
from pytest_httpx import HTTPXMock

from imbrace import ImbraceClient

BASE = "https://app-gatewayv2.imbrace.co"
AI_BASE = f"{BASE}/ai"

MESSAGES = [{"role": "user", "content": "Hello"}]


@pytest.fixture
def client():
    c = ImbraceClient(api_key="key_test")
    yield c
    c.close()


def test_complete(httpx_mock: HTTPXMock, client: ImbraceClient):
    payload = {
        "id": "cmpl_1",
        "model": "gpt-4o",
        "choices": [{"index": 0, "message": {"role": "assistant", "content": "Hi"}}],
    }
    httpx_mock.add_response(url=f"{AI_BASE}/completions", json=payload)

    result = client.ai.complete(model="gpt-4o", messages=MESSAGES)
    assert result["id"] == "cmpl_1"

    request = httpx_mock.get_requests()[0]
    body = json.loads(request.content)
    assert body["stream"] is False
    assert body["model"] == "gpt-4o"


def test_complete_with_params(httpx_mock: HTTPXMock, client: ImbraceClient):
    httpx_mock.add_response(url=f"{AI_BASE}/completions", json={"id": "cmpl_2"})

    client.ai.complete(model="gpt-4o", messages=MESSAGES, temperature=0.7, max_tokens=512)

    request = httpx_mock.get_requests()[0]
    body = json.loads(request.content)
    assert body["temperature"] == 0.7
    assert body["max_tokens"] == 512


def test_embed(httpx_mock: HTTPXMock, client: ImbraceClient):
    payload = {
        "model": "text-embedding-3-small",
        "data": [{"index": 0, "embedding": [0.1, 0.2, 0.3], "object": "embedding"}],
    }
    httpx_mock.add_response(url=f"{AI_BASE}/embeddings", json=payload)

    result = client.ai.embed(model="text-embedding-3-small", input=["hello world"])
    assert result["data"][0]["embedding"] == [0.1, 0.2, 0.3]

    request = httpx_mock.get_requests()[0]
    body = json.loads(request.content)
    assert body["input"] == ["hello world"]
