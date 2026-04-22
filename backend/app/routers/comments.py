from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db.scheme.comments import CommentCreate, CommentUpdate, CommentRead
from app.services.comments import CommentService

router = APIRouter(prefix="/comments", tags=["Comment"])

#댓글 추가
@router.post("/comments")
async def routers_comments_create(u_id:int, comment:CommentCreate, db:AsyncSession=Depends(get_db)):
    db_comment = CommentService.services_comments_create(db,comment,u_id)
    return await db_comment

#해당 게시글 댓글 조회
@router.get("/comments/{b_id}")
async def routers_board_comments_read(b_id:int, db:AsyncSession = Depends(get_db)):
    return await CommentService.services_board_comments_read(db, b_id)

#댓글 수정
@router.put("/comments/{c_id}")
async def routers_comments_update(c_id:int,comment_data:CommentUpdate, db:AsyncSession = Depends(get_db)):
    return await CommentService.services_comments_update(db, c_id, comment_data)

#게시물 삭제
@router.delete("/comments/{c_id}")
async def routers_comments_delete(c_id:int, db:AsyncSession = Depends(get_db)):
    return await CommentService.services_comments_delete(db, c_id)