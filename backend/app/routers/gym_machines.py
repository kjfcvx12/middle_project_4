from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.scheme.gym_machines import (
    GymMachineCreate,
    GymMachineUpdate,
    GymMachineDelete
)
from app.services import gym_machines as service

router = APIRouter(prefix="/gym_machines", tags=["Gym_Machine"])

# 헬스장에 운동기구 등록
@router.post("")
def createGymMachine(
    data: GymMachineCreate,
    db: Session = Depends(get_db),
    # user=Depends(get_manager_user)
):
    service.createGymMachineService(db, data.g_id, data.m_id, data.qty)

    return {
        "msg": "기구 등록 완료"
    }

# 운동기구 수량 수정
@router.put("")
def updateGymMachine(
    data: GymMachineUpdate,
    db: Session = Depends(get_db),
    # user=Depends(get_manager_user)
):
    service.updateGymMachineService(db, data.g_id, data.m_id, data.qty)

    return {
        "msg": "수량 수정 완료"
    }

# 운동기구 제거
@router.delete("")
def deleteGymMachine(
    data: GymMachineDelete,
    db: Session = Depends(get_db),
    # user=Depends(get_manager_user)
):
    service.deleteGymMachineService(db, data.g_id, data.m_id)

    return {
        "msg": "기구 제거 완료"
    }