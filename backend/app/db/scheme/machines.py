from pydantic import BaseModel, Field

#운동기구 등록
class MachineCreate(BaseModel):
    m_name:str
    dsc:str
    m_url:str | None = None
    p_id:int
    

#운동기구 수정
class MachineUpdate(BaseModel):
    m_name: str | None=None
    dsc: str | None=None
    m_url: str | None=None
    p_id: int | None=None



#운동기구 목록 조회
class MachineList(BaseModel):
    m_id:int
    m_name:str
    p_id:int

    class Config:
        from_attributes=True


#운동기구 상세 조회
class MachineDetail(BaseModel):
    m_id:int
    m_name:str
    dsc:str
    m_url:str | None
    p_id:int
    p_name:str
    
    class Config:
        from_attributes=True