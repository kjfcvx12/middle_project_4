from fastapi import Request

from app.core.jwt_handle import verify_token, create_access_token, create_refresh_token
from app.core.auth import set_auth_cookies
from app.db.crud.users import User_Crud
from app.db.database import get_db

from starlette.middleware.base import BaseHTTPMiddleware
from jwt import ExpiredSignatureError, InvalidTokenError


class RefreshTokenMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 1. 쿠키에서 토큰 추출
        access_token = request.cookies.get("access_token")
        refresh_token = request.cookies.get("refresh_token")
        
        is_token_refreshed = False
        new_access = None
        new_refresh = None

        # 2. 액세스 토큰 검증 및 재발급 로직
        try:
            if access_token:
                verify_token(access_token)  # 정상일 경우 통과
        except (ExpiredSignatureError, InvalidTokenError):
            # 액세스 토큰이 만료되었고 리프레시 토큰이 있는 경우
            if refresh_token:
                db = None
                try:
                    # 리프레시 토큰 검증 및 사용자 식별
                    u_id = verify_token(refresh_token)
                    
                    # 새로운 토큰 쌍 생성
                    new_access = create_access_token(u_id)
                    new_refresh = create_refresh_token(u_id)
                    
                    # DB 세션 생성 및 업데이트
                    db = await anext(get_db())
                    await User_Crud.update_refresh_token_by_id(db, u_id, new_refresh)
                    await db.commit()
                    
                    is_token_refreshed = True
                except Exception as e:
                    if db:
                        await db.rollback()
                    # 리프레시 토큰도 만료되었거나 DB 오류 시 조용히 넘김 (이후 인증 필터에서 처리)
                    pass
                finally:
                    if db:
                        await db.close() # 세션 누수 방지를 위해 반드시 닫기

        # 3. 본래 요청(라우터 로직) 수행
        response = await call_next(request)

        # 4. 토큰이 갱신되었다면 응답 쿠키에 주입
        if is_token_refreshed:
            set_auth_cookies(response, new_access, new_refresh)
            
        return response