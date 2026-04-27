from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from app.db.models.favorite_gyms import Favorite_Gym 
from app.db.scheme.favorite_gyms import Favorite_Gym_Create, Favorite_Gym_Read


class Favorite_Gym_Crud:
    # 헬스장 즐겨찾기 등록
    @staticmethod
    async def crud_favorite_gyms_create(db:AsyncSession, fg: Favorite_Gym_Create) -> str:          
        db_data=Favorite_Gym(**fg.model_dump())
        db.add(db_data)
        await db.flush()
        return '헬스장 즐겨찾기 등록'
    

    # 헬스장 즐겨찾기 취소
    @staticmethod
    async def crud_favorite_gyms_delete(db:AsyncSession , f_g_id:int)->str|None:
        db_data = await db.get(Favorite_Gym, f_g_id)
        if db_data:
            await db.delete(db_data)
            await db.flush()
            return '헬스장 즐겨찾기 취소'
        return None
    

    # 유저 체육관 즐겨찾기 목록 조회
    @staticmethod
    async def crud_favorite_gyms_by_u_id(db:AsyncSession, u_id:int) -> list[Favorite_Gym_Read]:
        db_data=await db.execute(select(Favorite_Gym)
                                 .options(joinedload(Favorite_Gym.gym))
                                 .where(Favorite_Gym.u_id==u_id)
                                 .order_by(Favorite_Gym.f_g_id.desc()))
        
        return db_data.scalars().all()