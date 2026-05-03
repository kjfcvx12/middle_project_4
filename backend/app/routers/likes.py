from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import auth_get_u_id

from app.db.database import get_db


from app.db.scheme.like_boards import Like_Board_Read
from app.db.scheme.like_comments import Like_Comment_Read
from app.db.scheme.like_gyms import Like_Gym_Read
from app.db.scheme.like_machines import Like_Machine_Read

from app.services.likes import Like_Service

router=APIRouter(prefix='/likes',tags=['LIke'])


# post 게시글 좋아요 추가
@router.post("/boards_create", response_model=Like_Board_Read)
async def router_like_boards_create(b_id:int,
                                    u_id:int=Depends(auth_get_u_id), 
                                    db:AsyncSession=Depends(get_db)):
    return await Like_Service.services_like_boards_create(db, u_id, b_id)

# delete 게시글 좋아요 해제
@router.delete("/boards_del", status_code=status.HTTP_204_NO_CONTENT)
async def router_like_boards_delete(l_b_id:int, db:AsyncSession=Depends(get_db)):
    return await Like_Service.services_like_boards_delete(db, l_b_id)

# get 게시글 좋아요 개수
@router.get("/boards_count")
async def router_like_boards_count(b_id:int, db:AsyncSession=Depends(get_db)):
    return await Like_Service.services_like_boards_count(db, b_id)


# post 댓글 좋아요 추가
@router.post("/comments_create", response_model=Like_Comment_Read)
async def router_like_comments_create(c_id:int,
                                      u_id:int=Depends(auth_get_u_id), 
                                      db:AsyncSession=Depends(get_db)):
    return await Like_Service.services_like_comments_create(db, u_id, c_id)

# delete 댓글 좋아요 해제
@router.delete("/comments_del", status_code=status.HTTP_204_NO_CONTENT)
async def router_like_comments_delete(l_c_id:int, db:AsyncSession=Depends(get_db)):
    return await Like_Service.services_like_comments_delete(db, l_c_id)

# get 댓글 좋아요 개수
@router.get("/comments_count")
async def router_like_comments_count(c_id:int, db:AsyncSession=Depends(get_db)):
    return await Like_Service.services_like_comments_count(db, c_id)


# post 헬스장 좋아요 추가
@router.post("/gyms_create", response_model=Like_Gym_Read)
async def router_like_gyms_create(g_id:int,
                                  u_id:int=Depends(auth_get_u_id), 
                                  db:AsyncSession=Depends(get_db)):
    return await Like_Service.services_like_gyms_create(db, u_id, g_id)

# delete 헬스장 좋아요 해제
@router.delete("/gyms_del", status_code=status.HTTP_204_NO_CONTENT)
async def router_like_gyms_delete(l_g_id:int, db:AsyncSession=Depends(get_db)):
    return await Like_Service.services_like_gyms_delete(db, l_g_id)

# get 헬스장 좋아요 개수
@router.get("/gyms_count")
async def router_like_gyms_count(g_id:int, db:AsyncSession=Depends(get_db)):
    return await Like_Service.services_like_gyms_count(db, g_id)


# post 운동기구 좋아요 추가
@router.post("/machines_create", response_model=Like_Machine_Read)
async def router_like_machines_create(m_id:int,
                                      u_id:int=Depends(auth_get_u_id), 
                                      db:AsyncSession=Depends(get_db)):
    return await Like_Service.services_like_machines_create(db, u_id, m_id)

# delete 운동기구 좋아요 해제
@router.delete("/_del", status_code=status.HTTP_204_NO_CONTENT)
async def router_like_machines_delete(l_m_id:int, db:AsyncSession=Depends(get_db)):
    return await Like_Service.services_like_machines_delete(db, l_m_id)

# get 운동기구 좋아요 개수
@router.get("/_count")
async def router_like_machines_count(m_id:int, db:AsyncSession=Depends(get_db)):
    return await Like_Service.services_like_machines_count(db, m_id)