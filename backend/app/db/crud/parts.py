#함수명
#crud_parts_create
#crud_parts_get
#crud_parts_delete

from sqlalchemy import select
from models.parts import Part
from sqlalchemy.orm import selectinload
from models.machines import Machine

#파트 생성
@staticmethod
async def crud_parts_create(db, part_create):
    created_part=Part(
        p_name=part_create.p_name
    )

    db.add(created_part)
    return created_part


#파트 삭제
@staticmethod
async def crud_parts_delete(db, part):
    await db.delete(part)
    return part


#파트 전체 조회
@staticmethod
async def crud_parts_get(db):
    check_part=select(Part)
    result=await db.execute(check_part)
    part_list=result.scalars().all()
    return part_list