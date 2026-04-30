from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import func
from app.db.models.like_comments import Like_Comment
from app.db.scheme.like_comments import Like_Comment_Create



class Like_Comment_Crud:
    # 댓글 좋아요
    @staticmethod
    async def crud_like_comments_create(db:AsyncSession, lc: Like_Comment_Create) -> str:          
        db_data=Like_Comment(**lc.model_dump())
        db.add(db_data)
        await db.flush()
        return '댓글 좋아요'
    

    # 댓글 좋아요 취소
    @staticmethod
    async def crud_like_comments_delete(db:AsyncSession , l_c_id:int)->str|None:
        db_data = await db.get(Like_Comment, l_c_id)
        if db_data:
            await db.delete(db_data)
            await db.flush()
            return '댓글 좋아요 취소'
        return None
    

    # 댓글 좋아요 개수
    @staticmethod
    async def crud_like_comments_count(db:AsyncSession, c_id:int)->int|None:
        db_data=await db.execute(select(func.count(Like_Comment)).
                                 filter(Like_Comment.c_id==c_id))
        
        return db_data.scalar() or 0


    # 유저 좋아요 댓글 페이지 조회
    @staticmethod
    async def crud_like_comments_page_by_u_id(db:AsyncSession, u_id:int, page: int = 1)->list[Like_Comment]:
        size=10
        skip = (page - 1) * size
        
        query=(select(Like_Comment)
               .options(joinedload(Like_Comment.comment))
               .where(Like_Comment.u_id==u_id)
               .order_by(Like_Comment.l_c_id.desc())
               .offset(skip)
               .limit(size))
        
        result=await db.execute(query)

        return result.scalars().unique().all()
    
