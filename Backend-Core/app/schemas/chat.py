from datetime import datetime
from pydantic import BaseModel
from typing import List, Literal

class ChatMessage(BaseModel):
    sender: Literal["user", "ai"]
    message: str
    timestamp: datetime

class ChatMessageRequest(BaseModel):
    message: str

class ChatMessageResponse(BaseModel):
    response: ChatMessage

class ChatHistoryResponse(BaseModel):
    messages: List[ChatMessage]