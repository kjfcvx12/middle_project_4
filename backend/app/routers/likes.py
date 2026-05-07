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


# post 게시글 좋아요 토글
@router.post("/boards/toggle", response_model=dict)
async def router_like_boards_toggle(b_id: int,
                                    u_id: int = Depends(auth_get_u_id), 
                                    db: AsyncSession = Depends(get_db)):
       return await Like_Service.services_like_boards_toggle(db, u_id, b_id)


# get 게시글 좋아요 개수
@router.get("/boards_count")
async def router_like_boards_count(b_id:int, db:AsyncSession=Depends(get_db)):
    return await Like_Service.services_like_boards_count(db, b_id)


# post 댓글 좋아요 토글
@router.post("/comments/toggle", response_model=dict)
async def router_like_comments_toggle(c_id: int,
                                      u_id: int = Depends(auth_get_u_id),
                                      db: AsyncSession = Depends(get_db)):
       return await Like_Service.services_like_comments_toggle(db, u_id, c_id)


# get 댓글 좋아요 개수
@router.get("/comments_count")
async def router_like_comments_count(c_id:int, db:AsyncSession=Depends(get_db)):
    return await Like_Service.services_like_comments_count(db, c_id)


# post 헬스장 좋아요 토글
@router.post("/gyms/toggle", response_model=dict)
async def router_like_gyms_toggle(g_id: int,
                                  u_id: int = Depends(auth_get_u_id),
                                  db: AsyncSession = Depends(get_db)):
        return await Like_Service.services_like_gyms_toggle(db, u_id, g_id)


# get 헬스장 좋아요 개수
@router.get("/gyms_count")
async def router_like_gyms_count(g_id:int, db:AsyncSession=Depends(get_db)):
    return await Like_Service.services_like_gyms_count(db, g_id)


# post 운동기구 좋아요 토글
@router.post("/machines/toggle", response_model=dict)
async def router_like_machines_toggle(m_id: int,
                                      u_id: int = Depends(auth_get_u_id),
                                      db: AsyncSession = Depends(get_db)):
        return await Like_Service.services_like_machines_toggle(db, u_id, m_id)


# get 운동기구 좋아요 개수
@router.get("/machines_count")
async def router_like_machines_count(m_id:int, db:AsyncSession=Depends(get_db)):
    return await Like_Service.services_like_machines_count(db, m_id)