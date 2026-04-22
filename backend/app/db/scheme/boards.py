from pydantic import BaseModel, Field
from datetime import datetime

class BoardBase(BaseModel):
    u_id : int
    b_content : str = Field(..., min_length=1,max_length=300)

class BoardCreate(BaseModel):
    b_content : str = Field(..., min_length=1, max_length=300)

class BoardUpdate(BaseModel):
    u_id : int
    b_content : str = Field(..., min_length=1, max_length=300)

class BoardRead(BaseModel):
    b_id : int
    i_id : int
    u_id : int
    u_name : str
    b_content : int
    like_count : int
    created_at : datetime
    updated_at : datetime | None=None

    class Config:
        from_attributes = True