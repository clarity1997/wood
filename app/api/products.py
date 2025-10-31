from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models import Product, Merchant, User, ProductStatus
from ..schemas import ProductCreate, ProductUpdate, ProductResponse
from ..auth import get_current_user, get_current_merchant
import os
import uuid
from ..config import settings

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=ProductResponse)
def create_product(
    product_data: ProductCreate,
    current_user: User = Depends(get_current_merchant),
    db: Session = Depends(get_db)
):
    # Get merchant
    merchant = db.query(Merchant).filter(Merchant.user_id == current_user.id).first()
    if not merchant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Merchant profile not found"
        )

    # Create product
    new_product = Product(
        merchant_id=merchant.id,
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        category_id=product_data.category_id,
        image_paths=[],
        status=ProductStatus.OFFLINE
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.get("/", response_model=List[ProductResponse])
def get_products(
    skip: int = 0,
    limit: int = 100,
    status_filter: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Product)
    if status_filter:
        query = query.filter(Product.status == status_filter)
    products = query.offset(skip).limit(limit).all()
    return products

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    current_user: User = Depends(get_current_merchant),
    db: Session = Depends(get_db)
):
    # Get merchant
    merchant = db.query(Merchant).filter(Merchant.user_id == current_user.id).first()
    if not merchant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Merchant profile not found"
        )

    # Get product
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.merchant_id == merchant.id
    ).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found or unauthorized"
        )

    # Update fields
    update_data = product_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product

@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    current_user: User = Depends(get_current_merchant),
    db: Session = Depends(get_db)
):
    # Get merchant
    merchant = db.query(Merchant).filter(Merchant.user_id == current_user.id).first()
    if not merchant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Merchant profile not found"
        )

    # Get product
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.merchant_id == merchant.id
    ).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found or unauthorized"
        )

    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}

@router.get("/merchant/my-products", response_model=List[ProductResponse])
def get_my_products(
    current_user: User = Depends(get_current_merchant),
    db: Session = Depends(get_db)
):
    merchant = db.query(Merchant).filter(Merchant.user_id == current_user.id).first()
    if not merchant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Merchant profile not found"
        )

    products = db.query(Product).filter(Product.merchant_id == merchant.id).all()
    return products
