from pydantic import BaseModel, Field
from datetime import datetime,timezone
from app.db.scheme.log_detail import LogDetailCreate

class LogCreate(BaseModel):
    r_id: int
    m_id: int
    attend: bool
    details: list[LogDetailCreate]



class Log_Read(BaseModel):
    u_id: int
    r_id: int
    m_id: int
    log_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    attend: bool