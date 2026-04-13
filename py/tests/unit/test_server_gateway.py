"""Unit tests for Server Gateway resources."""
import pytest
from pytest_httpx import HTTPXMock

from imbrace.core.auth.token_manager import TokenManager
from imbrace.core.http import HttpTransport, AsyncHttpTransport
from imbrace.server.resources.boards import BoardsResource, AsyncBoardsResource
from imbrace.server.resources.ai_agent import AiAgentResource, AsyncAiAgentResource
from imbrace.server.resources.categories import CategoriesResource, AsyncCategoriesResource
from imbrace.server.resources.schedule import ScheduleResource
from imbrace.server.resources.marketplace import MarketplaceResource, AsyncMarketplaceResource

BASE = "https://api.imbrace.co"


@pytest.fixture
def http():
    tm = TokenManager("srv_key")
    return HttpTransport(token_manager=tm, timeout=5, api_key="srv_key")


@pytest.fixture
def async_http():
    tm = TokenManager("srv_key")
    return AsyncHttpTransport(token_manager=tm, timeout=5, api_key="srv_key")


# ─── Server Boards ────────────────────────────────────────────────────────────

class TestServerBoards:
    def test_search(self, httpx_mock: HTTPXMock, http: HttpTransport):
        httpx_mock.add_response(
            url=f"{BASE}/3rd/board_search/board_1/search",
            json={"hits": [], "total": 0},
        )
        resource = BoardsResource(http, BASE)
        result = resource.search("board_1", q="hello")
        assert result["total"] == 0

        req = httpx_mock.get_requests()[0]
        assert req.method == "POST"
        assert "board_search/board_1/search" in str(req.url)

    def test_list_items(self, httpx_mock: HTTPXMock, http: HttpTransport):
        httpx_mock.add_response(
            url=f"{BASE}/3rd/boards/board_1/board_items?limit=20&skip=0",
            json={"items": []},
        )
        resource = BoardsResource(http, BASE)
        result = resource.list_items("board_1")
        assert "items" in result

    def test_create_items(self, httpx_mock: HTTPXMock, http: HttpTransport):
        httpx_mock.add_response(
            url=f"{BASE}/3rd/boards/create/board_1/board_items",
            json={"created": 2},
        )
        resource = BoardsResource(http, BASE)
        result = resource.create_items("board_1", [{"name": "a"}, {"name": "b"}])
        assert result["created"] == 2

        req = httpx_mock.get_requests()[0]
        assert req.method == "POST"
        import json
        body = json.loads(req.content)
        assert len(body["items"]) == 2

    def test_update_items(self, httpx_mock: HTTPXMock, http: HttpTransport):
        httpx_mock.add_response(
            url=f"{BASE}/3rd/boards/update/board_1/board_items",
            json={"updated": 1},
        )
        resource = BoardsResource(http, BASE)
        result = resource.update_items("board_1", [{"id": "x", "name": "new"}])
        assert result["updated"] == 1
        assert httpx_mock.get_requests()[0].method == "PUT"

    def test_delete_items(self, httpx_mock: HTTPXMock, http: HttpTransport):
        httpx_mock.add_response(
            url=f"{BASE}/3rd/boards/delete/board_1/board_items",
            json={"deleted": 1},
        )
        resource = BoardsResource(http, BASE)
        result = resource.delete_items("board_1", ["item_1"])
        assert result["deleted"] == 1

    def test_export_csv(self, httpx_mock: HTTPXMock, http: HttpTransport):
        httpx_mock.add_response(
            url=f"{BASE}/3rd/boards/board_1/export_csv",
            text="id,name\n1,foo\n",
        )
        resource = BoardsResource(http, BASE)
        result = resource.export_csv("board_1")
        assert "id,name" in result

    @pytest.mark.asyncio
    async def test_async_create_items(self, httpx_mock: HTTPXMock, async_http: AsyncHttpTransport):
        httpx_mock.add_response(
            url=f"{BASE}/3rd/boards/create/board_2/board_items",
            json={"created": 3},
        )
        resource = AsyncBoardsResource(async_http, BASE)
        result = await resource.create_items("board_2", [{"x": 1}, {"x": 2}, {"x": 3}])
        assert result["created"] == 3

    @pytest.mark.asyncio
    async def test_async_search(self, httpx_mock: HTTPXMock, async_http: AsyncHttpTransport):
        httpx_mock.add_response(
            url=f"{BASE}/3rd/board_search/board_1/search",
            json={"hits": [{"id": "a"}], "total": 1},
        )
        resource = AsyncBoardsResource(async_http, BASE)
        result = await resource.search("board_1")
        assert result["total"] == 1


