from pydantic import BaseModel, Field


class Like_Gym_Base(BaseModel):
    u_id : int
    g_id : int

class Like_Gym_Create(Like_Gym_Base):
    pass

class Like_Gym_In_DB(Like_Gym_Base):
    l_g_id : int

    class Config:
        from_attributes = True

class Like_Gym_Read(Like_Gym_In_DB):
    pass