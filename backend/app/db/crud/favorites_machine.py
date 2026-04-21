from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models.favorites_machine import Favorite_Machine


class FavoriteMachineCrud:

    # 조회
    @staticmethod
    async def crud_get_favorites_machine(db: AsyncSession, user_id: int):
        result = await db.execute(
            select(Favorite_Machine).where(
                Favorite_Machine.u_id == user_id
            )
        )
        return result.scalars().all()


    # 삭제
    @staticmethod
    async def crud_delete_favorite_machine(db: AsyncSession, user_id: int, m_id: int):
        result = await db.execute(
            select(Favorite_Machine).where(
                Favorite_Machine.u_id == user_id,
                Favorite_Machine.m_id == m_id
            )
        )
        fav = result.scalar_one_or_none()

        if fav:
            await db.delete(fav)
            await db.flush()
            return True

        return False


    # 토글
    @staticmethod
    async def crud_toggle_favorite_machine(db: AsyncSession, user_id: int, m_id: int):
        result = await db.execute(
            select(Favorite_Machine).where(
                Favorite_Machine.u_id == user_id,
                Favorite_Machine.m_id == m_id
            )
        )
        fav = result.scalar_one_or_none()

        if fav:
            await db.delete(fav)
            await db.flush()
            return "removed"

        new_fav = Favorite_Machine(u_id=user_id, m_id=m_id)
        db.add(new_fav)
        await db.flush()

        return "added"