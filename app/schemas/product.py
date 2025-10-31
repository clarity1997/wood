from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from ..models.product import ProductStatus

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category_id: Optional[int] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None
    status: Optional[ProductStatus] = None

class ProductResponse(ProductBase):
    id: int
    merchant_id: int
    image_paths: Optional[List[str]] = []
    status: ProductStatus
    created_at: datetime

    class Config:
        from_attributes = True
