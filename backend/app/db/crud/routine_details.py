from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models import Routine_Detail
from ..scheme import Routine_Detail_Create, Routine_Detail_Read,Routine_Detail_Update

class Routine_Detail_CRUD :

    @staticmethod
    async def crud_routines_details_create(db:AsyncSession,
                                           routine_details_data:Routine_Detail_Create,
                                           r_id:int) -> Routine_Detail :
        routine_detail_dict = routine_details_data.model_dump()
        routine_detail_dict["r_id"]=r_id
        new_routine_detail=Routine_Detail(**routine_detail_dict)

        db.add(new_routine_detail)

        await db.flush()
        await db.refresh(new_routine_detail)

        return new_routine_detail
    

    @staticmethod
    async def crud_routines_details_