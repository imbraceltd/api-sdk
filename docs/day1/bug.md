PS D:\HUANGJUNFENG\sdk\py> pytest tests/ -m integration -v
===================================== test session starts =====================================
platform win32 -- Python 3.13.0, pytest-9.0.1, pluggy-1.6.0 -- D:\Python\Python313\python.exe
cachedir: .pytest_cache
rootdir: D:\HUANGJUNFENG\sdk\py
configfile: pyproject.toml
plugins: anyio-3.7.1, Faker-40.5.1, asyncio-1.3.0, cov-7.0.0, django-4.12.0, httpx-0.36.0
asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 106 items / 95 deselected / 11 selected

tests/test_integration.py::test_get_account FAILED                                       [  9%]
tests/test_integration.py::test_list_channels FAILED                                     [ 18%]
tests/test_integration.py::test_list_agents FAILED                                       [ 27%]
tests/test_integration.py::test_list_teams FAILED                                        [ 36%]
tests/test_integration.py::test_list_my_teams FAILED                                     [ 45%]
tests/test_integration.py::test_list_contacts FAILED                                     [ 54%]
tests/test_integration.py::test_get_views_count FAILED                                   [ 63%]
tests/test_integration.py::test_list_messages FAILED                                     [ 72%]
tests/test_integration.py::test_list_boards FAILED                                       [ 81%]
tests/test_integration.py::test_list_users FAILED                                        [ 90%]
tests/test_integration.py::test_list_message_templates FAILED                            [100%]

========================================== FAILURES ===========================================
______________________________________ test_get_account _______________________________________

client = <imbrace.client.ImbraceClient object at 0x0000025C2DDC2E40>

    def test_get_account(client):

> result = client.account.get_account()
> ^^^^^^^^^^^^^^^^^^^^^^^^^^
> E       AttributeError: 'AccountResource' object has no attribute 'get_account'

tests\test_integration.py:36: AttributeError
_____________________________________ test_list_channels ______________________________________

client = <imbrace.client.ImbraceClient object at 0x0000025C2DDC2E40>

    def test_list_channels(client):

> result = client.channels.list()
> ^^^^^^^^^^^^^^^
> E       AttributeError: 'ImbraceClient' object has no attribute 'channels'. Did you mean: 'channel'?

tests\test_integration.py:43: AttributeError
______________________________________ test_list_agents _______________________________________

client = <imbrace.client.ImbraceClient object at 0x0000025C2DDC2E40>

    def test_list_agents(client):

> result = client.agent.list()
> ^^^^^^^^^^^^^^^^^^^

tests\test_integration.py:50:

---

src\imbrace\resources\agent.py:13: in list
    return self._http.request("GET", self._base).json()
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

---

self = <imbrace.http.HttpTransport object at 0x0000025C2DDC30E0>, method = 'GET'
url = 'https://app-gatewayv2.imbrace.co/v2/backend/templates'
kwargs = {'headers': {'x-access-token': 'api_6e2447e0-16d9-4d81-8a90-437924d13dd6'}}
retries = 0, max_retries = 2
headers = {'x-access-token': 'api_6e2447e0-16d9-4d81-8a90-437924d13dd6'}, token = None
res = <Response [401 Unauthorized]>

    def request(self, method: str, url: str, **kwargs) -> httpx.Response:
        retries = 0
        max_retries = 2

    headers = kwargs.pop("headers", {})
        if self.api_key:
            headers["x-access-token"] = self.api_key
        token = self.token_manager.get_token()
        if token:
            headers["x-access-token"] = token
        kwargs["headers"] = headers

    while True:
            try:
                res = self._client.request(method, url, **kwargs)
                if res.status_code < 400:
                    return res
                if res.status_code in [401, 403]:

> raise AuthError("Invalid or expired access token.")
> E                   imbrace.exceptions.AuthError: Invalid or expired access token.

src\imbrace\http.py:39: AuthError
_______________________________________ test_list_teams _______________________________________

client = <imbrace.client.ImbraceClient object at 0x0000025C2DDC2E40>

    def test_list_teams(client):

> result = client.teams.list()
> ^^^^^^^^^^^^^^^^^^^

tests\test_integration.py:57:

---

src\imbrace\resources\teams.py:16: in list
    return self._http.request("GET", f"{self._base}/v2/backend/teams", params=params).json()
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

---

