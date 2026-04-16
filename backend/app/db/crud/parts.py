#함수명
#crud_parts_create_part
#crud_parts_get_part
#crud_parts_delete_part

from sqlalchemy import select
from models.parts import Part
from sqlalchemy.orm import selectinload
from models.machines import Machine

#파트 생성
async def crud_parts_create_part(db, part_create):
    created_part=Part(
        p_name=part_create.p_name
    )

    db.add(created_part)
    return created_part


#파트 삭제
async def crud_parts_delete_part(db, part):
    await db.delete(part)
    return part


#파트 전체 조회
async def crud_parts_get_part(db):
    check_part=select(Part)
    result=await db.execute(check_part)
    part_list=result.scalars().all()
    return part_list