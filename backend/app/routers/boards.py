from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db.scheme.boards import BoardCreate, BoardRead, BoardUpdate
from app.services.boards import BoardService

router = APIRouter(prefix="/boards", tags=["Board"])

#게시물 추가
@router.post("/boards", response_model=BoardCreate)
async def routers_boards_create(board:BoardCreate, db:AsyncSession = Depends(get_db)):
    db_board = BoardService.services_boards_create(db,board)
    return db_board

#게시물 전체조회
@router.get("/boards", response_model=list[BoardRead])
async def routers_boards_all_read(db:AsyncSession = Depends(get_db)):
    return await BoardService.services_boards_all_read(db)

#게시물 수정
@router.put("/boards/{b_id}", response_model=BoardUpdate)
async def routers_boards_update(b_id:int, board_data:BoardUpdate, db:AsyncSession = Depends(get_db)):
    return await BoardService.services_boards_update(db,board_data, b_id)

#게시물 삭제
@router.delete("/boards/{b_id}")
async def routers_boards_delete(b_id:int, db:AsyncSession = Depends(get_db)):
    return await BoardService.services_boards_delete(db, b_id)
