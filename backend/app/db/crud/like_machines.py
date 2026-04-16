# crud_like_machines_create_like
# crud_like_machines_cancel_like
# crud_like_machine_get_like



from sqlalchemy import select
from models.like_machines import Like


#좋아요 생성
async def crud_like_machines_create_like(db, user_id, machine_id):
    created_like=Like(
        user_id=user_id,
        m_id=machine_id
    )
    db.add(created_like)
    return created_like

#좋아요 취소
async def crud_like_machines_cancel_like(db,like):
    await db.delete(like)
    return like

#좋아요 표시
async def crud_like_machine_get_like(db, user_id,machine_id):
    check_like=select(Like).where(
        Like.user_id==user_id,
        Like.m_id==machine_id
    )
    result=await db.execute(check_like)
    return result.scalar_one_or_none()