from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.db.models import Board
from app.db.crud.boards import BoardCrud
from app.db.scheme.boards import BoardCreate, BoardUpdate

class BoardService:

    #게시물 추가
    @staticmethod
    async def services_boards_create(db: AsyncSession, board_data: BoardCreate, u_id:int):
        try:
            new_board = await BoardCrud.crud_boards_create(db, board_data, u_id)

            await db.commit()
            await db.refresh(new_board)

            return new_board

        except Exception:
            await db.rollback()
            raise HTTPException(status_code=400, detail="400에러")
    
    #게시물 조회
    @staticmethod
    async def services_boards_read(
        db: AsyncSession,
        size : int,
        page: int = 1,
        sort: str = "created_at,desc",
        keyword: str | None = None
):
        if keyword:
            page = 1
        
        boards, total_count = await BoardCrud.crud_boards_read(
            db=db,
            page=page,
            size=size,
            sort=sort,
            keyword=keyword
    )

        return boards, total_count, page
    
    #게시글 상세조회
    @staticmethod
    async def services_boards_read_detail(db: AsyncSession, b_id: int):
        board = await BoardCrud.crud_boards_read_detail(db, b_id)

        if not board:
            raise HTTPException(status_code=404,detail="게시글을 찾을 수 없습니다")

        return board
    
    
    #게시물 수정
    @staticmethod
    async def services_boards_update(db:AsyncSession,b_id:int, board_data:BoardUpdate, u_id:int):
        stmt = select(Board).where(Board.b_id == b_id)
        result = await db.execute(stmt)
        db_board = result.scalar_one_or_none()

        if not db_board:
            raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다")
        if db_board.u_id != u_id:
            raise HTTPException(status_code=400, detail="수정 권한이 없습니다")
        
        if board_data.b_content is not None and not board_data.b_content.strip():
            raise HTTPException(status_code=400, detail="내용은 비어있을 수 없습니다")
        
        if db_board.b_content == board_data.b_content:
            raise HTTPException(status_code=400, detail="기존 내용과 동일하여 수정할 수 없습니다")

        try:
            update_board = await BoardCrud.crud_boards_update(db, db_board, board_data, u_id)

            await db.commit()
            await db.refresh(update_board)

            return update_board
        

        except Exception:
            await db.rollback()
            raise HTTPException(status_code=400, detail="게시글 수정 실패")

    #게시물 삭제
    @staticmethod
    async def services_boards_delete(db:AsyncSession, b_id:int, u_id:int):
        stmt = select(Board).where(Board.b_id == b_id)
        result = await db.execute(stmt)
        db_board = result.scalar_one_or_none()

        if not db_board:
            raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다")
        
        if db_board.u_id != u_id:
            raise HTTPException(status_code=400, detail="삭제 권한이 없습니다")
        
        try:
            await BoardCrud.crud_boards_delete(db, db_board, u_id)
            await db.commit()

            return None

        except Exception:
            await db.rollback()
            raise HTTPException(status_code=400, detail="게시글 삭제 실패")