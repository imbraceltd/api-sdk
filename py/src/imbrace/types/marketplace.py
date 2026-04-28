from typing import List, Optional, Dict, Any
from typing_extensions import TypedDict

class Product(TypedDict, total=False):
    _id: str
    name: str
    description: Optional[str]
    price: Optional[float]
    currency: Optional[str]
    category: Optional[str]
    image_url: Optional[str]
    created_at: str

class OrderStatus:
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"

class Order(TypedDict, total=False):
    _id: str
    product_id: str
    user_id: str
    status: str
    created_at: str

class CreateOrderInput(TypedDict, total=False):
    product_id: str
    config: Optional[Dict[str, Any]]

class EmailTemplate(TypedDict, total=False):
    _id: str
    name: Optional[str]
    subject: Optional[str]
    body: Optional[str]

class CreateEmailTemplateInput(TypedDict, total=False):
    name: str
    subject: Optional[str]
    body: Optional[str]

class MarketplaceFileDetails(TypedDict, total=False):
    _id: str
    name: Optional[str]
    url: Optional[str]

class MarketplaceFileUploadResponse(TypedDict, total=False):
    url: str
    file_id: Optional[str]

class MarketplaceCategory(TypedDict, total=False):
    _id: str
    name: str
