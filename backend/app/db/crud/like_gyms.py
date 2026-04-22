from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import func
from app.db.models.like_gyms import Like_Gym
from app.db.scheme.like_gyms import Like_Gym_Create


class Like_Gym_Crud:
    # 체육관 좋아요
    @staticmethod
    async def crud_like_gyms_create(db:AsyncSession, lg: Like_Gym_Create) -> str:          
        db_data=Like_Gym(**lg.model_dump())
        db.add(db_data)
        await db.flush()
        return '체육관 좋아요'
    

    # 체육관 좋아요 취소
    @staticmethod
    async def crud_like_gyms_delete(db:AsyncSession , l_g_id:int)->str|None:
        db_data = await db.get(Like_Gym, l_g_id)
        if db_data:
            await db.delete(db_data)
            await db.flush()
            return '체육관 좋아요 취소'
        return None
    

    # 체육관 좋아요 개수
    @staticmethod
    async def crud_like_gyms_count(db:AsyncSession, g_id:int)->int|None:
        db_data=await db.execute(select(func.count(Like_Gym)).
                                 filter(Like_Gym.g_id==g_id))
        
        return db_data.scalar()
    

    # 유저 좋아요 체육관 page 조회
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
    



