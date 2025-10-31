from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum, Text, ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..database import Base

class ProductStatus(str, enum.Enum):
    ONLINE = "online"
    OFFLINE = "offline"

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    merchant_id = Column(Integer, ForeignKey("merchants.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    price = Column(Float, nullable=False)
    image_paths = Column(ARRAY(String))
    status = Column(Enum(ProductStatus), default=ProductStatus.OFFLINE, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    merchant = relationship("Merchant", back_populates="products")
    category = relationship("Category", back_populates="products")
