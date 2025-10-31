from pydantic import BaseModel
from typing import List, Dict

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    merchant_id: int
    message: str

class ChatResponse(BaseModel):
    reply: str