# ─── AI Agent ─────────────────────────────────────────────────────────────────

class TestAiAgent:
    def test_answer_question(self, httpx_mock: HTTPXMock, http: HttpTransport):
        httpx_mock.add_response(
            url=f"{BASE}/3rd/ai-service/rag/answer_question",
            json={"answer": "42"},
        )
        resource = AiAgentResource(http, BASE)
        result = resource.answer_question("What is life?", assistant_id="asst_1")
        assert result["answer"] == "42"

        req = httpx_mock.get_requests()[0]
        import json
        body = json.loads(req.content)
        assert body["text"] == "What is life?"
        assert body["assistant_id"] == "asst_1"
        assert body["role"] == "user"

    def test_answer_question_with_thread(self, httpx_mock: HTTPXMock, http: HttpTransport):
        httpx_mock.add_response(
            url=f"{BASE}/3rd/ai-service/rag/answer_question",
            json={"answer": "yes"},
        )
        resource = AiAgentResource(http, BASE)
        resource.answer_question("Q?", assistant_id="asst_1", thread_id="thr_1")

        import json
        body = json.loads(httpx_mock.get_requests()[0].content)
        assert body["thread_id"] == "thr_1"

    def test_get_file(self, httpx_mock: HTTPXMock, http: HttpTransport):
        httpx_mock.add_response(
            url=f"{BASE}/3rd/ai-service/files/file_1",
            json={"id": "file_1", "name": "doc.pdf"},
        )
        resource = AiAgentResource(http, BASE)
        result = resource.get_file("file_1")
        assert result["id"] == "file_1"

    def test_delete_file(self, httpx_mock: HTTPXMock, http: HttpTransport):
        httpx_mock.add_response(
            url=f"{BASE}/3rd/ai-service/rag/files/file_1",
            json={"deleted": True},
        )
        resource = AiAgentResource(http, BASE)
        result = resource.delete_file("file_1")
        assert result["deleted"] is True
        assert httpx_mock.get_requests()[0].method == "DELETE"

    @pytest.mark.asyncio
    async def test_async_answer_question(self, httpx_mock: HTTPXMock, async_http: AsyncHttpTransport):
        httpx_mock.add_response(
            url=f"{BASE}/3rd/ai-service/rag/answer_question",
            json={"answer": "async answer"},
        )
        resource = AsyncAiAgentResource(async_http, BASE)
        result = await resource.answer_question("?", assistant_id="asst_2")
        assert result["answer"] == "async answer"


# ─── Categories ───────────────────────────────────────────────────────────────

