from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.db.models import Comment
from app.db.models import Board
from app.db.crud.comments import CommentCrud
from app.db.crud.boards import BoardCrud
from app.db.scheme.comments import CommentCreate, CommentUpdate


class CommentService:
    
    #댓글 추가
    @staticmethod #user push 후 함수에 current_user:int 추가
    async def services_comments_create(db: AsyncSession, b_id:int, comment_data: CommentCreate, u_id:int):

        if not comment_data.c_content or not comment_data.c_content.strip():
            raise HTTPException(status_code=400, detail="댓글 내용은 비어있을 수 없습니다")
        
        #db에서 board데이터 불러오는 곳
        stmt = select(Board).where(Board.b_id == b_id)
        result = await db.execute(stmt)
        db_board = result.scalar_one_or_none()

        if not db_board:
            raise HTTPException(status_code=404, detail="게시글이 존재하지 않습니다")
            
        try:
            new_comment = await CommentCrud.crud_comments_create(db, b_id, comment_data,u_id)

            await db.commit()
            await db.refresh(new_comment)

            return new_comment

        
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"댓글 작성 실패:{e}")
    
    #해당 게시글 댓글 조회
    @staticmethod
    async def services_board_comments_read(db: AsyncSession, b_id: int):
        board = await BoardCrud.crud_boards_bidread(db, b_id)
        if not board:
            raise HTTPException(status_code=404, detail="게시글이 존재하지 않습니다")

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

        return comment_list
    
    #댓글 수정
    @staticmethod
    async def services_comments_update(db:AsyncSession, b_id:int, c_id:int, comment_data:CommentUpdate, u_id:int):
        stmt = select(Comment).where(Comment.c_id == c_id)
        result = await db.execute(stmt)
        db_comment = result.scalar_one_or_none()

        if not db_comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="댓글을 찾을 수 없습니다")
        if db_comment.u_id != u_id:
            raise HTTPException(status_code=400, detail="수정 권한이 없습니다")
        
        if comment_data.c_content is not None and not comment_data.c_content.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="내용은 비어있을 수 없습니다")
        
        if db_comment.c_content == comment_data.c_content:
            raise HTTPException(status_code=400, detail="기존 내용과 동일하여 수정할 수 없습니다")
        try:
            update_comment = await CommentCrud.crud_comments_update(db, b_id, db_comment, comment_data, u_id)

            await db.commit()
            await db.refresh(update_comment)

            return update_comment
        
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"댓글 수정 실패 :{e}")
    
    #댓글 삭제
    @staticmethod
    async def services_comments_delete(db:AsyncSession, b_id:int, c_id:int, u_id:int):
        stmt = select(Comment).where(Comment.c_id == c_id, Comment.b_id == b_id)
        result = await db.execute(stmt)
        db_comment = result.scalar_one_or_none()

        if not db_comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="댓글을 찾을 수 없습니다")
        if db_comment.u_id != u_id:
            raise HTTPException(status_code=400, detail="삭제 권한이 없습니다")
        try:
            await CommentCrud.crud_comments_delete(db, b_id, db_comment, u_id)
            await db.commit()

            return None
        
        
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"댓글 삭제 실패{e}")