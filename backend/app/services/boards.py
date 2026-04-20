from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.db.models import Board
from app.db.crud.boards import BoardCrud
from app.db.scheme.boards import BoardCreate, BoardUpdate

class BoardService:

    #게시물 추가
    @staticmethod
    async def services_boards_create(db:AsyncSession, board_data:BoardCreate):
        if not board_data.b_content or not board_data.b_content.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="내용은 비어있을 수 없습니다")
        stmt = select(Board).where(Board.u_id == board_data.u_id)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 사용자입니다")
        return await BoardCrud.crud_boards_create(db, board_data)
    
    #게시물 전체조회
    @staticmethod
    async def services_boards_all_read(db:AsyncSession):
        return await BoardCrud.crud_boards_all_read(db)
    
    #게시물 수정
    @staticmethod
    async def services_boards_update(db:AsyncSession,b_id:int, board_data:BoardUpdate):
        stmt = select(Board).where(Board.b_id == b_id)
        result = await db.execute(stmt)
        db_board = result.scalar_one_or_none()

        if not db_board:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="게시물을 찾을 수 없습니다")
        
        if board_data.content is not None and not board_data.content.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="내용은 비어있을 수 없습니다")

        return await BoardCrud.crud_boards_update(db, db_board, board_data)

    #게시물 삭제
    @staticmethod
    async def services_boards_delete(db:AsyncSession, b_id:int):
        stmt = select(Board).where(Board.b_id == b_id)
        result = await db.execute(stmt)
        db_board = result.scalar_one_or_none()

        if not db_board:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="게시물을 찾을 수 없습니다")
        
        
        await BoardCrud.crud_boards_delete(db, db_board)
        return {"message": "게시물이 삭제되었습니다"}