from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.db.models.gym_staffs import Gym_Staff
from app.db.crud import gym_staffs as gym_staff_crud


# CREATE
async def services_gym_staff_create(db: Session, g_id: int, u_id: int):
    try:
        exist = db.query(Gym_Staff).filter(
            Gym_Staff.g_id == g_id,
            Gym_Staff.u_id == u_id
        ).first()

        if exist:
            raise HTTPException(status_code=400)

        obj = Gym_Staff(g_id=g_id, u_id=u_id)
        result=gym_staff_crud.crud_gym_staffs_create(db, obj)

        await db.commit()
        await db.refresh(result)
    except HTTPException:
        raise
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=400)


# DELETE
async def services_gym_staff_delete(db: Session, g_id: int, u_id: int):
    try:
        obj = db.query(Gym_Staff).filter(
            Gym_Staff.g_id == g_id,
            Gym_Staff.u_id == u_id
        ).first()

        if not obj:
            raise HTTPException(status_code=404)

        gym_staff_crud.crud_gym_staffs_delete(db, obj)

        await db.commit()
        return True

    except HTTPException:
        raise
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500)


# LIST
async def services_gym_staff_get(db: Session, g_id: int):
    try:
        staff_list = gym_staff_crud.crud_gym_staffs_get(db, g_id)

        if not staff_list:
            raise HTTPException(status_code=404)

        return staff_list

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500)