self = <imbrace.http.HttpTransport object at 0x0000025C2DDC30E0>, method = 'GET'
url = 'https://app-gatewayv2.imbrace.co/v2/backend/teams'
kwargs = {'headers': {'x-access-token': 'api_6e2447e0-16d9-4d81-8a90-437924d13dd6'}, 'params': {'limit': 20, 'skip': 0}}
retries = 0, max_retries = 2
headers = {'x-access-token': 'api_6e2447e0-16d9-4d81-8a90-437924d13dd6'}, token = None
res = <Response [401 Unauthorized]>

    def request(self, method: str, url: str, **kwargs) -> httpx.Response:
        retries = 0
        max_retries = 2

    headers = kwargs.pop("headers", {})
        if self.api_key:
            headers["x-access-token"] = self.api_key
        token = self.token_manager.get_token()
        if token:
            headers["x-access-token"] = token
        kwargs["headers"] = headers

    while True:
            try:
                res = self._client.request(method, url, **kwargs)
                if res.status_code < 400:
                    return res
                if res.status_code in [401, 403]:

> raise AuthError("Invalid or expired access token.")
> E                   imbrace.exceptions.AuthError: Invalid or expired access token.

src\imbrace\http.py:39: AuthError
_____________________________________ test_list_my_teams ______________________________________

client = <imbrace.client.ImbraceClient object at 0x0000025C2DDC2E40>

    def test_list_my_teams(client):

> result = client.teams.list_my()
> ^^^^^^^^^^^^^^^^^^^^^^

tests\test_integration.py:62:

---

src\imbrace\resources\teams.py:19: in list_my
    return self._http.request("GET", f"{self._base}/v2/backend/teams/my").json()
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

---

self = <imbrace.http.HttpTransport object at 0x0000025C2DDC30E0>, method = 'GET'
url = 'https://app-gatewayv2.imbrace.co/v2/backend/teams/my'
kwargs = {'headers': {'x-access-token': 'api_6e2447e0-16d9-4d81-8a90-437924d13dd6'}}
retries = 0, max_retries = 2
headers = {'x-access-token': 'api_6e2447e0-16d9-4d81-8a90-437924d13dd6'}, token = None
res = <Response [401 Unauthorized]>

    def request(self, method: str, url: str, **kwargs) -> httpx.Response:
        retries = 0
        max_retries = 2

    headers = kwargs.pop("headers", {})
        if self.api_key:
            headers["x-access-token"] = self.api_key
        token = self.token_manager.get_token()
        if token:
            headers["x-access-token"] = token
        kwargs["headers"] = headers

    while True:
            try:
                res = self._client.request(method, url, **kwargs)
                if res.status_code < 400:
                    return res
                if res.status_code in [401, 403]:

> raise AuthError("Invalid or expired access token.")
> E                   imbrace.exceptions.AuthError: Invalid or expired access token.

src\imbrace\http.py:39: AuthError
_____________________________________ test_list_contacts ______________________________________

client = <imbrace.client.ImbraceClient object at 0x0000025C2DDC2E40>

    def test_list_contacts(client):

> result = client.contacts.list(limit=5)
> ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

tests\test_integration.py:69:

---

