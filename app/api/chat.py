from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Merchant, Product, ChatHistory, User, ProductStatus
from ..schemas import ChatRequest, ChatResponse
from ..auth import get_current_user
from ..services.deepseek_service import deepseek_service

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/", response_model=ChatResponse)
async def chat_with_merchant(
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get merchant
    merchant = db.query(Merchant).filter(Merchant.id == chat_request.merchant_id).first()
    if not merchant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Merchant not found"
        )

    # Get merchant's online products
    products = db.query(Product).filter(
        Product.merchant_id == merchant.id,
        Product.status == ProductStatus.ONLINE
    ).all()

    # Generate product context
    product_context = await deepseek_service.generate_product_context(products)

    # Prepare messages for DeepSeek
    messages = [{"role": "user", "content": chat_request.message}]

    # Get response from DeepSeek
    reply = await deepseek_service.chat(messages, product_context)

    # Save chat history
    chat_history = ChatHistory(
        user_id=current_user.id,
        merchant_id=merchant.id,
        messages=[
            {"role": "user", "content": chat_request.message},
            {"role": "assistant", "content": reply}
        ]
    )
    db.add(chat_history)
    db.commit()

    return ChatResponse(reply=reply)
