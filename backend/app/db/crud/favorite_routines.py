from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from app.db.models.favorite_routines import Favorite_Routine
from app.db.scheme.favorite_routines import Favorite_Routine_Create, Favorite_Routine_Read


class Favorite_Routine_Crud:
    # 루틴 즐겨찾기 등록
    @staticmethod
    async def crud_favorite_routines_create(db:AsyncSession, fm: Favorite_Routine_Create) -> str:          
        db_data=Favorite_Routine(**fm.model_dump())
        db.add(db_data)
        await db.flush()
        return '루틴 즐겨찾기 등록'
    

    # 루틴 즐겨찾기 취소
    @staticmethod
    async def crud_favorite_routines_delete(db:AsyncSession , f_m_id:int)->str|None:
        db_data = await db.get(Favorite_Routine, f_m_id)
        if db_data:
            await db.delete(db_data)
            await db.flush()
            return '루틴 즐겨찾기 취소'
        return None
    

    # 유저 루틴 즐겨찾기 목록 조회
    @staticmethod
    async def crud_favorite_routines_by_u_id(db:AsyncSession, u_id:int) -> list[Favorite_Routine_Read]:
        db_data=await db.execute(select(Favorite_Routine)
                                 .options(joinedload(Favorite_Routine.routine))
                                 .where(Favorite_Routine.u_id==u_id)
                                 .order_by(Favorite_Routine.f_r_id.desc()))
        
        return db_data.scalars().all()