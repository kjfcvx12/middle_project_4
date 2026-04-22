from pydantic import BaseModel, Field

# CREATE
class Gym_Staff_Create(BaseModel):
    g_id: int
    u_id: int

# DELETE
class Gym_Staff_Delete(BaseModel):
    g_id: int
    u_id: int

# RESPONSE
class Gym_Staff_Response(BaseModel):
    g_s_id: int
    g_id: int
    u_id: int