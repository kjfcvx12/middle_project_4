from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.db.models.gym_machines import Gym_Machine
from app.db.crud import gym_machines as gym_machine_crud


# CREATE
async def services_gym_machine_create(db: AsyncSession, g_id: int, m_id: int, qty: int):
    try:
        exist = await gym_machine_crud.crud_gym_machine_get(db, g_id, m_id)

        if exist:
            raise HTTPException(status_code=400, detail="이미 등록된 기구입니다.")

        obj = Gym_Machine(g_id=g_id, m_id=m_id, qty=qty)

        result = await gym_machine_crud.crud_gym_machine_create(db, obj)

        await db.commit()
        await db.refresh(result)

        return {"msg": "기구 등록 완료"}

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# UPDATE
async def services_gym_machine_update(db: AsyncSession, g_id: int, m_id: int, qty: int):
    try:
        obj = await gym_machine_crud.crud_gym_machine_get(db, g_id, m_id)

        if not obj:
            raise HTTPException(status_code=404, detail="기구 정보 없음")

        obj.qty = qty

        await db.commit()
        await db.refresh(obj)

        return {"msg": "수량 수정 완료"}

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# DELETE
async def services_gym_machine_delete(db: AsyncSession, g_id: int, m_id: int):
    try:
        obj = await gym_machine_crud.crud_gym_machine_get(db, g_id, m_id)

        if not obj:
            raise HTTPException(status_code=404, detail="기구 정보 없음")

        await gym_machine_crud.crud_gym_machine_delete(db, obj)

        await db.commit()

        return {"msg": "기구 제거 완료"}

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# LIST
async def services_gym_machine_get(db: AsyncSession, g_id: int):
    try:
        machines = await gym_machine_crud.crud_gym_machines_get_id(db, g_id)

        return [
            {
                "g_id": m.g_id,
                "m_id": m.m_id,
                "qty": m.qty
            }
            for m in machines
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))