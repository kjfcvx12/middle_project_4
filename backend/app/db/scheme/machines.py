from pydantic import BaseModel

#운동기구 등록
class MachineCreate(BaseModel):
    m_name:str
    dsc:str
    m_url:str | None = None
    p_id:int
    

#운동기구 조회
class MachineRead(BaseModel):
    m_id:int
    m_name:str
    dsc:str
    m_url:str | None
    p_id:int

    class Config:
        from_attributes=True

#운동기구 수정
class MachineUpdate(BaseModel):
    m_name: str | None=None
    dsc: str | None=None
    m_url: str | None=None
    p_id: int | None=None
