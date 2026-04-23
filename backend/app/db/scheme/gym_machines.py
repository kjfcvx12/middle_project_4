from pydantic import BaseModel

# CREATE
class Gym_Machine_Create(BaseModel):
    g_id: int
    m_id: int
    qty: int = 1

# UPDATE
class Gym_Machine_Update(BaseModel):
    g_id: int
    m_id: int
    qty: int

# DELETE
class Gym_Machine_Delete(BaseModel):
    g_id: int
    m_id: int

# RESPONSE
class Gym_Machine_Response(BaseModel):
    g_m_id: int
    g_id: int
    m_id: int
    qty: int