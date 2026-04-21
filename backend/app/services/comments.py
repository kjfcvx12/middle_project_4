from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.db.models import Comment
from app.db.crud.comments import CommentCrud
from app.db.scheme.comments import CommentCreate, CommentUpdate

class CommentService:
    
    #댓글 추가
    @staticmethod #user push 후 함수에 current_user:int 추가
    async def services_comments_create(db: AsyncSession, comment_data: CommentCreate):
        try:
            if not comment_data.c_content or not comment_data.c_content.strip():
                raise HTTPException(status_code=400, detail="댓글 내용은 비어있을 수 없습니다")
            #user push 후 new_comment안에 1삭제 current_user 추가
            new_comment = await CommentCrud.crud_comments_create(db, comment_data,1)

            await db.commit()
            await db.refresh(new_comment)

            return {"msg": "댓글 작성 완료","data": new_comment}

        except HTTPException:
            await db.rollback()
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"댓글 작성 실패:{e}")
    
    #해당 게시글 댓글 조회
    @staticmethod
    async def services_board_comments_read(db: AsyncSession, b_id: int):
        comments = await CommentCrud.crud_board_comments_read(db, b_id)
        
        comment_list = []
        for comment in comments:
            comment_list.append({
                "c_id": comment.c_id,
                "b_id": comment.b_id,
                "u_id": comment.u_id,
                "c_content": comment.c_content,
                "created_at": comment.created_at,
                # "is_owner": comment.u_id == current_user
            })

        return {"msg": "댓글 조회 성공","data": comment_list}
    
    #댓글 수정
    @staticmethod
    async def services_comments_update(db:AsyncSession, c_id:int, comment_data:CommentUpdate):
        stmt = select(Comment).where(Comment.c_id == c_id)
        result = await db.execute(stmt)
        db_comment = result.scalar_one_or_none()

        if not db_comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="댓글을 찾을 수 없습니다")
        
        if comment_data.c_content is not None and not comment_data.c_content.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="내용은 비어있을 수 없습니다")
        
        try:
            update_comment = await CommentCrud.crud_comments_update(db, db_comment, comment_data)

            await db.commit()
            await db.refresh(update_comment)

            return{"msg":"댓글 수정 완료", "data" : update_comment}
        
        except HTTPException:
            await db.rollback()
            raise
        except Exception:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="댓글 수정 실패")
    
    #댓글 삭제
    @staticmethod
    async def services_comments_delete(db:AsyncSession, c_id:int):
        stmt = select(Comment).where(Comment.c_id == c_id)
        result = await db.execute(stmt)
        db_comment = result.scalar_one_or_none()

        if not db_comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="댓글을 찾을 수 없습니다")
        
        try:
            await CommentCrud.crud_comments_delete(db, db_comment)
            await db.commit()

            return {"message":"댓글이 삭제되었습니다"}
        
        except HTTPException:
            await db.rollback()
            raise
        except Exception:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="댓글 삭제 실패")