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

            return {
                "msg": "게시글 작성 성공",
                "data": new_board
        }

        except Exception:
            await db.rollback()
            raise
    
    #게시물 조회
    @staticmethod
    async def services_boards_read(
        db: AsyncSession,
        page: int = 1,
        size: int = 10,
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

        return {
            "msg": "조회 성공",
            "page": page,
            "size": size,
            "total_count": total_count,
            "data": boards
    }
    
    #게시글 상세조회
    @staticmethod
    async def services_boards_read_detail(db: AsyncSession, b_id: int):
        board = await BoardCrud.crud_boards_read_detail(db, b_id)

        if not board:
            raise HTTPException(status_code=404,detail="게시글을 찾을 수 없습니다")

        return {"msg": "조회 성공","data": board}
    
    
    #게시물 수정
    @staticmethod
    async def services_boards_update(db:AsyncSession,b_id:int, board_data:BoardUpdate):
        stmt = select(Board).where(Board.b_id == b_id)
        result = await db.execute(stmt)
        db_board = result.scalar_one_or_none()

        if not db_board:
            raise HTTPException(status_code=404, detail="게시물을 찾을 수 없습니다")
        
        if board_data.b_content is not None and not board_data.b_content.strip():
            raise HTTPException(status_code=400, detail="내용은 비어있을 수 없습니다")

        return await BoardCrud.crud_boards_update(db, db_board, board_data)

    #게시물 삭제
    @staticmethod
    async def services_boards_delete(db:AsyncSession, b_id:int):
        stmt = select(Board).where(Board.b_id == b_id)
        result = await db.execute(stmt)
        db_board = result.scalar_one_or_none()

        if not db_board:
            raise HTTPException(status_code=404, detail="게시물을 찾을 수 없습니다")
        
        
        await BoardCrud.crud_boards_delete(db, db_board)
        return {"message": "게시물이 삭제되었습니다"}