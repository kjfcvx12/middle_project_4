from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.scheme.gym_staffs import Gym_Staff_Create, Gym_Staff_Delete
from app.services import gym_staffs as service

router = APIRouter(prefix="/gym_staffs", tags=["Gym_Staff"])


# CREATE
@router.post("")
async def routers_gym_staff_create(
    data: Gym_Staff_Create,
    db: Session = Depends(get_db),
):
    return await service.services_gym_staff_create(
        db,
        data.g_id,
        data.u_id
    )


# DELETE
@router.delete("")
async def routers_gym_staff_delete(
    data: Gym_Staff_Delete,
    db: Session = Depends(get_db),
):
    return await service.services_gym_staff_delete(
        db,
        data.g_id,
        data.u_id
    )