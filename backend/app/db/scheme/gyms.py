from pydantic import BaseModel
from typing import Optional, List

# CREATE
class Gym_Create(BaseModel):
    g_name: str
    g_addr: str
    g_tel: str
    shower: bool = False
    parking: bool = False
    elev: bool = False
    open_time: Optional[str] = None

# UPDATE
class Gym_Update(BaseModel):
    g_name: Optional[str] = None
    g_addr: Optional[str] = None
    g_tel: Optional[str] = None
    shower: Optional[bool] = None
    parking: Optional[bool] = None
    elev: Optional[bool] = None
    open_time: Optional[str] = None

# RESPONSE
class Gym_Response(BaseModel):
    g_id: int
    g_name: str
    g_addr: str
    g_tel: str
    shower: bool
    parking: bool
    elev: bool
    open_time: Optional[str]

    class Config:
        from_attributes = True

# LIST RESPONSE ITEM
class Gym_List_Item(BaseModel):
    g_id: int
    g_name: str
    g_addr: str
    like_count: int = 0
    favorite_count: int = 0