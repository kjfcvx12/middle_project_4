from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.db.models import Comment
from app.db.crud.comments import CommentCrud
from app.db.scheme.comments import CommentCreate, CommentUpdate

class CommentService:
    
    #댓글 추가
    @staticmethod
    async def services_comments_create(db:AsyncSession, comment_data:CommentCreate):
        if not comment_data.content or not comment_data.content.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="내용은 비어있을 수 없습니다")
        stmt = select(Comment).where(Comment.u_id == comment_data.u_id)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 사용자입니다")
        return await CommentCrud.crud_comments_create(db, comment_data)
    
    #댓글 전체조회
    @staticmethod
    async def services_comments_all_read(db:AsyncSession):
        return await CommentCrud.crud_comments_all_read(db)
    
    #댓글 수정
    @staticmethod
    async def services_comments_update(db:AsyncSession, c_id:int, comment_data:CommentUpdate):
        stmt = select(Comment).where(Comment.c_id == c_id)
        result = await db.execute(stmt)
        db_comment = result.scalar_one_or_none()

        if not db_comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="댓글을 찾을 수 없습니다")
        
        if comment_data.content is not None and not comment_data.content.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="내용은 비어있을 수 없습니다")
        
        return await CommentCrud.crud_comments_update(db, db_comment, comment_data)
    
    #댓글 삭제
    @staticmethod
    async def services_comments_delete(db:AsyncSession, c_id:int):
        stmt = select(Comment).where(Comment.c_id == c_id)
        result = await db.execute(stmt)
        db_comment = result.scalar_one_or_none()

        if not db_comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="댓글을 찾을 수 없습니다")
        
        await CommentCrud.crud_comments_delete(db, db_comment)
        return {"message":"댓글이 삭제되었습니다"}