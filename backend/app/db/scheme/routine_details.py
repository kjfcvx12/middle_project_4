from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Annotated

class Routine_Detail_Base(BaseModel):
    m_id : int
    step : int
    sets : int
    reps : int
    rest_time : int | None = None
    weight : int | None = None

class Routine_Detail_Create(Routine_Detail_Base):
    r_id : int

class Routine_Detail_In_DB(Routine_Detail_Base):
    r_d_id : int

    class Config:
        from_attributes = True

class Routine_Detail_Update(BaseModel):
    m_id : int | None = None
    step: int | None = None
    sets: int | None = None
    reps: int | None = None
    rest_time: int | None = None

class Routine_Detail_Read(Routine_Detail_Base):
    r_d_id : int
    m_name: str | None = None
    p_name: str | None = None
    
    class Config:
        from_attributes = True

