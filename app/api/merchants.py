from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Merchant, User
from ..schemas import MerchantResponse, MerchantUpdate
from ..auth import get_current_merchant

router = APIRouter(prefix="/merchants", tags=["merchants"])

@router.get("/me", response_model=MerchantResponse)
def get_my_merchant_info(
    current_user: User = Depends(get_current_merchant),
    db: Session = Depends(get_db)
):
    merchant = db.query(Merchant).filter(Merchant.user_id == current_user.id).first()
    if not merchant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Merchant profile not found"
        )
    return merchant

@router.put("/me", response_model=MerchantResponse)
def update_my_merchant_info(
    merchant_data: MerchantUpdate,
    current_user: User = Depends(get_current_merchant),
    db: Session = Depends(get_db)
):
    merchant = db.query(Merchant).filter(Merchant.user_id == current_user.id).first()
    if not merchant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Merchant profile not found"
        )

    # 更新字段
    update_data = merchant_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(merchant, field, value)

    db.commit()
    db.refresh(merchant)
    return merchant
