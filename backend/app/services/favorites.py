from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.crud.favorites_gym import FavoriteGymCrud
from app.db.crud.favorites_machine import FavoriteMachineCrud
from app.db.crud.favorites_routine import FavoriteRoutineCrud

# -------- gym --------

async def service_get_favorites_gym(db: AsyncSession, user, u_id: int):
    if user.u_id != u_id:
        raise HTTPException(status_code=403, detail="권한 없음")

    data = await FavoriteGymCrud.crud_get_favorites_gym(db, u_id)

    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="즐겨찾기한 헬스장이 없습니다."
        )

    return data


async def service_toggle_favorite_gym(db: AsyncSession, user, gym_id: int):
    try:
        result = await FavoriteGymCrud.crud_toggle_favorite_gym(db, user.u_id, gym_id)

        await db.commit()

        if result == "added":
            return {"msg": "즐겨찾기 등록"}
        return {"msg": "즐겨찾기 취소"}

    except HTTPException:
        raise

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"즐겨찾기 처리 실패: {e}"
        )


async def service_delete_favorite_gym(db: AsyncSession, user, gym_id: int):
    try:
        result = await FavoriteGymCrud.crud_delete_favorite_gym(db, user.u_id, gym_id)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="삭제할 즐겨찾기가 없습니다."
            )

        await db.commit()

        return {"msg": "즐겨찾기 취소"}

    except HTTPException:
        raise

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"삭제 실패: {e}"
        )


# -------- machine --------

async def service_get_favorites_machine(db: AsyncSession, user, u_id: int):
    if user.u_id != u_id:
        raise HTTPException(status_code=403, detail="권한 없음")

    data = await FavoriteMachineCrud.crud_get_favorites_machine(db, u_id)

    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="즐겨찾기한 머신이 없습니다."
        )

    return data


async def service_toggle_favorite_machine(db: AsyncSession, user, m_id: int):
    try:
        result = await FavoriteMachineCrud.crud_toggle_favorite_machine(db, user.u_id, m_id)

        await db.commit()

        if result == "added":
            return {"msg": "즐겨찾기 등록"}
        return {"msg": "즐겨찾기 취소"}

    except HTTPException:
        raise

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"처리 실패: {e}"
        )


async def service_delete_favorite_machine(db: AsyncSession, user, m_id: int):
    try:
        result = await FavoriteMachineCrud.crud_delete_favorite_machine(db, user.u_id, m_id)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="삭제할 즐겨찾기가 없습니다."
            )

        await db.commit()

        return {"msg": "즐겨찾기 취소"}

    except HTTPException:
        raise

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"삭제 실패: {e}"
        )


# -------- routine --------

async def service_get_favorites_routine(db: AsyncSession, user, u_id: int):
    if user.u_id != u_id:
        raise HTTPException(status_code=403, detail="권한 없음")

    data = await FavoriteRoutineCrud.crud_get_favorites_routine(db, u_id)

    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="즐겨찾기한 루틴이 없습니다."
        )

    return data


async def service_toggle_favorite_routine(db: AsyncSession, user, r_id: int):
    try:
        result = await FavoriteRoutineCrud.crud_toggle_favorite_routine(db, user.u_id, r_id)

        await db.commit()

        if result == "added":
            return {"msg": "즐겨찾기 등록"}
        return {"msg": "즐겨찾기 취소"}

    except HTTPException:
        raise

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"처리 실패: {e}"
        )


async def service_delete_favorite_routine(db: AsyncSession, user, r_id: int):
    try:
        result = await FavoriteRoutineCrud.crud_delete_favorite_routine(db, user.u_id, r_id)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="삭제할 즐겨찾기가 없습니다."
            )

        await db.commit()

        return {"msg": "즐겨찾기 취소"}

    except HTTPException:
        raise

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"삭제 실패: {e}"
        )