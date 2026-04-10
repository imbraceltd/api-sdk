"""Tests for TokenManager."""
import threading
from imbrace.auth.token_manager import TokenManager


def test_initial_token_none():
    tm = TokenManager()
    assert tm.get_token() is None


def test_initial_token_set():
    tm = TokenManager("tok_abc")
    assert tm.get_token() == "tok_abc"


def test_set_token():
    tm = TokenManager()
    tm.set_token("tok_xyz")
    assert tm.get_token() == "tok_xyz"


def test_clear_token():
    tm = TokenManager("tok_abc")
    tm.clear()
    assert tm.get_token() is None


def test_thread_safety():
    tm = TokenManager()
    results = []

    def writer():
        for i in range(100):
            tm.set_token(f"tok_{i}")

    def reader():
        for _ in range(100):
            results.append(tm.get_token())

    threads = [threading.Thread(target=writer), threading.Thread(target=reader)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # Should not have raised any exceptions — all values are either None or a valid token string
    assert all(r is None or r.startswith("tok_") for r in results)
