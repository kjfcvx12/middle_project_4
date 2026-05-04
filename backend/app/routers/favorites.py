from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import auth_get_u_id

from app.db.database import get_db


from app.db.scheme.favorite_gyms import Favorite_Gym_Read
from app.db.scheme.favorite_machines import Favorite_Machine_Read
from app.db.scheme.favorite_routines import Favorite_Routine_Read

from app.services.favorites import Favorite_Service

router=APIRouter(prefix='/favorites',tags=['Favorite'])


# post 헬스장 즐겨찾기 추가
@router.post("/gyms_create", response_model=Favorite_Gym_Read)
async def router_favorite_gyms_create(g_id:int,
                                      u_id:int=Depends(auth_get_u_id), 
                                      db:AsyncSession=Depends(get_db)):
    return await Favorite_Service.services_favorite_gym_create(db, u_id, g_id)

# delete 헬스장 즐겨찾기 해제
@router.delete("/gyms_del", status_code=status.HTTP_204_NO_CONTENT)
async def router_favorite_gyms_delete(f_g_id:int, db:AsyncSession=Depends(get_db)):
    return await Favorite_Service.services_favorite_gym_delete(db, f_g_id)


# post 운동기구 즐겨찾기 추가
@router.post("/machines_create", response_model=Favorite_Machine_Read)
async def router_favorite_machines_create(m_id:int,
                                          u_id:int=Depends(auth_get_u_id), 
                                          db:AsyncSession=Depends(get_db)):
    return await Favorite_Service.services_favorite_machines_create(db, u_id, m_id)

# delete 운동기구 즐겨찾기 해제
@router.delete("/machines_del", status_code=status.HTTP_204_NO_CONTENT)
async def router_favorite_machines_delete(f_m_id:int, db:AsyncSession=Depends(get_db)):
    return await Favorite_Service.services_favorite_machines_delete(db, f_m_id)


# post 루틴 즐겨찾기 추가
@router.post("/routines_create", response_model=Favorite_Routine_Read)
async def router_favorite_routines_create(r_id:int,
                                          u_id:int=Depends(auth_get_u_id), 
                                          db:AsyncSession=Depends(get_db)):
    return await Favorite_Service.services_favorite_routines_create(db, u_id, r_id)

# delete 루틴 즐겨찾기 해제
@router.delete("/routines_del", status_code=status.HTTP_204_NO_CONTENT)
async def router_favorite_rounines_delete(f_r_id:int, db:AsyncSession=Depends(get_db)):
    return await Favorite_Service.services_favorite_routines_delete(db, f_r_id)