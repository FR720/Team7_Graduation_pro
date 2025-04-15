from datetime import datetime
from beanie import Document
from typing import Literal

class ChatMessage(Document):
    course_id: str
    user_id: str
    sender: Literal["user", "ai"]
    message: str
    timestamp: datetime = datetime.utcnow()

    class Settings:
        name = "chat_messages"