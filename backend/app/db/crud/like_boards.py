from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import func
from app.db.models.like_boards import Like_Board
from app.db.scheme.like_boards import Like_Board_Create



class Like_Board_Crud:
    # 게시글 좋아요
    @staticmethod
    async def crud_like_boards_create(db:AsyncSession, lb: Like_Board_Create) -> str:          
        db_data=Like_Board(**lb.model_dump())
        db.add(db_data)
        await db.flush()
        return '게시글 좋아요'
    

    # 게시글 좋아요 취소
    @staticmethod
    async def crud_like_boards_delete(db:AsyncSession , l_b_id:int)->str|None:
        db_data = await db.get(Like_Board, l_b_id)
        if db_data:
            await db.delete(db_data)
            await db.flush()
            return '게시글 좋아요 취소'
        return None
    

    # 게시글 좋아요 개수
    @staticmethod
    async def crud_like_boards_count(db:AsyncSession, b_id:int)->int|None:
        db_data=await db.execute(select(func.count(Like_Board)).
                                 filter(Like_Board.b_id==b_id))
        
        return db_data.scalar()


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
    
