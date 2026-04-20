from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.comments import Comment
from app.db.scheme.comments import CommentCreate,CommentUpdate

class CommentCrud:

    #댓글 추가
    @staticmethod
    async def crud_comments_create(db:AsyncSession, comment_data:CommentCreate, u_id:int):
        new_comment = Comment(
            b_id = comment_data.b_id,
            u_id = u_id,
            c_content = comment_data.c_content
        )
        db.add(new_comment)
        await db.flush()
        return new_comment
    
    #해당 게시글 댓글 조회
    @staticmethod
    async def crud_board_comments_read(db:AsyncSession, b_id:int):
        stmt = select(Comment).where(Comment.b_id == b_id).order_by(Comment.created_at.asc())
        result = await db.execute(stmt)
        comments = result.scalars().all()
        return comments
    
    #댓글 수정
    @staticmethod
    async def crud_comments_update(db:AsyncSession, db_comment:Comment, comment_data:CommentUpdate):
        if comment_data.c_content is not None:
            db_comment.c_content = comment_data.c_content
        return db_comment
    
    #댓글 삭제
    @staticmethod
    async def crud_comments_delete(db:AsyncSession, db_comment:Comment):
        await db.delete(db_comment)