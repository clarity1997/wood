from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..database import Base

class OrderStatus(str, enum.Enum):
    PENDING_PAYMENT = "pending_payment"  # 待付款
    PENDING_SHIPMENT = "pending_shipment"  # 待发货
    SHIPPED = "shipped"  # 已发货/待收货
    COMPLETED = "completed"  # 已完成
    CANCELLED = "cancelled"  # 已取消

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(Enum(OrderStatus), nullable=False, default=OrderStatus.PENDING_PAYMENT)
    shipping_address = Column(String, nullable=True)
    contact_name = Column(String, nullable=True)
    contact_phone = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_at_purchase = Column(Float, nullable=False)  # 购买时的价格
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    order = relationship("Order", back_populates="items")
    product = relationship("Product")
