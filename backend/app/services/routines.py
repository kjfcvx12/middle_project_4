from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.db.crud import Routine_CRUD
from app.db.scheme.routines import Routine_Create, Routine_Update
from fastapi import HTTPException
from app.db.models import Routine
from app.services.machines import Machines_Service
from app.db.crud import Routine_Detail_CRUD
import random

class Routine_Services:
    # 루틴 생성 서비스
    async def services_routines_create(
            db:AsyncSession,
            data : Routine_Create,
            u_id : int
    ) -> Routine:
        try:
            routine_dict = data.model_dump()
            routine_dict["u_id"] = u_id

            new_routine = await Routine_CRUD.crud_routines_create(db,routine_dict)

            await db.commit()
            await db.refresh(new_routine)

            return new_routine
        except Exception:
            await db.rollback()
            raise HTTPException(400,"루틴 생성 실패")

    # 루틴 전체 읽기
    async def services_routines_read_all(
            db: AsyncSession,
            name: str | None = None,
            p_id:int | None = None,
            u_id:int | None = None
    ) -> list[Routine]:
        return await Routine_CRUD.crud_routines_read_list(db,name,p_id,u_id)

    # 루틴 아이디 기반 읽기
    async def services_routines_read_detail_by_id(
            db:AsyncSession,
            r_id:int,
            u_id: int
    ) -> Routine:
        read_routine = await Routine_CRUD.crud_routines_read_detail_by_id(db, r_id)
        
        if not read_routine:
            raise HTTPException(404, "루틴 없음")
        
        if read_routine.u_id != u_id:
            raise HTTPException(403, "권한이 없습니다")

        return read_routine


    # 루틴 업데이트
    async def services_routines_update(
            db:AsyncSession,
            r_id : int,
            data: Routine_Update,
            u_id : int
    ) -> Routine | None:
        
        new_routine = await Routine_CRUD.crud_routines_read_by_id(db,r_id)

        if not new_routine :
            return None
        
        if new_routine.u_id != u_id:
            raise HTTPException(403,"권한이 없습니다")
        try:
            new_routine = await Routine_CRUD.crud_routines_update_by_id(
                db, r_id, data.model_dump(exclude_unset=True)
            )

            await db.commit()
            await db.refresh(new_routine)

            return new_routine
        
        except Exception:
            await db.rollback()
            raise HTTPException(400, "수정 실패")

    # 루틴 삭제
    async def services_routines_delete(
            db:AsyncSession,
            r_id:int,
            u_id:int
    ) -> bool:
        
        delete_routine = await Routine_CRUD.crud_routines_read_by_id(db, r_id)

        if not delete_routine:
            return False
        
        if delete_routine.u_id != u_id:
            raise HTTPException(403,"권한이 없습니다")
        try:
            success_delete_routine = await Routine_CRUD.crud_routines_delete(db, r_id)

            if not success_delete_routine:
                return False
            
            await db.commit()

            return True
        except Exception:
            await db.rollback()
            raise HTTPException(400, "삭제 실패")


        
    # 랜덤 루틴 생성
    @staticmethod
    async def services_routines_random_create (db:AsyncSession , p_name:str, count: int,u_id :int):
        try:
            
            machines = await Machines_Service.service_machines_get_by_p_name(db, p_name)


            if not machines:
                raise HTTPException(404, "해당 부위 없음")

            if len(machines) < count:
                raise HTTPException(400, "운동 개수 부족")

            
            selected = random.sample(machines,count)

            routine_name = f"{p_name} 추천 루틴"

            routine = await Routine_CRUD.crud_routines_create(db,{
                "r_name": routine_name,
                "p_id": selected[0].p_id,
                "u_id": u_id
            })
            await db.flush()
            r_id = int(routine.r_id) 
            
            
            details = []

            for i, m in enumerate(selected):
                details.append({
                    "r_id": r_id,
                    "m_id": int(m.m_id),
                    "step": i + 1,
                    "sets": random.choice([3, 4]),
                    "reps": random.choice([8, 10, 12]),
                    "rest_time": random.choice([60, 90]),
                    "weight": random.randrange(10,30,5 )
                })

            for d in details:
                new_detail = Routine_Detail_CRUD.crud_routine_details_create_sync(db, d)
                db.add(new_detail)
            
            await db.flush()
            await db.commit()
            

            return{
                'msg':'추천 루틴 생성 완료',
                "r_id": routine.r_id
            }
        except Exception:
            await db.rollback()
            raise HTTPException(400, "추천 루틴 생성 실패")
        

            
        