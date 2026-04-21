from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select, func
from app.db.models.like_machines import Like_Machine
from app.db.scheme.like_machines import Like_Machine_Create


class Like_Machine_Crud:
    # 운동기구 좋아요
    @staticmethod
    async def crud_like_machines_create(db:AsyncSession, lm: Like_Machine_Create) -> str:          
        db_data=Like_Machine(**lm.model_dump())
        db.add(db_data)
        await db.flush()
        return '운동기구 좋아요'
    

    # 운동기구 좋아요 취소
    @staticmethod
    async def crud_like_machines_delete(db:AsyncSession , l_m_id:int)->str|None:
        db_data = await db.get(Like_Machine, l_m_id)
        if db_data:
            await db.delete(db_data)
            await db.flush()
            return '운동기구 좋아요 취소'
        return None
    

    # 운동기구 좋아요 개수
    @staticmethod
    async def crud_like_machines_count(db:AsyncSession, m_id:int)->int|None:
        db_data=await db.execute(select(func.count(Like_Machine)).
                                 filter(Like_Machine.m_id==m_id))
        
        return db_data.scalar()

