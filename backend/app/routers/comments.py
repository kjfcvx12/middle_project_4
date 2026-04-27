from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db.scheme.comments import CommentCreate, CommentUpdate
from app.services.comments import CommentService

router = APIRouter(prefix="/boards", tags=["Comment"])

#댓글 추가
@router.post("/{b_id}/comments")
async def routers_comments_create(b_id:int, u_id:int, comment:CommentCreate, db:AsyncSession=Depends(get_db)):
    db_comment = await CommentService.services_comments_create(db, b_id, comment, u_id)
    return { "c_id":db_comment.c_id, "msg":"댓글 작성 완료"}

#해당 게시글 댓글 조회
@router.get("/{b_id}/comments")
async def routers_board_comments_read(b_id:int, db:AsyncSession = Depends(get_db)):
    return await CommentService.services_board_comments_read(db, b_id)

#댓글 수정
@router.put("/{b_id}/comments/{c_id}")
async def routers_comments_update(b_id:int, c_id:int,comment_data:CommentUpdate, u_id:int, db:AsyncSession = Depends(get_db)):
    await CommentService.services_comments_update(db, b_id, c_id, comment_data, u_id)
    return {"msg":"수정완료"}

#댓글 삭제
@router.delete("/{b_id}/comments/{c_id}")
async def routers_comments_delete(b_id:int, c_id:int,u_id:int, db:AsyncSession = Depends(get_db)):
    await CommentService.services_comments_delete(db=db, b_id=b_id, c_id=c_id, u_id=u_id)
    return {"msg":"댓글이 삭제되었습니다"}