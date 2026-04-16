from pydantic import BaseModel


# 운동기구 좋아요 생성
class LikeMachineCreate(BaseModel):
    m_id: int


# 좋아요 정보 조회
class LikeMachineRead(BaseModel):
    lm_id: int
    user_id: int
    m_id: int

    class Config:
        from_attributes = True