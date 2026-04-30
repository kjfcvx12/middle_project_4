from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models.gym_staffs import Gym_Staff


# CREATE
async def crud_gym_staffs_create(db: AsyncSession, obj: Gym_Staff):
    db.add(obj)
    await db.flush()
    return obj


# DELETE
async def crud_gym_staffs_delete(db: AsyncSession, obj: Gym_Staff):
    await db.delete(obj)
    await db.flush()


# LIST (특정 헬스장 트레이너 조회)
async def crud_gym_staffs_get(db: AsyncSession, g_id: int):
    result = await db.execute(
        select(Gym_Staff).where(Gym_Staff.g_id == g_id)
    )
    return result.scalars().all()


# EXIST CHECK
async def crud_gym_staffs_get_one(db: AsyncSession, g_id: int, u_id: int):
    result = await db.execute(
        select(Gym_Staff).where(
            Gym_Staff.g_id == g_id,
            Gym_Staff.u_id == u_id
        )
    )
    return result.scalar_one_or_none()