from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.scheme.gym_machines import (
    Gym_Machine_Create,
    Gym_Machine_Update,
    Gym_Machine_Delete
)
from app.services import gym_machines as service

router = APIRouter(prefix="/gym_machines", tags=["Gym_Machine"])


# CREATE
@router.post("")
async def create_gym_machine(
    data: Gym_Machine_Create,
    db: Session = Depends(get_db),
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
    db: Session = Depends(get_db),
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
    db: Session = Depends(get_db),
):
    return await service.services_gym_machine_delete(
        db,
        data.g_id,
        data.m_id
    )