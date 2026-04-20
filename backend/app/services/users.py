from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.db.crud.users import User_Crud

from app.db.scheme.users import User_Create, User_Update, User_Login

from app.db.scheme.favorite_gyms import Favorite_Gym_Read

from app.core.jwt_handle import get_password_hash, verify_password, create_access_token, create_refresh_token

class User_Service:

    # 전 유저 조회
    @staticmethod
    async def services_user_get_all(db:AsyncSession):
        user=await User_Crud.crud_user_get_all(db)

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='유저가 없습니다.')
        
        return user

    # 유저 u_id 조회
    @staticmethod
    async def services_user_get_u_id(db: AsyncSession, u_id: int):
        user = await User_Crud.crud_user_get_by_u_id(db, u_id)

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='해당 id의 사용자가 없습니다')
        
        return user
    

    # 유저 email 조회
    @staticmethod
    async def services_user_get_email(db: AsyncSession, email:str):
        user = await User_Crud.crud_user_get_by_email(db, email)

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='해당 email의 사용자가 없습니다')
        
        return user.email
    

    @staticmethod
    async def services_user_get_email_by_name_phone(db: AsyncSession, u_name:str, phone:str):
        try:
            user = await User_Crud.crud_user_get_by_email(db, u_name, phone)

            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail='해당 email의 사용자가 없습니다')
            

            u_id, domain = user.email.split("@")
            
            if len(u_id) <= 3:
                masked_id = u_id[0] + "*" * (len(u_id) - 1)
            else:
                masked_id = u_id[:3] + "*" * (len(u_id) - 3)
                
            return f"{masked_id}@{domain}"
        
        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                                detail=f"서버 오류가 발생했습니다: {e}")
    

    # 유저 로그인
    @staticmethod
    async def services_user_login(db: AsyncSession, login_data: User_Login):
        try:
            user=await User_Crud.crud_user_get_by_email(db, login_data.email)
            
            if not user or not verify_password(login_data.pw, user.pw):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="이메일 또는 비밀번호가 일치하지 않습니다.")
            
            token_data = {"email": user.email}
            access_token = create_access_token(u_id=user.u_id,**token_data)
            refresh_token = create_refresh_token(u_id=user.u_id)
            
            update_user=await User_Crud.crud_user_update_token(db, user.u_id, refresh_token)
            
            await db.commit()
            await db.refresh(update_user)
            return update_user, access_token, refresh_token
        
        except HTTPException:
            raise

        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"로그인 실패 :{e}")
    
    

    # 유저 생성
    @staticmethod
    async def services_user_create(db:AsyncSession, user:User_Create):
        try:
            already_user=await User_Crud.crud_user_get_by_email(db, user.email)

            if already_user:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='이미 등록된 이메일 입니다.')
            
            hashed_pw = get_password_hash(user.pw)
            new_user = await User_Crud.crud_user_create(db, user, hashed_pw)
            
            await db.commit()
            await db.refresh(new_user)
            return new_user
        
        except HTTPException:
            raise

        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"사용자 등록 실패 :{e}")
       
    
    # 유저 업데이트
    @staticmethod
    async def services_user_update(db:AsyncSession, u_id:int, user_update:User_Update):
        try :
            update_data=user_update.model_dump(exclude_unset=True)
            
            if update_data.get("pw"): 
                update_data['pw']=get_password_hash(update_data["pw"])
            
            updated_model = User_Update(**update_data) 

            update_user=await User_Crud.crud_user_update(db, u_id, updated_model)
            
            if not update_user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                    detail="수정할 사용자가 없습니다")
            
            
            await db.commit()
            await db.refresh(update_user)

            return update_user
        
        except HTTPException:
            raise

        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                                detail=f"사용자 정보 수정 실패 :{e}")


    @staticmethod
    async def services_user_delete(db: AsyncSession, u_id: int) -> dict:
        try: 
            delete_user = await User_Crud.crud_user_delete(db, u_id)
        
            if not delete_user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                    detail='삭제할 유저가 없습니다')

            await db.commit()
            return {'message':'유저 삭제'}
        
        except HTTPException:
            raise

        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                                detail=f"사용자 삭제 실패 :{e}")
    









    # 유저 운동기록 조회
    @staticmethod
    async def services_user_get_logs(db: AsyncSession, u_id: int, page: int):
        try:
            # 1. CRUD 호출하여 데이터와 전체 개수 가져오기
            # offset 계산: (페이지 번호 - 1) * 페이지당 개수
            #offset = (page - 1) * size
            logs, offset, total = await Log_Crud.crud_log_get_by_u_id(db, u_id, page)

            # 2. 유저 혹은 기록 존재 여부 체크
            if not logs and page == 1:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="운동 기록을 찾을 수 없습니다."
                )

            # 3. 데이터 포맷팅 (성공 응답 구조 생성)
            return {
                "total": total,
                "page": page,
                "size": size,
                "data": [
                    {
                        "log_id": log.id,
                        "r_id": log.routine_id,
                        "r_name": log.routine_name,
                        "log_date": log.created_at
                    }
                    for log in logs
                ]
            }

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"운동 기록 조회 중 서버 오류 발생: {str(e)}"
            )


    # 유저 체육관 즐겨찾기 목록 조회
    # 유저 운동기구 즐겨찾기 목록 조회
    # 유저 루틴 즐겨찾기 목록 조회
    

    # 유저가 좋아요 누른 체육관


    # 유저가 좋아요 누른 운동기구

    # 유저가 좋아요 누른 루틴


    # 유저가 좋아요 누른 게시물

