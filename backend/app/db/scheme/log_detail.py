from pydantic import BaseModel
from typing import Optional

class LogDetailCreate(BaseModel):
    sets: int
    reps: int
    fail_memo: Optional[str] = None
    memo: str

class Log_Detail_Read(BaseModel):
    sets: int
    reps: int
    fail_memo: Optional[str] = None
    memo: str