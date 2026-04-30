from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from sqlalchemy import select

from app.db.models.favorite_gyms import Favorite_Gym
from app.db.models.favorite_machines import Favorite_Machine
from app.db.models.favorite_routines import Favorite_Routine

from app.db.scheme.favorite_gyms import Favorite_Gym_Read, Favorite_Gym_Create
from app.db.scheme.favorite_machines import Favorite_Machine_Read, Favorite_Machine_Create
from app.db.scheme.favorite_routines import Favorite_Routine_Read, Favorite_Routine_Create

from app.db.crud.favorite_gyms import Favorite_Gym_Crud
from app.db.crud.favorite_machines import Favorite_Machine_Crud
from app.db.crud.favorite_routines import Favorite_Routine_Crud


from app.db.models.like_boards import Like_Board
from app.db.models.like_comments import Like_Comment
from app.db.models.like_gyms import Like_Gym
from app.db.models.like_machines import Like_Machine

from app.db.scheme.like_boards import Like_Board_Read, Like_Board_Create
from app.db.scheme.like_comments import Like_Comment_Read, Like_Comment_Base
from app.db.scheme.like_gyms import Like_Gym_Read, Like_Gym_Create
from app.db.scheme.like_machines import Like_Machine_Read, Like_Machine_Create

from app.db.crud.like_boards import Like_Board_Crud
from app.db.crud.like_comments import Like_Comment_Crud
from app.db.crud.like_gyms import Like_Gym_Crud
from app.db.crud.like_machines import Like_Machine_Crud



class Fav_Like_Service:

    # 체육관 즐겨찾기 추가
    @staticmethod
    async def services_favorite_gym_create(db:AsyncSession, u_id:int, g_id:int) -> Favorite_Gym_Read:
        try:

            query = select(Favorite_Gym).where(
                Favorite_Gym.u_id==u_id, 
                Favorite_Gym.g_id==g_id)
            
            check= await db.scalar(query)

            if check:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="이미 즐겨찾기에 등록된 체육관입니다.")

            db_data = Favorite_Gym_Create(u_id=u_id, g_id=g_id)

            new_db=await Favorite_Gym_Crud.crud_favorite_gyms_create(db, db_data)
            
            await db.commit()
            await db.refresh(new_db)
            
            return new_db
        
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                                detail=f"체육관 즐겨찾기 실패 :{e}")


    # 체육관 즐겨찾기 해제
    @staticmethod
    async def services_favorite_gym_delete(db: AsyncSession, f_g_id: int) -> dict:
        try: 
            db_data = await Favorite_Gym_Crud.crud_favorite_gyms_delete(db, f_g_id)
        
            if not db_data:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                    detail='해제할 즐겨찾기가 없습니다')

            await db.commit()
            return {'message':'체육관 즐겨찾기 해제'}
        
        except HTTPException:
            raise

        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                                detail=f"체육관 즐겨찾기 해제 실패 :{e}")
    

    # 운동기구 즐겨찾기 추가
    @staticmethod
    async def services_favorite_machines_create(db:AsyncSession, u_id:int, m_id:int) -> Favorite_Machine_Read:
        try:

            query = select(Favorite_Machine).where(
                Favorite_Machine.u_id==u_id, 
                Favorite_Machine.m_id==m_id)
            
            check= await db.scalar(query)

            if check:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="이미 즐겨찾기에 등록된 운동기구입니다.")

            db_data = Favorite_Machine_Create(u_id=u_id, m_id=m_id)

            new_db=await Favorite_Machine_Crud.crud_favorite_machines_create(db, db_data)
            
            await db.commit()
            await db.refresh(new_db)
            
            return new_db
        
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                                detail=f"운동기구 즐겨찾기 실패 :{e}")


    # 운동기구 즐겨찾기 해제
    @staticmethod
    async def services_favorite_machines_delete(db: AsyncSession, f_m_id: int) -> dict:
        try: 
            db_data = await Favorite_Machine_Crud.crud_favorite_machines_delete(db, f_m_id)
        
            if not db_data:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                    detail='해제할 즐겨찾기가 없습니다')

            await db.commit()
            return {'message':'운동기구 즐겨찾기 해제'}
        
        except HTTPException:
            raise

        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                                detail=f"운동기구 즐겨찾기 해제 실패 :{e}")
        

    # 루틴 즐겨찾기 추가
    @staticmethod
    async def services_favorite_machines_create(db:AsyncSession, u_id:int, m_id:int) -> Favorite_Machine_Read:
        try:

            query = select(Favorite_Machine).where(
                Favorite_Machine.u_id==u_id, 
                Favorite_Machine.m_id==m_id)
            
            check= await db.scalar(query)

            if check:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="이미 즐겨찾기에 등록된 운동기구입니다.")

            db_data = Favorite_Machine_Create(u_id=u_id, m_id=m_id)

            new_db=await Favorite_Machine_Crud.crud_favorite_machines_create(db, db_data)
            
            await db.commit()
            await db.refresh(new_db)
            
            return new_db
        
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                                detail=f"운동기구 즐겨찾기 실패 :{e}")


    # 운동기구 즐겨찾기 해제
    @staticmethod
    async def services_favorite_machines_delete(db: AsyncSession, f_m_id: int) -> dict:
        try: 
            db_data = await Favorite_Machine_Crud.crud_favorite_machines_delete(db, f_m_id)
        
            if not db_data:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                    detail='해제할 즐겨찾기가 없습니다')

            await db.commit()
            return {'message':'운동기구 즐겨찾기 해제'}
        
        except HTTPException:
            raise

        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                                detail=f"운동기구 즐겨찾기 해제 실패 :{e}")