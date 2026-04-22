from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.scheme.gym_machines import Gym_Machine_Create, Gym_Machine_Update, Gym_Machine_Delete
from app.services import gym_machines as service

router = APIRouter(prefix="/gym_machines", tags=["Gym_Machine"])

# 헬스장에 운동기구 등록
@router.post("")
def create_gym_machine(
    data: Gym_Machine_Create,
    db: Session = Depends(get_db),
    # user=Depends(get_manager_user)
):
    service.create_gym_machine_service(db, data.g_id, data.m_id, data.qty)

    return {
        "msg": "기구 등록 완료"
    }

# 운동기구 수량 수정
@router.put("")
def update_gym_machine(
    data: Gym_Machine_Update,
    db: Session = Depends(get_db),
    # user=Depends(get_manager_user)
):
    service.update_gym_machine_service(db, data.g_id, data.m_id, data.qty)

    return {
        "msg": "수량 수정 완료"
    }

# 운동기구 제거
@router.delete("")
def delete_gym_machine(
    data: Gym_Machine_Delete,
    db: Session = Depends(get_db),
    # user=Depends(get_manager_user)
):
    service.delete_gym_machine_service(db, data.g_id, data.m_id)

    return {
        "msg": "기구 제거 완료"
    }