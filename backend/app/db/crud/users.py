from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.users import User 
from app.db.scheme.users import User_Create, User_Update



class User_Crud:
    # 유저 이메일 찾기
    @staticmethod
    async def crud_user_get_by_email(db: AsyncSession, email: str) -> User | None:
        result = await db.execute(select(User).filter(User.email == email))
        return result.scalars().first()
    

    # 유저 u_id 찾기
    @staticmethod
    async def crud_user_get_by_u_id(db:AsyncSession,u_id:int) -> User | None:
        result = await db.execute(select(User).filter(User.u_id == u_id))
        return result.scalars().first()

    
    # 유저 생성
    @staticmethod
    async def crud_user_create(db:AsyncSession, user: User_Create, hashed_pw:str) -> User:          
        user_data = user.model_dump()
        user_data["pw"] = hashed_pw
        db_user=User(**user_data)
        db.add(db_user)
        await db.flush()
        return db_user


    # 유저 업데이트
    @staticmethod
    async def crud_user_update(db:AsyncSession, u_id:int, user:User_Update)->User|None:
        db_user=await db.get(User, u_id)
        
        if db_user:           
        
            update_user= user.model_dump(exclude_unset=True)

            for key, value in update_user.items():
                setattr(db_user, key, value)

            await db.flush()
            return db_user
            
        return None
    

    # 유저 삭제
    @staticmethod
    async def crud_user_delete(db:AsyncSession , u_id:int)->User|None:
        db_user = await db.get(User, u_id)
        if db_user:
            await db.delete(db_user)
            await db.flush()
            return db_user
        return None
    

    # 유저 토큰 업데이트
    @staticmethod
    async def crud_user_update_token(db: AsyncSession, u_id: int, token: str | None)->User:
        db_user = await db.get(User, u_id)
        
        if db_user:
            db_user.refresh_token = token
            await db.flush()
        
        return db_user
 
