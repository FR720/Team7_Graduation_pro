from datetime import datetime
from beanie import Document
from pydantic import EmailStr

class User(Document):
    name: str
    email: EmailStr
    password: str
    created_at: datetime = datetime.utcnow()
    is_admin: bool = False

    class Settings:
        name = "users"