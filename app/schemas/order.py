from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from ..models.order import OrderStatus

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int
    price_at_purchase: float

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
    shipping_address: Optional[str] = None
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None

class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    price_at_purchase: float
    product_name: Optional[str] = None
    product_image: Optional[str] = None

    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_price: float
    status: OrderStatus
    shipping_address: Optional[str]
    contact_name: Optional[str]
    contact_phone: Optional[str]
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True

class OrderStatusUpdate(BaseModel):
    status: OrderStatus
