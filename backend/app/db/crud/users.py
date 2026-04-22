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