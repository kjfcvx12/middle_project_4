#함수명
# service_machines_create
# service_machines_get
# service_machines_update
# service_machines_delete
# service_machines_detail

from sqlalchemy.orm import selectinload
from fastapi import HTTPException
from sqlalchemy import select, func
from app.db.models.machines import Machine
from app.db.crud.machines import Machines_CRUD



class Machines_Service:

    #운동기구 생성
    @staticmethod
    async def service_machines_create(db, machine_create,admin:int):
        try:
            if not machine_create.m_name:
                raise HTTPException(400, "이름을 입력하시오")
            
            if not machine_create.dsc:
                raise HTTPException(400, "설명을 입력하시오")


            new_machine=await Machines_CRUD.crud_machines_create(db, machine_create)

            await db.commit()
            await db.refresh(new_machine)

            return {
                "m_id":new_machine.m_id,
                "msg":"성공적으로 등록되었습니다"
            }
        
        except HTTPException:
            raise
        
        except Exception:
            await db.rollback()
            raise HTTPException(500,"등록중 오류 발생")


    #운동기구 수정
    @staticmethod
    async def service_machines_update(db, m_id,machine_update,admin:int):
        try:
            query=select(Machine).where(Machine.m_id==m_id)
            result=await db.execute(query)
            machine=result.scalar_one_or_none()

            if not machine:
                raise HTTPException(400, "운동기구가 없습니다")
            
            await Machines_CRUD.crud_machines_update(db, machine, machine_update)

            await db.commit()
            await db.refresh(machine)
            return{"msg":"성공적으로 수정되었습니다"}
    

        except HTTPException:
            raise
        
        except Exception:
            await db.rollback()
            raise HTTPException(500,"수정중 오류 발생")


    #운동기구 삭제
    @staticmethod
    async def service_machines_delete(db, m_id, admin:int):
        try:
            query=select(Machine).where(Machine.m_id==m_id)
            result=await db.execute(query)
            machine=result.scalar_one_or_none()


            
            if not machine:
                raise HTTPException(404, "운동기구가 없습니다")
            
            await Machines_CRUD.crud_machines_delete(db, machine)
            await db.commit()
            return {"msg":"성공적으로 삭제되었습니다"}
        
        except HTTPException:
            raise

        except Exception:
            await db.rollback()
            raise HTTPException(500,"삭제 중 오류 발생")





    #운동기구 목록 조회
    @staticmethod
    async def service_machines_get(
        db,
        page:int=1,
        name:str | None = None,
        p_id:int | None = None
    ):
        
        if page<1:
            raise HTTPException(400, "page는 1 이상")
        
        
        #CRUD 호출(쿼리 및 페이징)
        total,machine_list=await Machines_CRUD.crud_machines_get(db, part=p_id, keyword=name, page=page)

        #응답
        data=[
            {
                "m_id":m.m_id,
                "m_name":m.m_name,
                "p_id":m.p_id
            }
            for m in machine_list
        ]

        return{
            "total":total,
            "page":page,
            "data":data
        }


    #운동기구 상세 조회(유지)
    @staticmethod
    async def service_machines_detail(db, m_id):
        query=select(Machine).options(selectinload(Machine.part)).where(Machine.m_id==m_id)

        result=await db.execute(query)
        machine=result.scalar_one_or_none()

        if not machine:
            raise HTTPException(404, "해당 운동기구가 없습니다")
        return{
            "m_id":machine.m_id,
            "m_name":machine.m_name,
            "dsc":machine.dsc,
            "m_url":machine.m_url,
            "p_name":machine.part.p_name
        }
    


