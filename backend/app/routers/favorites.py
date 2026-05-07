from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import auth_get_u_id

from app.db.database import get_db


from app.db.scheme.favorite_gyms import Favorite_Gym_Read
from app.db.scheme.favorite_machines import Favorite_Machine_Read
from app.db.scheme.favorite_routines import Favorite_Routine_Read

from app.services.favorites import Favorite_Service

router=APIRouter(prefix='/favorites',tags=['Favorite'])


# post 헬스장 즐겨찾기 토글
@router.post("/gyms/toggle", response_model=dict)
async def router_favorite_gyms_toggle(g_id: int,
                                      u_id: int = Depends(auth_get_u_id),
                                      db: AsyncSession = Depends(get_db)):
        return await Favorite_Service.services_favorite_machines_toggle(db, u_id, g_id)


# post 운동기구 즐겨찾기 토글
@router.post("/machines/toggle", response_model=dict)
async def router_favorite_machines_toggle(m_id: int,
                                          u_id: int = Depends(auth_get_u_id),
                                          db: AsyncSession = Depends(get_db)):
        return await Favorite_Service.services_favorite_machines_toggle(db, u_id, m_id)


# post 루틴 즐겨찾기 토글
@router.post("/routines/toggle", response_model=dict)
async def router_favorite_routines_toggle(r_id: int,
                                          u_id: int = Depends(auth_get_u_id),
                                          db: AsyncSession = Depends(get_db)):
        return await Favorite_Service.services_favorite_routines_toggle(db, u_id, r_id)
