from pydantic import BaseModel, Field
from datetime import datetime, timezone

class CommentBase(BaseModel):
    b_id : int
    u_id : int
    c_content : str

class CommentCreate(BaseModel):
    b_id : int
    c_content : str = Field(..., min_length=1, max_length=300)

class CommentUpdate(BaseModel):
    b_id : int
    u_id : int
    c_content : str = Field(..., min_length=1 ,max_length=300)


class CommentRead(BaseModel):
    c_id : int
    u_id : int
    u_name : str
    c_content : str
    created_at : datetime 
    updated_at : datetime | None=None
    
    class Config:
        from_attributes = True