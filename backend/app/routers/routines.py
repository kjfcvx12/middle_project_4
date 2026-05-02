from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.routines import Routine_Services
from app.core.auth import auth_get_admin_id, auth_get_u_id, auth_get_staff_role
from app.db.scheme.routines import Routine_Create, Routine_Update

router = APIRouter(prefix="/routines", tags=["Routine"])

# 루틴 생성 라우터
@router.post("/")
async def routers_routines_create(
    data : Routine_Create,
    db : AsyncSession=Depends(get_db),
    u_id: int = Depends(auth_get_u_id)
):
    new_routine = await Routine_Services.services_routines_create(db,data,u_id)

    return {"msg":"루틴 생성 완료",
            "r_id": new_routine.r_id}
# 루틴 전체 조회 라우터
@router.get("/")
async def routers_routines_read_all(
    name:str | None=None,
    p_id:int | None=None,
    u_id:int = Depends(auth_get_u_id),
    db:AsyncSession=Depends(get_db)
):
    read_routines = await Routine_Services.services_routines_read_all(db,name,p_id,u_id)

    return {
        "data": [
            {
                "r_id": i.r_id,
                "r_name": i.r_name,
                "u_id": i.u_id,
                "p_id": i.p_id,
                "p_name": i.part.p_name if i.part else None
            }
            for i in read_routines
        ]
    }

# 루틴 아이디기반 상세 조회 라우터
@router.get("/{r_id}")
async def routers_routines_read_detail_by_r_id(r_id:int, db:AsyncSession=Depends(get_db)):
    read_routine = await Routine_Services.services_routines_read_detail_by_id(db,r_id)

    return{
        "r_id":read_routine.r_id,
        "r_name":read_routine.r_name,
        "u_id":read_routine.u_id,
        "p_id":read_routine.p_id,
        "p_name":read_routine.part.p_name if read_routine.part else None
    }

# 루틴 업데이트 라우터
@router.put("/{r_id}")
async def routers_routines_update(r_id:int,data:Routine_Update,u_id:int=Depends(auth_get_u_id),db:AsyncSession=Depends(get_db)):
    await Routine_Services.services_routines_update(db,r_id,data,u_id)

    return{"msg":"루틴 수정 완료"}


# 루틴 삭제 라우터
@router.delete("/{r_id}")
async def routers_routines_delete(r_id:int,u_id:int = Depends(auth_get_u_id),db:AsyncSession=Depends(get_db)):
    await Routine_Services.services_routines_delete(db,r_id,u_id)

    return {"msg":"삭제 완료"}