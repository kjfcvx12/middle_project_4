#함수명
# crud_machines_create
# crud_machines_get
# crud_machines_update
# crud_machines_delete



from sqlalchemy import select, func
from models.machines import Machine

class Machines_CRUD:

    #새 운동기구 생성
    @staticmethod
    async def crud_machines_create(db, machine_create):
        machine_query=Machine(
            m_name=machine_create.m_name,
            dsc=machine_create.dsc,
            m_url=machine_create.m_url,
            p_id=machine_create.p_id
        )
        db.add(machine_query)
        await db.flush()

        return machine_query


    # 운동기구 수정
    @staticmethod
    async def crud_machines_update(db, machine, machine_update):
        machine_query=machine_update.dict(exclude_unset=True)
        for key, value in machine_query.items():
            setattr(machine, key, value)
        
        await db.flush()
        return machine

    #운동기구 삭제
    @staticmethod
    async def crud_machines_delete(db, machine):
        await db.delete(machine)

        await db.flush()
        return machine

    
    #운동기구 조회 기능
    @staticmethod
    async def crud_machines_get(db,part=None,keyword=None,page:int=1,size=10):
        machine_query=select(Machine)

        #파트 검색
        if part is not None:
            machine_query=machine_query.where(Machine.p_id==part)

        #기구 검색
        if keyword:
            machine_query=machine_query.where(Machine.m_name.ilike(f"%{keyword}%"))

        #정렬(order_by)
        machine_query=machine_query.order_by(Machine.m_id.desc())

        #전체 개수 먼저 구하기
        total_machine=select(func.count()).select_from(machine_query.subquery())
        total=(await db.execute(total_machine)).scalar()

        #페이지네이션을 적용
        machine_query=machine_query.offset((page-1)*size).limit(size)

        result=await db.execute(machine_query)
        machine_list=result.scalars().all()


        #total + 데이터와 같이 반환
        return total, machine_list

        
