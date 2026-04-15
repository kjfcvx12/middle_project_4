from pydantic import BaseModel, Field, EmailStr
from datetime import datetime,timezone
from typing import Annotated


class User_Base(BaseModel):
    u_name: str
    email: EmailStr


class User_Create(BaseModel):
    u_name: str
    email: EmailStr
    pw: Annotated[str, Field(max_length=72)]
    info: str


class User_Login(BaseModel):
    email: EmailStr
    pw: Annotated[str, Field(max_length=72)]


class User_Update(BaseModel):
    pw: Annotated[str, Field(max_length=72, default=None)] 
    u_name: str | None = None    
    info: str | None = None


class User_In_DB(User_Base):
    u_id: int
    role: str
    signup_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        from_attributes = True


class User_Read(User_In_DB):
    pass




