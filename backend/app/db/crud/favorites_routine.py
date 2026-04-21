from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models.favorites_routine import Favorite_Routine


class FavoriteRoutineCrud:

    @staticmethod
    async def crud_get_favorites_routine(db: AsyncSession, user_id: int):
        result = await db.execute(
            select(Favorite_Routine).where(
                Favorite_Routine.u_id == user_id
            )
        )
        return result.scalars().all()


    @staticmethod
    async def crud_delete_favorite_routine(db: AsyncSession, user_id: int, r_id: int):
        result = await db.execute(
            select(Favorite_Routine).where(
                Favorite_Routine.u_id == user_id,
                Favorite_Routine.r_id == r_id
            )
        )
        fav = result.scalar_one_or_none()

        if fav:
            await db.delete(fav)
            await db.flush()
            return True

        return False


    @staticmethod
    async def crud_toggle_favorite_routine(db: AsyncSession, user_id: int, r_id: int):
        result = await db.execute(
            select(Favorite_Routine).where(
                Favorite_Routine.u_id == user_id,
                Favorite_Routine.r_id == r_id
            )
        )
        fav = result.scalar_one_or_none()

        if fav:
            await db.delete(fav)
            await db.flush()
            return "removed"

        new_fav = Favorite_Routine(u_id=user_id, r_id=r_id)
        db.add(new_fav)
        await db.flush()

        return "added"