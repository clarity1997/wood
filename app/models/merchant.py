from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from ..database import Base

class Merchant(Base):
    __tablename__ = "merchants"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    shop_name = Column(String, nullable=False)
    description = Column(Text)

    user = relationship("User", back_populates="merchant")
    products = relationship("Product", back_populates="merchant")
    chat_history = relationship("ChatHistory", back_populates="merchant")
