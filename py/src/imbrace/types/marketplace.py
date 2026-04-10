from __future__ import annotations
from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel


class ProductVariant(BaseModel):
    id: str
    name: str
    price: float
    stock: int
    attributes: Optional[Dict[str, Any]] = None


class Product(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    price: float
    currency: str = "USD"
    images: List[str] = []
    variants: List[ProductVariant] = []
    category: Optional[str] = None
    tags: List[str] = []
    is_active: bool = True
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


OrderStatus = Literal["pending", "confirmed", "processing", "shipped", "delivered", "cancelled", "refunded"]


class OrderItem(BaseModel):
    product_id: str
    variant_id: Optional[str] = None
    quantity: int
    unit_price: float
    total_price: float


class Order(BaseModel):
    id: str
    buyer_id: str
    seller_id: Optional[str] = None
    items: List[OrderItem]
    status: OrderStatus
    total_amount: float
    currency: str = "USD"
    shipping_address: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class CreateOrderInput(BaseModel):
    items: List[Dict[str, Any]]  # [{ product_id, variant_id?, quantity }]
    shipping_address: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None
