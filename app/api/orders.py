from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Order, OrderItem, User, Product, Merchant, Cart, OrderStatus
from ..schemas import OrderCreate, OrderResponse, OrderStatusUpdate, OrderItemResponse
from ..auth import get_current_user, get_current_merchant

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderResponse)
def create_order(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 计算总价
    total_price = sum(item.price_at_purchase * item.quantity for item in order_data.items)

    # 检查用户余额
    if current_user.balance < total_price:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient balance. Required: {total_price}, Available: {current_user.balance}"
        )

    # 扣除余额
    current_user.balance -= total_price

    # 创建订单
    new_order = Order(
        user_id=current_user.id,
        total_price=total_price,
        status=OrderStatus.PENDING_PAYMENT,
        shipping_address=order_data.shipping_address,
        contact_name=order_data.contact_name,
        contact_phone=order_data.contact_phone
    )
    db.add(new_order)
    db.flush()  # 获取订单ID

    # 创建订单项
    for item_data in order_data.items:
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item_data.product_id,
            quantity=item_data.quantity,
            price_at_purchase=item_data.price_at_purchase
        )
        db.add(order_item)

    # 清空购物车
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if cart:
        cart.items = []

    db.commit()
    db.refresh(new_order)

    # 加载订单项并添加商品信息
    order_items_with_product = []
    for item in new_order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        item_response = OrderItemResponse(
            id=item.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price_at_purchase=item.price_at_purchase,
            product_name=product.name if product else None,
            product_image=product.image_paths[0] if product and product.image_paths else None
        )
        order_items_with_product.append(item_response)

    return OrderResponse(
        id=new_order.id,
        user_id=new_order.user_id,
        total_price=new_order.total_price,
        status=new_order.status,
        shipping_address=new_order.shipping_address,
        contact_name=new_order.contact_name,
        contact_phone=new_order.contact_phone,
        created_at=new_order.created_at,
        updated_at=new_order.updated_at,
        items=order_items_with_product
    )

@router.get("/my-orders", response_model=List[OrderResponse])
def get_my_orders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    orders = db.query(Order).filter(Order.user_id == current_user.id).order_by(Order.created_at.desc()).all()

    result = []
    for order in orders:
        order_items_with_product = []
        for item in order.items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            item_response = OrderItemResponse(
                id=item.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price_at_purchase=item.price_at_purchase,
                product_name=product.name if product else None,
                product_image=product.image_paths[0] if product and product.image_paths else None
            )
            order_items_with_product.append(item_response)

        result.append(OrderResponse(
            id=order.id,
            user_id=order.user_id,
            total_price=order.total_price,
            status=order.status,
            shipping_address=order.shipping_address,
            contact_name=order.contact_name,
            contact_phone=order.contact_phone,
            created_at=order.created_at,
            updated_at=order.updated_at,
            items=order_items_with_product
        ))

    return result

@router.get("/merchant/orders", response_model=List[OrderResponse])
def get_merchant_orders(
    current_user: User = Depends(get_current_merchant),
    db: Session = Depends(get_db)
):
    # 获取商家
    merchant = db.query(Merchant).filter(Merchant.user_id == current_user.id).first()
    if not merchant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Merchant not found"
        )

    # 获取包含该商家商品的所有订单
    merchant_product_ids = [p.id for p in merchant.products]

    order_items = db.query(OrderItem).filter(
        OrderItem.product_id.in_(merchant_product_ids)
    ).all()

    order_ids = list(set([item.order_id for item in order_items]))
    orders = db.query(Order).filter(Order.id.in_(order_ids)).order_by(Order.created_at.desc()).all()

    result = []
    for order in orders:
        # 只包含该商家的商品
        merchant_items = [item for item in order.items if item.product_id in merchant_product_ids]

        order_items_with_product = []
        for item in merchant_items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            item_response = OrderItemResponse(
                id=item.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price_at_purchase=item.price_at_purchase,
                product_name=product.name if product else None,
                product_image=product.image_paths[0] if product and product.image_paths else None
            )
            order_items_with_product.append(item_response)

        result.append(OrderResponse(
            id=order.id,
            user_id=order.user_id,
            total_price=order.total_price,
            status=order.status,
            shipping_address=order.shipping_address,
            contact_name=order.contact_name,
            contact_phone=order.contact_phone,
            created_at=order.created_at,
            updated_at=order.updated_at,
            items=order_items_with_product
        ))

    return result

@router.put("/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: int,
    status_update: OrderStatusUpdate,
    current_user: User = Depends(get_current_merchant),
    db: Session = Depends(get_db)
):
    # 获取商家
    merchant = db.query(Merchant).filter(Merchant.user_id == current_user.id).first()
    if not merchant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Merchant not found"
        )

    # 获取订单
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    # 验证订单包含该商家的商品
    merchant_product_ids = [p.id for p in merchant.products]
    has_merchant_product = any(item.product_id in merchant_product_ids for item in order.items)

    if not has_merchant_product:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this order"
        )

    # 更新状态
    order.status = status_update.status
    db.commit()
    db.refresh(order)

    # 构建响应
    order_items_with_product = []
    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        item_response = OrderItemResponse(
            id=item.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price_at_purchase=item.price_at_purchase,
            product_name=product.name if product else None,
            product_image=product.image_paths[0] if product and product.image_paths else None
        )
        order_items_with_product.append(item_response)

    return OrderResponse(
        id=order.id,
        user_id=order.user_id,
        total_price=order.total_price,
        status=order.status,
        shipping_address=order.shipping_address,
        contact_name=order.contact_name,
        contact_phone=order.contact_phone,
        created_at=order.created_at,
        updated_at=order.updated_at,
        items=order_items_with_product
    )
