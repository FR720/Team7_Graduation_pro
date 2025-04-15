from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str
    is_admin: bool = False

class UserResponse(UserBase):
    id: str
    created_at: datetime
    is_admin: bool

class Token(BaseModel):
    token: str
    user: UserResponse

class LoginSchema(BaseModel):
    email: EmailStr
    password: str