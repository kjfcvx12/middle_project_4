from fastapi import APIRouter, Depends
from app.services.logs import *
from app.core.jwt_handle import get_current_user
from app.db.database import get_db
from app.db.scheme.logs import LogCreate

router = APIRouter(prefix="/logs")

# 생성
@router.post("/")
def create_log(data: LogCreate, db=Depends(get_db), user=Depends(get_current_user)):
    return service_create_log(db, user, data)

# 조회
@router.get("/")
def get_logs(db=Depends(get_db), user=Depends(get_current_user)):
    return service_get_logs(db, user)

# 삭제
@router.delete("/{log_id}")
def delete_log(log_id: int, db=Depends(get_db), user=Depends(get_current_user)):
    return service_delete_log(db, user, log_id)