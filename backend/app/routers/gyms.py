from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.db.database import get_db
from app.db.scheme.gyms import Gym_Create, Gym_Update, Gym_Response

from app.services import gyms as gym_service
from app.services import gym_staffs as gym_staffs_service
from app.services import gym_machines as gym_machines_service

from app.db.models.like_gyms import Like_Gym
from app.db.models.favorite_gyms import Favorite_Gym

from typing import Optional

from app.core.auth import (
    auth_get_admin_id,
    auth_get_staff_role,
    auth_get_u_id,
)

router = APIRouter(prefix="/gyms", tags=["Gyms"])


# =========================
# CREATE
# =========================
@router.post("")
async def routers_gym_create(
    data: Gym_Create,
    db: AsyncSession = Depends(get_db),
    admin_id: int = Depends(auth_get_admin_id)
):
    return await gym_service.services_gym_create(db, data)


# =========================
# LIST 
# =========================
@router.get("")
async def routers_gyms_list(
    page: int = 1,
    size: int = 10,
    sort: str | None = None,
    name: str | None = None,
    address: str | None = None,
    db: AsyncSession = Depends(get_db),
    u_id: Optional[int] = Depends(auth_get_u_id),  # ⭐ 하나만 사용
):
    skip = (page - 1) * size

    result = await gym_service.services_gym_list(
        db=db,
        skip=skip,
        limit=size,
        name=name,
        address=address,
        sort=sort,
    )

    rows = result.get("data", [])
    gym_ids = [row["g_id"] for row in rows]

    # ⭐ 안전장치 (여기 중요)
    if not gym_ids:
        return result

    like_set = set()
    fav_set = set()

    # =========================
    # 로그인 유저 있을 때만
    # =========================
    if u_id is not None:

        like_rows = await db.execute(
            select(Like_Gym.g_id)
            .where(
                Like_Gym.u_id == u_id,
                Like_Gym.g_id.in_(gym_ids)
            )
        )
        like_set = set(like_rows.scalars().all())

        fav_rows = await db.execute(
            select(Favorite_Gym.g_id)
            .where(
                Favorite_Gym.u_id == u_id,
                Favorite_Gym.g_id.in_(gym_ids)
            )
        )
        fav_set = set(fav_rows.scalars().all())

    # =========================
    # count (항상)
    # =========================
    like_count_rows = await db.execute(
        select(Like_Gym.g_id, func.count())
        .group_by(Like_Gym.g_id)
        .where(Like_Gym.g_id.in_(gym_ids))
    )
    like_count_map = dict(like_count_rows.all())

    fav_count_rows = await db.execute(
        select(Favorite_Gym.g_id, func.count())
        .group_by(Favorite_Gym.g_id)
        .where(Favorite_Gym.g_id.in_(gym_ids))
    )
    fav_count_map = dict(fav_count_rows.all())

    # =========================
    # merge
    # =========================
    for row in rows:
        g_id = row["g_id"]

        row["like_yn"] = g_id in like_set
        row["favorite_yn"] = g_id in fav_set

        row["like_count"] = like_count_map.get(g_id, 0)
        row["favorite_count"] = fav_count_map.get(g_id, 0)

    return result


# =========================
# SEARCH
# =========================
@router.get("/search")
async def routers_gym_search(
    name: str | None,
    address: str | None,
    db: AsyncSession = Depends(get_db)
):
    return await gym_service.services_gym_search(db, name, address)


# =========================
# DETAIL
# =========================
@router.get("/{g_id}", response_model=Gym_Response)
async def routers_gym_detail(
    g_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await gym_service.services_gym_get(db, g_id)


# =========================
# UPDATE
# =========================
@router.put("/{g_id}")
async def routers_gym_update(
    g_id: int,
    data: Gym_Update,
    db: AsyncSession = Depends(get_db),
    staff_role: str = Depends(auth_get_staff_role)
):
    return await gym_service.services_gym_update(db, g_id, data)


# =========================
# DELETE
# =========================
@router.delete("/{g_id}")
async def routers_gym_delete(
    g_id: int,
    db: AsyncSession = Depends(get_db),
    admin_id: int = Depends(auth_get_admin_id)
):
    return await gym_service.services_gym_delete(db, g_id)


# =========================
# STAFF
# =========================
@router.get("/{g_id}/staff")
async def routers_gym_staffs_get(
    g_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await gym_staffs_service.services_gym_staff_get(db, g_id)


# =========================
# MACHINES
# =========================
@router.get("/{g_id}/machines")
async def routers_gym_machines_get(
    g_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await gym_machines_service.services_gym_machine_get(db, g_id)


# =========================
# LIKE TOGGLE
# =========================
@router.post("/{g_id}/like")
async def routers_gym_like_toggle(
    g_id: int,
    db: AsyncSession = Depends(get_db),
    u_id: int = Depends(auth_get_u_id)
):
    result = await db.execute(
        select(Like_Gym).where(
            Like_Gym.g_id == g_id,
            Like_Gym.u_id == u_id
        )
    )
    like = result.scalar_one_or_none()

    if like:
        await db.delete(like)
        await db.commit()
        return {"liked": False}

    db.add(Like_Gym(g_id=g_id, u_id=u_id))
    await db.commit()

    return {"liked": True}


# =========================
# FAVORITE TOGGLE
# =========================
@router.post("/{g_id}/favorite")
async def routers_gym_favorite_toggle(
    g_id: int,
    db: AsyncSession = Depends(get_db),
    u_id: int = Depends(auth_get_u_id)
):
    result = await db.execute(
        select(Favorite_Gym).where(
            Favorite_Gym.g_id == g_id,
            Favorite_Gym.u_id == u_id
        )
    )
    favorite = result.scalar_one_or_none()

    if favorite:
        await db.delete(favorite)
        await db.commit()
        return {"favorited": False}

    db.add(Favorite_Gym(g_id=g_id, u_id=u_id))
    await db.commit()

    return {"favorited": True}