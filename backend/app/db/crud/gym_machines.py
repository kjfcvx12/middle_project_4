from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models.gym_machines import Gym_Machine


# CREATE
async def crud_gym_machine_create(db: AsyncSession, obj: Gym_Machine):
    db.add(obj)
    await db.flush()
    return obj


# READ
async def crud_gym_machine_get(db: AsyncSession, g_id: int, m_id: int):
    result = await db.execute(
        select(Gym_Machine).where(
            Gym_Machine.g_id == g_id,
            Gym_Machine.m_id == m_id
        )
    )
    return result.scalar_one_or_none()


# UPDATE
async def crud_gym_machine_update(db: AsyncSession, obj: Gym_Machine, qty: int):
    obj.qty = qty
    await db.flush()
    return obj


# DELETE
async def crud_gym_machine_delete(db: AsyncSession, obj: Gym_Machine):
    await db.delete(obj)
    await db.flush()


# LIST
async def crud_gym_machines_get_id(db: AsyncSession, g_id: int):
    result = await db.execute(
        select(Gym_Machine).where(Gym_Machine.g_id == g_id)
    )
    return result.scalars().all()