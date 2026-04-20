from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.boards import Board
from app.db.scheme.boards import BoardCreate, BoardUpdate

class BoardCrud:
    
    #게시물 추가
    @staticmethod
    async def crud_boards_create(db:AsyncSession, board_data:BoardCreate):
        new_board = Board(
            u_id = board_data.u_id,
            b_content = board_data.b_content
        )
        db.add(new_board)
        await db.commit()
        await db.refresh(new_board)
        return new_board
    
    #게시물 전체조회
    @staticmethod
    async def crud_boards_all_read(db:AsyncSession):
        result = await db.execute(select(Board))
        return result.scalars().all()
    
    #게시물 수정
    @staticmethod
    async def crud_boards_update(db:AsyncSession, db_board:Board, board_data:BoardUpdate):
        if board_data.b_content is not None:
            db_board.b_content = board_data.b_content

        await db.commit()
        await db.refresh(db_board)
        return db_board
    
    #게시물 삭제
    @staticmethod
    async def crud_boards_delete(db:AsyncSession, db_board:Board):
        await db.delete(db_board)
        await db.commit()