from sqlalchemy import Column, Integer, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    merchant_id = Column(Integer, ForeignKey("merchants.id"), nullable=False)
    messages = Column(JSON, nullable=False)  # [{"role": "user", "content": "..."}, ...]
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="chat_history")
    merchant = relationship("Merchant", back_populates="chat_history")
