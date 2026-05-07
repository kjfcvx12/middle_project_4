from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import func
from app.db.models.like_comments import Like_Comment
from app.db.scheme.like_comments import Like_Comment_Create



class Like_Comment_Crud:
    # 댓글 좋아요 토글
    @staticmethod
    async def crud_like_comments_toggle(db: AsyncSession, u_id: int, c_id: int) -> dict:
        # 기존 좋아요 확인
        query = select(Like_Comment).where(Like_Comment.u_id == u_id, Like_Comment.c_id == c_id)
        existing_like = await db.scalar(query)

        if existing_like:
            await db.delete(existing_like)
            status = "unliked"
        else:
            new_like = Like_Comment(u_id=u_id, c_id=c_id)
            db.add(new_like)
            status = "liked"

        await db.flush()
        
        return {"status": status}
    

    # 댓글 좋아요 개수
    @staticmethod
    async def crud_like_comments_count(db:AsyncSession, c_id:int)->int|None:
        query = (
        select(func.count())
        .select_from(Like_Comment)
        .filter(Like_Comment.c_id == c_id)
        )   

        db_data = await db.execute(query)
        
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
    
