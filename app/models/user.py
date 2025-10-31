from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..database import Base

class UserRole(str, enum.Enum):
    USER = "user"
    MERCHANT = "merchant"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.USER)
    created_at = Column(DateTime, default=datetime.utcnow)

    merchant = relationship("Merchant", back_populates="user", uselist=False)
    chat_history = relationship("ChatHistory", back_populates="user")
    cart = relationship("Cart", back_populates="user", uselist=False)
    orders = relationship("Order", back_populates="user")
