from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.scheme.gym_machines import (
    Gym_Machine_Create,
    Gym_Machine_Update,
    Gym_Machine_Delete
)
from app.services import gym_machines as service
from app.core.auth import auth_get_admin_id


router = APIRouter(
    prefix="/gym_machines",
    tags=["Gym_Machine"],
    redirect_slashes=False
)


# CREATE
@router.post("")
async def routers_gym_machine_create(
    data: Gym_Machine_Create,
    #admin: int = Depends(auth_get_admin_id),
    db: AsyncSession = Depends(get_db),
):
    return await service.services_gym_machine_create(
        db,
        data.g_id,
        data.m_id,
        data.qty
    )


# UPDATE 
@router.put("")
async def routers_gym_machine_update(
    data: Gym_Machine_Update,
    #admin: int = Depends(auth_get_admin_id),
    db: AsyncSession = Depends(get_db),
):
    return await service.services_gym_machine_update(
        db,
        data.g_id,
        data.m_id,
        data.qty
    )


# DELETE
@router.delete("")
async def routers_gym_machine_delete(
    data: Gym_Machine_Delete,
    #admin: int = Depends(auth_get_admin_id),
    db: AsyncSession = Depends(get_db),
):
    return await service.services_gym_machine_delete(
        db,
        data.g_id,
        data.m_id
    )