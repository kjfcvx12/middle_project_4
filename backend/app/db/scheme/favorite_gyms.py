from pydantic import BaseModel, Field


class Favorite_Gym_Base(BaseModel):
    u_id : int
    g_id : int

class Favorite_Gym_Create(Favorite_Gym_Base):
    pass

class Favorite_Gym_In_DB(Favorite_Gym_Base):
    f_g_id : int

    class Config:
        from_attributes = True

class Favorite_Gym_Read(Favorite_Gym_Base):
    pass