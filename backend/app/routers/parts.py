from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db.scheme.parts import PartCreate
from app.services.parts import Parts_service

router=APIRouter(prefix="/parts",tags=["Part"])

#부위 생성
@router.post("")
async def router_parts_create(
    created_part:PartCreate,
    admin:int,
    db:AsyncSession=Depends(get_db)):
    return await Parts_service.service_parts_create(db, created_part, admin)

#부위 삭제
@router.delete("{p_id}")
async def router_parts_delete(
    p_id:int,
    admin:int,
    db:AsyncSession=Depends(get_db)):
    return await Parts_service.service_parts_delete(db, p_id, admin)

#부위 전체 조회
@router.get("")
async def router_parts_get(
    db:AsyncSession=Depends(get_db)):
    return await Parts_service.service_parts_get(db)


#부위 단일 조회
@router.get("")
async def router_parts_id(
    p_id:int, 
    db:AsyncSession=Depends(get_db)):
    return await Parts_service.service_parts_id(db, p_id)
