from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.boards import Board
from app.db.scheme.boards import BoardCreate, BoardUpdate

class BoardCrud:
    #게시물 추가
    @staticmethod
    async def crud_board_create(db:AsyncSession, board_data:BoardCreate):
        new_board = Board(
            u_id = board_data.u_id,
            content = board_data.content
        )
        db.add(new_board)
        await db.commit()
        await db.refresh(new_board)
        return new_board
    
    #게시물 전체조회
    @staticmethod
    async def crud_board_allread(db:AsyncSession):
        result = await db.execute(select(Board))
        return result.scalars().all()
    
    @staticmethod
    async def crud_board_update(db:AsyncSession, db_board:Board, board_data:BoardUpdate):
        if board_data.content is not None:
            db_board.content = board_data.content

        await db.commit()
        await db.refresh(db_board)
        return db_board
    
    #게시물 삭제
    @staticmethod
    async def crud_board_delete(db:AsyncSession, db_board:Board):
        await db.delete(db_board)
        await db.commit()