from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.scheme.gym_staffs import GymStaffCreate, GymStaffDelete
from app.services import gym_staffs as service

router = APIRouter(prefix="/gym_staffs", tags=["Gym_Staff"])

# 헬스장에 트레이너 등록
@router.post("")
def createGymStaff(
    data: GymStaffCreate,
    db: Session = Depends(get_db),
    # user=Depends(get_manager_user) (권한 : 매니저)
):
    result = service.createGymStaffService(db, data.g_id, data.u_id)

    if result is None:
        raise HTTPException(
            status_code=400
        )

    return {
        "msg": "트레이너 등록 완료"
    }

# 헬스장에 트레이너 제거
@router.delete("")
def deleteGymStaff(
    data: GymStaffDelete,
    db: Session = Depends(get_db),
    # user=Depends(get_manager_user) (권한 : 매니저)
):
    result = service.deleteGymStaffService(db, data.g_id, data.u_id)

    if result is None:
        raise HTTPException(
            status_code=404
        )

    return {
        "msg": "트레이너 등록 취소"
    }

# 헬스장 트레이너 조회
@router.get("/{g_id}")
def getGymStaff(
    g_id: int,
    db: Session = Depends(get_db)
):
    data = service.getGymStaffService(db, g_id)

    return {
        "data": [
            {
                "g_s_id": d.g_s_id,
                "g_id": d.g_id,
                "u_id": d.u_id,
            }
            for d in data
        ]
    }