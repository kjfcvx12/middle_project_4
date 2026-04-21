from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.scheme.gyms import GymCreate, GymUpdate, GymResponse, GymListItem
from app.services import gyms as gym_service

router = APIRouter(prefix="/gyms", tags=["Gyms"])

# 헬스장 등록
@router.post("")
def createGym(
    data: GymCreate,
    db: Session = Depends(get_db),
):
    gym = gym_service.createGymService(db, data)

    return {
        "msg": "헬스장 등록 완료",
        "g_id": gym.g_id
    }

# 헬스장 목록 조회
@router.get("")
def listGyms(
    page: int = 1,
    size: int = 10,
    sort: str | None = None,
    name: str | None = None,
    address: str | None = None,
    db: Session = Depends(get_db),
):
    skip = (page - 1) * size

    gyms, total = gym_service.listGymService(
        db=db,
        skip=skip,
        limit=size,
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
        "size": size,
        "data": data,
    }

# 헬스장 상세 조회
@router.get("/{g_id}", response_model=GymResponse)
def gymDetail(
    g_id: int,
    db: Session = Depends(get_db),
):
    return gym_service.getGymService(db, g_id)

# 헬스장 정보 수정
@router.put("/{g_id}")
@router.put("/{g_id}")
def updateGym(
    g_id: int,
    data: GymUpdate,
    db: Session = Depends(get_db),
):
    gym = gym_service.updateGymService(db, g_id, data)

    return {
        "msg": "수정 완료",
        "g_id": gym.g_id
    }

# 헬스장 삭제
@router.delete("/{g_id}")
@router.delete("/{g_id}")
def deleteGym(
    g_id: int,
    db: Session = Depends(get_db),
):
    gym_service.deleteGymService(db, g_id)

    return {
        "msg": "헬스장 삭제 완료"
    }

# 헬스장 소속 트레이너 조회
@router.get("/{g_id}/staff")
def getGymStaff(
    g_id: int,
    db: Session = Depends(get_db),
):
    return gym_service.getGymTrainerService(db, g_id)

# 헬스장 운동기구 목록 조회
@router.get("/machines/{g_id}")
def getGymMachines(
    g_id: int,
    db: Session = Depends(get_db),
):
    return gym_service.getGymMachinesService(db, g_id)