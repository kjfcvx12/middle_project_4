from pydantic import BaseModel, Field
from datetime import datetime, timezone

class CommentBase(BaseModel):
    b_id : int
    u_id : int
    c_content : str

class CommentCreate(BaseModel):
    c_content : str = Field(..., min_length=1, max_length=300)

class CommentUpdate(BaseModel):
    c_content : str = Field(..., min_length=1 ,max_length=300)


class CommentRead(BaseModel):
    c_id : int
    u_id : int | None = None
    u_name : str | None = None
    c_content : str = Field(..., min_length=1 ,max_length=300)
    created_at : datetime | None = None
    updated_at : datetime | None = None
    
    class Config:
        from_attributes = True