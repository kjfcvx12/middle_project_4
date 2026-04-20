from pydantic import BaseModel
from typing import Optional, List

# CREATE
class GymCreate(BaseModel):
    g_name: str
    g_addr: str
    g_tel: str
    shower: bool = False
    parking: bool = False
    elev: bool = False
    open_time: Optional[str] = None

# UPDATE
class GymUpdate(BaseModel):
    g_name: Optional[str] = None
    g_addr: Optional[str] = None
    g_tel: Optional[str] = None
    shower: Optional[bool] = None
    parking: Optional[bool] = None
    elev: Optional[bool] = None
    open_time: Optional[str] = None

# RESPONSE
class GymResponse(BaseModel):
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
class GymListItem(BaseModel):
    g_id: int
    g_name: str
    g_addr: str
    like_count: int = 0
    favorite_count: int = 0