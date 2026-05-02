from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.routine_details import Routine_Detail_Services
from app.core.auth import auth_get_u_id
from app.db.scheme import Routine_Detail_Create, Routine_Detail_Update

router=APIRouter(prefix="/routine_details", tags=["Rouine_Detail"])

@router.post("/")
async def routers_routine_details_create(
    data : Routine_Detail_Create,
    db:AsyncSession=Depends(get_db)
):
    await Routine_Detail_Services.services_routine_details_create(db,data)

    return {"msg" : "운동 추가 완료"}

@router.get("/{r_id}")
async def routers_routine_details_read_by_r_id(
    r_id:int,
    db:AsyncSession = Depends(get_db)
):
    read_routine_details = await Routine_Detail_Services.services_routine_details_read_by_id(
        db,r_id
    )

    return{
        "data" : [
            {
                "m_id" : i.m_id,
                "m_name" : i.machine.m_name if i.machine else None,
                "step" : i.step,
                "sets" : i.sets,
                "reps" : i.reps,
                "rest_time" : i.rest_time,
                "p_name" : i.machine.part.p_name if i.machine and i.machine.part else None,
                "weight" : i.weight
            }
            for i in read_routine_details
        ]
    }

@router.get("/one/{r_d_id}")
async def routers_routine_detail_read_by_r_d_id(
    r_d_id :int,
    db: AsyncSession=Depends(get_db),
    u_id : int = Depends(auth_get_u_id)
):
    read_routine_detail = await Routine_Detail_Services.service_routine_detail_read_by_r_d_id(db,r_d_id)

    return{
        "r_d_id" : read_routine_detail.r_d_id,
        "r_id" : read_routine_detail.r_id,
        "m_id" : read_routine_detail.m_id,
        "m_name" : read_routine_detail.machine.m_name if read_routine_detail.machine else None,
        "step" : read_routine_detail.step,
        "sets" : read_routine_detail.sets,
        "reps" : read_routine_detail.reps,
        "rest_time" : read_routine_detail.rest_time,
        "weight" : read_routine_detail.weight,
        "p_name" : (read_routine_detail.machine.part.p_name if 
                    read_routine_detail.machine and 
                    read_routine_detail.machine.part else None)
    }

@router.put("{r_d_id}")
async def routers_routines_details_update(
    r_d_id : int,
    data : Routine_Detail_Update,
    db:AsyncSession = Depends(get_db),
    u_id : int = Depends(auth_get_u_id)
):
    await Routine_Detail_Services.services_routine_details_update(db,r_d_id,data,u_id)

    return {"msg" : "수정완료"}

@router.delete("/{r_d_id}")
async def routers_routine_details_delete(
    r_d_id:int,
    db:AsyncSession = Depends(get_db),
    u_id : int = Depends(auth_get_u_id)
):
    await Routine_Detail_Services.services_routine_details_delete(db,r_d_id,u_id)

    return {"msg" : "삭제완료"}