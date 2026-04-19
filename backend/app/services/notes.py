from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.db.crud.notes import Note_Crud
from app.db.scheme.notes import Note_Create, Note_Read, Note_Rece_del, Note_Send_del

class Note_Service:

    # 본인 보낸쪽지함 조회
    @staticmethod
    async def services_note_get_send_me_all(db:AsyncSession, u_id:int):
        note=await Note_Crud.crud_note_get_send_me_all(db, u_id)

        if not note:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='보내신 쪽지가 없습니다.')
        
        return note
    

    # 본인 받은쪽지함 조회
    @staticmethod
    async def services_note_get_rece_me_all(db:AsyncSession, u_id:int):
        note=await Note_Crud.crud_note_get_rece_me_all(db, u_id)

        if not note:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='받으신 쪽지가 없습니다.')
        
        return note
    
    # 쪽지 상세
    @staticmethod
    async def services_note_get_by_n_id(db:AsyncSession, n_id:int):
        note=await Note_Crud.crud_note_get_by_n_id(db, n_id)

        if not note:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='해당 쪽지가 없습니다.')
        
        return note

 

    # 쪽지 생성
    @staticmethod
    async def services_note_create(db:AsyncSession, note:Note_Create) -> str:

        try:
            new_note = await Note_Crud.crud_note_create(db, note)
            
            await db.commit()
            await db.refresh(new_note)

            if note.rece_id=='admin':
                msg="문의가 관리자에게 접수되었습니다."
            else:
                msg=f"쪽지가 {note.rece_id}님에게 전송되었습니다."

            return msg 
        
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail=f"쪽지 전송 실패 :{e}")
       
    
    # 송신자 삭제 변경
    @staticmethod
    async def services_note_del_send(db:AsyncSession, n_id:int, u_id:int, note_del_send:Note_Send_del) -> str:
        try:
            note_del=note_del_send.model_dump(exclude_unset=True)

            note=await Note_Crud.crud_note_send_update(db, n_id, u_id, note_del)
            
            if not note:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                    detail="삭제할 보내신 쪽지가 없습니다")
            
            
            await db.commit()
            await db.refresh(note)

            return "보낸 편지함의 쪽지를 삭제하였습니다."
        
        except HTTPException:
            raise

        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                                detail=f"보낸 쪽지 삭제 실패 :{e}")
    


    # 송신자 삭제 변경
    @staticmethod
    async def services_note_del_rece(db:AsyncSession, n_id:int, u_id:int, note_del_rece:Note_Rece_del) -> str:
        try:
            note_del=note_del_rece.model_dump(exclude_unset=True)

            note=await Note_Crud.crud_note_rece_update(db, n_id, u_id, note_del)

            if not note:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                    detail="삭제할 받으신 쪽지가 없습니다")
            
            
            await db.commit()
            await db.refresh(note)

            return "받은 편지함의 쪽지를 삭제하였습니다."

        except HTTPException:
            raise

        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                                detail=f"받은 쪽지 삭제 실패 :{e}")
        

    # 관리자 전체 유령 쪽지 삭제
    @staticmethod
    async def services_ghost_note_delete(db: AsyncSession) -> str:
        try: 
            delete_note = await Note_Crud.crud_ghost_note_delete(db)
        
            if not delete_note:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                    detail='유령쪽지가 존재하지 않습니다.')

            await db.commit()
            return "유령쪽지 전체 삭제"
        
        except HTTPException:
            raise

        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                                detail=f"유령쪽지 삭제 실패 :{e}")
    