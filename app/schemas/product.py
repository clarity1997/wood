from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional, List
from ..models.product import ProductStatus
from ..config import settings

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

    @field_validator('image_paths', mode='before')
    @classmethod
    def convert_image_paths(cls, v):
        """将相对路径转换为完整URL"""
        if v is None:
            return []
        return [f"{settings.BASE_URL}/uploads/{path}" if not path.startswith('http') else path for path in v]

    class Config:
        from_attributes = True
