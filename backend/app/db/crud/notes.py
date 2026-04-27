from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.db.models.notes import Note 
from app.db.scheme.notes import Note_Create, Note_Read, Note_Send_del, Note_Rece_del



class Note_Crud:

    # 본인 보낸쪽지함 조회
    @staticmethod
    async def crud_note_get_send_me_all(db: AsyncSession, u_id: int) -> list[Note] | None:
        result=await db.execute(select(Note).filter(Note.send_id==u_id, Note.send_del == False))
        return result.scalars().all()
    

    # 본인 받은쪽지함 조회
    @staticmethod
    async def crud_note_get_rece_me_all(db: AsyncSession, u_id: int) -> list[Note] | None:
        result=await db.execute(select(Note).filter(Note.rece_id==u_id, Note.rece_del == False))
        return result.scalars().all()
    
    
    # 쪽지 상세
    @staticmethod
    async def crud_note_get_by_n_id(db: AsyncSession, n_id:int) -> Note|None:
        result=await db.execute(select(Note).filter(Note.n_id==n_id))
        return result.scalar_one_or_none()


    # 쪽지 생성
    @staticmethod
    async def crud_note_create(db:AsyncSession, note: Note_Create, u_id:int) -> Note:
        note_data = note.model_dump()

        db_note=Note(**note_data, send_id=u_id)
        db.add(db_note)
        await db.flush()
        return db_note


    # 본인 보낸쪽지함 삭제 변경
    @staticmethod
    async def crud_note_send_update(db:AsyncSession, n_id:int, u_id:int, note:Note_Send_del) -> str:
        result=await db.execute(select(Note).
                                 filter(Note.n_id==n_id, Note.send_id==u_id))
        
        db_note=result.scalar_one_or_none()
        
        if db_note:
            db_note.send_del=note.send_del
            
            await db.flush()
            return "쪽지를 삭제했습니다."
            
        return "삭제할 쪽지가 없습니다."
    

    # 본인 받은쪽지함 삭제 변경
    @staticmethod
    async def crud_note_rece_update(db:AsyncSession, n_id:int, u_id:int, note:Note_Rece_del) -> str:
        result=await db.execute(select(Note).
                                 filter(Note.n_id==n_id, Note.rece_id==u_id))
        
        db_note=result.scalar_one_or_none()
        
        if db_note:
            db_note.rece_del=note.rece_del
            
            await db.flush()
            return "쪽지를 삭제했습니다."
            
        return "삭제할 쪽지가 없습니다."


    # 관리자 전체 유령 쪽지 삭제
    @staticmethod
    async def crud_ghost_note_delete(db:AsyncSession) -> str:
        result = await db.execute(
            delete(Note).filter(Note.send_del == True, Note.rece_del == True)
        )
        
        deleted_count = result.rowcount
        
        if deleted_count > 0:
            await db.flush()
            return f"유령 쪽지 {deleted_count}개 삭제했습니다."
        
        return "삭제할 유령 쪽지가 없습니다."
    