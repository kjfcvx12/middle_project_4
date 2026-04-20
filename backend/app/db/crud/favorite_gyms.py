from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.favorite_gyms import Favorite_Gym 
from app.db.scheme.favorite_gyms import Like_Gym_Create, Like_Gym_Read



class Favorite_Gym_Crud:
    # 헬스장 즐겨찾기 생성
    @staticmethod
    async def crud_favorite_gyms_create(db:AsyncSession, fg: Like_Gym_Create) -> str:          
        db_data=Favorite_Gym(**fg)
        db.add(db_data)
        await db.flush()
        return '헬스장 즐겨찾기 등록'
    

    # 헬스장 즐겨찾기 생성
    @staticmethod
    async def crud_favorite_gyms_delete(db:AsyncSession , f_g_id:int)->str|None:
        db_data = await db.get(Favorite_Gym, f_g_id)
        if db_data:
            await db.delete(db_data)
            await db.flush()
            return '헬스장 즐겨찾기 취소'
        return None