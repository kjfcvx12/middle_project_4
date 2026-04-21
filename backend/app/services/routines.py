from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.db.crud import Routine_CRUD
from app.db.scheme.routines import Routine_Create, Routine_Update
from fastapi import HTTPException

# 루틴 생성 서비스
async def services_routines_create(
        db:AsyncSession,
        data : Routine_Create,
        u_id : int
):
    routine_dict = data.model_dump()
    routine_dict["u_id"] = u_id

    new_routine = await Routine_CRUD.crud_routines_create(db,routine_dict)

    await db.commit()
    await db.refresh(new_routine)

    return new_routine

# 루틴 전체 읽기
async def services_routines_read_all(
        db: AsyncSession,
        name: str | None = None,
        p_id:int | None = None,
        u_id:int | None = None
):
    return await Routine_CRUD.crud_routines_read_list(db,name,p_id,u_id)

# 루틴 아이디 기반 읽기
async def services_routines_read_detail_by_id(
        db:AsyncSession,
        r_id:int
):
    read_routine = await Routine_CRUD.crud_routines_read_detail_by_id(db, r_id)
    
    if not read_routine:
        return None

    return read_routine


# 루틴 업데이트
async def services_routines_update(
        db:AsyncSession,
        r_id : int,
        data: Routine_Update,
        u_id : int
):
    new_routine = await Routine_CRUD.crud_routines_read_by_id(db,r_id)

    if not new_routine :
        return None
    
    if new_routine.u_id != u_id:
        raise HTTPException(403,"권한이 없습니다")
    
    new_routine = await Routine_CRUD.crud_routines_update_by_id(
        db, r_id, data.model_dump(exclude_unset=True)
    )

    await db.commit()
    await db.refresh(new_routine)

    return new_routine

# 루틴 삭제
async def services_routines_delete(
        db:AsyncSession,
        r_id:int,
        u_id:int
):
    delete_routine = await Routine_CRUD.crud_routines_read_by_id(db, r_id)

    if not delete_routine:
        return False
    
    if delete_routine.u_id != u_id:
        raise HTTPException(403,"권한이 없습니다")
    
    success_delete_routine = await Routine_CRUD.crud_routines_delete(db, r_id)

    if not success_delete_routine:
        return False
    
    await db.commit()

    return True


    
    
    

        
    