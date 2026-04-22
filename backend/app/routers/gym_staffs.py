from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.scheme.gym_staffs import Gym_Staff_Create, Gym_Staff_Delete
from app.services import gym_staffs as service

router = APIRouter(prefix="/gym_staffs", tags=["Gym_Staff"])

# 헬스장에 트레이너 등록
@router.post("")
def create_gym_staff(
    data: Gym_Staff_Create,
    db: Session = Depends(get_db),
    # user=Depends(get_manager_user)
):
    service.create_gym_staff_service(db, data.g_id, data.u_id)

    return {
        "msg": "트레이너 등록 완료"
    }

# 헬스장에 트레이너 제거
@router.delete("")
def delete_gym_staff(
    data: Gym_Staff_Delete,
    db: Session = Depends(get_db),
    # user=Depends(get_manager_user)
):
    service.delete_gym_staff_service(db, data.g_id, data.u_id)

    return {
        "msg": "트레이너 등록 취소"
    }

# 헬스장 트레이너 조회
@router.get("/{g_id}")
def get_gym_staff(
    g_id: int,
    db: Session = Depends(get_db)
):
    data = service.get_gym_staff_service(db, g_id)

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