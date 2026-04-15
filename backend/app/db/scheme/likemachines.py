from pydantic import BaseModel


#운동 기구 좋아요 생성
class Like_MachineCreate(BaseModel):
    m_id:int

#좋아요 정보 표시
class Like_MachineRead(BaseModel):
    l_m_id:int
    u_id:int
    m_id:int

    class Config:
        from_attributes = True