from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.favorite_machines import Favorite_Machine
from app.db.scheme.favorite_machines import Favorite_Machine_Create, Favorite_Machine_Read


class Favorite_Machine_Crud:
    # 운동기구 즐겨찾기 등록
    @staticmethod
    async def crud_favorite_machines_create(db:AsyncSession, fm: Favorite_Machine_Create) -> str:          
        db_data=Favorite_Machine(**fm.model_dump())
        db.add(db_data)
        await db.flush()
        return '운동기구 즐겨찾기 등록'
    

    # 운동기구 즐겨찾기 취소
    @staticmethod
    async def crud_favorite_machines_delete(db:AsyncSession , f_m_id:int)->str|None:
        db_data = await db.get(Favorite_Machine, f_m_id)
        if db_data:
            await db.delete(db_data)
            await db.flush()
            return '운동기구 즐겨찾기 취소'
        return None
    

    # 유저 운동기구 즐겨찾기 목록 조회
    @staticmethod
    async def crud_favorite_gyms_by_u_id(db:AsyncSession, u_id:int) -> list[Favorite_Machine_Read]:
        db_data=await db.execute(select(Favorite_Machine).
                                 filter(Favorite_Machine.u_id==u_id))
        
        return db_data.scalars().all()