from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.crud.logs import Log_Crud
from app.db.crud.log_detail import *


# 생성
async def service_create_log(db: AsyncSession,  u_id : int, data):
    try:
        log = await Log_Crud.crud_create_log(db, u_id, data)

        await crud_create_log_details(db, log.log_id, data.details)

        await db.commit()
        await db.refresh(log)

        return log

    except HTTPException:
        raise

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"로그 생성 실패: {e}"
        )


# 목록 조회
async def service_get_logs(db: AsyncSession, u_id : int):
    logs = await Log_Crud.crud_get_logs(db, u_id)

    if not logs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="로그가 없습니다."
        )

    return logs


# 추가: 상세 조회 (더보기)
async def service_get_log_detail(db: AsyncSession, u_id:int, log_id: int):
    log = await Log_Crud.crud_get_log_detail(db, u_id, log_id)

    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="로그가 없습니다."
        )

    return log


# 삭제
async def service_delete_log(db: AsyncSession,  u_id : int, log_id: int):
    try:
        result = await Log_Crud.crud_delete_log(db, u_id, log_id)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="삭제할 로그가 없습니다."
            )

        await db.commit()

        return {"msg": "삭제 완료"}

    except HTTPException:
        raise

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"삭제 실패: {e}"
        )