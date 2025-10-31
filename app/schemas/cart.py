from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .product import ProductResponse

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = 1

class CartItemUpdate(BaseModel):
    quantity: int

class CartItemResponse(BaseModel):
    id: int
    cart_id: int
    product_id: int
    quantity: int
    product: ProductResponse
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CartResponse(BaseModel):
    id: int
    user_id: int
    items: List[CartItemResponse]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
