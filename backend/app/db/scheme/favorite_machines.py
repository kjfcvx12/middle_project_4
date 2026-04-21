from pydantic import BaseModel, Field


class Favorite_Machine_Base(BaseModel):
    u_id : int
    m_id : int

class Favorite_Machine_Create(Favorite_Machine_Base):
    pass

class Favorite_Machine_In_DB(Favorite_Machine_Base):
    f_m_id : int

    class Config:
        from_attributes = True

class Favorite_Machine_Read(Favorite_Machine_Base):
    pass