from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import func
from app.db.models.like_machines import Like_Machine
from app.db.scheme.like_machines import Like_Machine_Create


class Like_Machine_Crud:
    # 운동기구 좋아요 토글
    @staticmethod
    async def crud_like_machines_toggle(db: AsyncSession, u_id: int, m_id: int) -> dict:
        # 기존 좋아요 확인
        query = select(Like_Machine).where(Like_Machine.u_id == u_id, Like_Machine.m_id == m_id)
        existing_like = await db.scalar(query)

        if existing_like:
            await db.delete(existing_like)
            status = "unliked"
        else:
            new_like = Like_Machine(u_id=u_id, m_id=m_id)
            db.add(new_like)
            status = "liked"

        await db.flush()
        
        return {"status": status}
    

    # 운동기구 좋아요 개수
    @staticmethod
    async def crud_like_machines_count(db:AsyncSession, m_id:int)->int|None:
        query = (
        select(func.count())
        .select_from(Like_Machine)
        .filter(Like_Machine.m_id == m_id)
        )   

        db_data = await db.execute(query)
        
        return db_data.scalar() or 0


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
    

