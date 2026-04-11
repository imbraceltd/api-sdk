from typing import Optional
import threading

# Quản lý access token cho authentication
# Thread-safe implementation
class TokenManager:
    """Thread-safe TokenManager for Imbrace SDK.

    Quản lý access token với thread safety.
    """

    def __init__(self, initial_token: Optional[str] = None):
        self._token = initial_token
        self._lock = threading.Lock()

    def set_token(self, token: str) -> None:
        """Thiết lập access token mới với thread safety.

        Args:
            token: Access token mới
        """
        with self._lock:
            self._token = token

    def get_token(self) -> Optional[str]:
        """Lấy access token hiện tại với thread safety.

        Returns:
            Access token hoặc None nếu chưa có
        """
        with self._lock:
            return self._token

    def clear(self) -> None:
        """Xóa access token hiện tại với thread safety."""
        with self._lock:
            self._token = None
