from pydantic import BaseModel, Field

# CREATE / DELETE 요청
class GymStaffCreate(BaseModel):
    g_id: int
    u_id: int


class GymStaffDelete(BaseModel):
    g_id: int
    u_id: int

# RESPONSE
class GymStaffResponse(BaseModel):
    g_s_id: int
    g_id: int
    u_id: int