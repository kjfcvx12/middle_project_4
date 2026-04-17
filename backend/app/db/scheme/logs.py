from pydantic import BaseModel
from typing import List, Optional

class LogDetailCreate(BaseModel):
    sets: int
    reps: int
    fail_memo: Optional[str] = None
    memo: str

class LogCreate(BaseModel):
    r_id: int
    m_id: int
    attend: bool
    details: List[LogDetailCreate]  # 여러 세트 입력