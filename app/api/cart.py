from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Cart, CartItem, Product, User
from ..schemas import CartItemCreate, CartItemUpdate, CartItemResponse, CartResponse
from ..auth import get_current_user
from typing import List

router = APIRouter(prefix="/cart", tags=["cart"])

def get_or_create_cart(user: User, db: Session) -> Cart:
    """Get user's cart or create one if it doesn't exist"""
    cart = db.query(Cart).filter(Cart.user_id == user.id).first()
    if not cart:
        cart = Cart(user_id=user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart

@router.get("/", response_model=CartResponse)
def get_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's cart"""
    cart = get_or_create_cart(current_user, db)
    return cart

@router.post("/items", response_model=CartItemResponse)
def add_to_cart(
    item_data: CartItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add item to cart"""
    # Verify product exists
    product = db.query(Product).filter(Product.id == item_data.product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    # Get or create cart
    cart = get_or_create_cart(current_user, db)

    # Check if item already exists in cart
    existing_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == item_data.product_id
    ).first()

    if existing_item:
        # Update quantity
        existing_item.quantity += item_data.quantity
        db.commit()
        db.refresh(existing_item)
        return existing_item
    else:
        # Create new cart item
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=item_data.product_id,
            quantity=item_data.quantity
        )
        db.add(cart_item)
        db.commit()
        db.refresh(cart_item)
        return cart_item

@router.put("/items/{item_id}", response_model=CartItemResponse)
def update_cart_item(
    item_id: int,
    item_data: CartItemUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update cart item quantity"""
    cart = get_or_create_cart(current_user, db)

    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.cart_id == cart.id
    ).first()

    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )

    if item_data.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantity must be greater than 0"
        )

    cart_item.quantity = item_data.quantity
    db.commit()
    db.refresh(cart_item)
    return cart_item

@router.delete("/items/{item_id}")
def delete_cart_item(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove item from cart"""
    cart = get_or_create_cart(current_user, db)

    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.cart_id == cart.id
    ).first()

    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )

    db.delete(cart_item)
    db.commit()
    return {"message": "Item removed from cart"}

@router.delete("/clear")
def clear_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Clear all items from cart"""
    cart = get_or_create_cart(current_user, db)

    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    db.commit()
    return {"message": "Cart cleared"}
