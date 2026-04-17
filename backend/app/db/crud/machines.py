#함수명
# crud_machines_create_machine
# crud_machines_get_machine
# crud_machines_update_machine
# crud_machines_delete_machine



from sqlalchemy import select
from models.machines import Machine


#새 운동기구 생성
@staticmethod
async def crud_machines_create_machine(db, machine_create):
    make_machine=Machine(
        m_name=machine_create.m_name,
        dsc=machine_create.dsc,
        m_url=machine_create.m_url,
        p_id=machine_create.p_id
    )
    db.add(make_machine)
    return make_machine


# 운동기구 수정
@staticmethod
async def crud_machines_update_machine(db, machine, machine_update):
    update_machine=machine_update.dict(exclude_unset=True)
    for key, value in update_machine.items():
        setattr(machine, key, value)
    return machine

#운동기구 삭제
@staticmethod
async def crud_machines_delete_machine(db, machine):
    await db.delete(machine)


#운동기구 조회 기능
@staticmethod
async def crud_machines_get_machine(db, part=None, keyword=None):
    check_machine=select(Machine)

    #파트 검색
    if part:
        check_machine=check_machine.where(Machine.p_id==part)

    #이름 검색
    if keyword:
        check_machine=check_machine.where(Machine.m_name.like(f"%{keyword}"))

    result=await db.execute(check_machine)
    machine_list=result.scalars().all()

    return machine_list

    
