from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Union
from ..models.user import UserRole

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRole

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Union[UserRole, str]  # Accept both enum and string

    model_config = {"use_enum_values": False}

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class TokenData(BaseModel):
    username: Optional[str] = None
