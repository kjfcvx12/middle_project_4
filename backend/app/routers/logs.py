from fastapi import APIRouter, Depends
from app.schema.logs import LogCreate
from app.services.logs import create_log_service, get_logs_service
from app.core.jwt_handle import get_current_user
from app.db.database import get_db

router = APIRouter()

# 기록 생성
@router.post("/")
def create_log(data: LogCreate, db=Depends(get_db), user=Depends(get_current_user)):
    return create_log_service(db, user, data)

# 기록 조회
@router.get("/")
def get_logs(db=Depends(get_db), user=Depends(get_current_user)):
    return get_logs_service(db, user)