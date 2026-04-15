from fastapi import APIRouter, Depends, Response, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import set_auth_cookies, auth_get_u_id

from app.db.database import get_db

from app.db.scheme.users import User_Read, User_Login, User_Create, User_Update

from app.services.users import User_Service



router=APIRouter(prefix='/users',tags=['User'])


# GET 현재 사용자 확인
@router.get('/me')
async def router_me(u_id: int = Depends(auth_get_u_id)):
    return u_id


# POST 회원가입
@router.post('/signup',response_model=User_Read)
async def router_signup(user:User_Create, db:AsyncSession=Depends(get_db)):
    return await User_Service.services_user_create(db, user)


# POST 로그인
@router.post("/login")
async def router_login(user:User_Login, response:Response, db:AsyncSession=Depends(get_db)):
    result=await User_Service.services_user_login(db, user)
    db_user, access_token, refresh_token=result
    set_auth_cookies(response, access_token, refresh_token)
    return {"message": "로그인 성공"}


# POST 로그아웃
@router.post("/logout")
async def router_logout(response:Response):
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return {"message": "로그아웃성공"}


# GET email 조회
@router.get('/email', response_model=User_Read)
async def router_get_user_email(email: str, db: AsyncSession = Depends(get_db)):
    return await User_Service.services_user_get_email(db, email)


# GET 특정 id 사용자 조회
@router.get('/id/{u_id}', response_model=User_Read)
async def router_get_user_id(u_id: int, db: AsyncSession = Depends(get_db)):
    return await User_Service.services_user_get_u_id(db, u_id)


# PUT	현재 id 사용자 수정
@router.put("/edit", response_model=User_Read)
async def router_update_u_id(user_update: User_Update,
                         u_id:int=Depends(auth_get_u_id),  
                         db: AsyncSession = Depends(get_db)):
    return await User_Service.services_user_update(db, u_id, user_update)


# DELETE 현재 id 사용자 삭제
@router.delete("/del", status_code=status.HTTP_204_NO_CONTENT)
async def router_delete_u_id(u_id:int=Depends(auth_get_u_id),
                         db: AsyncSession = Depends(get_db)):
    await User_Service.services_user_delete(db,u_id)