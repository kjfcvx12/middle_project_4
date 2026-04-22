from sqlalchemy.orm import selectinload
from fastapi import HTTPException
from sqlalchemy import select, func
from app.db.models.parts import Part
from app.db.crud.parts import Parts_CRUD


class Parts_service:
    

    #파트 생성
    @staticmethod
    async def service_parts_create(db, part_create, admin:int):
        try:
            if not part_create.p_name:
                raise HTTPException(400, "운동 부위 이름을 입력하시오")
            
            part_query=await Parts_CRUD.crud_parts_create(db, part_create)

            await db.commit()
            await db.refresh(part_query)

            return {
                "p_id":part_query.p_id,
                "msg":"등록완료"
            }
        except HTTPException:
            raise

        except Exception:
            await db.rollback()
            raise HTTPException(500, "부위 생성중 오류 발생")
        

    #파트 삭제
    @staticmethod
    async def service_parts_delete(db, p_id, admin:int):
        try:
            part=await Parts_CRUD.crud_parts_id(db, p_id)

            if not part:
                raise HTTPException(404, "해당 부위가 없습니다")
            
            await Parts_CRUD.crud_parts_delete(db,part)
            await db.commit()

            return {"msg":"삭제완료"}
        
        except HTTPException:
            raise

        except Exception:
            await db.rollback()
            raise HTTPException(500, "삭제 중 오류 발생")


    #파트 전체 조회
    @staticmethod
    async def service_parts_get(db):
        all_part=await Parts_CRUD.crud_parts_get(db)

        return{
            "data":[{
                "p_id":p.p_id,
                "p_name":p.p_name
            }
            for p in all_part
        ]
      }
    
    #파트 단일 조회
    @staticmethod
    async def service_parts_id(db, p_id):
        part_id=await Parts_CRUD.crud_parts_id(db, p_id)

        if not part_id:
            raise HTTPException(404, "해당 부위 없음")
        
        return{
            "data":[
            {
                "p_id":part_id.p_id,
                "p_name":part_id.p_name
            }
        ]
      }
    