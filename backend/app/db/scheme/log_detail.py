from pydantic import BaseModel
from typing import Optional

class LogDetailCreate(BaseModel):
    sets: int
    reps: int
    weight: int = 0          # 추가
    duration: int = 0        # 추가
    fail_memo: Optional[str] = None
    memo: str

class Log_Detail_Read(BaseModel):
    sets: int
    reps: int
    weight: int = 0          # 추가
    duration: int = 0        # 추가
    fail_memo: Optional[str] = None
    memo: str

class Config:
        from_attributes = True   # (pydantic v2)
        # orm_mode = True        # (pydantic v1이면 이거)