from fastapi import APIRouter, Depends, Response, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import set_auth_cookies, auth_get_u_id,  auth_get_admin_id

from app.db.database import get_db

from app.db.scheme.users import User_Read, User_Login, User_Create, User_Update

from app.services.users import User_Service

from app.db.scheme.logs import Log_Read
from app.db.scheme.favorite_gyms import Favorite_Gym_Read
from app.db.scheme.favorite_machines import Favorite_Machine_Read
from app.db.scheme.favorite_routines import Favorite_Routine_Read

from app.db.scheme.like_boards import Like_Board_Read
from app.db.scheme.like_comments import Like_Comment_Read
from app.db.scheme.like_gyms import Like_Gym_Read
from app.db.scheme.like_machines import Like_Machine_Read


router=APIRouter(prefix='/users',tags=['User'])


# GET 현재 사용자 확인
@router.get('/me')
async def router_user_me(u_id: int = Depends(auth_get_u_id)):
    return u_id

# Get 현재 사용자 정보
@router.get("/profile", response_model=User_Read)
async def router_user_profile(u_id: int = Depends(auth_get_u_id), db:AsyncSession=Depends(get_db)):
    return await User_Service.services_user_get_u_id(db, u_id)

# POST 회원가입
@router.post('/signup',response_model=User_Read)
async def router_user_signup(user:User_Create, db:AsyncSession=Depends(get_db)):
    return await User_Service.services_user_create(db, user)


# POST 로그인
@router.post("/login")
async def router_user_login(user:User_Login, response:Response, db:AsyncSession=Depends(get_db)):
    result=await User_Service.services_user_login(db, user)
    db_user, access_token, refresh_token=result
    set_auth_cookies(response, access_token, refresh_token, autologin=user.autologin)
    return db_user


# POST 로그아웃
@router.post("/logout")
async def router_user_logout(response:Response):
    response.delete_cookie(key="access_token", path="/")
    response.delete_cookie(key="refresh_token", path="/")
    return {"message": "로그아웃성공"}


# GET 전 유저 조회
@router.get('/all', response_model=list[User_Read])
async def router_user_get_user_all(admin:int=Depends(auth_get_admin_id), db: AsyncSession=Depends(get_db)):
    return await User_Service.services_user_get_all(db)


# GET 잊은 email 조회
@router.get('/find_email', response_model=str)
async def router_user_get_user_name_phone(u_name: str, phone: str, db: AsyncSession = Depends(get_db)):
    return await User_Service.services_user_get_email_by_name_phone(db, u_name, phone)


# GET admin 특정 id 사용자 조회
@router.get('/{u_id}', response_model=User_Read)
async def router_user_get_user_id(u_id: int, admin:int=Depends(auth_get_admin_id), db: AsyncSession = Depends(get_db)):
    return await User_Service.services_user_get_u_id(db, u_id)


# PUT	현재 id 사용자 수정
@router.put("/edit", response_model=User_Read)
async def router_user_update_u_id(user_update: User_Update,
                         u_id:int=Depends(auth_get_u_id),  
                         db: AsyncSession = Depends(get_db)):
    return await User_Service.services_user_update(db, u_id, user_update)


# DELETE 현재 id 사용자 삭제
@router.delete("/del", status_code=status.HTTP_204_NO_CONTENT)
async def router_user_delete_u_id(u_id:int=Depends(auth_get_u_id),
                         db: AsyncSession = Depends(get_db)):
    return await User_Service.services_user_delete(db,u_id)


# 유저 운동기록 조회
@router.get("/logs/{u_id}", response_model=list[Log_Read])
async def router_user_get_logs_by_u_id(page:int,
                         u_id:int=Depends(auth_get_u_id),  
                         db: AsyncSession = Depends(get_db)):
    return await User_Service.services_user_get_logs_by_u_id(db, u_id, page)


# 유저 체육관 즐겨찾기 목록 조회
@router.get("/favorite_gyms/{u_id}", response_model=list[Favorite_Gym_Read])
async def router_user_favorite_gyms_get_all(u_id:int=Depends(auth_get_u_id),
                                            db: AsyncSession = Depends(get_db)):
    return await User_Service.services_user_favorite_gyms_get_all(db, u_id)


# 유저 운동기구 즐겨찾기 목록 조회
@router.get("/favorite_machines/{u_id}", response_model=list[Favorite_Machine_Read])
async def router_user_favorite_machines_get_all(u_id:int=Depends(auth_get_u_id),
                                                db: AsyncSession = Depends(get_db)):
    return await User_Service.services_user_favorite_machines_get_all(db, u_id)


# 유저 루틴 즐겨찾기 목록 조회
@router.get("/favorite_routines/{u_id}", response_model=list[Favorite_Routine_Read])
async def router_user_favorite_routines_get_all(u_id:int=Depends(auth_get_u_id),
                                                db: AsyncSession = Depends(get_db)):
    return await User_Service.services_user_favorite_routines_get_all(db, u_id)


# 유저가 좋아요 누른 게시글
@router.get("/like_boards/{u_id}", response_model=list[Like_Board_Read])
async def router_user_like_boards_get_page(page:int, 
                                           u_id:int=Depends(auth_get_u_id),
                                           db: AsyncSession = Depends(get_db)):
    return await User_Service.services_user_like_boards_get_page(db, u_id, page)


# 유저가 좋아요 누른 댓글
@router.get("/like_comments/{u_id}", response_model=list[Like_Comment_Read])
async def router_user_like_comments_get_page(page:int, 
                                             u_id:int=Depends(auth_get_u_id),
                                             db: AsyncSession = Depends(get_db)):
    return await User_Service.services_user_like_comments_get_page(db, u_id, page)


# 유저가 좋아요 누른 운동기구
@router.get("/like_machines/{u_id}", response_model=list[Like_Machine_Read])
async def router_user_like_machines_get_page(page:int, 
                                             u_id:int=Depends(auth_get_u_id),
                                             db: AsyncSession = Depends(get_db)):
    return await User_Service.services_user_like_machines_get_page(db, u_id, page)


# 유저가 좋아요 누른 체육관
@router.get("/like_gyms/{u_id}", response_model=list[Like_Gym_Read])
async def router_user_like_gyms_get_page(page:int, 
                                         u_id:int=Depends(auth_get_u_id),
                                         db: AsyncSession = Depends(get_db)):
    return await User_Service.services_user_like_gyms_get_page(db, u_id, page)
