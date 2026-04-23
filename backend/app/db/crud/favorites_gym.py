from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models.favorites_gym import Favorite_Gym


class FavoriteGymCrud:

    # 특정 유저 즐겨찾기 조회
    @staticmethod
    async def crud_get_favorites_gym(db: AsyncSession, u_id: int):
        result = await db.execute(
            select(Favorite_Gym).where(
                Favorite_Gym.u_id == u_id
            )
        )
        return result.scalars().all()


    # 삭제
    @staticmethod
    async def crud_delete_favorite_gym(db: AsyncSession, u_id: int, gym_id: int):
        result = await db.execute(
            select(Favorite_Gym).where(
                Favorite_Gym.u_id == u_id,
                Favorite_Gym.gym_id == gym_id
            )
        )
        fav = result.scalar_one_or_none()

        if fav:
            await db.delete(fav)
            await db.flush()
            return True

        return False


    # 즐겨찾기 토글
    @staticmethod
    async def crud_toggle_favorite_gym(db: AsyncSession, u_id: int, gym_id: int):
        result = await db.execute(
            select(Favorite_Gym).where(
                Favorite_Gym.u_id == u_id,
                Favorite_Gym.gym_id == gym_id
            )
        )
        fav = result.scalar_one_or_none()

        if fav:
            await db.delete(fav)
            await db.flush()   
            return "removed"

        new_fav = Favorite_Gym(u_id=u_id, gym_id=gym_id)
        db.add(new_fav)
        await db.flush()       

        return "added"