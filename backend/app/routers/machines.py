#정신나갈거같아
#함수명
# router_machines_create
# router_machines_get
# router_machines_update
# router_machines_delete
# router_machines_detail

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.services.machines import Machines_Service
from app.db.scheme.machines import MachineCreate, MachineUpdate

router=APIRouter(prefix="/machines",tags=["Machine"])


#운동기구 생성
@router.post("")
async def router_machines_create(
    machine_create:MachineCreate,
    admin:int,
    db:AsyncSession=Depends(get_db)):
    return await Machines_Service.service_machines_create(db, machine_create=machine_create, admin=admin)


#운동기구 목록 조회
@router.get("")
async def router_machines_get(
    page:int=1,
    name:str|None=None,
    p_id:int|None=None,
    db:AsyncSession=Depends(get_db)):

    return await Machines_Service.service_machines_get(db,page,name,p_id)

#운동기구 상세 조회
@router.get("/{m_id}")
async def router_machines_detail(m_id:int,
                                 db:AsyncSession=Depends(get_db)):

    return await Machines_Service.service_machines_detail(db, m_id)


#운동기구 수정
@router.put("/{m_id}")
async def router_machines_update(
    m_id:int,
    machine_update:MachineUpdate,
    admin:int,
    db:AsyncSession=Depends(get_db)):

    return await Machines_Service.service_machines_update(db, m_id, machine_update,admin=admin)

#운동기구 삭제
@router.delete("/{m_id}")
async def router_machines_delete(
    m_id:int,
    admin:int,
    db:AsyncSession=Depends(get_db)):

    return await Machines_Service.service_machines_delete(db, m_id,admin=admin)