from pydantic import BaseModel, Field


class Like_Machine_Base(BaseModel):
    u_id : int
    m_id : int

class Like_Machine_Create(Like_Machine_Base):
    pass

class Like_Machine_In_DB(Like_Machine_Base):
    l_m_id : int

    class Config:
        from_attributes = True

class Like_Machine_Read(Like_Machine_In_DB):
    pass