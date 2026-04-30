from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.db.models.gym_staffs import Gym_Staff
from app.db.crud import gym_staffs as gym_staff_crud


# CREATE
async def services_gym_staff_create(db: AsyncSession, g_id: int, u_id: int):
    try:
        exist = await gym_staff_crud.crud_gym_staffs_get_one(db, g_id, u_id)

        if exist:
            raise HTTPException(status_code=400)

        obj = Gym_Staff(g_id=g_id, u_id=u_id)
        result = await gym_staff_crud.crud_gym_staffs_create(db, obj)

        await db.commit()
        await db.refresh(result)

        return {"msg": "트레이너 등록 완료"}

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# DELETE
async def services_gym_staff_delete(db: AsyncSession, g_id: int, u_id: int):
    try:
        obj = await gym_staff_crud.crud_gym_staffs_get_one(db, g_id, u_id)

        if not obj:
            raise HTTPException(status_code=404, detail=str(e))

        await gym_staff_crud.crud_gym_staffs_delete(db, obj)

        await db.commit()

        return {"msg": "트레이너 등록 취소"}

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# LIST
async def services_gym_staff_get(db: AsyncSession, g_id: int):
    try:
        staff_list = await gym_staff_crud.crud_gym_staffs_get(db, g_id)

        return [
            {
                "u_id": staff.u_id
            }
            for staff in staff_list
        ]

    except Exception as e:
        raise HTTPException(status_code=500)