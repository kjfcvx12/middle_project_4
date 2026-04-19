from fastapi import APIRouter, Depends, Response, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import set_auth_cookies, auth_get_u_id,  auth_get_admin_id

from app.db.database import get_db

from app.db.scheme.notes import Note_Create, Note_Read, Note_Rece_del, Note_Send_del

from app.services.notes import Note_Service



router=APIRouter(prefix='/notes',tags=['Note'])


# 본인 보낸쪽지함 조회
@router.get('/inbox', response_model=list[Note_Read])
async def router_note_get_send_me_all(u_id: int = Depends(auth_get_u_id),
                                      db:AsyncSession=Depends(get_db)):
    return await Note_Service.services_note_get_send_me_all(db, u_id)
    

# 본인 받은쪽지함 조회
@router.get('/outbox', response_model=list[Note_Read])
async def router_note_get_rece_me_all(u_id: int = Depends(auth_get_u_id),
                                      db:AsyncSession=Depends(get_db)):
    return await Note_Service.services_note_get_rece_me_all(db, u_id)


# 쪽지 상세
@router.get('/{n_id}}', response_model=Note_Read)
async def router_note_get_by_n_id(n_id: int, u_id:int=Depends(auth_get_u_id), 
                                  db:AsyncSession=Depends(get_db)):
    return await Note_Service.services_note_get_by_n_id(db, n_id)


# 쪽지 생성
@router.post('/create')
async def router_note_create(note:Note_Create, u_id:int=Depends(auth_get_u_id), 
                             db:AsyncSession=Depends(get_db)):
    return await Note_Service.services_note_create(db, note)


# 송신자 삭제 변경
@router.put("/inbox/{n_id}")
async def router_note_send_del(note:Note_Send_del, n_id:int, 
                               u_id:int=Depends(auth_get_u_id), 
                               db:AsyncSession=Depends(get_db)):
    return await Note_Service.services_note_del_send(db, n_id, u_id, note)


# 수신자 삭제 변경
@router.put("/outbox/{n_id}")
async def router_note_rece_del(note:Note_Send_del, n_id:int, 
                               u_id:int=Depends(auth_get_u_id), 
                               db:AsyncSession=Depends(get_db)):
    return await Note_Service.services_note_del_rece(db, n_id, u_id, note)


# 관리자 전체 유령 쪽지 삭제
@router.delete("/del", status_code=status.HTTP_204_NO_CONTENT)
async def router_ghost_note_delete(admin:int=Depends(auth_get_admin_id),
                                   db: AsyncSession = Depends(get_db)):
    await Note_Service.services_ghost_note_delete(db)