src\imbrace\resources\contacts.py:13: in list
    return self._http.request("GET", f"{self._base}/contacts",

---

self = <imbrace.http.HttpTransport object at 0x0000025C2DDC30E0>, method = 'GET'
url = 'https://app-gatewayv2.imbrace.co/v1/backend/contacts'
kwargs = {'headers': {'x-access-token': 'api_6e2447e0-16d9-4d81-8a90-437924d13dd6'}, 'params': {'limit': 5, 'skip': 0}}
retries = 0, max_retries = 2
headers = {'x-access-token': 'api_6e2447e0-16d9-4d81-8a90-437924d13dd6'}, token = None
res = <Response [401 Unauthorized]>

    def request(self, method: str, url: str, **kwargs) -> httpx.Response:
        retries = 0
        max_retries = 2

    headers = kwargs.pop("headers", {})
        if self.api_key:
            headers["x-access-token"] = self.api_key
        token = self.token_manager.get_token()
        if token:
            headers["x-access-token"] = token
        kwargs["headers"] = headers

    while True:
            try:
                res = self._client.request(method, url, **kwargs)
                if res.status_code < 400:
                    return res
                if res.status_code in [401, 403]:

> raise AuthError("Invalid or expired access token.")
> E                   imbrace.exceptions.AuthError: Invalid or expired access token.

src\imbrace\http.py:39: AuthError
____________________________________ test_get_views_count _____________________________________

client = <imbrace.client.ImbraceClient object at 0x0000025C2DDC2E40>

    def test_get_views_count(client):

> result = client.conversations.get_views_count()
> ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

tests\test_integration.py:76:

---

src\imbrace\resources\conversations.py:18: in get_views_count
    return self._http.request("GET", f"{self._base}/v2/backend/team_conversations/_views_count",

---

self = <imbrace.http.HttpTransport object at 0x0000025C2DDC30E0>, method = 'GET'
url = 'https://app-gatewayv2.imbrace.co/v2/backend/team_conversations/_views_count'
kwargs = {'headers': {'x-access-token': 'api_6e2447e0-16d9-4d81-8a90-437924d13dd6'}, 'params': {}}
retries = 0, max_retries = 2
headers = {'x-access-token': 'api_6e2447e0-16d9-4d81-8a90-437924d13dd6'}, token = None
res = <Response [401 Unauthorized]>

    def request(self, method: str, url: str, **kwargs) -> httpx.Response:
        retries = 0
        max_retries = 2

    headers = kwargs.pop("headers", {})
        if self.api_key:
            headers["x-access-token"] = self.api_key
        token = self.token_manager.get_token()
        if token:
            headers["x-access-token"] = token
        kwargs["headers"] = headers

    while True:
            try:
                res = self._client.request(method, url, **kwargs)
                if res.status_code < 400:
                    return res
                if res.status_code in [401, 403]:

> raise AuthError("Invalid or expired access token.")
> E                   imbrace.exceptions.AuthError: Invalid or expired access token.

src\imbrace\http.py:39: AuthError
_____________________________________ test_list_messages ______________________________________

client = <imbrace.client.ImbraceClient object at 0x0000025C2DDC2E40>

    def test_list_messages(client):

> result = client.messages.list(limit=5)
> ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

tests\test_integration.py:83:

---

src\imbrace\resources\messages.py:13: in list
    return self._http.request("GET", self._base, params={"limit": limit, "skip": skip}).json()
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

---

self = <imbrace.http.HttpTransport object at 0x0000025C2DDC30E0>, method = 'GET'
url = 'https://app-gatewayv2.imbrace.co/v1/backend/conversation_messages'
kwargs = {'headers': {'x-access-token': 'api_6e2447e0-16d9-4d81-8a90-437924d13dd6'}, 'params': {'limit': 5, 'skip': 0}}
retries = 0, max_retries = 2
headers = {'x-access-token': 'api_6e2447e0-16d9-4d81-8a90-437924d13dd6'}, token = None
res = <Response [401 Unauthorized]>

    def request(self, method: str, url: str, **kwargs) -> httpx.Response:
        retries = 0
        max_retries = 2

    headers = kwargs.pop("headers", {})
        if self.api_key:
            headers["x-access-token"] = self.api_key
        token = self.token_manager.get_token()
        if token:
            headers["x-access-token"] = token
        kwargs["headers"] = headers

    while True:
            try:
                res = self._client.request(method, url, **kwargs)
                if res.status_code < 400:
                    return res
                if res.status_code in [401, 403]:

> raise AuthError("Invalid or expired access token.")
> E                   imbrace.exceptions.AuthError: Invalid or expired access token.

src\imbrace\http.py:39: AuthError
______________________________________ test_list_boards _______________________________________

client = <imbrace.client.ImbraceClient object at 0x0000025C2DDC2E40>

    def test_list_boards(client):

> result = client.boards.list()
> ^^^^^^^^^^^^^^^^^^^^

tests\test_integration.py:90:

---

src\imbrace\resources\boards.py:14: in list
    return self._http.request("GET", self._base, params={"limit": limit, "skip": skip}).json()
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

---

self = <imbrace.http.HttpTransport object at 0x0000025C2DDC30E0>, method = 'GET'
url = 'https://app-gatewayv2.imbrace.co/v1/backend/board'
kwargs = {'headers': {'x-access-token': 'api_6e2447e0-16d9-4d81-8a90-437924d13dd6'}, 'params': {'limit': 20, 'skip': 0}}
retries = 0, max_retries = 2
headers = {'x-access-token': 'api_6e2447e0-16d9-4d81-8a90-437924d13dd6'}, token = None
res = <Response [401 Unauthorized]>

    def request(self, method: str, url: str, **kwargs) -> httpx.Response:
        retries = 0
        max_retries = 2

    headers = kwargs.pop("headers", {})
        if self.api_key:
            headers["x-access-token"] = self.api_key
        token = self.token_manager.get_token()
        if token:
            headers["x-access-token"] = token
        kwargs["headers"] = headers

    while True:
            try:
                res = self._client.request(method, url, **kwargs)
                if res.status_code < 400:
                    return res
                if res.status_code in [401, 403]:

> raise AuthError("Invalid or expired access token.")
> E                   imbrace.exceptions.AuthError: Invalid or expired access token.

src\imbrace\http.py:39: AuthError
_______________________________________ test_list_users _______________________________________

client = <imbrace.client.ImbraceClient object at 0x0000025C2DDC2E40>

    def test_list_users(client):

> result = client.settings.list_users(limit=5)
> ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

tests\test_integration.py:97:

---

src\imbrace\resources\settings.py:32: in list_users
    return self._http.request("GET", f"{self._base}/v1/backend/users", params=params).json()
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

---

self = <imbrace.http.HttpTransport object at 0x0000025C2DDC30E0>, method = 'GET'
url = 'https://app-gatewayv2.imbrace.co/v1/backend/users'
kwargs = {'headers': {'x-access-token': 'api_6e2447e0-16d9-4d81-8a90-437924d13dd6'}, 'params': {'limit': 5, 'skip': 0}}
retries = 0, max_retries = 2
headers = {'x-access-token': 'api_6e2447e0-16d9-4d81-8a90-437924d13dd6'}, token = None
res = <Response [401 Unauthorized]>

    def request(self, method: str, url: str, **kwargs) -> httpx.Response:
        retries = 0
        max_retries = 2

    headers = kwargs.pop("headers", {})
        if self.api_key:
            headers["x-access-token"] = self.api_key
        token = self.token_manager.get_token()
        if token:
            headers["x-access-token"] = token
        kwargs["headers"] = headers

    while True:
            try:
                res = self._client.request(method, url, **kwargs)
                if res.status_code < 400:
                    return res
                if res.status_code in [401, 403]:

> raise AuthError("Invalid or expired access token.")
> E                   imbrace.exceptions.AuthError: Invalid or expired access token.

src\imbrace\http.py:39: AuthError
_________________________________ test_list_message_templates _________________________________

client = <imbrace.client.ImbraceClient object at 0x0000025C2DDC2E40>

    def test_list_message_templates(client):

> result = client.settings.list_message_templates()
> ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

tests\test_integration.py:102:

---

src\imbrace\resources\settings.py:17: in list_message_templates
    return self._http.request("GET", f"{self._base}/v2/backend/message_templates", params=params).json()
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

---

self = <imbrace.http.HttpTransport object at 0x0000025C2DDC30E0>, method = 'GET'
url = 'https://app-gatewayv2.imbrace.co/v2/backend/message_templates'
kwargs = {'headers': {'x-access-token': 'api_6e2447e0-16d9-4d81-8a90-437924d13dd6'}, 'params': {'limit': 20, 'skip': 0}}
retries = 0, max_retries = 2
headers = {'x-access-token': 'api_6e2447e0-16d9-4d81-8a90-437924d13dd6'}, token = None
res = <Response [401 Unauthorized]>

    def request(self, method: str, url: str, **kwargs) -> httpx.Response:
        retries = 0
        max_retries = 2

    headers = kwargs.pop("headers", {})
        if self.api_key:
            headers["x-access-token"] = self.api_key
        token = self.token_manager.get_token()
        if token:
            headers["x-access-token"] = token
        kwargs["headers"] = headers

    while True:
            try:
                res = self._client.request(method, url, **kwargs)
                if res.status_code < 400:
                    return res
                if res.status_code in [401, 403]:

> raise AuthError("Invalid or expired access token.")
> E                   imbrace.exceptions.AuthError: Invalid or expired access token.

src\imbrace\http.py:39: AuthError
====================================== warnings summary =======================================
tests\test_integration.py:21
  D:\HUANGJUNFENG\sdk\py\tests\test_integration.py:21: PytestUnknownMarkWarning: Unknown pytest.mark.integration - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
    pytestmark = pytest.mark.integration

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=================================== short test summary info ===================================
FAILED tests/test_integration.py::test_get_account - AttributeError: 'AccountResource' object has no attribute 'get_account'
FAILED tests/test_integration.py::test_list_channels - AttributeError: 'ImbraceClient' object has no attribute 'channels'. Did you mean: 'channel'?
FAILED tests/test_integration.py::test_list_agents - imbrace.exceptions.AuthError: Invalid or expired access token.
FAILED tests/test_integration.py::test_list_teams - imbrace.exceptions.AuthError: Invalid or expired access token.
FAILED tests/test_integration.py::test_list_my_teams - imbrace.exceptions.AuthError: Invalid or expired access token.
FAILED tests/test_integration.py::test_list_contacts - imbrace.exceptions.AuthError: Invalid or expired access token.
FAILED tests/test_integration.py::test_get_views_count - imbrace.exceptions.AuthError: Invalid or expired access token.
FAILED tests/test_integration.py::test_list_messages - imbrace.exceptions.AuthError: Invalid or expired access token.
FAILED tests/test_integration.py::test_list_boards - imbrace.exceptions.AuthError: Invalid or expired access token.
FAILED tests/test_integration.py::test_list_users - imbrace.exceptions.AuthError: Invalid or expired access token.
FAILED tests/test_integration.py::test_list_message_templates - imbrace.exceptions.AuthError: Invalid or expired access token.
======================== 11 failed, 95 deselected, 1 warning in 1.55s =========================
