from app.db.models.logs import Log
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

class Log_Crud:
    # 로그 생성 (detail 제외)
    async def crud_create_log(db: AsyncSession, u_id, data):
        log = Log(
            u_id=u_id,
            r_id=data.r_id,
            m_id=data.m_id,
            attend=data.attend
        )
        db.add(log)
        await db.flush()  # id 확보

        return log


    # 로그 목록 조회 (detail 없음)
    async def crud_get_logs(db: AsyncSession, u_id):
        result = await db.execute(
            select(Log).where(Log.u_id == u_id)
        )
        return result.scalars().all()


    # 로그 상세 조회 (detail 포함)
    async def crud_get_log_detail(db: AsyncSession, u_id, log_id):
        result = await db.execute(
            select(Log)
            .options(selectinload(Log.details))  
            .where(
                Log.u_id == u_id,
                Log.log_id == log_id
            )
        )
        return result.scalar_one_or_none()


    # 삭제
    async def crud_delete_log(db: AsyncSession, u_id, log_id):
        result = await db.execute(
            select(Log).where(
                Log.u_id == u_id,
                Log.log_id == log_id
            )
        )
        log = result.scalar_one_or_none()

        if log:
            await db.delete(log)
            await db.flush()
            return True
        return False