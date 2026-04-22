from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from ..models import Routine_Detail , Machine

class Routine_Detail_CRUD :
    # 세로운 루틴 디테일 생성
    @staticmethod
    async def crud_routine_details_create(db:AsyncSession,data : dict) -> Routine_Detail :
        new_routine_detail = Routine_Detail(**data)
        db.add(new_routine_detail)

        await db.flush()

        return new_routine_detail
    
    # 루틴 아이디 기반 루틴 디테일 읽기
    @staticmethod
    async def crud_routine_details_read_by_id(db:AsyncSession, r_id:int)->list[Routine_Detail]:
        query = (select(Routine_Detail)
                .options(joinedload(Routine_Detail.machine).joinedload(Machine.part))
                .where(Routine_Detail.r_id==r_id)
                .order_by(Routine_Detail.step)
        )

        result = await db.execute(query)
        return result.scalars().all()
    
    # 서비스에서 사용하기위한 루틴 읽기
    @staticmethod
    async def crud_routine_detail_get_by_r_d_id(
        db: AsyncSession,
        r_d_id: int
    ):
        query = (
            select(Routine_Detail)
            .options(joinedload(Routine_Detail.routine),joinedload(Routine_Detail.machine).joinedload(Machine.part))
            .where(Routine_Detail.r_d_id == r_d_id)
        )

        result = await db.execute(query)
        return result.scalars().first()
    
    # 루틴 디테일 업데이트 없는 작성하지 않은 매개변수들은 반영되지 않음
    @staticmethod
    async def crud_routine_details_update(db:AsyncSession,r_d_id :int,data: dict)-> Routine_Detail | None:
        new_routine_detail = await db.get(Routine_Detail, r_d_id)

        if not new_routine_detail:
            return None
        
        for key, value in data.items():
            setattr(new_routine_detail,key,value)

        await db.flush()
        return new_routine_detail
    
    # 루틴 디테일 삭제 루틴 디테일 아이디가 같다면 삭제됨
    @staticmethod
    async def crud_routine_details_delete(db:AsyncSession,r_d_id:int) -> bool:
        
        delete_routine_detail= await db.get(Routine_Detail, r_d_id)

        if not delete_routine_detail:
            return False
        
        await db.delete(delete_routine_detail)
        return True