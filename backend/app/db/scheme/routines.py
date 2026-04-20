from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Annotated

class Routine_Base(BaseModel):
    r_name: Annotated[str, Field(max_length=100)]

class Routine_Create(Routine_Base):
    u_id : int | None = None
    p_id : int  | None = None

class Routine_In_DB(Routine_Base):
    r_id : int
    u_id : int | None = None
    p_id : int | None = None

    class Config:
        from_attributes = True

class Routine_Update(BaseModel):
    r_name: str | None = None
    p_id: int | None = None

class Routine_Read(Routine_Base):
    r_id : int
    u_id : int | None = None
    p_id : int  | None = None
    p_name: str | None = None
    
    class Config:
        from_attributes = True