from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db.scheme.comments import CommentCreate, CommentUpdate, CommentRead
from app.services.comments import CommentService

router = APIRouter(prefix="/comments", tags=["Comment"])

#댓글 추가
@router.post("/comments")
async def routers_comments_create(comment:CommentCreate, db:AsyncSession=Depends(get_db)):
    db_comment = CommentService.services_comments_create(db,comment)
    return await db_comment

#해당 게시글 댓글 조회
@router.get("/boards/{b_id}")
async def routers_board_comments_read(
    page:int = Query(1, ge=1),
    size:int = Query(10, ge=1),
    sort:str=Query("created_at,desc"),
    keyword:str | None = Query(None),
    db:AsyncSession = Depends(get_db)):

    return await CommentService.services_board_comments_read(db, page, size, sort, keyword)

#댓글 수정
@router.put("/comments/{c_id}")
async def routers_comments_update(c_id:int,comment_data:CommentUpdate, db:AsyncSession = Depends(get_db)):
    return await CommentService.services_comments_update(db, c_id, comment_data)

#게시물 삭제
@router.delete("/comments/{c_id}")
async def routers_comments_delete(c_id:int, db:AsyncSession = Depends(get_db)):
    return await CommentService.services_comments_delete(db, c_id)