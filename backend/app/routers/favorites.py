from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.favorites import *
from app.core.jwt_handle import get_current_user
from app.db.database import get_db
from app.db.scheme.favorites import *

router = APIRouter(
    prefix="/favorites",
    tags=["Favorite"]
)


# -------- gym --------

@router.post("/favorite_gyms")
async def toggle_gym(
    data: FavoriteGymCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    return await service_toggle_favorite_gym(db, user, data.gym_id)


@router.delete("/favorite_gyms")
async def delete_gym(
    data: FavoriteGymCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    return await service_delete_favorite_gym(db, user, data.gym_id)


@router.get("/users/favorite_gym/{u_id}")
async def get_gym(
    u_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    data = await service_get_favorites_gym(db, user, u_id)

    return {
        "data": [
            {
                "g_id": f.gym.gym_id,
                "g_name": f.gym.g_name
            }
            for f in data
        ]
    }


# -------- machine --------

@router.post("/favorite_machines")
async def toggle_machine(
    data: FavoriteMachineCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    return await service_toggle_favorite_machine(db, user, data.m_id)


@router.delete("/favorite_machines")
async def delete_machine(
    data: FavoriteMachineCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    return await service_delete_favorite_machine(db, user, data.m_id)


@router.get("/users/favorite_machine/{u_id}")
async def get_machine(
    u_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    data = await service_get_favorites_machine(db, user, u_id)

    return {
        "data": [
            {
                "m_id": f.machine.m_id,
                "m_name": f.machine.m_name
            }
            for f in data
        ]
    }


# -------- routine --------

@router.post("/favorite_routines")
async def toggle_routine(
    data: FavoriteRoutineCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    return await service_toggle_favorite_routine(db, user, data.r_id)


@router.delete("/favorite_routines")
async def delete_routine(
    data: FavoriteRoutineCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    return await service_delete_favorite_routine(db, user, data.r_id)


@router.get("/users/favorite_routines/{u_id}")
async def get_routine(
    u_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    data = await service_get_favorites_routine(db, user, u_id)

    return {
        "data": [
            {
                "r_id": f.routine.r_id,
                "r_name": f.routine.r_name
            }
            for f in data
        ]
    }