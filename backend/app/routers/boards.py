from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db.scheme.boards import BoardCreate, BoardUpdate
from app.services.boards import BoardService
from fastapi import Query
from typing import Optional


router = APIRouter(prefix="/boards", tags=["Board"])

#게시물 추가
@router.post("/boards")
async def routers_boards_create(u_id:int, board:BoardCreate, db:AsyncSession = Depends(get_db)):
    db_board = BoardService.services_boards_create(db,board, u_id)
    return await db_board

#게시물 조회
@router.get("/boards")
async def routers_boards_read(
    page: int = Query(1, ge=1),
    size : int = 10,
    sort: str = Query("created_at,desc"),
    keyword: str | None = Query(None),
    db: AsyncSession = Depends(get_db)
):
    return await BoardService.services_boards_read(
        db=db,
        page=page,
        size=size,
        sort=sort,
        keyword=keyword
    )

#게시글 상세조회
@router.get("/boards/{b_id}")
async def get_board_read_detail(b_id: int,db: AsyncSession = Depends(get_db)):
    return await BoardService.services_boards_read_detail(db, b_id)


#게시물 수정
@router.put("/boards/{b_id}")
async def routers_boards_update(b_id:int, board_data:BoardUpdate,u_id:int, db:AsyncSession = Depends(get_db)):
    return await BoardService.services_boards_update(db, b_id, board_data, u_id)

#게시물 삭제
@router.delete("/boards/{b_id}")
async def routers_boards_delete(b_id:int,u_id:int, db:AsyncSession = Depends(get_db)):
    return await BoardService.services_boards_delete(db, b_id, u_id)
