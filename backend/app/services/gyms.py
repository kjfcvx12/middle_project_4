from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from fastapi import HTTPException

from app.db.crud import gyms as gym_crud
from app.db.models.like_gyms import Like_Gym
from app.db.models.favorite_gyms import Favorite_Gym

from app.db.crud.like_gyms import Like_Gym_Crud
from app.db.crud.favorite_gyms import Favorite_Gym_Crud

from app.db.scheme.gyms import Gym_Create, Gym_Update


# =========================
# CREATE
# =========================
async def services_gym_create(db: AsyncSession, data: Gym_Create):
    try:
        gym = await gym_crud.crud_gym_create(db, data)
        await db.commit()
        await db.refresh(gym)

        return {
            "msg": "헬스장 등록 완료",
            "g_id": gym.g_id
        }

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# =========================
# LIST
# =========================
async def services_gym_list(
    db: AsyncSession,
    skip: int,
    limit: int,
    name: str | None = None,
    address: str | None = None,
    sort: str | None = None
):
    try:
        gyms, total = await gym_crud.crud_gyms_gets(
            db=db,
            skip=skip,
            limit=limit,
            name=name,
            address=address,
            sort=sort
        )

        result = []

        for gym in gyms:
            # 🔥 dict 기반
            result.append({
                "g_id": gym["g_id"],
                "g_name": gym["g_name"],
                "g_addr": gym["g_addr"],
                "like_count": gym["like_count"],
                "favorite_count": gym["favorite_count"]
            })

        return {
            "total": total,
            "page": (skip // limit) + 1,
            "size": limit,
            "data": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# DETAIL
# =========================
async def services_gym_get(db: AsyncSession, g_id: int):
    try:
        gym = await gym_crud.crud_gym_get(db, g_id)

        if not gym:
            raise HTTPException(status_code=404, detail="gym not found")

        like_count = await Like_Gym_Crud.crud_like_gyms_count(db, g_id)
        favorite_count = await Favorite_Gym_Crud.crud_favorite_gyms_count(db, g_id)

        return {
            "g_id": gym.g_id,
            "g_name": gym.g_name,
            "g_addr": gym.g_addr,
            "g_tel": gym.g_tel,
            "shower": gym.shower,
            "parking": gym.parking,
            "elev": gym.elev,
            "open_time": gym.open_time,
            "like_count": like_count,
            "favorite_count": favorite_count
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# UPDATE
# =========================
async def services_gym_update(db: AsyncSession, g_id: int, data: Gym_Update):
    try:
        gym = await gym_crud.crud_gym_get(db, g_id)

        if not gym:
            raise HTTPException(status_code=404, detail="gym not found")

        gym = await gym_crud.crud_gym_update(db, gym, data)

        await db.commit()
        await db.refresh(gym)

        return {
            "msg": "수정 완료",
            "data": {
                "g_id": gym.g_id,
                "g_name": gym.g_name,
                "g_addr": gym.g_addr,
                "g_tel": gym.g_tel,
                "shower": gym.shower,
                "parking": gym.parking,
                "elev": gym.elev,
                "open_time": gym.open_time
            }
        }

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# =========================
# DELETE (🔥 안정 버전)
# =========================
async def services_gym_delete(db: AsyncSession, g_id: int):
    try:
        gym = await gym_crud.crud_gym_get(db, g_id)

        if not gym:
            raise HTTPException(status_code=404, detail="gym not found")

        await db.execute(
            delete(Like_Gym).where(Like_Gym.g_id == g_id)
        )

        await db.execute(
            delete(Favorite_Gym).where(Favorite_Gym.g_id == g_id)
        )

        await gym_crud.crud_gym_delete(db, gym)

        await db.commit()

        return {"msg": "헬스장 삭제 완료"}

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# SEARCH
# =========================
async def services_gym_search(db: AsyncSession, name: str | None, address: str | None):
    try:
        gyms = await gym_crud.crud_gyms_search(db, name, address)

        if not gyms:
            raise HTTPException(status_code=404, detail="검색 결과 없음")

        return [
            {
                "g_id": g.g_id,
                "g_name": g.g_name,
                "g_addr": g.g_addr,
                "g_tel": g.g_tel,
                "shower": g.shower,
                "parking": g.parking,
                "elev": g.elev,
                "open_time": g.open_time
            }
            for g in gyms
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))