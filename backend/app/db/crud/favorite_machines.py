from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from app.db.models.favorite_machines import Favorite_Machine
from app.db.scheme.favorite_machines import Favorite_Machine_Create, Favorite_Machine_Read


class Favorite_Machine_Crud:
    # 운동기구 즐겨찾기 토글
    @staticmethod
    async def crud_favorite_machines_toggle(db: AsyncSession, u_id: int, m_id: int) -> dict:
        # 기존 즐겨찾기 확인
        query = select(Favorite_Machine).where(Favorite_Machine.u_id == u_id, Favorite_Machine.m_id == m_id)
        existing_fav = await db.scalar(query)

        if existing_fav:
            await db.delete(existing_fav)
            status = "unfavorite"
        else:
            new_fav = Favorite_Machine(u_id=u_id, m_id=m_id)
            db.add(new_fav)
            status = "favorited"

        await db.flush()
        
        return {"status": status}
    

    # 유저 운동기구 즐겨찾기 목록 조회
    @staticmethod
    async def crud_favorite_machines_by_u_id(db:AsyncSession, u_id:int) -> list[Favorite_Machine_Read]:
        db_data=await db.execute(select(Favorite_Machine)
                                 .options(joinedload(Favorite_Machine.machine))
                                 .where(Favorite_Machine.u_id==u_id)
                                 .order_by(Favorite_Machine.f_m_id.desc()))
        
        
        return db_data.scalars().all()