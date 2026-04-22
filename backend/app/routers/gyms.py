from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.scheme.gyms import Gym_Create, Gym_Update, Gym_Response
from app.services import gyms as gym_service
from app.services import gym_staffs as gym_staffs_service
from app.services import gym_machines as gym_machines_service

router = APIRouter(prefix="/gyms", tags=["Gyms"])


# CREATE
@router.post("")
def routers_gym_create(
    data: Gym_Create,
    db: Session = Depends(get_db),
):
    gym = gym_service.services_gym_create(db, data)

    return {
        "msg": "헬스장 등록 완료",
        "g_id": gym.g_id
    }


# LIST
@router.get("")
def routers_gyms_list(
    page: int = 1,
    sort: str | None = None,
    name: str | None = None,
    address: str | None = None,
    db: Session = Depends(get_db),
):
    gyms, total = gym_service.services_gym_list(
        db=db,
        name=name,
        address=address,
        sort=sort
    )

    data = [
        {
            "g_id": g.g_id,
            "g_name": g.g_name,
            "g_addr": g.g_addr,
            "like_count": getattr(g, "like_count", 0),
            "favorite_count": getattr(g, "favorite_count", 0),
        }
        for g in gyms
    ]

    return {
        "total": total,
        "page": page,
        "data": data,
    }


# DETAIL
@router.get("/{g_id}", response_model=Gym_Response)
def routers_gym_detail(
    g_id: int,
    db: Session = Depends(get_db),
):
    return gym_service.services_gym_service_get(db, g_id)


# UPDATE
@router.put("/{g_id}")
def routers_gym_update(
    g_id: int,
    data: Gym_Update,
    db: Session = Depends(get_db),
):
    gym = gym_service.services_gym_update(db, g_id, data)

    return {
        "msg": "수정 완료",
        "g_id": gym.g_id
    }


# DELETE
@router.delete("/{g_id}")
def routers_gym_delete(
    g_id: int,
    db: Session = Depends(get_db),
):
    gym_service.services_gym_delete(db, g_id)

    return {
        "msg": "헬스장 삭제 완료"
    }


# STAFF
@router.get("/{g_id}/staff")
def routers_gym_staffs_get(
    g_id: int,
    db: Session = Depends(get_db),
):
    return gym_staffs_service.services_gym_staff_get(db, g_id)


# MACHINES
@router.get("/machines/{g_id}")
def routers_gym_machines_get(
    g_id: int,
    db: Session = Depends(get_db),
):
    return gym_machines_service.services_gym_machine_get(db, g_id)