class TestCategories:
    def test_list(self, httpx_mock: HTTPXMock, http: HttpTransport):
        httpx_mock.add_response(
            url=f"{BASE}/3rd/categories?organization_id=org_1",
            json=[{"id": "cat_1", "name": "Sales"}],
        )
        resource = CategoriesResource(http, BASE)
        result = resource.list("org_1")
        assert len(result) == 1
        assert result[0]["name"] == "Sales"

    def test_get(self, httpx_mock: HTTPXMock, http: HttpTransport):
        httpx_mock.add_response(
            url=f"{BASE}/3rd/categories/cat_1",
            json={"id": "cat_1", "name": "Sales"},
        )
        resource = CategoriesResource(http, BASE)
        result = resource.get("cat_1")
        assert result["id"] == "cat_1"

    def test_create(self, httpx_mock: HTTPXMock, http: HttpTransport):
        httpx_mock.add_response(
            url=f"{BASE}/3rd/categories",
            json={"id": "cat_2", "name": "Support"},
        )
        resource = CategoriesResource(http, BASE)
        result = resource.create("org_1", "Support", apply_to=["board"])
        assert result["name"] == "Support"

        req = httpx_mock.get_requests()[0]
        assert req.method == "POST"
        assert req.headers["organization_id"] == "org_1"

    def test_delete(self, httpx_mock: HTTPXMock, http: HttpTransport):
        httpx_mock.add_response(
            url=f"{BASE}/3rd/categories/cat_1",
            json={"deleted": True},
        )
        resource = CategoriesResource(http, BASE)
        result = resource.delete("cat_1")
        assert result["deleted"] is True
        assert httpx_mock.get_requests()[0].method == "DELETE"

    @pytest.mark.asyncio
    async def test_async_list(self, httpx_mock: HTTPXMock, async_http: AsyncHttpTransport):
        httpx_mock.add_response(
            url=f"{BASE}/3rd/categories?organization_id=org_1",
            json=[{"id": "cat_1"}],
        )
        resource = AsyncCategoriesResource(async_http, BASE)
        result = await resource.list("org_1")
        assert result[0]["id"] == "cat_1"


# ─── Schedule ─────────────────────────────────────────────────────────────────

class TestSchedule:
    def test_list(self, httpx_mock: HTTPXMock, http: HttpTransport):
        httpx_mock.add_response(
            url=f"{BASE}/3rd/organization/org_1/users/user_1/schedulers",
            json={"schedulers": []},
        )
        resource = ScheduleResource(http, BASE)
        result = resource.list("org_1", "user_1")
        assert "schedulers" in result

    def test_list_with_event_type(self, httpx_mock: HTTPXMock, http: HttpTransport):
        httpx_mock.add_response(
            url=f"{BASE}/3rd/organization/org_1/users/user_1/schedulers?event_type=meeting",
            json={"schedulers": [{"id": "sch_1"}]},
        )
        resource = ScheduleResource(http, BASE)
        result = resource.list("org_1", "user_1", event_type="meeting")
        assert len(result["schedulers"]) == 1

    @pytest.mark.asyncio
    async def test_async_list(self, httpx_mock: HTTPXMock, async_http: AsyncHttpTransport):
        httpx_mock.add_response(
            url=f"{BASE}/3rd/organization/org_1/users/user_1/schedulers",
            json={"schedulers": [{"id": "sch_1"}]},
        )
        from imbrace.server.resources.schedule import AsyncScheduleResource
        resource = AsyncScheduleResource(async_http, BASE)
        result = await resource.list("org_1", "user_1")
        assert result["schedulers"][0]["id"] == "sch_1"


# ─── Marketplace ──────────────────────────────────────────────────────────────

class TestMarketplace:
    def test_get_email_template(self, httpx_mock: HTTPXMock, http: HttpTransport):
        httpx_mock.add_response(
            url=f"{BASE}/3rd/organization/org_1/marketplaces/email-templates/tpl_1",
            json={"id": "tpl_1", "subject": "Welcome"},
        )
        resource = MarketplaceResource(http, BASE)
        result = resource.get_email_template("org_1", "tpl_1")
        assert result["subject"] == "Welcome"

        req = httpx_mock.get_requests()[0]
        assert req.method == "GET"
        assert "email-templates/tpl_1" in str(req.url)

    @pytest.mark.asyncio
    async def test_async_get_email_template(self, httpx_mock: HTTPXMock, async_http: AsyncHttpTransport):
        httpx_mock.add_response(
            url=f"{BASE}/3rd/organization/org_1/marketplaces/email-templates/tpl_2",
            json={"id": "tpl_2", "subject": "Newsletter"},
        )
        resource = AsyncMarketplaceResource(async_http, BASE)
        result = await resource.get_email_template("org_1", "tpl_2")
        assert result["id"] == "tpl_2"
