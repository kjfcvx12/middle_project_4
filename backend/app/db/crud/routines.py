from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models import Routine
from ..scheme import Routine_Create, Routine_Update

class Routine_CRUD :

    # 유저 아이디가 있으면 유저 아이디를 값에 추가하여 디비에 저장함
    # 루틴을 새로 만들 때 유저 아이디가 없어도 됨(db에 직접 넣을때를 대비)
    # 어드민이 만들어 넣는다면 어떻게 할지 회의가 필요함
    @staticmethod
    async def crud_routines_create(db:AsyncSession, 
                                   routine_data:Routine_Create, 
                                   u_id : int | None = None) -> Routine:
        routine_dict=routine_data.model_dump()
        if u_id is not None :
            routine_dict["u_id"]=u_id
        new_routine=Routine(**routine_dict)
        db.add(new_routine)
        await db.flush()
        await db.refresh(new_routine)

        return new_routine
    
    # 루틴 아이디 기준 수정할 수 있음
    # 수정할 때 모든 부분은 안넣어도됨
    @staticmethod
    async def crud_routines_update_by_id(db:AsyncSession,
                                   routine_data:Routine_Update,
                                   r_id:int) -> Routine | None:
        db_routine = await db.get(Routine, r_id)
        if db_routine :
            update_data=routine_data.model_dump(exclude_unset=True)
            for key,value in update_data.items():
                setattr(db_routine, key, value)
            await db.flush()
            return db_routine
        return None
    
    # 전체 루틴 조회 (관리자용)
    @staticmethod
    async def crud_routines_read_all(
        db:AsyncSession) -> list[Routine]:
        result = await db.execute(select(Routine))
        return result.scalars().all()

    
        
    