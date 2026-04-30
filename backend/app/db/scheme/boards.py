from pydantic import BaseModel, Field
from datetime import datetime

class BoardBase(BaseModel):
    u_id : int | None = None
    b_content : str = Field(..., min_length=1,max_length=300)

class BoardCreate(BaseModel):
    b_content : str = Field(..., min_length=1, max_length=300)

class BoardUpdate(BaseModel):
    b_content : str = Field(..., min_length=1, max_length=300)

class BoardRead(BaseModel):
    b_id : int
    u_id : int | None = None
    u_name : str | None = None
    b_content : str | None = None
    created_at : datetime | None = None
    updated_at : datetime | None = None

    class Config:
        from_attributes = True