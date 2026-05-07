from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from sqlalchemy.orm import selectinload, joinedload
from app.db.models.favorite_gyms import Favorite_Gym 
from app.db.scheme.favorite_gyms import Favorite_Gym_Create, Favorite_Gym_Read


class Favorite_Gym_Crud:
    # 헬스장 즐겨찾기 토글
    @staticmethod
    async def crud_favorite_gyms_toggle(db: AsyncSession, u_id: int, g_id: int) -> dict:
        # 기존 즐겨찾기 확인
        query = select(Favorite_Gym).where(Favorite_Gym.u_id == u_id, Favorite_Gym.g_id == g_id)
        existing_fav = await db.scalar(query)

        if existing_fav:
            await db.delete(existing_fav)
            status = "unfavorite"
        else:
            new_fav = Favorite_Gym(u_id=u_id, g_id=g_id)
            db.add(new_fav)
            status = "favorited"

        await db.flush()
        
        return {"status": status}
    

    # 유저 헬스장 즐겨찾기 목록 조회
    @staticmethod
    async def crud_favorite_gyms_by_u_id(db:AsyncSession, u_id:int) -> list[Favorite_Gym_Read]:
        db_data=await db.execute(select(Favorite_Gym)
                                 .options(joinedload(Favorite_Gym.gym))
                                 .where(Favorite_Gym.u_id==u_id)
                                 .order_by(Favorite_Gym.f_g_id.desc()))
        
        return db_data.scalars().all()
    

    # 유저 헬스장 즐겨찾기 수 반환
    @staticmethod
    async def crud_favorite_gyms_count(db: AsyncSession, g_id: int) -> int:
        result = await db.execute(
            select(func.count(Favorite_Gym.f_g_id))
            .where(Favorite_Gym.g_id == g_id)
        )
        return result.scalar() or 0