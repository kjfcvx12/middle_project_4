from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select, func
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

