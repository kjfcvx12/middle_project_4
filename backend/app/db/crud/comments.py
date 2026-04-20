from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.comments import Comment
from app.db.scheme.comments import CommentCreate,CommentUpdate

class CommentCrud:

    #댓글 추가
    @staticmethod
    async def crud_comments_create(db:AsyncSession, comment_data:CommentCreate):
        new_comment = Comment(
            c_content = comment_data.c_content
        )
        db.add(new_comment)
        await db.commit()
        await db.refresh(new_comment)
        return new_comment
    
    #댓글 전체조회
    @staticmethod
    async def crud_comments_all_read(db:AsyncSession):
        result = await db.execute(select(Comment))
        return result.scalars().all()
    
    #댓글 수정
    @staticmethod
    async def crud_comments_update(db:AsyncSession, db_comment:Comment, comment_data:CommentUpdate):
        if comment_data.c_content is not None:
            db_comment.c_content = comment_data.c_content

        await db.commit()
        await db.refresh(db_comment)
        return db_comment
    
    #댓글 삭제
    @staticmethod
    async def crud_comments_delete(db:AsyncSession, db_comment:Comment):
        await db.delete(db_comment)
        await db.commit()