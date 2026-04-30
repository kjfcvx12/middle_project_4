from fastapi import Request, Response, HTTPException, Depends, status
from fastapi import Request, Response, HTTPException, Depends, status
from jwt import ExpiredSignatureError, InvalidTokenError
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.database import get_db
from app.db.models.users import User

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.database import get_db
from app.db.models.users import User

from app.core.settings import settings
from app.core.jwt_handle import verify_token, create_access_token


#JWT토큰을 쿠키로 설정하려고
#httponly=True : 쿠키를 만들면 js에서 접근 불가(xss공격방어)
#samesite="Lax" 외부 도메인 요청 시 쿠키 전송 제한됨
def set_auth_cookies(response:Response, access_token:str, refresh_token:str, autologin:bool=False)->None:
    access_max_age = int(settings.access_token_expire.total_seconds()) if autologin else None

    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=access_max_age,
        secure=False,
        httponly=True,
        samesite="Lax"
    )

    refresh_max_age = int(settings.refresh_token_expire.total_seconds()) if autologin else None

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=refresh_max_age,
        secure=False,
        httponly=True,
        samesite="Lax"
    )


#사용자 쿠키에 액세스 토큰있는지 확인
#쿠키에서 가져온 액세스 토큰 검증/유효한지 안한지 -> 인증 로직

async def auth_get_u_id(request:Request, response: Response)-> int:
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")

    if access_token:
        try:
            u_id = verify_token(access_token)
            if u_id: return u_id
        except ExpiredSignatureError:
            pass # 액세스 만료 시 리프레시 토큰 확인으로 넘어감
        except InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid Token")

    # 액세스 토큰이 없거나 만료됨 -> 리프레시 토큰 확인
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Session expired")
    

    try:
        u_id = verify_token(refresh_token)
        
        new_access = create_access_token(u_id=u_id, data={"sub": str(u_id)})
        response.set_cookie(
            key="access_token",
            value=new_access,
            max_age=int(settings.access_token_expire.total_seconds()),
            secure=False,
            httponly=True,
            samesite="Lax"
        )
        return u_id
        
    except (ExpiredSignatureError, InvalidTokenError):
        raise HTTPException(status_code=401, detail="Refresh token expired")


# 관리자 확인
async def auth_get_admin_id(u_id: int = Depends(auth_get_u_id), db: AsyncSession = Depends(get_db)) -> int:
  
    result = await db.execute(select(User.role).filter(User.u_id == u_id))
    role = result.scalar_one_or_none()
    
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="사용자가 없습니다.")
    
    if role!='admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="관리자 권한이 필요합니다.")
    
    return u_id


async def auth_get_staff_role(u_id: int = Depends(auth_get_u_id), db: AsyncSession = Depends(get_db)) -> int:
  
    result = await db.execute(select(User.role).filter(User.u_id == u_id))
    role = result.scalar_one_or_none()
    
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="사용자가 없습니다.")

    if not role in ['trainer', 'manager', 'admin']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="직원만 접근이 가능합니다.")
    
    return role





#토크이 없거나 유효하지 않아도 오류 안던지고 그냥 None 반환함
async def get_optional(request:Request)-> Optional[int]:
    access_token=request.cookies.get("access_token")
    if not access_token:
        return None
    
    try:
        return verify_token(access_token)
    
    except (ExpiredSignatureError, InvalidTokenError):
        return None