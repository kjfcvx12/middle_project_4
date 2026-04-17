from fastapi import APIRouter, Depends
from app.services.favorites import *
from app.core.jwt_handle import get_current_user
from app.db.database import get_db

router = APIRouter()

# 즐겨찾기 추가
@router.post("/{log_id}")
def add_fav(log_id: int, db=Depends(get_db), user=Depends(get_current_user)):
    return add_favorite_service(db, user, log_id)

# 조회
@router.get("/")
def get_fav(db=Depends(get_db), user=Depends(get_current_user)):
    return get_favorites_service(db, user)

# 삭제
@router.delete("/{log_id}")
def delete_fav(log_id: int, db=Depends(get_db), user=Depends(get_current_user)):
    return delete_favorite_service(db, user, log_id)