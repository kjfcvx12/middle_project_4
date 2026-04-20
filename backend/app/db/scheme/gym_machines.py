from pydantic import BaseModel

# CREATE
class GymMachineCreate(BaseModel):
    g_id: int
    m_id: int
    qty: int = 1

# UPDATE
class GymMachineUpdate(BaseModel):
    g_id: int
    m_id: int
    qty: int

# DELETE
class GymMachineDelete(BaseModel):
    g_id: int
    m_id: int

# RESPONSE
class GymMachineResponse(BaseModel):
    g_m_id: int
    g_id: int
    m_id: int
    qty: int