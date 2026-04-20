from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Annotated


class Like_Routine_Base(BaseModel):
    u_id : int
    r_id : int

class Like_Routine_Create(Like_Routine_Base):
    pass

class Like_Routine_In_DB(Like_Routine_Base):
    l_r_id : int

    class Config:
        from_attributes = True

class Like_Routine_Read(Like_Routine_Base):
    pass
