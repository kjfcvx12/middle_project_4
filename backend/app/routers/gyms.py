from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.scheme.gyms import Gym_Create, Gym_Update, Gym_Response
from app.services import gyms as gym_service
from app.services import gym_staffs as gym_staffs_service
from app.services import gym_machines as gym_machines_service
from app.core.auth import auth_get_u_id, auth_get_admin_id

router = APIRouter(prefix="/gyms", tags=["Gyms"])


# CREATE
@router.post("")
async def routers_gym_create(
    data: Gym_Create,
    db: AsyncSession = Depends(get_db),
    # admin_id: int = Depends(auth_get_admin_id)
):
    return await gym_service.services_gym_create(db, data)


# LIST
@router.get("")
async def routers_gyms_list(
    page: int = 1,
    size: int = 10,
    sort: str | None = None,
    name: str | None = None,
    address: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    skip = (page - 1) * size

    return await gym_service.services_gym_list(
        db=db,
        skip=skip,
        limit=size,
        name=name,
        address=address,
        sort=sort,
    )


# SEARCH
@router.get("/search")
async def routers_gym_search(
    name: str | None,
    address: str | None,
    db: AsyncSession = Depends(get_db)
):
    return await gym_service.services_gym_search(db, name, address)


# DETAIL
@router.get("/{g_id}", response_model=Gym_Response)
async def routers_gym_detail(
    g_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await gym_service.services_gym_get(db, g_id)


# UPDATE
@router.put("/{g_id}")
async def routers_gym_update(
    g_id: int,
    data: Gym_Update,
    db: AsyncSession = Depends(get_db),
):
    return await gym_service.services_gym_update(db, g_id, data)


# DELETE
@router.delete("/{g_id}")
async def routers_gym_delete(
    g_id: int,
    db: AsyncSession = Depends(get_db),
    # admin_id: int = Depends(auth_get_admin_id)
):
    return await gym_service.services_gym_delete(db, g_id)


# STAFF
@router.get("/{g_id}/staff")
async def routers_gym_staffs_get(
    g_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await gym_staffs_service.services_gym_staff_get(db, g_id)


# MACHINES
@router.get("/{g_id}/machines")
async def routers_gym_machines_get(
    g_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await gym_machines_service.services_gym_machine_get(db, g_id)