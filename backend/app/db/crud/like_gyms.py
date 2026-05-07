from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import func
from app.db.models.like_gyms import Like_Gym
from app.db.scheme.like_gyms import Like_Gym_Create


class Like_Gym_Crud:  
    # 체육관 좋아요 토글
    @staticmethod
    async def crud_like_gyms_toggle(db: AsyncSession, u_id: int, g_id: int) -> dict:
        # 기존 좋아요 확인
        query = select(Like_Gym).where(Like_Gym.u_id == u_id, Like_Gym.g_id == g_id)
        existing_like = await db.scalar(query)

        if existing_like:
            await db.delete(existing_like)
            status = "unliked"
        else:
            new_like = Like_Gym(u_id=u_id, g_id=g_id)
            db.add(new_like)
            status = "liked"

        await db.flush()
        
        return {"status": status}

    

    # 헬스장 좋아요 개수
    @staticmethod
    async def crud_like_gyms_count(db: AsyncSession, g_id: int) -> int:
        query = (
        select(func.count())
        .select_from(Like_Gym)
        .filter(Like_Gym.g_id == g_id)
        )   

        db_data = await db.execute(query)
        
        return db_data.scalar() or 0
    

    # 유저 좋아요 헬스장 page 조회
    @staticmethod
    async def crud_like_gyms_page_by_u_id(db:AsyncSession, u_id:int, page: int = 1)->list[Like_Gym]:
        size=10
        skip = (page - 1) * size
        
        query=(select(Like_Gym)
               .options(joinedload(Like_Gym.gym))
               .where(Like_Gym.u_id==u_id)
               .order_by(Like_Gym.l_g_id.desc())
               .offset(skip)
               .limit(size))
        
        result=await db.execute(query)

        return result.scalars().unique().all()
    



