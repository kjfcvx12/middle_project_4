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
    # user=Depends(get_manager_user) (권한 : 매니저/관리자)
):
    result = service.createGymMachineService(
        db, data.g_id, data.m_id, data.qty
    )

    if result is None:
        raise HTTPException(
            status_code=400
        )

    return {
        "msg": "기구 등록 완료"
    }

# 운동기구 수량 수정
@router.put("")
def updateGymMachine(
    data: GymMachineUpdate,
    db: Session = Depends(get_db),
    # user=Depends(get_manager_user) (권한 : 매니저/관리자)
):
    result = service.updateGymMachineService(
        db, data.g_id, data.m_id, data.qty
    )

    if result is None:
        raise HTTPException(
            status_code=400
        )

    return {
        "msg": "수량 수정 완료"
    }

# 운동기구 제거
@router.delete("")
def deleteGymMachine(
    data: GymMachineDelete,
    db: Session = Depends(get_db),
    # user=Depends(get_manager_user) (권한 : 매니저/관리자)
):
    result = service.deleteGymMachineService(
        db, data.g_id, data.m_id
    )

    if result is None:
        raise HTTPException(
            status_code=404
        )

    return {
        "msg": "기구 제거 완료"
    }