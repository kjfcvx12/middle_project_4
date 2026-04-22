from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.scheme.users import UserCreate, UserUpdate, UserResponse
from app.db.crud.users import (
    create_user,
    get_all_users,
    get_user_by_id,
    get_user_by_email,
    update_user,
    delete_user,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse)
def create_user_api(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다.")

    return create_user(db, user_data)


@router.get("/", response_model=list[UserResponse])
def read_users_api(db: Session = Depends(get_db)):
    return get_all_users(db)


@router.get("/{u_id}", response_model=UserResponse)
def read_user_api(u_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, u_id)
    if not user:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")
    return user


@router.put("/{u_id}", response_model=UserResponse)
def update_user_api(u_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    user = update_user(db, u_id, user_data)
    if not user:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")
    return user


@router.delete("/{u_id}")
def delete_user_api(u_id: int, db: Session = Depends(get_db)):
    user = delete_user(db, u_id)
    if not user:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")
    return {"message": f"{u_id}번 유저가 삭제되었습니다."}