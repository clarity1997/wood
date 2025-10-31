from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Product, Merchant, User
from ..auth import get_current_merchant
import os
import uuid
from ..config import settings

router = APIRouter(prefix="/upload", tags=["upload"])

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

def validate_image(file: UploadFile):
    # Check file extension
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )

@router.post("/product/{product_id}/images")
async def upload_product_images(
    product_id: int,
    files: List[UploadFile] = File(...),
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

    # Ensure upload directory exists
    upload_dir = os.path.join(settings.UPLOAD_DIR, "products", str(product_id))
    os.makedirs(upload_dir, exist_ok=True)

    uploaded_paths = []
    for file in files:
        validate_image(file)

        # Generate unique filename
        ext = os.path.splitext(file.filename)[1]
        filename = f"{uuid.uuid4()}{ext}"
        file_path = os.path.join(upload_dir, filename)

        # Save file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Store relative path
        relative_path = f"products/{product_id}/{filename}"
        uploaded_paths.append(relative_path)

    # Update product image paths
    if product.image_paths is None:
        product.image_paths = []
    product.image_paths = product.image_paths + uploaded_paths
    db.commit()
    db.refresh(product)

    return {
        "message": "Images uploaded successfully",
        "image_paths": uploaded_paths,
        "total_images": len(product.image_paths)
    }

@router.delete("/product/{product_id}/images")
def delete_product_image(
    product_id: int,
    image_path: str,
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

    # Remove from database
    if product.image_paths and image_path in product.image_paths:
        product.image_paths.remove(image_path)
        db.commit()

        # Delete physical file
        full_path = os.path.join(settings.UPLOAD_DIR, image_path)
        if os.path.exists(full_path):
            os.remove(full_path)

        return {"message": "Image deleted successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )
