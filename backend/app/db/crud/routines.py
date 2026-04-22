from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from ..models import Routine
from ..scheme import Routine_Create, Routine_Update
from fastapi import APIRouter, Depends, HTTPException


class Routine_CRUD :

    router = APIRouter(prefix="/routines", tags=["Routine"])

    # 루틴 생성
    @staticmethod
    async def crud_routines_create(db:AsyncSession, data : dict)-> Routine :
        new_routine = Routine(**data)
        db.add(new_routine)
        await db.flush()
        

        return new_routine
    
    # r_id 기반 단일조회
    @staticmethod
    async def crud_routines_read_by_id(db:AsyncSession, r_id:int) -> Routine | None :
        query = (
            select(Routine).options(joinedload(Routine.part)).where(Routine.r_id == r_id)
        )

        result = await db.execute(query)

        return result.scalars().first()

    # 루틴 전체 조회
    @staticmethod
    async def crud_routines_read_list(db:AsyncSession, name:str |None =None,
                                      p_id:int |None=None,
                                      u_id:int |None=None):
        query = (select(Routine).options(joinedload(Routine.part)))

        if name:
            query = query.where(Routine.r_name.contains(name))
        if p_id:
            query = query.where(Routine.p_id == p_id)
        if u_id:
            query = query.where(Routine.u_id == u_id)

        result = await db.execute(query)
        
        return result.scalars().all()
    
    # 루틴 상세(디테일아님) 루틴아이디로 조회
    @staticmethod
    async def crud_routines_read_detail_by_id(db:AsyncSession, r_id:int):
        query = (
            select(Routine).options(joinedload(Routine.part)).where(Routine.r_id==r_id)
        )
        result = await db.execute(query)
        
        return result.scalars().first()
    

    # 루틴 아이디로 불러와서 값 수정 업데이트
    @staticmethod
    async def crud_routines_update_by_id(db:AsyncSession , r_id:int, data:dict):
        upadate_routine = await db.get(Routine, r_id)

        if not upadate_routine:
            return None
        
        for key, value in data.items():
            setattr(upadate_routine, key, value)

        await db.flush()
        return upadate_routine
    
    # 루틴 아이디 불러와서 값 있으면 삭제
    @staticmethod
    async def crud_routines_delete(db:AsyncSession, r_id : int):
        delete_routine = await db.get(Routine, r_id)

        if not delete_routine:
            return False
        await db.delete(delete_routine)
        return True
    