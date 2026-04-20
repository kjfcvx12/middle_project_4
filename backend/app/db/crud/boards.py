from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.boards import Board
from app.db.scheme.boards import BoardCreate, BoardUpdate
from sqlalchemy import func

class BoardCrud:
    
    #게시물 추가
    @staticmethod
    async def crud_boards_create(db:AsyncSession, board_data:BoardCreate):
        new_board = Board(
            u_id = board_data.u_id,
            b_content = board_data.b_content
        )
        db.add(new_board)
        await db.flush()
        return new_board
    
    #게시물 전체조회
    @staticmethod
    async def crud_boards_read(
        db: AsyncSession,
        page: int,
        size: int,
        sort: str,
        keyword: str | None = None):

        stmt = select(Board)
        count_stmt = select(func.count()).select_from(Board)

    # 검색
        if keyword:
            condition = Board.b_content.ilike(f"%{keyword}%")
            stmt = stmt.where(condition)
            count_stmt = count_stmt.where(condition)

    # 정렬
        sort_field, sort_order = sort.split(",")
        sort_column = getattr(Board, sort_field)

        if sort_order == "desc":
            stmt = stmt.order_by(sort_column.desc())
        else:
            stmt = stmt.order_by(sort_column.asc())

    # 페이징
        offset = (page - 1) * size
        stmt = stmt.offset(offset).limit(size)

        result = await db.execute(stmt)
        boards = result.scalars().all()

        count_result = await db.execute(count_stmt)
        total_count = count_result.scalar()

        return boards, total_count
    
    #게시글 상세조회
    @staticmethod
    async def crud_boards_read_detail(db: AsyncSession, b_id: int):
        stmt = select(Board).where(Board.b_id == b_id)
        result = await db.execute(stmt)
        board = result.scalar_one_or_none()
        return board

    
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