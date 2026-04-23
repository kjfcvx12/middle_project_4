<<<<<<< HEAD
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.users import User 
from app.db.scheme.users import User_Create, User_Update



class User_Crud:

    # 모든 유저 조회
    @staticmethod
    async def crud_user_get_all(db: AsyncSession) -> list[User] | None:
        result=await db.execute(select(User))
        return result.scalars().all()
    

    # 유저 이메일 찾기
    @staticmethod
    async def crud_user_get_by_email(db: AsyncSession, email: str) -> User | None:
        result = await db.execute(select(User).filter(User.email == email))
        return result.scalars().first()

    # 유저 이름&전화로 이메일 찾기
    @staticmethod
    async def crud_user_get_by_name_phone(db: AsyncSession, u_name: str, phone: str) -> User | None:
        result = await db.execute(select(User).filter(User.u_name == u_name, User.phone==phone))
        return result.scalars().first()
    

    # 유저 u_id 찾기
    @staticmethod
    async def crud_user_get_by_u_id(db:AsyncSession,u_id:int) -> User | None:
        result = await db.execute(select(User).filter(User.u_id == u_id))
        return result.scalars().first()
    

    # role 찾기
    @staticmethod
    async def crud_user_get_by_role(db:AsyncSession, u_id:int) -> User |None:
        result=await db.execute(select(User.role).filter(User.u_id==u_id))
        return result.scalar_one_or_none()
    
    
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
 
=======
from sqlalchemy.orm import Session
from app.db.models.users import User
from app.db.scheme.users import UserCreate, UserUpdate


def create_user(db: Session, user_data: UserCreate):
    user = User(
        email=user_data.email,
        pw=user_data.pw,   # 테스트용이라 평문 저장
        u_name=user_data.u_name,
        role=user_data.role,
        info=user_data.info
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_all_users(db: Session):
    return db.query(User).all()


def get_user_by_id(db: Session, u_id: int):
    return db.query(User).filter(User.u_id == u_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def update_user(db: Session, u_id: int, user_data: UserUpdate):
    user = db.query(User).filter(User.u_id == u_id).first()
    if not user:
        return None

    update_dict = user_data.model_dump(exclude_unset=True)

    for key, value in update_dict.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, u_id: int):
    user = db.query(User).filter(User.u_id == u_id).first()
    if not user:
        return None

    db.delete(user)
    db.commit()
    return user
>>>>>>> origin/ekkim
