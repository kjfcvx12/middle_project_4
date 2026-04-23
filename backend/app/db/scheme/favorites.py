from pydantic import BaseModel

# 단순 ID
class FavoriteGymCreate(BaseModel):
    gym_id: int

class FavoriteMachineCreate(BaseModel):
    m_id: int

class FavoriteRoutineCreate(BaseModel):
    r_id: int
    