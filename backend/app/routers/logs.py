from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.logs import *
from app.core.auth import auth_get_u_id
from app.db.database import get_db
from app.db.scheme.logs import LogCreate

router = APIRouter(
    prefix="/logs",
    tags=["Log"]
)


# 생성
@router.post("/")
async def create_log(
    data: LogCreate,
    db: AsyncSession = Depends(get_db),
    u_id=Depends(auth_get_u_id)
):
    return await service_create_log(db, u_id, data)


# 목록 조회
@router.get("/")
async def get_logs(
    db: AsyncSession = Depends(get_db),
    u_id=Depends(auth_get_u_id)
):
    print(" 로그 API 들어옴")
    return await service_get_logs(db, u_id)


# 더보기 (핵심)
@router.get("/{log_id}")
async def get_log_detail(
    log_id: int,
    db: AsyncSession = Depends(get_db),
    u_id=Depends(auth_get_u_id)
):
    return await service_get_log_detail(db, u_id, log_id)


# 삭제
@router.delete("/{log_id}")
async def delete_log(
    log_id: int,
    db: AsyncSession = Depends(get_db),
    u_id=Depends(auth_get_u_id)
):
    return await service_delete_log(db, u_id, log_id)