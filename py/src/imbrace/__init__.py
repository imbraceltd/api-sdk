from .client import ImbraceClient, AsyncImbraceClient
from .app.client import AppGatewayClient, AsyncAppGatewayClient
from .server.client import ServerGatewayClient, AsyncServerGatewayClient
from .core.exceptions import ImbraceError, AuthError, ApiError, NetworkError
from .core.api_key import ImbraceApiKey, ImbraceApiKeyResponse, extract_api_key

__all__ = [
    # Unified clients
    "ImbraceClient",
    "AsyncImbraceClient",
    # Gateway clients (standalone usage)
    "AppGatewayClient",
    "AsyncAppGatewayClient",
    "ServerGatewayClient",
    "AsyncServerGatewayClient",
    # Errors
    "ImbraceError",
    "AuthError",
    "ApiError",
    "NetworkError",
    # API Key helpers
    "ImbraceApiKey",
    "ImbraceApiKeyResponse",
    "extract_api_key",
]
__version__ = "2.0.0"
