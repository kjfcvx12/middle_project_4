from pydantic import BaseModel, EmailStr,Field
from typing import Optional
from datetime import datetime


#운동부위 생성
class PartCreate(BaseModel):
    p_name:str


#운동부위 조회
class PartList(BaseModel):
    p_id:int
    p_name:str

    class Config:
        from_attributes=True


