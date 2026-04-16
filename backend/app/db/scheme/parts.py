from pydantic import BaseModel, EmailStr,Field
from typing import Optional
from datetime import datetime


class PartsCreate(BaseModel):
    p_name:str

#
class PartRead(BaseModel):
    p_id:int
    p_name:str

    class Config:
        from_attributes=True