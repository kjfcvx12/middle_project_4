from sqlalchemy import select
from app.db.models.machines import Machine
from app.db.models.parts import Part

class Parts_CRUD:

    #파트 생성
    @staticmethod
    async def crud_parts_create(db, part_create):
        created_part=Part(p_name=part_create.p_name)
        db.add(created_part)
        await db.flush()
        return created_part


    #파트 삭제
    @staticmethod
    async def crud_parts_delete(db, part):
        await db.delete(part)
        await db.flush()
        return part


    #파트 전체 조회
    @staticmethod
    async def crud_parts_get(db):
        check_part=select(Part)
        result=await db.execute(check_part)
        return result.scalars().all()
        
    
    #파트 단일 조회(아이디 조회)
    @staticmethod
    async def crud_parts_id(db, p_id):
        part_query=select(Part).where(Part.p_id==p_id)
        result=await db.execute(part_query)
        return result.scalar_one_or_none()