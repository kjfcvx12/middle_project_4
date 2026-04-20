from pydantic import BaseModel
from typing import List
from app.db.scheme.log_detail import LogDetailCreate

class LogCreate(BaseModel):
    r_id: int
    m_id: int
    attend: bool
    details: List[LogDetailCreate]