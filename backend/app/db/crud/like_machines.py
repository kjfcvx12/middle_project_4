from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import func
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


    # 유저 좋아요 운동기구 page 조회
    @staticmethod
    async def crud_like_machines_page_by_u_id(db:AsyncSession, u_id:int, page: int = 1)->list[Like_Machine]:
        size=10
        skip = (page - 1) * size
        
        query=(select(Like_Machine)
               .options(joinedload(Like_Machine.machine))
               .where(Like_Machine.u_id==u_id)
               .order_by(Like_Machine.l_m_id.desc())
               .offset(skip)
               .limit(size))
        
        result=await db.execute(query)

        return result.scalars().unique().all()
    

