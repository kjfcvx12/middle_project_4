from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.db.models.users import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    pw: str
    u_name: str
    role: UserRole = UserRole.USER
    info: Optional[str] = None


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    pw: Optional[str] = None
    u_name: Optional[str] = None
    role: Optional[UserRole] = None
    refresh_token: Optional[str] = None
    info: Optional[str] = None


class UserResponse(BaseModel):
    u_id: int
    email: str
    u_name: str
    role: UserRole
    refresh_token: Optional[str]
    signup_date: datetime
    info: Optional[str]

    class Config:
        from_attributes = True