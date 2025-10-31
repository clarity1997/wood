from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from ..database import get_db
from ..models import Product, ProductStatus
from ..schemas import ProductResponse

router = APIRouter(prefix="/search", tags=["search"])

@router.get("/", response_model=List[ProductResponse])
def search_products(
    q: Optional[str] = Query(None, description="Search keyword"),
    min_price: Optional[float] = Query(None, description="Minimum price"),
    max_price: Optional[float] = Query(None, description="Maximum price"),
    category_id: Optional[int] = Query(None, description="Category ID"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    # Start with online products only
    query = db.query(Product).filter(Product.status == ProductStatus.ONLINE)

    # Apply keyword search
    if q:
        query = query.filter(
            or_(
                Product.name.ilike(f"%{q}%"),
                Product.description.ilike(f"%{q}%")
            )
        )

    # Apply price filters
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    # Apply category filter
    if category_id is not None:
        query = query.filter(Product.category_id == category_id)

    products = query.offset(skip).limit(limit).all()
    return products
