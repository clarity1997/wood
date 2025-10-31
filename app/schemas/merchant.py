from pydantic import BaseModel
from typing import Optional

class MerchantBase(BaseModel):
    shop_name: str
    description: Optional[str] = None

class MerchantCreate(MerchantBase):
    pass

class MerchantUpdate(BaseModel):
    shop_name: Optional[str] = None
    description: Optional[str] = None

class MerchantResponse(MerchantBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
