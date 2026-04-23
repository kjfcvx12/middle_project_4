from app.db.models.log_details import LogDetail
from sqlalchemy.ext.asyncio import AsyncSession

# detail 생성
async def crud_create_log_details(db: AsyncSession, log_id, details):
    for d in details:
        detail = LogDetail(
            log_id=log_id,
            sets=d.sets,
            reps=d.reps,
            fail_memo=d.fail_memo,
            memo=d.memo
        )
        db.add(detail)

    await db.flush()