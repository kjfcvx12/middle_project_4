from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.db.models.favorite_gyms import Favorite_Gym
from app.db.models.favorite_machines import Favorite_Machine
from app.db.models.favorite_routines import Favorite_Routine

from app.db.scheme.favorite_gyms import Favorite_Gym_Read, Favorite_Gym_Create
from app.db.scheme.favorite_machines import Favorite_Machine_Read, Favorite_Machine_Create
from app.db.scheme.favorite_routines import Favorite_Routine_Read, Favorite_Routine_Create

from app.db.crud.favorite_gyms import Favorite_Gym_Crud
from app.db.crud.favorite_machines import Favorite_Machine_Crud
from app.db.crud.favorite_routines import Favorite_Routine_Crud


from app.db.models.gyms import Gym
from app.db.models.machines import Machine
from app.db.models.routines import Routine


class Favorite_Service:

    # 헬스장 즐겨찾기 토글
    @staticmethod
    async def services_favorite_gym_toggle(db: AsyncSession, u_id: int, g_id: int) -> dict:
        # 1. 헬스장 존재 여부 확인
        db_data = await db.get(Gym, g_id)
        if not db_data:
            raise HTTPException(status_code=404, detail="헬스장를 찾을 수 없습니다.")

        try:
            # 2. CRUD 토글 로직 호출
            result = await Favorite_Gym_Crud.crud_favorite_gyms_toggle(db, u_id, g_id)

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
    

    # 운동기구 즐겨찾기 토글
    @staticmethod
    async def services_favorite_machines_toggle(db: AsyncSession, u_id: int, m_id: int) -> dict:
        # 1. 운동기구 존재 여부 확인
        db_data = await db.get(Machine, m_id)
        if not db_data:
            raise HTTPException(status_code=404, detail="운동기구를 찾을 수 없습니다.")

        try:
            # 2. CRUD 토글 로직 호출
            result = await Favorite_Machine_Crud.crud_favorite_machines_toggle(db, u_id, m_id)

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
        

    # 루틴 즐겨찾기 토글
    @staticmethod
    async def services_favorite_routines_toggle(db: AsyncSession, u_id: int, r_id: int) -> dict:
        # 1. 루틴 존재 여부 확인
        db_data = await db.get(Routine, r_id)
        if not db_data:
            raise HTTPException(status_code=404, detail="루틴을 찾을 수 없습니다.")

        try:
            # 2. CRUD 토글 로직 호출
            result = await Favorite_Routine_Crud.crud_favorite_routines_toggle(db, u_id, r_id)

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
        

    