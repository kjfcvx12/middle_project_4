from pydantic import BaseModel, Field
from datetime import datetime,timezone
from typing import Annotated


class Note_Base(BaseModel):
    rece_id: int
    title: str
    content: str


class Note_Create(Note_Base):
    send_id:int



class Note_Send_del(BaseModel):
    send_del: bool  


class Note_Rece_del(BaseModel):
    rece_del: bool


class Note_In_DB(Note_Base):
    n_id: int
    n_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        from_attributes = True


class Note_Read(Note_In_DB):
    send_id:int




