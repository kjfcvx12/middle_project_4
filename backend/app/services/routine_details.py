from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.db.crud import Routine_Detail_CRUD
from app.db.scheme.routine_details import Routine_Detail_Create, Routine_Detail_Update

class Routine_Detail_Services:

    # 루틴 디테일 생성
    async def services_routine_details_create(db:AsyncSession, data : Routine_Detail_Create):
        
        try:
            new_routine_detail = await Routine_Detail_CRUD.crud_routine_details_create(db,data.model_dump())

            await db.commit()

            return new_routine_detail
        except Exception:
            await db.rollback()
            raise HTTPException(400, "운동 추가 실패")

    # 루틴 아이디 기반으로 루틴 디테일 읽어오기
    async def services_routine_details_read_by_id(db:AsyncSession, r_id : int):
        read_routine_detail = await Routine_Detail_CRUD.crud_routine_details_read_by_id(db, r_id)

        if not read_routine_detail :
            return None
        
        return read_routine_detail

    # 루틴 디테일 아이디 기반으로 디테일 읽기
    async def service_routine_detail_read_by_r_d_id(
            db: AsyncSession,
            r_d_id: int
    ):
        read_routine_detail = await Routine_Detail_CRUD.crud_routine_detail_get_by_r_d_id(db,r_d_id)

        if not read_routine_detail:
            return None
        return read_routine_detail

    # 루틴 디테일 아이디 기반 업데이트
    async def services_routine_details_update(db:AsyncSession, r_d_id:int, data : Routine_Detail_Update, u_id:int):

        update_routine_detail = await Routine_Detail_CRUD.crud_routine_detail_get_by_r_d_id(db,r_d_id)

        if not update_routine_detail:
            return None
        
        if update_routine_detail.routine.u_id != u_id:
            raise HTTPException(403, "권한이 없습니다")
        
        try:
            update_routine_detail = await Routine_Detail_CRUD.crud_routine_details_update(
                db, r_d_id, data.model_dump(exclude_unset=True)
            )

            await db.commit()

            return update_routine_detail
        except Exception:
            await db.rollback()
            raise HTTPException(400, "수정 실패")

    # 루틴 디테일 기반 삭제
    async def services_routine_details_delete(
            db: AsyncSession,
            r_d_id : int,
            u_id: int
    ):
        delete_routine_detail = await Routine_Detail_CRUD.crud_routine_detail_get_by_r_d_id(db, r_d_id)

        if not delete_routine_detail:
            return False
        
        if delete_routine_detail.routine.u_id != u_id:
            raise HTTPException(403, "권한이 없습니다")
        
        try:
            success_delete_routine_detail = await Routine_Detail_CRUD.crud_routine_details_delete(db, r_d_id)

            if not success_delete_routine_detail:
                return False
            
            await db.commit()

            return True
        except Exception:
            await db.rollback()
            raise HTTPException(400, "삭제 실패")

