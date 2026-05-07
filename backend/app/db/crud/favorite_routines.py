from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from app.db.models.favorite_routines import Favorite_Routine
from app.db.scheme.favorite_routines import Favorite_Routine_Create, Favorite_Routine_Read


class Favorite_Routine_Crud:
    # 루틴 즐겨찾기 토글
    @staticmethod
    async def crud_favorite_routines_toggle(db: AsyncSession, u_id: int, r_id: int) -> dict:
        # 기존 즐겨찾기 확인
        query = select(Favorite_Routine).where(Favorite_Routine.u_id == u_id, Favorite_Routine.r_id == r_id)
        existing_fav = await db.scalar(query)

        if existing_fav:
            await db.delete(existing_fav)
            status = "unfavorite"
        else:
            new_fav = Favorite_Routine(u_id=u_id, r_id=r_id)
            db.add(new_fav)
            status = "favorited"

        await db.flush()
        
        return {"status": status}
    

    # 유저 루틴 즐겨찾기 목록 조회
    @staticmethod
    async def crud_favorite_routines_by_u_id(db:AsyncSession, u_id:int) -> list[Favorite_Routine_Read]:
        db_data=await db.execute(select(Favorite_Routine)
                                 .options(joinedload(Favorite_Routine.routines))
                                 .where(Favorite_Routine.u_id==u_id)
                                 .order_by(Favorite_Routine.f_r_id.desc()))
        
        return db_data.scalars().all()