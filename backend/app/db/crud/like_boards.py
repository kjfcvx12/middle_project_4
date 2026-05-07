from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import func
from app.db.models.like_boards import Like_Board
from app.db.scheme.like_boards import Like_Board_Create



class Like_Board_Crud:
    # 게시글 좋아요 토글
    @staticmethod
    async def crud_like_boards_toggle(db: AsyncSession, u_id: int, b_id: int) -> dict:
        # 기존 좋아요 확인
        query = select(Like_Board).where(Like_Board.u_id == u_id, Like_Board.b_id == b_id)
        existing_like = await db.scalar(query)

        if existing_like:
            await db.delete(existing_like)
            status = "unliked"
        else:
            new_like = Like_Board(u_id=u_id, b_id=b_id)
            db.add(new_like)
            status = "liked"

        await db.flush()
        
        return {"status": status}


    # 게시글 좋아요 개수
    @staticmethod
    async def crud_like_boards_count(db:AsyncSession, b_id:int)->int|None:
        query = (
        select(func.count())
        .select_from(Like_Board)
        .filter(Like_Board.b_id == b_id)
        )   

        db_data = await db.execute(query)
        
        return db_data.scalar() or 0


    # 유저 좋아요 게시글 페이지 조회
    @staticmethod
    async def crud_like_boards_page_by_u_id(db:AsyncSession, u_id:int, page: int = 1)->list[Like_Board]:
        size=10
        skip = (page - 1) * size
        
        query=(select(Like_Board)
               .options(joinedload(Like_Board.board))
               .where(Like_Board.u_id==u_id)
               .order_by(Like_Board.l_b_id.desc())
               .offset(skip)
               .limit(size))
        
        result=await db.execute(query)

        return result.scalars().unique().all()
    
