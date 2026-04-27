from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db.scheme.boards import BoardCreate, BoardUpdate
from app.services.boards import BoardService
from fastapi import Query


router = APIRouter(prefix="/boards", tags=["Boards"])

# 게시물 추가
@router.post("/create")
async def routers_boards_create(
    u_id: int,
    board: BoardCreate,
    db: AsyncSession = Depends(get_db)
):
    new_board = await BoardService.services_boards_create(
        db=db,
        board_data=board,
        u_id=u_id
    )

    return {
        "msg": "게시글 작성 성공",
        "data": new_board
    }

#게시물 조회
@router.get("")
async def routers_boards_read(
    page: int = Query(default=1, ge=1),
    size : int = Query(default=10, ge=1, le=100),
    sort: str = Query("created_at,desc"),
    keyword: str | None = Query(None),
    db: AsyncSession = Depends(get_db)
):
    
    boards, total_count, page = await BoardService.services_boards_read(
        db=db,
        page=page,
        size=size,
        sort=sort,
        keyword=keyword
    )
    return {
        "msg":"조회성공",
        "page":page,
        "total_count":total_count,
        "data": boards
    }

# 게시글 상세조회
@router.get("/{b_id}")
async def get_board_read_detail(
    b_id: int,
    db: AsyncSession = Depends(get_db)
):
    board = await BoardService.services_boards_read_detail(db, b_id)

    return {
        "msg": "조회 성공",
        "data": board
    }


# 게시물 수정
@router.put("/{b_id}")
async def routers_boards_update(
    b_id: int,
    board_data: BoardUpdate,
    u_id: int,
    db: AsyncSession = Depends(get_db)
):
    update_board = await BoardService.services_boards_update(
        db=db,
        b_id=b_id,
        board_data=board_data,
        u_id=u_id
    )

    return {
        "msg": "게시글 수정 완료",
        "data": update_board
    }

# 게시물 삭제
@router.delete("/{b_id}")
async def routers_boards_delete(
    b_id: int,
    u_id: int,
    db: AsyncSession = Depends(get_db)
):
    await BoardService.services_boards_delete(
        db=db,
        b_id=b_id,
        u_id=u_id
    )

    return {
        "msg": "게시글이 삭제되었습니다"
    }