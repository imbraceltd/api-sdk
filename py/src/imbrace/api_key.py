from typing import Optional, TypedDict


class ImbraceApiKey(TypedDict):
    """Shape của object apiKey trong response từ Imbrace Gateway."""
    _id: str
    apiKey: str
    organization_id: str
    user_id: str
    is_active: bool
    expired_at: str
    created_at: str
    updated_at: str
    is_temp: bool


class ImbraceApiKeyResponse(TypedDict):
    """Response đầy đủ từ auth endpoint của Imbrace Gateway."""
    apiKey: ImbraceApiKey
    expires_in: int


def extract_api_key(res: ImbraceApiKeyResponse) -> str:
    """Lấy giá trị key thật từ API Key response.

    Example:
        res = requests.get(".../auth/key").json()
        key = extract_api_key(res)  # res["apiKey"]["apiKey"]
        client = ImbraceClient(api_key=key)
    """
    return res["apiKey"]["apiKey"]
