from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from sqlalchemy import select

from app.db.models.like_boards import Like_Board
from app.db.models.like_comments import Like_Comment
from app.db.models.like_gyms import Like_Gym
from app.db.models.like_machines import Like_Machine

from app.db.scheme.like_boards import Like_Board_Read, Like_Board_Create
from app.db.scheme.like_comments import Like_Comment_Read, Like_Comment_Create
from app.db.scheme.like_gyms import Like_Gym_Read, Like_Gym_Create
from app.db.scheme.like_machines import Like_Machine_Read, Like_Machine_Create

from app.db.crud.like_boards import Like_Board_Crud
from app.db.crud.like_comments import Like_Comment_Crud
from app.db.crud.like_gyms import Like_Gym_Crud
from app.db.crud.like_machines import Like_Machine_Crud


class Like_Service:

    # 게시글 좋아요 추가
    @staticmethod
    async def services_like_boards_create(db:AsyncSession, u_id:int, b_id:int) -> Like_Board_Read:
        try:

            query = select(Like_Board).where(
                Like_Board.u_id==u_id, 
                Like_Board.b_id==b_id)
            
            check= await db.scalar(query)

            if check:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="이미 좋아요한 게시글입니다.")

            db_data = Like_Board_Create(u_id=u_id, b_id=b_id)

            new_db=await Like_Comment_Crud.crud_like_comments_create(db, db_data)
            
            await db.commit()
            await db.refresh(new_db)
            
            return new_db
        
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                                detail=f"게시글 좋아요 실패 :{e}")


    # 게시글 좋아요 해제
    @staticmethod
    async def services_like_boards_delete(db: AsyncSession, l_b_id: int) -> dict:
        try: 
            db_data = await Like_Board_Crud.crud_like_boards_delete(db, l_b_id)
        
            if not db_data:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                    detail='해제할 좋아요가 없습니다')

            await db.commit()
            return {'message':'게시글 좋아요 해제'}
        
        except HTTPException:
            raise

        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                                detail=f"게시글 좋아요 해제 실패 :{e}")


    # 게시글 좋아요 개수
    @staticmethod
    async def services_like_boards_count(db: AsyncSession, b_id: int) -> int|None:
        return await Like_Board_Crud.crud_like_boards_count(db, b_id)


    # 댓글 좋아요 추가
    @staticmethod
    async def services_like_comments_create(db:AsyncSession, u_id:int, c_id:int) -> Like_Comment_Read:
        try:

            query = select(Like_Comment).where(
                Like_Comment.u_id==u_id, 
                Like_Comment.c_id==c_id)
            
            check= await db.scalar(query)

            if check:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="이미 좋아요한 댓글입니다.")

            db_data = Like_Comment_Create(u_id=u_id, c_id=c_id)

            new_db=await Like_Comment_Crud.crud_like_comments_create(db, db_data)
            
            await db.commit()
            await db.refresh(new_db)
            
            return new_db
        
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                                detail=f"댓글 좋아요 실패 :{e}")


    # 댓글 좋아요 해제
    @staticmethod
    async def services_like_comments_delete(db: AsyncSession, l_c_id: int) -> dict:
        try: 
            db_data = await (db, l_c_id)
        
            if not db_data:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                    detail='해제할 좋아요가 없습니다')

            await db.commit()
            return {'message':' 좋아요 해제'}
        
        except HTTPException:
            raise

        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                                detail=f" 좋아요 해제 실패 :{e}")
        


    # 댓글 좋아요 개수
    @staticmethod
    async def services_like_comments_count(db: AsyncSession, c_id: int) -> int|None:
        return await Like_Comment_Crud.crud_like_comments_count(db, c_id)









    
    #  좋아요 추가
    @staticmethod
    async def services_ (db:AsyncSession, u_id:int, b_id:int) -> :
        try:

            query = select().where(
                .u_id==u_id, 
                ._id==_id)
            
            check= await db.scalar(query)

            if check:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="이미 좋아요한 입니다.")

            db_data = (u_id=u_id, _id=_id)

            new_db=await (db, db_data)
            
            await db.commit()
            await db.refresh(new_db)
            
            return new_db
        
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                                detail=f" 좋아요 실패 :{e}")


    #  좋아요 해제
    @staticmethod
    async def services_like__delete(db: AsyncSession, l__id: int) -> dict:
        try: 
            db_data = await (db, l__id)
        
            if not db_data:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                    detail='해제할 좋아요가 없습니다')

            await db.commit()
            return {'message':' 좋아요 해제'}
        
        except HTTPException:
            raise

        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                                detail=f" 좋아요 해제 실패 :{e}")
    
    #  좋아요 추가
    @staticmethod
    async def services_ (db:AsyncSession, u_id:int, b_id:int) -> :
        try:

            query = select().where(
                .u_id==u_id, 
                ._id==_id)
            
            check= await db.scalar(query)

            if check:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="이미 좋아요한 입니다.")

            db_data = (u_id=u_id, _id=_id)

            new_db=await (db, db_data)
            
            await db.commit()
            await db.refresh(new_db)
            
            return new_db
        
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                                detail=f" 좋아요 실패 :{e}")


    #  좋아요 해제
    @staticmethod
    async def services_like__delete(db: AsyncSession, l__id: int) -> dict:
        try: 
            db_data = await (db, l__id)
        
            if not db_data:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                    detail='해제할 좋아요가 없습니다')

            await db.commit()
            return {'message':' 좋아요 해제'}
        
        except HTTPException:
            raise

        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                                detail=f" 좋아요 해제 실패 :{e}")
    
    