from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

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

from app.db.models.boards import Board
from app.db.models.comments import Comment
from app.db.models.gyms import Gym
from app.db.models.machines import Machine


class Like_Service:
    # 게시글 좋아요 토글
    @staticmethod
    async def services_like_boards_toggle(db: AsyncSession, u_id: int, b_id: int) -> dict:
        # 1. 게시글 존재 여부 확인
        db_data = await db.get(Board, b_id)
        if not db_data:
            raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")

        try:
            # 2. CRUD 토글 로직 호출
            result = await Like_Board_Crud.crud_like_boards_toggle(db, u_id, b_id)

            # 모든 작업이 성공하면 커밋
            await db.commit()
            return result

        except IntegrityError:
            # 중복된 좋아요 요청이 들어왔을 경우 (Race Condition)
            await db.rollback()
            raise HTTPException(
                status_code=400, 
                detail="이미 처리 중이거나 변경된 요청입니다. 잠시 후 다시 시도해주세요."
            )
        except Exception as e:
            # 기타 예상치 못한 에러 처리
            await db.rollback()
            raise e


    # 게시글 좋아요 개수
    @staticmethod
    async def services_like_boards_count(db: AsyncSession, b_id: int) -> int|None:
        return await Like_Board_Crud.crud_like_boards_count(db, b_id)


    # 댓글 좋아요 토글
    @staticmethod
    async def services_like_comments_toggle(db: AsyncSession, u_id: int, c_id: int) -> dict:
        # 1. 댓글 존재 여부 확인
        db_data = await db.get(Comment, c_id)
        if not db_data:
            raise HTTPException(status_code=404, detail="댓글을 찾을 수 없습니다.")

        try:
            # 2. CRUD 토글 로직 호출
            result = await Like_Comment_Crud.crud_like_comments_toggle(db, u_id, c_id)

            # 모든 작업이 성공하면 커밋
            await db.commit()
            return result

        except IntegrityError:
            # 중복된 좋아요 요청이 들어왔을 경우 (Race Condition)
            await db.rollback()
            raise HTTPException(
                status_code=400, 
                detail="이미 처리 중이거나 변경된 요청입니다. 잠시 후 다시 시도해주세요."
            )
        except Exception as e:
            # 기타 예상치 못한 에러 처리
            await db.rollback()
            raise e
        


    # 댓글 좋아요 개수
    @staticmethod
    async def services_like_comments_count(db: AsyncSession, c_id: int) -> int|None:
        return await Like_Comment_Crud.crud_like_comments_count(db, c_id)

    
    # 헬스장 좋아요 토글
    @staticmethod
    async def services_like_gyms_toggle(db: AsyncSession, u_id: int, g_id: int) -> dict:
        # 1. 헬스장 존재 여부 확인
        db_data = await db.get(Gym, g_id)
        if not db_data:
            raise HTTPException(status_code=404, detail="헬스장을 찾을 수 없습니다.")

        try:
            # 2. CRUD 토글 로직 호출
            result = await Like_Gym_Crud.crud_like_gyms_toggle(db, u_id, g_id)

            # 모든 작업이 성공하면 커밋
            await db.commit()
            return result

        except IntegrityError:
            # 중복된 좋아요 요청이 들어왔을 경우 (Race Condition)
            await db.rollback()
            raise HTTPException(
                status_code=400, 
                detail="이미 처리 중이거나 변경된 요청입니다. 잠시 후 다시 시도해주세요."
            )
        except Exception as e:
            # 기타 예상치 못한 에러 처리
            await db.rollback()
            raise e
        
    
    # 헬스장 좋아요 개수
    @staticmethod
    async def services_like_gyms_count(db: AsyncSession, g_id: int) -> int|None:
        return await Like_Gym_Crud.crud_like_gyms_count(db, g_id)


    # 운동기구 좋아요 토글
    @staticmethod
    async def services_like_machines_toggle(db: AsyncSession, u_id: int, m_id: int) -> dict:
        # 1. 운동기구 존재 여부 확인
        db_data = await db.get(Machine, m_id)
        if not db_data:
            raise HTTPException(status_code=404, detail="운동기구를 찾을 수 없습니다.")

        try:
            # 2. CRUD 토글 로직 호출
            result = await Like_Machine_Crud.crud_like_machines_toggle(db, u_id, m_id)

            # 모든 작업이 성공하면 커밋
            await db.commit()
            return result

        except IntegrityError:
            # 중복된 좋아요 요청이 들어왔을 경우 (Race Condition)
            await db.rollback()
            raise HTTPException(
                status_code=400, 
                detail="이미 처리 중이거나 변경된 요청입니다. 잠시 후 다시 시도해주세요."
            )
        except Exception as e:
            # 기타 예상치 못한 에러 처리
            await db.rollback()
            raise e
    
    
    # 운동기구 좋아요 개수
    @staticmethod
    async def services_like_machines_count(db: AsyncSession, m_id: int) -> int|None:
        return await Like_Machine_Crud.crud_like_machines_count(db, m_id)